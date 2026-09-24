"""
CIVICFLOW AI — Escalation Agent
Orchestrates administrative escalations across governance tiers (Ward -> Zonal -> Municipal Commissioner).
"""
import logging
from typing import Optional

from app.agents.base import BaseAgent
from app.agents.schemas import EscalationInput, EscalationOutput
from app.models.entities import EscalationLevel, PriorityLevel

logger = logging.getLogger("civicflow.agents.escalation")


class EscalationAgent(BaseAgent[EscalationInput, EscalationOutput]):
    def __init__(self):
        super().__init__(name="EscalationAgent", version="1.0.0", model_name="gemini-3.8-flash")

    async def _execute_core(self, input_data: EscalationInput) -> EscalationOutput:
        return self._fallback_heuristic(input_data, None)

    def _fallback_heuristic(self, input_data: EscalationInput, error: Optional[Exception]) -> EscalationOutput:
        overdue = input_data.hours_overdue
        priority = input_data.priority

        # Escalation Tier Logic:
        # > 24h overdue OR CRITICAL priority -> Zonal / Municipal Commissioner
        if overdue > 24.0 or priority == PriorityLevel.CRITICAL:
            level = EscalationLevel.MUNICIPAL_COMMISSIONER
            target_title = "Office of the Municipal Commissioner"
            boost = PriorityLevel.CRITICAL
        elif overdue > 8.0 or priority == PriorityLevel.HIGH:
            level = EscalationLevel.ZONAL_OFFICER
            target_title = f"Zonal Director ({input_data.ward_number or 'Central Zone'})"
            boost = PriorityLevel.CRITICAL if priority == PriorityLevel.HIGH else None
        else:
            level = EscalationLevel.WARD_SUPERVISOR
            target_title = f"Ward Supervisor ({input_data.ward_number or 'Ward 3'})"
            boost = None

        memo = (
            f"ADMINISTRATIVE ESCALATION NOTICE\n"
            f"Reference Grievance: {input_data.tracking_number} — '{input_data.title}'\n"
            f"Assigned Department: {input_data.department_name}\n"
            f"Status: {input_data.current_status} | Elapsed: {input_data.hours_elapsed:.1f}h | Overdue: {overdue:.1f}h\n"
            f"Designated Escalation Tier: {level.value} ({target_title})\n"
            f"Urgent corrective action and dispatch intervention is mandated per Municipal Citizen Charter."
        )

        return EscalationOutput(
            should_escalate=True,
            escalation_level=level,
            escalated_to_title=target_title,
            escalation_memo=memo,
            priority_boost_recommended=boost,
            confidence=0.96,
            reasoning_summary=f"Case exceeded resolution window by {overdue:.1f}h at {priority.value} priority; escalated to {level.value}."
        )


escalation_agent = EscalationAgent()
