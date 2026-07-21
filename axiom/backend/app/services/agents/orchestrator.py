"""
Agent Orchestrator — coordinates the multi-agent system.
Routes sensor data through the correct agent pipeline.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import structlog

from app.services.agents.sensor_monitor_agent import (
    SensorHealthMonitorAgent, SensorReading, AnomalyAlert, HealthStatus,
)
from app.services.agents.fault_diagnosis_agent import FaultDiagnosisAgent, DiagnosisReport
from app.services.agents.predictive_maintenance_agent import PredictiveMaintenanceAgent
from app.services.agents.shift_handover_agent import ShiftHandoverAgent, ShiftEvent
from app.services.agents.report_saver import ReportSaver
from app.services.knowledge_graph.neo4j_client import Neo4jClient

logger = structlog.get_logger()

@dataclass
class OrchestratorResult:
    """Combined result from multi-agent processing."""
    alerts: list[AnomalyAlert]
    diagnoses: list[DiagnosisReport]
    health_summary: dict
    actions_generated: int

class AgentOrchestrator:
    """
    Coordinates the multi-agent pipeline:

    Sensor Data → Monitor Agent → (if anomaly) → Diagnosis Agent
                                               → Predictive Agent
                                               → Handover Agent (logs event)
    """

    def __init__(self, neo4j_client: Optional[Neo4jClient] = None):
        self.monitor = SensorHealthMonitorAgent()
        self.diagnosis = FaultDiagnosisAgent(neo4j_client=neo4j_client)
        self.predictive = PredictiveMaintenanceAgent()
        self.handover = ShiftHandoverAgent()
        self._neo4j = neo4j_client

    async def process_sensor_batch(
        self, readings: list[SensorReading]
    ) -> OrchestratorResult:
        """
        Process a batch of sensor readings through the full agent pipeline.

        1. Monitor Agent analyzes all readings
        2. For anomalies, Diagnosis Agent generates root cause hypotheses
        3. All events logged for Shift Handover Agent
        """
        # Step 1: Sensor Health Monitor
        alerts = self.monitor.analyze_batch(readings)

        # Step 2: For each alert, run Fault Diagnosis
        diagnoses = []
        for alert in alerts:
            if alert.status in (HealthStatus.CRITICAL, HealthStatus.WARNING):
                diagnosis = await self.diagnosis.diagnose(alert)
                diagnoses.append(diagnosis)

                # Log to handover agent
                self.handover.log_alarm(
                    alert,
                    action_taken=(
                        diagnosis.recommended_actions[0].action
                        if diagnosis.recommended_actions
                        else "Under investigation"
                    ),
                )

        # Build health summary
        equipment_tags = set(r.equipment_tag for r in readings)
        health_summary = {}
        for tag in equipment_tags:
            health_summary[tag] = self.monitor.get_equipment_health_summary(tag)

        logger.info(
            "Orchestrator batch complete",
            readings=len(readings),
            alerts=len(alerts),
            diagnoses=len(diagnoses),
        )

        return OrchestratorResult(
            alerts=alerts,
            diagnoses=diagnoses,
            health_summary=health_summary,
            actions_generated=sum(len(d.recommended_actions) for d in diagnoses),
        )

    async def get_predictive_report(
        self,
        equipment_tag: str,
        parameter_history: dict[str, list[float]],
        critical_limits: dict[str, float],
        equipment_type: str = "pump",
        hours_in_service: float = 10000,
        next_pm: Optional[datetime] = None,
    ):
        """Run predictive maintenance analysis for specific equipment."""
        return self.predictive.predict(
            equipment_tag=equipment_tag,
            parameter_history=parameter_history,
            critical_limits=critical_limits,
            next_scheduled_pm=next_pm,
            equipment_type=equipment_type,
            hours_since_last_maintenance=hours_in_service,
        )

    async def generate_shift_handover(
        self,
        shift_start: datetime,
        shift_end: datetime,
    ):
        """Generate shift handover report."""
        report = await self.handover.generate_report(shift_start, shift_end)
        return report, self.handover.format_report_text(report)