"""
Agent API Router — exposes the multi-agent system via REST endpoints.
All reports are persisted to data/reports/ with naming convention:
    {equipment}_{shift}_{status}_{timestamp}.json
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import structlog

from app.services.agents.orchestrator import AgentOrchestrator
from app.services.agents.sensor_monitor_agent import SensorReading
from app.services.agents.report_saver import ReportSaver

logger = structlog.get_logger()
router = APIRouter()
report_saver = ReportSaver()

class SensorDataPoint(BaseModel):
    equipment_tag: str
    parameter: str
    value: float
    unit: str
    timestamp: Optional[datetime] = None

class SensorBatchRequest(BaseModel):
    readings: list[SensorDataPoint]

class PredictiveRequest(BaseModel):
    equipment_tag: str
    parameter_history: dict[str, list[float]]
    critical_limits: dict[str, float]
    equipment_type: str = "pump"
    hours_in_service: float = 10000
    next_pm_date: Optional[datetime] = None

class HandoverRequest(BaseModel):
    shift_start: datetime
    shift_end: datetime

@router.post("/analyze-sensors")
async def analyze_sensors(request: Request, data: SensorBatchRequest):
    """
    Process sensor readings through the multi-agent pipeline.

    Flow:
    1. Sensor Monitor Agent checks all readings for anomalies
    2. Fault Diagnosis Agent analyzes anomalies (root cause + suggestions)
    3. Events logged for shift handover

    Returns alerts, diagnoses, and health summary.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    # Convert to internal format
    readings = [
        SensorReading(
            equipment_tag=r.equipment_tag,
            parameter=r.parameter,
            value=r.value,
            unit=r.unit,
            timestamp=r.timestamp or datetime.utcnow(),
        )
        for r in data.readings
    ]

    result = await orchestrator.process_sensor_batch(readings)

    response_data = {
        "total_readings": len(readings),
        "anomalies_detected": len(result.alerts),
        "diagnoses_generated": len(result.diagnoses),
        "actions_suggested": result.actions_generated,
        "alerts": [
            {
                "equipment_tag": a.equipment_tag,
                "parameter": a.parameter,
                "value": a.current_value,
                "unit": a.unit,
                "status": a.status.value,
                "severity_score": a.severity_score,
                "reason": a.reason,
                "trend": a.trend_info,
            }
            for a in result.alerts
        ],
        "diagnoses": [
            {
                "equipment_tag": d.equipment_tag,
                "alert_summary": d.alert_summary,
                "confidence": d.confidence_level,
                "hypotheses": [
                    {
                        "cause": h.cause,
                        "confidence": h.confidence,
                        "category": h.category,
                        "evidence": h.evidence,
                    }
                    for h in d.hypotheses
                ],
                "recommended_actions": [
                    {
                        "action": a.action,
                        "priority": a.priority,
                        "effort": a.estimated_effort,
                        "parts_needed": a.parts_needed,
                        "sop_reference": a.sop_reference,
                    }
                    for a in d.recommended_actions
                ],
            }
            for d in result.diagnoses
        ],
        "health_summary": result.health_summary,
    }

    # Save sensor analysis report
    equipment_tags = list(set(r.equipment_tag for r in data.readings))
    sensor_report_path = report_saver.save_sensor_analysis(
        report_data=response_data,
        equipment_tags=equipment_tags,
        alerts=result.alerts,
    )
    response_data["report_saved_to"] = sensor_report_path

    # Save individual diagnosis reports
    diagnosis_report_paths = []
    for d in result.diagnoses:
        diag_data = {
            "equipment_tag": d.equipment_tag,
            "alert_summary": d.alert_summary,
            "confidence": d.confidence_level,
            "hypotheses": [
                {"cause": h.cause, "confidence": h.confidence, "category": h.category, "evidence": h.evidence}
                for h in d.hypotheses
            ],
            "recommended_actions": [
                {"action": a.action, "priority": a.priority, "effort": a.estimated_effort,
                 "parts_needed": a.parts_needed, "sop_reference": a.sop_reference}
                for a in d.recommended_actions
            ],
            "similar_past_incidents": d.similar_past_incidents,
        }
        path = report_saver.save_fault_diagnosis(
            report_data=diag_data,
            equipment_tag=d.equipment_tag,
            confidence_level=d.confidence_level,
        )
        diagnosis_report_paths.append(path)
    response_data["diagnosis_reports_saved_to"] = diagnosis_report_paths

    return response_data

@router.post("/predict-maintenance")
async def predict_maintenance(request: Request, data: PredictiveRequest):
    """
    Run predictive maintenance analysis for specific equipment.
    Returns Remaining Useful Life estimate and maintenance recommendations.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    report = await orchestrator.get_predictive_report(
        equipment_tag=data.equipment_tag,
        parameter_history=data.parameter_history,
        critical_limits=data.critical_limits,
        equipment_type=data.equipment_type,
        hours_in_service=data.hours_in_service,
        next_pm=data.next_pm_date,
    )

    response_data = {
        "equipment_tag": report.equipment_tag,
        "overall_health_score": report.overall_health_score,
        "risk_summary": report.risk_summary,
        "rul_estimates": [
            {
                "parameter": r.parameter,
                "days_to_failure": r.estimated_days_to_failure,
                "confidence_interval": r.confidence_interval,
                "risk_score": r.risk_score,
                "method": r.method,
                "health_pct": r.current_health_pct,
            }
            for r in report.rul_estimates
        ],
        "recommendations": [
            {
                "action": r.action,
                "recommended_date": r.recommended_date.isoformat(),
                "urgency": r.urgency,
                "cost_early_intervention": r.cost_of_early_intervention,
                "cost_unplanned_failure": r.cost_of_unplanned_failure,
                "reasoning": r.reasoning,
            }
            for r in report.maintenance_recommendations
        ],
    }

    # Save predictive report
    pred_report_path = report_saver.save_predictive_report(
        report_data=response_data,
        equipment_tag=data.equipment_tag,
        risk_level=report.risk_summary,
    )
    response_data["report_saved_to"] = pred_report_path

    return response_data

@router.post("/shift-handover")
async def generate_handover(request: Request, data: HandoverRequest):
    """
    Generate a shift handover report for the specified time window.
    Summarizes all events, alarms, and pending items.
    """
    neo4j = getattr(request.app.state, "neo4j", None)
    orchestrator = AgentOrchestrator(neo4j_client=neo4j)

    report, formatted_text = await orchestrator.generate_shift_handover(
        shift_start=data.shift_start,
        shift_end=data.shift_end,
    )

    response_data = {
        "shift": {
            "type": report.shift_type,
            "start": report.shift_start.isoformat(),
            "end": report.shift_end.isoformat(),
        },
        "summary": report.executive_summary,
        "stats": {
            "total_alarms": report.total_alarms,
            "critical_alarms": report.critical_alarms,
            "maintenance_actions": report.maintenance_actions,
        },
        "critical_items": report.critical_items,
        "work_in_progress": report.work_in_progress,
        "watch_items": report.watch_items,
        "upcoming": report.upcoming_activities,
        "formatted_report": formatted_text,
    }

    # Collect equipment tags from critical items and health changes
    equipment_tags = list(set(
        item.get("equipment", "")
        for item in report.critical_items + report.equipment_health_changes + report.work_in_progress
        if item.get("equipment")
    ))

    # Save shift handover report
    handover_path = report_saver.save_shift_handover(
        report_data=response_data,
        shift_type=report.shift_type,
        has_critical=report.critical_alarms > 0,
        shift_start=report.shift_start,
        equipment_tags=equipment_tags,
    )
    response_data["report_saved_to"] = handover_path

    return response_data

@router.get("/reports")
async def list_reports(
    category: Optional[str] = None,
    equipment: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    List all saved reports. Filter by category, equipment tag, or status.

    Categories: sensor_analysis, fault_diagnosis, predictive, shift_handover
    Status in filename: NORMAL, WARNING, CRITICAL, HIGH-RISK, LOW-RISK, etc.
    """
    from pathlib import Path
    import json

    base = report_saver.base_dir
    results = []

    # Determine which subdirs to scan
    if category and (base / category).is_dir():
        subdirs = [base / category]
    else:
        subdirs = [d for d in base.iterdir() if d.is_dir()]

    for subdir in subdirs:
        for filepath in sorted(subdir.glob("*.json"), reverse=True):
            name = filepath.stem  # e.g. P-101A_day_CRITICAL_20240701_143022
            parts = name.split("_")

            # Apply filters
            if equipment and equipment.upper() not in name.upper():
                continue
            if status and status.upper() not in name.upper():
                continue

            # Parse naming convention
            file_info = {
                "filename": filepath.name,
                "category": subdir.name,
                "path": str(filepath),
                "size_bytes": filepath.stat().st_size,
                "created": datetime.fromtimestamp(filepath.stat().st_ctime).isoformat(),
            }

            # Extract equipment/shift/status from filename parts
            if len(parts) >= 4:
                # Last two parts are date_time, work backwards
                file_info["timestamp"] = f"{parts[-2]}_{parts[-1]}"
                file_info["status_label"] = parts[-3] if len(parts) >= 4 else ""
                file_info["shift"] = parts[-4] if len(parts) >= 5 else ""
                file_info["equipment"] = "_".join(parts[:-4]) if len(parts) > 4 else parts[0]

            results.append(file_info)

    return {
        "total_reports": len(results),
        "reports_directory": str(base),
        "reports": results[:100],  # Limit to 100 most recent
    }

@router.get("/reports/{category}/{filename}")
async def get_report(category: str, filename: str):
    """Retrieve a specific saved report by category and filename."""
    from pathlib import Path
    import json

    filepath = report_saver.base_dir / category / filename
    if not filepath.exists() or not filepath.is_file():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Report not found: {category}/{filename}")

    # Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid filename")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "filename": filename,
        "category": category,
        "data": data,
    }