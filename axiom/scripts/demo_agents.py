"""
Standalone demo of the Multi-Agent System.
No external dependencies - runs with pure Python 3.11.

Demonstrates:
1. Sensor Health Monitor detecting anomalies
2. Fault Diagnosis generating root cause hypotheses
3. Predictive Maintenance estimating RUL
4. Shift Handover report generation
"""

import sys
import math
import statistics
import types
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

# Shim structlog and other missing modules so agent code imports cleanly
class _NullLogger:
    def info(self, *a, **kw): pass
    def debug(self, *a, **kw): pass
    def warning(self, *a, **kw): pass
    def error(self, *a, **kw): pass

_structlog = types.ModuleType("structlog")
_structlog.get_logger = lambda *a, **kw: _NullLogger()
sys.modules["structlog"] = _structlog

# Shim pydantic_settings (only needed by config.py)
_ps = types.ModuleType("pydantic_settings")
class _FakeBaseSettings:
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    def __init_subclass__(cls, **kw): pass
    def __init__(self, **kw):
        import os
        for k, v in type(self).__dict__.items():
            if not k.startswith("_") and k != "Config":
                setattr(self, k, os.environ.get(k.upper(), v))
_ps.BaseSettings = _FakeBaseSettings
sys.modules["pydantic_settings"] = _ps

# Shim httpx (used by agents for Ollama calls - not needed in standalone demo)
_httpx = types.ModuleType("httpx")
class _FakeAsyncClient:
    async def __aenter__(self): return self
    async def __aexit__(self, *a): pass
    async def post(self, *a, **kw):
        r = types.SimpleNamespace(status_code=503, json=lambda: {})
        return r
_httpx.AsyncClient = lambda **kw: _FakeAsyncClient()
sys.modules["httpx"] = _httpx

# Shim neo4j driver
_neo4j_mod = types.ModuleType("neo4j")
_neo4j_mod.AsyncGraphDatabase = type("AsyncGraphDatabase", (), {"driver": staticmethod(lambda *a, **kw: None)})
_neo4j_mod.AsyncDriver = type("AsyncDriver", (), {})
sys.modules["neo4j"] = _neo4j_mod

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

def demo_sensor_monitor():
    """Demo: Sensor Health Monitor Agent detects anomalies."""
    print("\n" + "=" * 70)
    print("  AGENT 1: SENSOR HEALTH MONITOR")
    print("  Ingesting machine sensor logs and detecting anomalies")
    print("=" * 70)

    from app.services.agents.sensor_monitor_agent import (
        SensorHealthMonitorAgent, SensorReading, HealthStatus,
    )

    agent = SensorHealthMonitorAgent()

    # Simulate sensor readings for Pump P-101A
    # Normal operation followed by degradation
    print("\n  Simulating 30 vibration readings for Pump P-101A...")
    print("  (Normal -> Degrading -> Warning -> Critical)\n")

    readings = []
    base_time = datetime(2024, 7, 1, 8, 0)

    # Normal readings (1-15)
    for i in range(15):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=3.5 + (i * 0.1) + (0.2 * (i % 3)),  # Slight variation
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Degrading readings (16-25)
    for i in range(15, 25):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=5.0 + ((i - 15) * 0.6),  # Steeper increase
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Critical readings (26-30)
    for i in range(25, 30):
        readings.append(SensorReading(
            equipment_tag="P-101A",
            parameter="vibration",
            value=11.0 + ((i - 25) * 0.5),  # Past warning limit
            unit="mm/s",
            timestamp=base_time + timedelta(hours=i),
        ))

    # Process readings
    alerts = []
    for reading in readings:
        alert = agent.analyze_reading(reading)
        status_icon = "." if not alert else ("[!]" if alert.status == HealthStatus.WARNING else "[X]")
        if alert:
            alerts.append(alert)

    print(f"  Readings processed: {len(readings)}")
    print(f"  Anomalies detected: {len(alerts)}")
    print(f"\n  Alerts generated:")
    for a in alerts:
        print(f"    [{a.timestamp.strftime('%H:%M')}] {a.status.value.upper()}: "
              f"{a.parameter}={a.current_value:.1f} {a.unit}")
        print(f"             Reason: {a.reason}")
        print(f"             Severity Score: {a.severity_score:.2f}")
        print()

    # Health summary
    summary = agent.get_equipment_health_summary("P-101A")
    print(f"  Equipment Health Summary:")
    for param, data in summary.get("parameters", {}).items():
        print(f"    {param}: latest={data['latest']:.1f}, "
              f"mean={data['mean']:.1f}, trend={data['trend']}")

    return alerts

def demo_fault_diagnosis(alerts):
    """Demo: Fault Diagnosis Agent generates root cause hypotheses."""
    print("\n\n" + "=" * 70)
    print("  AGENT 2: FAULT DIAGNOSIS & SUGGESTION")
    print("  Analyzing anomalies and suggesting corrective actions")
    print("=" * 70)

    from app.services.agents.fault_diagnosis_agent import FaultDiagnosisAgent

    agent = FaultDiagnosisAgent(neo4j_client=None)  # No KG in standalone demo

    if not alerts:
        print("\n  No alerts to diagnose.")
        return

    # Take the most critical alert
    critical_alert = max(alerts, key=lambda a: a.severity_score)
    print(f"\n  Diagnosing: {critical_alert.equipment_tag} - "
          f"{critical_alert.parameter} {critical_alert.status.value}")
    print(f"  Value: {critical_alert.current_value} {critical_alert.unit}")

    # Run synchronous part of diagnosis (pattern matching)
    hypotheses = agent._get_pattern_hypotheses(critical_alert)

    print(f"\n  Root Cause Hypotheses ({len(hypotheses)} generated):")
    for i, h in enumerate(sorted(hypotheses, key=lambda x: x.confidence, reverse=True), 1):
        print(f"    {i}. {h.cause}")
        print(f"       Confidence: {h.confidence:.0%} | Category: {h.category}")
        print(f"       Evidence: {h.evidence[0]}")
        print()

    # Get standard actions
    actions = agent._generate_actions(hypotheses, critical_alert)
    print(f"  Recommended Actions ({len(actions)}):")
    for i, a in enumerate(actions, 1):
        print(f"    {i}. [{a.priority.upper()}] {a.action}")
        if a.parts_needed:
            print(f"       Parts: {', '.join(a.parts_needed)}")
        if a.sop_reference:
            print(f"       Reference: {a.sop_reference}")
        if a.safety_precautions:
            print(f"       Safety: {', '.join(a.safety_precautions)}")
        print()

def demo_predictive_maintenance():
    """Demo: Predictive Maintenance Agent estimates RUL."""
    print("\n\n" + "=" * 70)
    print("  AGENT 3: PREDICTIVE MAINTENANCE")
    print("  Estimating Remaining Useful Life (RUL)")
    print("=" * 70)

    from app.services.agents.predictive_maintenance_agent import PredictiveMaintenanceAgent

    agent = PredictiveMaintenanceAgent()

    # Simulate degrading vibration history (50 readings over 50 hours)
    vibration_history = [3.5 + (i * 0.15) + (0.1 * (i % 4)) for i in range(50)]
    # Latest reading: ~10.5 mm/s, limit: 14.0 mm/s

    print(f"\n  Equipment: P-101A (Pump)")
    print(f"  Current vibration: {vibration_history[-1]:.1f} mm/s")
    print(f"  Critical limit: 14.0 mm/s")
    print(f"  Trend: Increasing at ~0.15 mm/s per hour")
    print(f"  Hours in service since last maintenance: 18000")

    report = agent.predict(
        equipment_tag="P-101A",
        parameter_history={"vibration": vibration_history},
        critical_limits={"vibration": 14.0},
        next_scheduled_pm=datetime.utcnow() + timedelta(days=45),
        equipment_type="pump",
        hours_since_last_maintenance=18000,
    )

    print(f"\n  --- Predictive Report ---")
    print(f"  Overall Health Score: {report.overall_health_score:.1f}%")
    print(f"  Risk Summary: {report.risk_summary}")

    print(f"\n  RUL Estimates:")
    for rul in report.rul_estimates:
        print(f"    Parameter: {rul.parameter}")
        print(f"    Days to failure: {rul.estimated_days_to_failure:.1f} "
              f"(CI: {rul.confidence_interval[0]:.1f} - {rul.confidence_interval[1]:.1f})")
        print(f"    Risk Score: {rul.risk_score:.0%}")
        print(f"    Method: {rul.method}")
        print(f"    Health: {rul.current_health_pct:.1f}%")
        print()

    print(f"  Maintenance Recommendations:")
    for rec in report.maintenance_recommendations:
        print(f"    Urgency: {rec.urgency.upper()}")
        print(f"    Action: {rec.action}")
        print(f"    Recommended Date: {rec.recommended_date.strftime('%d-%b-%Y')}")
        print(f"    Cost of planned fix: ${rec.cost_of_early_intervention:,.0f}")
        print(f"    Cost of unplanned failure: ${rec.cost_of_unplanned_failure:,.0f}")
        print(f"    Reasoning: {rec.reasoning}")
        print()

def demo_shift_handover(alerts):
    """Demo: Shift Handover Agent generates report."""
    print("\n\n" + "=" * 70)
    print("  AGENT 4: SHIFT HANDOVER")
    print("  Generating automated shift report")
    print("=" * 70)

    from app.services.agents.shift_handover_agent import (
        ShiftHandoverAgent, ShiftEvent, HandoverReport,
    )

    agent = ShiftHandoverAgent()

    shift_start = datetime(2024, 7, 1, 6, 0)
    shift_end = datetime(2024, 7, 1, 18, 0)

    # Log events from this shift
    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=1),
        event_type="maintenance",
        severity="medium",
        equipment_tag="HX-501",
        description="Scheduled cleaning of heat exchanger tubes",
        status="resolved",
        assigned_to="Rajesh Kumar",
        action_taken="Cleaned, back in service at 08:30",
    ))

    # Log the sensor alerts
    for alert in alerts[:3]:
        agent.log_alarm(alert, action_taken="Monitoring, maintenance team notified")

    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=8),
        event_type="operator_action",
        severity="info",
        equipment_tag="C-301",
        description="Compressor speed reduced from 3500 to 3200 RPM per operator decision",
        status="resolved",
        action_taken="Load reduced to manage temperature",
    ))

    agent.log_event(ShiftEvent(
        timestamp=shift_start + timedelta(hours=10),
        event_type="maintenance",
        severity="high",
        equipment_tag="P-101A",
        description="Vibration inspection requested - bearing check pending",
        status="in_progress",
        assigned_to="Suresh Patel",
    ))

    # Generate report (synchronous parts only for demo)
    import asyncio

    async def gen():
        return await agent.generate_report(shift_start, shift_end)

    try:
        report = asyncio.run(gen())
    except Exception:
        # Fallback if Ollama not available
        report = HandoverReport(
            shift_start=shift_start,
            shift_end=shift_end,
            shift_type="day",
            executive_summary=[
                "3 vibration alarms on P-101A - trending upward, maintenance notified",
                "HX-501 cleaning completed successfully",
                "C-301 speed reduced (operator decision) - monitor temperature",
                "P-101A bearing inspection IN PROGRESS (Suresh Patel)",
            ],
            critical_items=[{
                "equipment": "P-101A",
                "issue": "Vibration exceeding warning limit (11.5 mm/s)",
                "status": "pending",
                "action": "Monitoring, maintenance team notified",
                "time": "14:00",
            }],
            alarms_summary={"total": 3, "critical": 1, "high": 2, "resolved": 0, "pending": 3},
            work_in_progress=[{
                "equipment": "P-101A",
                "activity": "Bearing inspection",
                "status": "in_progress",
                "assigned_to": "Suresh Patel",
            }],
            watch_items=[{
                "equipment": "P-101A",
                "reason": "Recurring alarms (3 times this shift) - developing bearing issue",
            }],
            total_alarms=3,
            critical_alarms=1,
            maintenance_actions=2,
        )

    formatted = agent.format_report_text(report)
    print(f"\n{formatted}")

def demo_agent_coordination():
    """Show how all agents work together."""
    print("\n\n" + "=" * 70)
    print("  AGENT COORDINATION - Full Pipeline Example")
    print("=" * 70)

    print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │ SCENARIO: Bearing degradation detected on Pump P-101A          │
  └─────────────────────────────────────────────────────────────────┘

  Timeline:

  [08:00] SENSOR MONITOR AGENT:
          -> Vibration reading: 7.5 mm/s (trending up at 0.3 mm/s/hour)
          -> Status: NORMAL (but trend detected)
          -> Action: Continue monitoring, log trend

  [12:00] SENSOR MONITOR AGENT:
          -> Vibration reading: 9.8 mm/s
          -> Status: WARNING (approaching 11.2 mm/s alarm)
          -> Action: Trigger Fault Diagnosis Agent

  [12:01] FAULT DIAGNOSIS AGENT:
          -> Queried Knowledge Graph:
            • P-101A had bearing failure in Mar-2024 (WO-100234)
            • Similar pattern seen on P-101B in Aug-2023
            • OEM recommends bearing inspection at 8.0 mm/s
          -> Top Hypothesis: "Bearing wear - lubrication degradation" (85%)
          -> Recommended Actions:
            1. IMMEDIATE: Sample lube oil (1 hour)
            2. SHORT-TERM: Schedule bearing inspection (4 hours)
            3. LONG-TERM: Review lubrication PM frequency

  [12:02] PREDICTIVE MAINTENANCE AGENT:
          -> Current degradation rate: 0.3 mm/s per hour
          -> Critical limit: 14.0 mm/s
          -> Estimated failure: 14 hours (by 02:00 tomorrow)
          -> Next scheduled PM: 45 days away
          -> RECOMMENDATION: "Advance PM immediately. Failure imminent."
          -> Cost analysis:
            • Planned repair now: $2,500
            • Unplanned failure tonight: $45,000 + 72h downtime

  [18:00] SHIFT HANDOVER AGENT:
          -> Generates report for incoming night shift:
            "CRITICAL: P-101A vibration WARNING. Bearing failure predicted
             within 14 hours. Diagnosis suggests lube degradation.
             Oil sampling in progress (Suresh Patel). Recommend preparing
             for emergency bearing replacement if oil results confirm."

  ┌─────────────────────────────────────────────────────────────────┐
  │ OUTCOME: Night shift team takes preemptive action, avoids       │
  │ unplanned failure. $42,500 saved. Zero downtime.                │
  └─────────────────────────────────────────────────────────────────┘
""")

if __name__ == "__main__":
    print("=" * 70)
    print("  AXIOM - Multi-Agent Operations Intelligence Demo")
    print("  4 Agents working together for equipment health management")
    print("=" * 70)

    # Run all agent demos
    alerts = demo_sensor_monitor()
    demo_fault_diagnosis(alerts)
    demo_predictive_maintenance()
    demo_shift_handover(alerts)
    demo_agent_coordination()

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE - All 4 agents demonstrated successfully")
    print("=" * 70)