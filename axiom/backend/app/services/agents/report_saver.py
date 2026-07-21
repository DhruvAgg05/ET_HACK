"""
Report persistence service.
Saves all agent-generated reports to disk with structured naming convention.

Naming Convention:
    {equipment_tag}_{shift}_{status}_{YYYYMMDD_HHMMSS}.json

Examples:
    P-101A_day_CRITICAL_20240701_143022.json
    C-301_night_NORMAL_20240701_230015.json
    MULTI_day_WARNING_20240702_060000.json        (multi-equipment batch)
    FLEET_day_HANDOVER_20240702_180000.json        (shift handover)
    P-101A_NA_PREDICTION_20240703_091500.json      (predictive report)

Directory structure:
    data/reports/
    ├── sensor_analysis/       # From /analyze-sensors
    ├── fault_diagnosis/       # Individual diagnosis reports
    ├── predictive/            # From /predict-maintenance
    └── shift_handover/        # From /shift-handover
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any
import structlog

from app.config import settings

logger = structlog.get_logger()

REPORTS_BASE = Path(settings.upload_dir).parent / "reports"

def _sanitize(value: str) -> str:
    """Sanitize a string for use in filenames. Remove/replace unsafe chars."""
    safe = value.replace("/", "-").replace("\\", "-").replace(" ", "_")
    # Keep only alphanumeric, dash, underscore
    return "".join(c for c in safe if c.isalnum() or c in "-_").strip("_-")

def _determine_shift(timestamp: datetime | None = None) -> str:
    """Determine shift name from hour: day (06-14), evening (14-22), night (22-06)."""
    if timestamp is None:
        timestamp = datetime.utcnow()
    hour = timestamp.hour
    if 6 <= hour < 14:
        return "day"
    elif 14 <= hour < 22:
        return "evening"
    else:
        return "night"

def _determine_status(alerts: list | None = None, has_critical: bool = False) -> str:
    """Determine overall status label for filename."""
    if has_critical:
        return "CRITICAL"
    if alerts:
        severities = []
        for a in alerts:
            if hasattr(a, "status"):
                severities.append(a.status.value if hasattr(a.status, "value") else str(a.status))
            elif isinstance(a, dict):
                severities.append(a.get("status", ""))
        if "critical" in severities:
            return "CRITICAL"
        if "warning" in severities or "anomaly" in severities:
            return "WARNING"
    return "NORMAL"

class ReportSaver:
    """Persists agent reports to structured directories with naming convention."""

    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir else REPORTS_BASE
        # Create subdirectories
        for subdir in ["sensor_analysis", "fault_diagnosis", "predictive", "shift_handover"]:
            (self.base_dir / subdir).mkdir(parents=True, exist_ok=True)

    def save_sensor_analysis(
        self,
        report_data: dict,
        equipment_tags: list[str],
        alerts: list,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save sensor analysis report.
        Name: {equipment}_{shift}_{status}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = self._equipment_label(equipment_tags)
        shift = _determine_shift(ts)
        status = _determine_status(alerts)

        filename = f"{equipment}_{shift}_{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "sensor_analysis" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_fault_diagnosis(
        self,
        report_data: dict,
        equipment_tag: str,
        confidence_level: str,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save individual fault diagnosis report.
        Name: {equipment}_{shift}_{confidence}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = _sanitize(equipment_tag)
        shift = _determine_shift(ts)
        status = confidence_level.upper()  # HIGH / MEDIUM / LOW

        filename = f"{equipment}_{shift}_DIAGNOSIS-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "fault_diagnosis" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_predictive_report(
        self,
        report_data: dict,
        equipment_tag: str,
        risk_level: str,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Save predictive maintenance report.
        Name: {equipment}_{shift}_{risk}_{timestamp}.json
        """
        ts = timestamp or datetime.utcnow()
        equipment = _sanitize(equipment_tag)
        shift = _determine_shift(ts)

        # Map health to status label
        if "HIGH RISK" in risk_level.upper():
            status = "HIGH-RISK"
        elif "MODERATE" in risk_level.upper():
            status = "MODERATE-RISK"
        else:
            status = "LOW-RISK"

        filename = f"{equipment}_{shift}_PREDICTION-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "predictive" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def save_shift_handover(
        self,
        report_data: dict,
        shift_type: str,
        has_critical: bool,
        shift_start: datetime,
        equipment_tags: list[str] | None = None,
    ) -> str:
        """
        Save shift handover report.
        Name: {equipment}_{shift}_{status}_{timestamp}.json
        """
        ts = shift_start
        equipment = self._equipment_label(equipment_tags) if equipment_tags else "FLEET"
        shift = shift_type.lower()
        status = "CRITICAL" if has_critical else ("WARNING" if report_data.get("stats", {}).get("total_alarms", 0) > 0 else "NORMAL")

        filename = f"{equipment}_{shift}_HANDOVER-{status}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.base_dir / "shift_handover" / filename

        self._write(filepath, report_data)
        return str(filepath)

    def _equipment_label(self, tags: list[str]) -> str:
        """Build equipment portion of filename from tag list."""
        if not tags:
            return "UNKNOWN"
        unique = sorted(set(_sanitize(t) for t in tags if t))
        if len(unique) == 1:
            return unique[0]
        elif len(unique) <= 3:
            return "_".join(unique)
        else:
            return f"MULTI-{len(unique)}eq"

    def _write(self, filepath: Path, data: dict):
        """Write report data as JSON."""
        # Make datetimes serializable
        serializable = json.loads(
            json.dumps(data, default=str, ensure_ascii=False)
        )
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

        logger.info("Report saved", path=str(filepath))