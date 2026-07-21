"""
Shift Handover Agent
Automatically generates comprehensive shift handover reports by summarizing
all events, alarms, actions, and pending items from a shift period.
"""

import httpx
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import structlog

from app.config import settings
from app.services.agents.sensor_monitor_agent import AnomalyAlert, HealthStatus

logger = structlog.get_logger()

@dataclass
class ShiftEvent:
    timestamp: datetime
    event_type: str  # "alarm", "maintenance", "process_deviation", "safety", "operator_action"
    severity: str  # "critical", "high", "medium", "low", "info"
    equipment_tag: str
    description: str
    status: str  # "resolved", "pending", "in_progress"
    action_taken: str = ""
    assigned_to: str = ""

@dataclass
class HandoverSection:
    title: str
    items: list[dict]
    priority: str  # "critical", "high", "medium", "low"

@dataclass
class HandoverReport:
    shift_start: datetime
    shift_end: datetime
    shift_type: str  # "day", "night", "evening"
    generated_at: datetime = field(default_factory=datetime.utcnow)

    # Summary
    executive_summary: list[str] = field(default_factory=list)
    critical_items: list[dict] = field(default_factory=list)

    # Detailed sections
    alarms_summary: dict = field(default_factory=dict)
    equipment_health_changes: list[dict] = field(default_factory=list)
    work_in_progress: list[dict] = field(default_factory=list)
    completed_activities: list[dict] = field(default_factory=list)
    upcoming_activities: list[dict] = field(default_factory=list)
    watch_items: list[dict] = field(default_factory=list)

    # Stats
    total_alarms: int = 0
    critical_alarms: int = 0
    maintenance_actions: int = 0

class ShiftHandoverAgent:
    """
    Generates structured shift handover reports by:
    1. Collecting all events from the shift period
    2. Categorizing and prioritizing
    3. Summarizing using LLM
    4. Formatting for incoming team
    """

    def __init__(self):
        self._events: list[ShiftEvent] = []

    def log_event(self, event: ShiftEvent):
        """Log a shift event for inclusion in handover report."""
        self._events.append(event)

    def log_alarm(
        self,
        alert: AnomalyAlert,
        action_taken: str = "",
        resolved: bool = False,
    ):
        """Convert an anomaly alert to a shift event."""
        self._events.append(ShiftEvent(
            timestamp=alert.timestamp,
            event_type="alarm",
            severity="critical" if alert.status == HealthStatus.CRITICAL else "high",
            equipment_tag=alert.equipment_tag,
            description=f"{alert.parameter}: {alert.current_value} {alert.unit} — {alert.reason}",
            status="resolved" if resolved else "pending",
            action_taken=action_taken,
        ))

    async def generate_report(
        self,
        shift_start: datetime,
        shift_end: datetime,
        upcoming_pm: list[dict] | None = None,
    ) -> HandoverReport:
        """Generate the full shift handover report."""
        logger.info(
            "Generating handover report",
            shift_start=shift_start.isoformat(),
            shift_end=shift_end.isoformat(),
        )

        # Filter events to this shift
        shift_events = [
            e for e in self._events
            if shift_start <= e.timestamp <= shift_end
        ]

        # Determine shift type
        hour = shift_start.hour
        shift_type = "day" if 6 <= hour < 14 else ("evening" if 14 <= hour < 22 else "night")

        # Categorize events
        alarms = [e for e in shift_events if e.event_type == "alarm"]
        maintenance = [e for e in shift_events if e.event_type == "maintenance"]
        deviations = [e for e in shift_events if e.event_type == "process_deviation"]
        safety = [e for e in shift_events if e.event_type == "safety"]

        # Build alarm summary
        alarms_summary = {
            "total": len(alarms),
            "critical": sum(1 for a in alarms if a.severity == "critical"),
            "high": sum(1 for a in alarms if a.severity == "high"),
            "resolved": sum(1 for a in alarms if a.status == "resolved"),
            "pending": sum(1 for a in alarms if a.status == "pending"),
        }

        # Critical items (unresolved critical/high severity)
        critical_items = [
            {
                "equipment": e.equipment_tag,
                "issue": e.description,
                "status": e.status,
                "action": e.action_taken or "NEEDS ATTENTION",
                "time": e.timestamp.strftime("%H:%M"),
            }
            for e in shift_events
            if e.severity in ("critical", "high") and e.status != "resolved"
        ]

        # Equipment health changes
        equipment_changes = self._summarize_equipment_changes(shift_events)

        # Work in progress
        wip = [
            {
                "equipment": e.equipment_tag,
                "activity": e.description,
                "status": e.status,
                "assigned_to": e.assigned_to,
            }
            for e in shift_events
            if e.status == "in_progress"
        ]

        # Completed activities
        completed = [
            {
                "equipment": e.equipment_tag,
                "activity": e.description,
                "completed_at": e.timestamp.strftime("%H:%M"),
            }
            for e in shift_events
            if e.status == "resolved" and e.event_type == "maintenance"
        ]

        # Watch items (trending parameters, recurring alarms)
        watch_items = self._identify_watch_items(shift_events)

        # Generate executive summary
        executive_summary = await self._generate_summary(
            shift_events, alarms_summary, critical_items, shift_type
        )

        report = HandoverReport(
            shift_start=shift_start,
            shift_end=shift_end,
            shift_type=shift_type,
            executive_summary=executive_summary,
            critical_items=critical_items,
            alarms_summary=alarms_summary,
            equipment_health_changes=equipment_changes,
            work_in_progress=wip,
            completed_activities=completed,
            upcoming_activities=upcoming_pm or [],
            watch_items=watch_items,
            total_alarms=len(alarms),
            critical_alarms=alarms_summary["critical"],
            maintenance_actions=len(maintenance),
        )

        logger.info(
            "Handover report generated",
            events=len(shift_events),
            critical_items=len(critical_items),
            watch_items=len(watch_items),
        )

        return report

    def format_report_text(self, report: HandoverReport) -> str:
        """Format the handover report as readable text."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"  SHIFT HANDOVER REPORT")
        lines.append(f"  Shift: {report.shift_type.upper()} "
                     f"({report.shift_start.strftime('%d-%b %H:%M')} to "
                     f"{report.shift_end.strftime('%d-%b %H:%M')})")
        lines.append(f"  Generated: {report.generated_at.strftime('%d-%b-%Y %H:%M')}")
        lines.append("=" * 70)

        # Executive Summary
        lines.append("\n  EXECUTIVE SUMMARY:")
        for item in report.executive_summary:
            lines.append(f"    • {item}")

        # Critical Items
        if report.critical_items:
            lines.append(f"\n  ⚠️  CRITICAL ITEMS REQUIRING IMMEDIATE ATTENTION ({len(report.critical_items)}):")
            for item in report.critical_items:
                lines.append(f"    [{item['time']}] {item['equipment']}: {item['issue']}")
                lines.append(f"             Status: {item['status']} | Action: {item['action']}")

        # Alarm Summary
        lines.append(f"\n  ALARM SUMMARY:")
        lines.append(f"    Total: {report.alarms_summary.get('total', 0)} | "
                     f"Critical: {report.alarms_summary.get('critical', 0)} | "
                     f"Resolved: {report.alarms_summary.get('resolved', 0)} | "
                     f"Pending: {report.alarms_summary.get('pending', 0)}")

        # Work in Progress
        if report.work_in_progress:
            lines.append(f"\n  WORK IN PROGRESS ({len(report.work_in_progress)}):")
            for wip in report.work_in_progress:
                lines.append(f"    • {wip['equipment']}: {wip['activity']}")
                if wip.get('assigned_to'):
                    lines.append(f"      Assigned to: {wip['assigned_to']}")

        # Watch Items
        if report.watch_items:
            lines.append(f"\n  WATCH ITEMS (monitor closely):")
            for item in report.watch_items:
                lines.append(f"    • {item['equipment']}: {item['reason']}")

        # Upcoming
        if report.upcoming_activities:
            lines.append(f"\n  UPCOMING ACTIVITIES (next 12 hours):")
            for act in report.upcoming_activities[:5]:
                lines.append(f"    • {act.get('description', act)}")

        lines.append("\n" + "=" * 70)
        return "\n".join(lines)

    def _summarize_equipment_changes(self, events: list[ShiftEvent]) -> list[dict]:
        """Identify equipment whose health status changed during the shift."""
        equipment_events: dict[str, list[ShiftEvent]] = {}
        for e in events:
            equipment_events.setdefault(e.equipment_tag, []).append(e)

        changes = []
        for tag, tag_events in equipment_events.items():
            severities = [e.severity for e in tag_events]
            if "critical" in severities or "high" in severities:
                changes.append({
                    "equipment": tag,
                    "events_count": len(tag_events),
                    "worst_severity": "critical" if "critical" in severities else "high",
                    "latest_status": tag_events[-1].status,
                })

        return changes

    def _identify_watch_items(self, events: list[ShiftEvent]) -> list[dict]:
        """Identify items that need continued monitoring."""
        watch = []

        # Recurring alarms (same equipment, multiple times)
        equipment_alarm_count: dict[str, int] = {}
        for e in events:
            if e.event_type == "alarm":
                equipment_alarm_count[e.equipment_tag] = (
                    equipment_alarm_count.get(e.equipment_tag, 0) + 1
                )

        for tag, count in equipment_alarm_count.items():
            if count >= 2:
                watch.append({
                    "equipment": tag,
                    "reason": f"Recurring alarms ({count} times this shift) — may indicate developing issue",
                })

        # Unresolved items
        pending = [e for e in events if e.status == "pending" and e.severity in ("high", "medium")]
        for e in pending:
            watch.append({
                "equipment": e.equipment_tag,
                "reason": f"Unresolved: {e.description}",
            })

        return watch

    async def _generate_summary(
        self,
        events: list[ShiftEvent],
        alarms: dict,
        critical: list,
        shift_type: str,
    ) -> list[str]:
        """Generate executive summary bullets, using LLM if available."""
        # Build summary from data (works without LLM)
        summary = []

        if not events:
            summary.append("Quiet shift — no significant events or alarms.")
            return summary

        # Alarm overview
        if alarms["critical"] > 0:
            pending = alarms["pending"]
            resolved_msg = "All resolved." if pending == 0 else f"{pending} still pending."
            summary.append(
                f"{alarms['critical']} critical alarm(s) occurred. {resolved_msg}"
            )
        elif alarms["total"] > 0:
            summary.append(f"{alarms['total']} alarms total, none critical. {alarms['resolved']} resolved.")
        else:
            summary.append("No alarms during this shift.")

        # Critical items
        if critical:
            tags = ", ".join(set(item["equipment"] for item in critical))
            summary.append(f"ATTENTION NEEDED: {tags}")

        # Equipment count
        unique_equipment = set(e.equipment_tag for e in events)
        summary.append(f"{len(unique_equipment)} equipment items had events logged.")

        # Try LLM for more natural summary
        try:
            event_text = "\n".join(
                f"[{e.timestamp.strftime('%H:%M')}] {e.equipment_tag}: {e.description} ({e.status})"
                for e in events[:20]
            )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_chat_model,
                        "messages": [{
                            "role": "user",
                            "content": f"Summarize this {shift_type} shift in 2-3 bullet points "
                                      f"for the incoming maintenance team:\n\n{event_text}",
                        }],
                        "stream": False,
                        "options": {"temperature": 0.2, "num_predict": 200},
                    },
                )
                if response.status_code == 200:
                    llm_summary = response.json()["message"]["content"]
                    # Add LLM summary as additional context
                    for line in llm_summary.strip().split("\n"):
                        line = line.strip().lstrip("•-* ")
                        if line and line not in summary:
                            summary.append(line)
        except Exception:
            pass  # LLM summary is optional enhancement

        return summary[:5]

    def clear_events(self):
        """Clear event log (after shift handover is generated)."""
        self._events.clear()