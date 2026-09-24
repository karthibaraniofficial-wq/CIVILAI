"""
CIVICFLOW AI — Follow-up Agent
Periodically monitors SLA progress, evaluates impending breaches, and triggers notifications.
"""
import logging
from typing import Optional

from app.agents.base import BaseAgent
from app.agents.schemas import FollowupInput, FollowupOutput

logger = logging.getLogger("civicflow.agents.followup")


class FollowupAgent(BaseAgent[FollowupInput, FollowupOutput]):
    def __init__(self):
        super().__init__(name="FollowupAgent", version="1.0.0", model_name="gemini-3.8-flash")

    async def _execute_core(self, input_data: FollowupInput) -> FollowupOutput:
        return self._fallback_heuristic(input_data, None)

    def _fallback_heuristic(self, input_data: FollowupInput, error: Optional[Exception]) -> FollowupOutput:
        elapsed = input_data.hours_elapsed

        # Benchmark based on priority
        sla_limit = 24.0
        if input_data.priority.value == "CRITICAL":
            sla_limit = 4.0
        elif input_data.priority.value == "HIGH":
            sla_limit = 24.0
        elif input_data.priority.value == "MEDIUM":
            sla_limit = 48.0
        elif input_data.priority.value == "LOW":
            sla_limit = 96.0

        ratio = elapsed / sla_limit

        if ratio >= 1.0:
            health = "BREACHED"
            action = "TRIGGER_ESCALATION"
            msg = f"SLA breached for grievance {input_data.tracking_number} ({elapsed:.1f}h elapsed > {sla_limit}h SLA). Automated escalation initiated."
        elif ratio >= 0.70:
            health = "AT_RISK"
            action = "SEND_FIELD_REMINDER"
            msg = f"Approaching SLA warning threshold for {input_data.tracking_number} ({elapsed:.1f}h of {sla_limit}h consumed). Expedited dispatch advised."
        else:
            health = "ON_TRACK"
            action = "NO_ACTION"
            msg = f"Grievance {input_data.tracking_number} is progressing within target SLA schedule."

        return FollowupOutput(
            health_status=health,
            recommended_action=action,
            action_message=msg,
            confidence=0.95,
            reasoning_summary=f"SLA consumption ratio calculated at {ratio*100:.1f}%. Recommended action: {action}."
        )


followup_agent = FollowupAgent()
