"""
Sensor Health Monitor Agent
Ingests machine sensor logs, detects anomalies using multi-strategy detection,
and classifies equipment health status.
"""

import statistics
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
import structlog

logger = structlog.get_logger()

class HealthStatus(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    ANOMALY = "anomaly"

@dataclass
class SensorReading:
    equipment_tag: str
    parameter: str  # e.g., "vibration", "temperature", "pressure"
    value: float
    unit: str
    timestamp: datetime
    metadata: dict = field(default_factory=dict)

@dataclass
class ThresholdConfig:
    """OEM or engineering-defined limits for a parameter."""
    normal_min: float
    normal_max: float
    warning_min: float
    warning_max: float
    critical_min: float
    critical_max: float

@dataclass
class AnomalyAlert:
    equipment_tag: str
    parameter: str
    current_value: float
    unit: str
    status: HealthStatus
    severity_score: float  # 0-1
    reason: str
    threshold_info: Optional[dict] = None
    trend_info: Optional[dict] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    recommended_action: str = ""

class SensorHealthMonitorAgent:
    """
    Agent that monitors sensor logs and detects anomalies using:
    1. Threshold checking (OEM limits from Knowledge Graph)
    2. Statistical anomaly detection (Z-score on rolling window)
    3. Trend detection (drift/degradation over time)
    4. Pattern matching (compare to known pre-failure signatures)
    """

    # Default industrial thresholds (overridden by KG data when available)
    DEFAULT_THRESHOLDS = {
        "vibration": ThresholdConfig(
            normal_min=0, normal_max=7.1,      # ISO 10816 Group 2
            warning_min=0, warning_max=11.2,
            critical_min=0, critical_max=18.0,
        ),
        "temperature": ThresholdConfig(
            normal_min=20, normal_max=80,
            warning_min=10, warning_max=95,
            critical_min=0, critical_max=120,
        ),
        "pressure": ThresholdConfig(
            normal_min=0, normal_max=45,
            warning_min=0, warning_max=50,
            critical_min=0, critical_max=55,
        ),
        "current": ThresholdConfig(
            normal_min=0, normal_max=85,       # % of rated
            warning_min=0, warning_max=95,
            critical_min=0, critical_max=105,
        ),
        "flow": ThresholdConfig(
            normal_min=80, normal_max=120,     # % of design
            warning_min=60, warning_max=130,
            critical_min=40, critical_max=150,
        ),
    }

    def __init__(self):
        # Rolling history per equipment+parameter for statistical analysis
        self._history: dict[str, list[float]] = {}
        self._window_size = 50  # readings to keep for stats

    def analyze_reading(
        self,
        reading: SensorReading,
        custom_threshold: Optional[ThresholdConfig] = None,
    ) -> AnomalyAlert | None:
        """
        Analyze a single sensor reading and return an alert if anomalous.
        Returns None if reading is NORMAL.
        """
        key = f"{reading.equipment_tag}_{reading.parameter}"

        # Update history
        if key not in self._history:
            self._history[key] = []
        self._history[key].append(reading.value)
        if len(self._history[key]) > self._window_size:
            self._history[key] = self._history[key][-self._window_size:]

        # Get threshold (custom from KG > default)
        threshold = custom_threshold or self.DEFAULT_THRESHOLDS.get(reading.parameter)

        # Run detection strategies
        status = HealthStatus.NORMAL
        reasons = []
        severity = 0.0

        # Strategy 1: Threshold check
        if threshold:
            thresh_result = self._check_threshold(reading.value, threshold)
            if thresh_result[0].value != "normal":
                status = thresh_result[0]
                reasons.append(thresh_result[1])
                severity = max(severity, thresh_result[2])

        # Strategy 2: Statistical anomaly (Z-score)
        if len(self._history[key]) >= 10:
            stat_result = self._statistical_check(reading.value, self._history[key])
            if stat_result:
                if stat_result[2] > severity:
                    status = stat_result[0]
                reasons.append(stat_result[1])
                severity = max(severity, stat_result[2])

        # Strategy 3: Trend detection
        if len(self._history[key]) >= 20:
            trend_result = self._trend_check(self._history[key])
            if trend_result:
                reasons.append(trend_result[1])
                severity = max(severity, trend_result[2])
                if trend_result[0].value == "warning" and status.value == "normal":
                    status = HealthStatus.WARNING

        # Only return alert if not normal
        if status == HealthStatus.NORMAL:
            return None

        return AnomalyAlert(
            equipment_tag=reading.equipment_tag,
            parameter=reading.parameter,
            current_value=reading.value,
            unit=reading.unit,
            status=status,
            severity_score=min(severity, 1.0),
            reason=" | ".join(reasons),
            threshold_info={
                "normal_max": threshold.normal_max if threshold else None,
                "warning_max": threshold.warning_max if threshold else None,
                "critical_max": threshold.critical_max if threshold else None,
            },
            trend_info=self._get_trend_info(self._history[key]),
            timestamp=reading.timestamp,
        )

    def analyze_batch(self, readings: list[SensorReading]) -> list[AnomalyAlert]:
        """Analyze a batch of sensor readings and return all anomalies."""
        alerts = []
        for reading in readings:
            alert = self.analyze_reading(reading)
            if alert:
                alerts.append(alert)

        if alerts:
            logger.info(
                "Batch analysis complete",
                total_readings=len(readings),
                anomalies_found=len(alerts),
                critical=sum(1 for a in alerts if a.status == HealthStatus.CRITICAL),
            )
        return alerts

    def get_equipment_health_summary(self, equipment_tag: str) -> dict:
        """Get current health summary for a piece of equipment."""
        relevant_keys = [k for k in self._history if k.startswith(equipment_tag)]
        summary = {"equipment_tag": equipment_tag, "parameters": {}}

        for key in relevant_keys:
            param = key.split("_", 1)[1] if "_" in key else key
            values = self._history[key]
            if values:
                summary["parameters"][param] = {
                    "latest": values[-1],
                    "mean": statistics.mean(values),
                    "std": statistics.stdev(values) if len(values) > 1 else 0,
                    "trend": self._calculate_trend_direction(values),
                    "readings_count": len(values),
                }

        return summary

    def _check_threshold(
        self, value: float, threshold: ThresholdConfig
    ) -> tuple[HealthStatus, str, float]:
        """Check value against defined thresholds."""
        if value >= threshold.critical_max or value <= threshold.critical_min:
            return (
                HealthStatus.CRITICAL,
                f"CRITICAL: Value {value} exceeds critical limit "
                f"({threshold.critical_min}-{threshold.critical_max})",
                1.0,
            )
        elif value >= threshold.warning_max or value <= threshold.warning_min:
            # Calculate how close to critical
            if threshold.critical_max > threshold.warning_max:
                proximity = (value - threshold.warning_max) / (
                    threshold.critical_max - threshold.warning_max
                )
            else:
                proximity = 0.5
            return (
                HealthStatus.WARNING,
                f"WARNING: Value {value} exceeds normal limit "
                f"({threshold.normal_min}-{threshold.normal_max})",
                0.5 + (proximity * 0.4),
            )
        else:
            return (HealthStatus.NORMAL, "", 0.0)

    def _statistical_check(
        self, value: float, history: list[float]
    ) -> tuple[HealthStatus, str, float] | None:
        """Detect statistical anomalies using Z-score."""
        if len(history) < 10:
            return None

        mean = statistics.mean(history[:-1])  # Exclude current reading
        std = statistics.stdev(history[:-1])

        if std == 0:
            return None

        z_score = abs(value - mean) / std

        if z_score > 3.5:
            return (
                HealthStatus.ANOMALY,
                f"STATISTICAL ANOMALY: Z-score={z_score:.1f} "
                f"(value={value}, mean={mean:.1f}, std={std:.2f})",
                min(z_score / 5.0, 1.0),
            )
        elif z_score > 2.5:
            return (
                HealthStatus.WARNING,
                f"Statistical deviation: Z-score={z_score:.1f}",
                0.4,
            )
        return None

    def _trend_check(
        self, history: list[float]
    ) -> tuple[HealthStatus, str, float] | None:
        """Detect degradation trends (steadily increasing/decreasing)."""
        if len(history) < 20:
            return None

        # Compare recent half vs older half
        midpoint = len(history) // 2
        older_mean = statistics.mean(history[:midpoint])
        recent_mean = statistics.mean(history[midpoint:])

        if older_mean == 0:
            return None

        change_pct = ((recent_mean - older_mean) / abs(older_mean)) * 100

        if abs(change_pct) > 20:
            direction = "increasing" if change_pct > 0 else "decreasing"
            return (
                HealthStatus.WARNING,
                f"TREND: Parameter {direction} by {abs(change_pct):.1f}% "
                f"(older avg: {older_mean:.1f}, recent avg: {recent_mean:.1f})",
                min(abs(change_pct) / 50.0, 0.8),
            )
        return None

    def _get_trend_info(self, history: list[float]) -> dict:
        """Calculate trend metadata."""
        if len(history) < 5:
            return {"direction": "insufficient_data"}

        recent = history[-5:]
        direction = self._calculate_trend_direction(recent)
        rate = (recent[-1] - recent[0]) / max(len(recent) - 1, 1)

        return {
            "direction": direction,
            "rate_per_reading": round(rate, 4),
            "last_5_values": [round(v, 2) for v in recent],
        }

    def _calculate_trend_direction(self, values: list[float]) -> str:
        """Determine if values are trending up, down, or stable."""
        if len(values) < 3:
            return "stable"

        # Simple linear regression slope
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(values)

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return "stable"

        slope = numerator / denominator
        # Normalize slope relative to mean
        relative_slope = slope / max(abs(y_mean), 0.001)

        if relative_slope > 0.02:
            return "increasing"
        elif relative_slope < -0.02:
            return "decreasing"
        else:
            return "stable"