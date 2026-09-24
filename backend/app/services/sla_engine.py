"""
CIVICFLOW AI — Deterministic SLA Monitoring & Escalation Subsystem
Continuous evaluation of active complaints, deadline warnings, breach detection,
and automated multi-tier administrative escalations.
"""
from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional
from uuid import uuid4

from app.core.events import event_bus
from app.db.repository import repo
from app.models.entities import (
    Complaint, ComplaintEvent, ComplaintStatus, Escalation, 
    EscalationLevel, Notification, PriorityLevel
)

logger = logging.getLogger("civicflow.sla_engine")


class SlaEngine:
    def evaluate_complaint(self, complaint: Complaint) -> Dict[str, any]:
        """
        Evaluates a single active complaint against statutory SLA deadlines.
        """
        if complaint.status in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED, ComplaintStatus.REJECTED]:
            return {"status": "RESOLVED_OR_CLOSED", "action": "NONE"}

        if not complaint.sla_target_at:
            return {"status": "NO_SLA_SET", "action": "NONE"}

        now = datetime.now(timezone.utc)
        target = complaint.sla_target_at
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)

        warning_at = complaint.sla_warning_at or (target - (target - complaint.created_at) * 0.33)
        if warning_at.tzinfo is None:
            warning_at = warning_at.replace(tzinfo=timezone.utc)

        # 1. Check for Breach
        if now >= target:
            hours_overdue = round((now - target).total_seconds() / 3600, 2)
            escalation = self._trigger_breach_escalation(complaint, hours_overdue)
            return {
                "status": "BREACHED",
                "hours_overdue": hours_overdue,
                "escalation_id": escalation.id if escalation else None,
                "action": "ESCALATED",
            }

        # 2. Check for Warning
        if now >= warning_at:
            hours_remaining = round((target - now).total_seconds() / 3600, 2)
            self._trigger_warning_alert(complaint, hours_remaining)
            return {
                "status": "WARNING",
                "hours_remaining": hours_remaining,
                "action": "WARNING_NOTIFIED",
            }

        return {"status": "ON_TRACK", "action": "NONE"}

    def _trigger_breach_escalation(self, complaint: Complaint, hours_overdue: float) -> Optional[Escalation]:
        """Triggers administrative escalation upon SLA deadline breach."""
        # Avoid duplicate escalations for the same complaint if already escalated
        existing_esc = next((e for e in repo.escalations if e.complaint_id == complaint.id and not e.is_resolved), None)
        if existing_esc:
            return existing_esc

        # Determine escalation tier based on priority and overdue duration
        if complaint.priority == PriorityLevel.CRITICAL or hours_overdue > 12.0:
            level = EscalationLevel.MUNICIPAL_COMMISSIONER
            target_title = "Office of the Municipal Commissioner"
            new_priority = PriorityLevel.CRITICAL
        elif complaint.priority == PriorityLevel.HIGH or hours_overdue > 4.0:
            level = EscalationLevel.ZONAL_OFFICER
            target_title = f"Zonal Director ({complaint.ward_number or 'Central Zone'})"
            new_priority = PriorityLevel.CRITICAL
        else:
            level = EscalationLevel.WARD_SUPERVISOR
            target_title = f"Ward Supervisor ({complaint.ward_number or 'Ward 3'})"
            new_priority = PriorityLevel.HIGH

        memo = (
            f"STATUTORY SLA BREACH ESCALATION\n"
            f"Grievance: {complaint.tracking_number} — '{complaint.title}'\n"
            f"Department: {complaint.department_name or 'Municipal Desk'}\n"
            f"Overdue Duration: {hours_overdue} Hours\n"
            f"Escalation Level: {level.value} ({target_title})\n"
            f"Action: Priority boosted to {new_priority.value}. Immediate field dispatch required."
        )

        escalation = Escalation(
            complaint_id=complaint.id,
            escalation_level=level,
            reason=f"SLA breached by {hours_overdue} hours. Mandatory statutory escalation.",
            triggered_by="SLA_ENGINE",
            previous_priority=complaint.priority,
            new_priority=new_priority,
            escalated_to_name=target_title,
            resolution_notes=memo,
        )
        repo.create_escalation(escalation)

        # Notify Authority
        repo.notifications.append(Notification(
            complaint_id=complaint.id,
            notification_type="AUTHORITY_SLA_BREACH",
            severity="CRITICAL",
            title=f"URGENT ESCALATION: {complaint.tracking_number}",
            message=f"Grievance {complaint.tracking_number} breached SLA by {hours_overdue}h. Escalated to {target_title}.",
        ))

        # Notify Citizen
        repo.notifications.append(Notification(
            complaint_id=complaint.id,
            notification_type="CITIZEN_ESCALATION_UPDATE",
            severity="WARNING",
            title="Grievance Escalated to Senior Municipal Authority",
            message=f"Your grievance {complaint.tracking_number} has been escalated to {target_title} for expedited resolution.",
        ))

        # Add Audit Event
        repo.add_complaint_event(ComplaintEvent(
            complaint_id=complaint.id,
            event_type="SLA_BREACH_ESCALATED",
            previous_state=complaint.status.value,
            new_state=ComplaintStatus.ESCALATED.value,
            actor_type="SYSTEM",
            title=f"SLA Breached — Escalated to {level.value}",
            description=f"Automated breach trigger at {hours_overdue}h overdue. Priority boosted to {new_priority.value}.",
            metadata={"hours_overdue": hours_overdue, "escalated_to": target_title},
        ))

        complaint.priority = new_priority
        return escalation

    def _trigger_warning_alert(self, complaint: Complaint, hours_remaining: float):
        """Generates warning alert when SLA threshold enters final countdown."""
        # Avoid duplicate warning events within 2 hours
        events = repo.get_complaint_events(complaint.id)
        recent_warning = next((e for e in events if e.event_type == "SLA_WARNING_GENERATED"), None)
        if recent_warning:
            return

        repo.add_complaint_event(ComplaintEvent(
            complaint_id=complaint.id,
            event_type="SLA_WARNING_GENERATED",
            actor_type="SYSTEM",
            title="SLA Warning Threshold Reached",
            description=f"Approaching deadline. {hours_remaining} hours remaining for resolution.",
            metadata={"hours_remaining": hours_remaining},
        ))

        repo.notifications.append(Notification(
            complaint_id=complaint.id,
            notification_type="OPERATOR_SLA_WARNING",
            severity="WARNING",
            title=f"SLA Warning: {complaint.tracking_number}",
            message=f"Only {hours_remaining}h remaining for {complaint.title}. Ensure field team is actively resolving.",
        ))

    def run_cycle(self) -> List[Dict[str, any]]:
        """Evaluates all open complaints in the system."""
        active = [
            c for c in repo.complaints.values() 
            if c.status not in [ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED, ComplaintStatus.REJECTED]
        ]
        results = []
        for c in active:
            res = self.evaluate_complaint(c)
            results.append({"complaint_id": c.id, "tracking": c.tracking_number, **res})
        return results


sla_engine = SlaEngine()
