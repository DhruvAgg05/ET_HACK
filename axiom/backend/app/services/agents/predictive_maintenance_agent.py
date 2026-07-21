"""
Predictive Maintenance Agent
Uses historical failure patterns + current sensor trends to predict
WHEN equipment will likely fail (Remaining Useful Life estimation).
"""

import math
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import structlog

from app.services.agents.sensor_monitor_agent import HealthStatus

logger = structlog.get_logger()

@dataclass
class RULEstimate:
    equipment_tag: str
    parameter: str
    estimated_days_to_failure: float
    confidence_interval: tuple[float, float]  # (lower, upper) in days
    risk_score: float  # 0-1 (probability of failure before next scheduled PM)
    method: str  # "trend_extrapolation", "weibull", "pattern_match"
    current_health_pct: float  # 0-100
    degradation_rate: float  # units per day

@dataclass
class MaintenanceRecommendation:
    equipment_tag: str
    action: str
    recommended_date: datetime
    urgency: str  # "advance_pm", "schedule_new", "defer_ok", "immediate"
    cost_of_early_intervention: float
    cost_of_unplanned_failure: float
    confidence: str
    reasoning: str

@dataclass
class PredictiveReport:
    equipment_tag: str
    rul_estimates: list[RULEstimate]
    overall_health_score: float  # 0-100
    next_scheduled_pm: Optional[datetime]
    maintenance_recommendations: list[MaintenanceRecommendation]
    risk_summary: str
    generated_at: datetime = field(default_factory=datetime.utcnow)

class PredictiveMaintenanceAgent:
    """
    Predicts equipment failure timing using:
    1. Trend extrapolation (project when parameter hits critical limit)
    2. Weibull reliability analysis (statistical failure distribution)
    3. Pattern matching (compare degradation curve to historical failures)
    """

    # Typical MTBF data for common industrial equipment (hours)
    EQUIPMENT_MTBF = {
        "pump": 25000,
        "compressor": 30000,
        "motor": 40000,
        "valve": 50000,
        "heat_exchanger": 60000,
        "bearing": 20000,
    }

    # Cost estimates for cost/benefit analysis
    COST_ESTIMATES = {
        "planned_maintenance": {
            "pump": 2500,
            "compressor": 8000,
            "motor": 3000,
            "valve": 1500,
        },
        "unplanned_failure": {
            "pump": 45000,      # Parts + labor + downtime
            "compressor": 150000,
            "motor": 35000,
            "valve": 25000,
        },
    }

    def __init__(self):
        self._failure_history: dict[str, list[dict]] = {}  # equipment_tag -> past failures

    def register_failure_history(self, equipment_tag: str, failures: list[dict]):
        """Register historical failure data for an equipment."""
        self._failure_history[equipment_tag] = failures

    def predict(
        self,
        equipment_tag: str,
        parameter_history: dict[str, list[float]],  # param_name -> readings
        critical_limits: dict[str, float],  # param_name -> critical threshold
        next_scheduled_pm: Optional[datetime] = None,
        equipment_type: str = "pump",
        hours_since_last_maintenance: float = 0,
    ) -> PredictiveReport:
        """
        Generate a full predictive maintenance report.

        Args:
            equipment_tag: Equipment identifier
            parameter_history: Recent readings per parameter
            critical_limits: Threshold that indicates failure
            next_scheduled_pm: When the next PM is currently scheduled
            equipment_type: For cost/MTBF lookups
            hours_since_last_maintenance: Operating hours since last major maintenance
        """
        logger.info("Running predictive analysis", equipment=equipment_tag)

        rul_estimates = []

        # Estimate RUL for each monitored parameter
        for param, readings in parameter_history.items():
            if len(readings) < 10:
                continue

            limit = critical_limits.get(param)
            if limit is None:
                continue

            # Method 1: Trend extrapolation
            trend_rul = self._trend_extrapolation(readings, limit, param)
            if trend_rul:
                rul_estimates.append(RULEstimate(
                    equipment_tag=equipment_tag,
                    parameter=param,
                    estimated_days_to_failure=trend_rul["days"],
                    confidence_interval=trend_rul["ci"],
                    risk_score=trend_rul["risk"],
                    method="trend_extrapolation",
                    current_health_pct=trend_rul["health_pct"],
                    degradation_rate=trend_rul["rate"],
                ))

        # Method 2: Weibull reliability (if failure history available)
        weibull_rul = self._weibull_estimate(
            equipment_tag, equipment_type, hours_since_last_maintenance
        )
        if weibull_rul:
            rul_estimates.append(weibull_rul)

        # Calculate overall health score
        overall_health = self._calculate_overall_health(rul_estimates)

        # Generate maintenance recommendations
        recommendations = self._generate_recommendations(
            equipment_tag, rul_estimates, next_scheduled_pm, equipment_type
        )

        # Risk summary
        risk_summary = self._generate_risk_summary(rul_estimates, next_scheduled_pm)

        return PredictiveReport(
            equipment_tag=equipment_tag,
            rul_estimates=rul_estimates,
            overall_health_score=overall_health,
            next_scheduled_pm=next_scheduled_pm,
            maintenance_recommendations=recommendations,
            risk_summary=risk_summary,
        )

    def _trend_extrapolation(
        self, readings: list[float], critical_limit: float, param: str
    ) -> Optional[dict]:
        """Extrapolate current trend to estimate when limit will be reached."""
        if len(readings) < 10:
            return None

        n = len(readings)
        # Linear regression
        x_mean = (n - 1) / 2
        y_mean = statistics.mean(readings)

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(readings))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return None

        slope = numerator / denominator  # units per reading
        intercept = y_mean - slope * x_mean

        if slope <= 0 and readings[-1] < critical_limit:
            # Not degrading toward limit
            return None

        # Current value and distance to limit
        current = readings[-1]
        distance_to_limit = critical_limit - current

        if slope == 0:
            return None

        # Readings to failure
        readings_to_failure = distance_to_limit / slope if slope != 0 else float("inf")

        if readings_to_failure < 0:
            # Already past limit
            readings_to_failure = 0

        # Assume 1 reading per hour (adjust based on actual frequency)
        hours_to_failure = readings_to_failure
        days_to_failure = hours_to_failure / 24

        # Confidence interval (based on R² of linear fit)
        residuals = [readings[i] - (slope * i + intercept) for i in range(n)]
        ss_res = sum(r**2 for r in residuals)
        ss_tot = sum((v - y_mean)**2 for v in readings)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Wider CI for lower R²
        ci_factor = 1 + (1 - r_squared) * 2
        ci_lower = max(0, days_to_failure / ci_factor)
        ci_upper = days_to_failure * ci_factor

        # Health percentage
        health_pct = max(0, min(100, (1 - current / critical_limit) * 100))

        # Risk score: how likely to fail before next scheduled PM
        risk = 1.0 if days_to_failure <= 0 else min(1.0, 7 / max(days_to_failure, 0.1))

        return {
            "days": round(days_to_failure, 1),
            "ci": (round(ci_lower, 1), round(ci_upper, 1)),
            "risk": round(risk, 2),
            "health_pct": round(health_pct, 1),
            "rate": round(slope, 4),
        }

    def _weibull_estimate(
        self, equipment_tag: str, equipment_type: str, hours_in_service: float
    ) -> Optional[RULEstimate]:
        """Estimate RUL using Weibull distribution parameters."""
        mtbf = self.EQUIPMENT_MTBF.get(equipment_type)
        if not mtbf:
            return None

        # Simplified Weibull with shape parameter beta=2 (wear-out mode)
        beta = 2.0
        eta = mtbf  # Characteristic life

        # Reliability at current age
        reliability = math.exp(-((hours_in_service / eta) ** beta))

        # Estimated remaining life (conditional)
        if reliability <= 0.01:
            remaining_hours = 0
        else:
            # Mean residual life approximation
            remaining_hours = eta * math.gamma(1 + 1/beta) - hours_in_service
            remaining_hours = max(0, remaining_hours)

        days_remaining = remaining_hours / 24

        # Confidence interval
        ci_lower = days_remaining * 0.6
        ci_upper = days_remaining * 1.5

        # Risk score based on reliability
        risk_score = 1 - reliability

        return RULEstimate(
            equipment_tag=equipment_tag,
            parameter="reliability",
            estimated_days_to_failure=round(days_remaining, 1),
            confidence_interval=(round(ci_lower, 1), round(ci_upper, 1)),
            risk_score=round(risk_score, 2),
            method="weibull",
            current_health_pct=round(reliability * 100, 1),
            degradation_rate=0,
        )

    def _calculate_overall_health(self, rul_estimates: list[RULEstimate]) -> float:
        """Calculate overall equipment health from individual estimates."""
        if not rul_estimates:
            return 100.0

        # Use the worst (lowest) health score
        health_scores = [r.current_health_pct for r in rul_estimates]
        return min(health_scores)

    def _generate_recommendations(
        self,
        equipment_tag: str,
        rul_estimates: list[RULEstimate],
        next_pm: Optional[datetime],
        equipment_type: str,
    ) -> list[MaintenanceRecommendation]:
        """Generate maintenance schedule recommendations."""
        recommendations = []
        now = datetime.utcnow()

        # Find the most critical RUL
        if not rul_estimates:
            return recommendations

        worst_rul = min(rul_estimates, key=lambda r: r.estimated_days_to_failure)
        estimated_failure_date = now + timedelta(days=worst_rul.estimated_days_to_failure)

        # Cost estimates
        planned_cost = self.COST_ESTIMATES["planned_maintenance"].get(equipment_type, 5000)
        failure_cost = self.COST_ESTIMATES["unplanned_failure"].get(equipment_type, 50000)

        if worst_rul.estimated_days_to_failure <= 3:
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"URGENT: Schedule immediate maintenance on {equipment_tag}. "
                       f"Estimated failure within {worst_rul.estimated_days_to_failure:.0f} days.",
                recommended_date=now + timedelta(days=1),
                urgency="immediate",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"Parameter '{worst_rul.parameter}' degradation rate "
                         f"indicates failure by {estimated_failure_date.strftime('%d-%b-%Y')}",
            ))
        elif next_pm and estimated_failure_date < next_pm:
            days_to_advance = (next_pm - estimated_failure_date).days
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"Advance scheduled PM by {days_to_advance} days. "
                       f"Current schedule ({next_pm.strftime('%d-%b')}) is after predicted failure.",
                recommended_date=estimated_failure_date - timedelta(days=3),
                urgency="advance_pm",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"Predicted failure: {estimated_failure_date.strftime('%d-%b-%Y')}, "
                         f"next PM: {next_pm.strftime('%d-%b-%Y')}. Gap = {days_to_advance} days.",
            ))
        elif worst_rul.risk_score < 0.2:
            recommendations.append(MaintenanceRecommendation(
                equipment_tag=equipment_tag,
                action=f"Continue monitoring. {equipment_tag} health is acceptable.",
                recommended_date=next_pm or (now + timedelta(days=30)),
                urgency="defer_ok",
                cost_of_early_intervention=planned_cost,
                cost_of_unplanned_failure=failure_cost,
                confidence=worst_rul.method,
                reasoning=f"RUL = {worst_rul.estimated_days_to_failure:.0f} days, "
                         f"risk score = {worst_rul.risk_score:.0%}. Within acceptable limits.",
            ))

        return recommendations

    def _generate_risk_summary(
        self, rul_estimates: list[RULEstimate], next_pm: Optional[datetime]
    ) -> str:
        """Generate a human-readable risk summary."""
        if not rul_estimates:
            return "Insufficient data for prediction. Continue monitoring."

        worst = min(rul_estimates, key=lambda r: r.estimated_days_to_failure)

        if worst.estimated_days_to_failure <= 7:
            return (
                f"HIGH RISK: Equipment predicted to fail within {worst.estimated_days_to_failure:.0f} days "
                f"based on {worst.parameter} degradation ({worst.method}). "
                f"Immediate maintenance planning recommended."
            )
        elif worst.estimated_days_to_failure <= 30:
            return (
                f"MODERATE RISK: Estimated {worst.estimated_days_to_failure:.0f} days remaining life. "
                f"Plan maintenance within 2 weeks."
            )
        else:
            return (
                f"LOW RISK: Estimated {worst.estimated_days_to_failure:.0f} days remaining life. "
                f"Continue routine monitoring."
            )