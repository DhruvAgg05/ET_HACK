"""
Fault Diagnosis & Suggestion Agent
When the Sensor Monitor detects an anomaly, this agent determines probable cause
and recommends corrective actions by reasoning across the Knowledge Graph.
"""

import httpx
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import structlog

from app.config import settings
from app.services.agents.sensor_monitor_agent import AnomalyAlert, HealthStatus
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class DiagnosisHypothesis:
    cause: str
    confidence: float  # 0-1
    evidence: list[str]  # Supporting references
    category: str  # "mechanical", "electrical", "process", "instrumentation"

@dataclass
class CorrectionAction:
    action: str
    priority: str  # "immediate", "short_term", "long_term"
    estimated_effort: str  # "1h", "4h", "1 day", etc.
    parts_needed: list[str] = field(default_factory=list)
    sop_reference: str = ""
    safety_precautions: list[str] = field(default_factory=list)

@dataclass
class DiagnosisReport:
    equipment_tag: str
    alert_summary: str
    hypotheses: list[DiagnosisHypothesis]
    recommended_actions: list[CorrectionAction]
    similar_past_incidents: list[dict]
    confidence_level: str  # "high", "medium", "low"
    generated_at: datetime = field(default_factory=datetime.utcnow)
    references: list[str] = field(default_factory=list)

class FaultDiagnosisAgent:
    """
    Diagnoses equipment faults by:
    1. Querying Knowledge Graph for equipment history and similar failures
    2. Cross-referencing OEM troubleshooting guides
    3. Using LLM reasoning (Ishikawa/5-Why) for root cause analysis
    4. Generating ranked corrective actions with SOP references
    """

    # Common failure mode patterns (used when KG data is limited)
    FAILURE_PATTERNS = {
        "vibration": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Bearing degradation (inner/outer race wear)",
                    confidence=0.75,
                    evidence=["Most common cause of vibration increase in rotating equipment"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Misalignment (angular or parallel)",
                    confidence=0.65,
                    evidence=["Often occurs after maintenance involving coupling disconnect"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Imbalance (fouling, erosion, or loose component)",
                    confidence=0.55,
                    evidence=["Check for deposit buildup or missing balance weight"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Looseness (structural or rotating)",
                    confidence=0.45,
                    evidence=["Check foundation bolts and bearing housing"],
                    category="mechanical",
                ),
            ],
            "trending_up": [
                DiagnosisHypothesis(
                    cause="Progressive bearing wear — lubrication degradation likely",
                    confidence=0.7,
                    evidence=["Gradual increase pattern typical of lube contamination"],
                    category="mechanical",
                ),
            ],
        },
        "temperature": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Cooling system insufficiency (fouled cooler or low coolant flow)",
                    confidence=0.7,
                    evidence=["Check heat exchanger pressure drop and coolant level"],
                    category="process",
                ),
                DiagnosisHypothesis(
                    cause="Bearing overheating (lubrication failure)",
                    confidence=0.65,
                    evidence=["Correlate with vibration data for confirmation"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Overloading (operating above design capacity)",
                    confidence=0.5,
                    evidence=["Check current draw and flow rate vs design"],
                    category="process",
                ),
            ],
        },
        "pressure": {
            "high_value": [
                DiagnosisHypothesis(
                    cause="Downstream blockage or restriction",
                    confidence=0.7,
                    evidence=["Check downstream valves, filters, and line condition"],
                    category="process",
                ),
                DiagnosisHypothesis(
                    cause="Control valve malfunction (stuck closed)",
                    confidence=0.6,
                    evidence=["Check valve position feedback vs command"],
                    category="instrumentation",
                ),
            ],
            "low_value": [
                DiagnosisHypothesis(
                    cause="Leak in system (flange, seal, or pipe)",
                    confidence=0.7,
                    evidence=["Inspect for visible leaks, check system inventory"],
                    category="mechanical",
                ),
                DiagnosisHypothesis(
                    cause="Pump/compressor degradation (worn impeller or valves)",
                    confidence=0.6,
                    evidence=["Compare discharge pressure vs speed curve"],
                    category="mechanical",
                ),
            ],
        },
    }

    STANDARD_ACTIONS = {
        "mechanical": [
            CorrectionAction(
                action="Perform vibration spectrum analysis to confirm failure mode",
                priority="immediate",
                estimated_effort="2h",
                safety_precautions=["Lock-out/Tag-out if accessing rotating parts"],
            ),
            CorrectionAction(
                action="Inspect and sample lubrication oil (send for analysis)",
                priority="immediate",
                estimated_effort="1h",
                sop_reference="SOP-MAINT-045: Lubrication Sampling Procedure",
            ),
            CorrectionAction(
                action="Schedule bearing replacement during next available window",
                priority="short_term",
                estimated_effort="8h",
                parts_needed=["Bearing (check OEM spec)", "Seal set", "Lubricant"],
                sop_reference="SOP-MAINT-023: Bearing Replacement Procedure",
                safety_precautions=["PTW required", "Isolate and depressurize", "LOTO"],
            ),
        ],
        "process": [
            CorrectionAction(
                action="Check and clean heat exchanger / cooling system",
                priority="short_term",
                estimated_effort="4h",
                sop_reference="SOP-MAINT-067: Heat Exchanger Cleaning",
            ),
            CorrectionAction(
                action="Verify process parameters against design basis",
                priority="immediate",
                estimated_effort="1h",
            ),
        ],
        "instrumentation": [
            CorrectionAction(
                action="Calibrate sensor / verify reading with portable instrument",
                priority="immediate",
                estimated_effort="1h",
                sop_reference="SOP-INST-012: Instrument Calibration",
            ),
            CorrectionAction(
                action="Check control valve stroke and positioner",
                priority="short_term",
                estimated_effort="2h",
            ),
        ],
    }

    def __init__(self, neo4j_client: Optional[Neo4jClient] = None):
        self.neo4j = neo4j_client

    async def diagnose(self, alert: AnomalyAlert) -> DiagnosisReport:
        """
        Generate a full diagnosis report for an anomaly alert.
        Combines pattern matching, KG lookup, and LLM reasoning.
        """
        logger.info(
            "Starting fault diagnosis",
            equipment=alert.equipment_tag,
            parameter=alert.parameter,
            status=alert.status.value,
        )

        # Step 1: Get hypotheses from pattern library
        hypotheses = self._get_pattern_hypotheses(alert)

        # Step 2: Enrich with Knowledge Graph data (if available)
        similar_incidents = []
        if self.neo4j:
            kg_context = await self._query_knowledge_graph(alert)
            similar_incidents = kg_context.get("similar_incidents", [])
            # Adjust confidence based on historical evidence
            hypotheses = self._adjust_confidence_from_history(hypotheses, kg_context)

        # Step 3: Get LLM-powered deeper analysis (if Ollama available)
        llm_hypotheses = await self._llm_reasoning(alert, hypotheses)
        if llm_hypotheses:
            hypotheses.extend(llm_hypotheses)

        # Step 4: Generate corrective actions
        actions = self._generate_actions(hypotheses, alert)

        # Step 5: Determine overall confidence
        confidence = self._assess_overall_confidence(hypotheses, similar_incidents)

        # Build report
        report = DiagnosisReport(
            equipment_tag=alert.equipment_tag,
            alert_summary=(
                f"{alert.parameter} {alert.status.value} on {alert.equipment_tag}: "
                f"{alert.current_value} {alert.unit} — {alert.reason}"
            ),
            hypotheses=sorted(hypotheses, key=lambda h: h.confidence, reverse=True)[:5],
            recommended_actions=actions,
            similar_past_incidents=similar_incidents,
            confidence_level=confidence,
            references=[],
        )

        logger.info(
            "Diagnosis complete",
            equipment=alert.equipment_tag,
            hypotheses=len(report.hypotheses),
            actions=len(report.recommended_actions),
            confidence=confidence,
        )

        return report

    def _get_pattern_hypotheses(self, alert: AnomalyAlert) -> list[DiagnosisHypothesis]:
        """Get initial hypotheses from the failure pattern library."""
        param_patterns = self.FAILURE_PATTERNS.get(alert.parameter, {})

        # Determine sub-pattern based on alert characteristics
        if alert.status == HealthStatus.CRITICAL:
            key = "high_value"
        elif "trending" in (alert.trend_info or {}).get("direction", ""):
            key = "trending_up"
        else:
            key = "high_value"

        hypotheses = param_patterns.get(key, [])

        # Deep copy to avoid mutating the class patterns
        return [
            DiagnosisHypothesis(
                cause=h.cause,
                confidence=h.confidence,
                evidence=list(h.evidence),
                category=h.category,
            )
            for h in hypotheses
        ]

    async def _query_knowledge_graph(self, alert: AnomalyAlert) -> dict:
        """Query KG for equipment history, similar failures, and OEM data."""
        context = {
            "equipment_history": {},
            "similar_incidents": [],
            "oem_recommendations": [],
        }

        if not self.neo4j:
            return context

        try:
            # Get equipment full context
            equip_context = await self.neo4j.get_equipment_context(alert.equipment_tag)
            if equip_context:
                context["equipment_history"] = equip_context

                # Extract similar incidents
                incidents = equip_context.get("incidents", [])
                work_orders = equip_context.get("work_orders", [])
                context["similar_incidents"] = [
                    {"type": "incident", "data": inc} for inc in incidents[:5]
                ] + [
                    {"type": "work_order", "data": wo} for wo in work_orders[:5]
                ]

        except Exception as e:
            logger.warning("KG query failed", error=str(e))

        return context

    def _adjust_confidence_from_history(
        self, hypotheses: list[DiagnosisHypothesis], kg_context: dict
    ) -> list[DiagnosisHypothesis]:
        """Increase confidence for hypotheses supported by historical data."""
        history_text = str(kg_context).lower()

        for hypothesis in hypotheses:
            # Check if similar cause appears in history
            cause_keywords = hypothesis.cause.lower().split()
            matches = sum(1 for kw in cause_keywords if kw in history_text)
            if matches > 2:
                hypothesis.confidence = min(hypothesis.confidence + 0.15, 0.98)
                hypothesis.evidence.append("Supported by equipment history in Knowledge Graph")

        return hypotheses

    async def _llm_reasoning(
        self, alert: AnomalyAlert, existing_hypotheses: list[DiagnosisHypothesis]
    ) -> list[DiagnosisHypothesis]:
        """Use LLM for deeper diagnostic reasoning."""
        try:
            prompt = f"""You are an industrial equipment diagnostic expert.

Equipment: {alert.equipment_tag}
Parameter: {alert.parameter}
Current Value: {alert.current_value} {alert.unit}
Status: {alert.status.value}
Alert Reason: {alert.reason}
Trend: {alert.trend_info}

Existing hypotheses:
{chr(10).join(f'- {h.cause} (confidence: {h.confidence:.0%})' for h in existing_hypotheses)}

Based on your expertise, are there any additional root causes we should consider?
Particularly think about:
1. Recently changed conditions that could cause this
2. Interaction effects between multiple parameters
3. Less obvious causes specific to this equipment type

Provide 1-2 additional hypotheses if relevant, or confirm the existing ones are comprehensive.
Format: JSON array of objects with "cause", "confidence" (0-1), "category", "evidence" fields."""

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.1, "num_predict": 500},
                    },
                )

                if response.status_code == 200:
                    import json
                    content = response.json()["message"]["content"]
                    data = json.loads(content)
                    hypotheses_data = data if isinstance(data, list) else data.get("hypotheses", [])
                    return [
                        DiagnosisHypothesis(
                            cause=h.get("cause", ""),
                            confidence=float(h.get("confidence", 0.5)),
                            evidence=[h.get("evidence", "LLM analysis")],
                            category=h.get("category", "general"),
                        )
                        for h in hypotheses_data[:2]
                    ]
        except Exception as e:
            logger.debug("LLM reasoning unavailable", error=str(e))

        return []

    def _generate_actions(
        self, hypotheses: list[DiagnosisHypothesis], alert: AnomalyAlert
    ) -> list[CorrectionAction]:
        """Generate corrective actions based on top hypotheses."""
        actions = []

        # Get actions for the top hypothesis category
        if hypotheses:
            top_category = hypotheses[0].category
            category_actions = self.STANDARD_ACTIONS.get(top_category, [])
            actions.extend(category_actions)

        # Add severity-specific immediate action
        if alert.status == HealthStatus.CRITICAL:
            actions.insert(0, CorrectionAction(
                action=f"IMMEDIATE: Reduce load on {alert.equipment_tag} or prepare for controlled shutdown",
                priority="immediate",
                estimated_effort="15min",
                safety_precautions=[
                    "Notify control room",
                    "Alert maintenance team on standby",
                    "Verify backup equipment readiness",
                ],
            ))

        return actions

    def _assess_overall_confidence(
        self, hypotheses: list[DiagnosisHypothesis], similar_incidents: list
    ) -> str:
        """Assess overall diagnosis confidence."""
        if not hypotheses:
            return "low"

        top_confidence = hypotheses[0].confidence if hypotheses else 0
        has_history = len(similar_incidents) > 0

        if top_confidence > 0.7 and has_history:
            return "high"
        elif top_confidence > 0.5:
            return "medium"
        else:
            return "low"