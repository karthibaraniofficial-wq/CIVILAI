"""
CIVICFLOW AI — Priority and SLA Agent
Calculates multi-factor urgency matrix and determines dynamic SLA deadlines.
"""
import logging
from typing import Optional

from app.agents.base import BaseAgent
from app.agents.schemas import PrioritySlaInput, PrioritySlaOutput
from app.models.entities import PriorityLevel

logger = logging.getLogger("civicflow.agents.priority")


class PrioritySlaAgent(BaseAgent[PrioritySlaInput, PrioritySlaOutput]):
    def __init__(self):
        super().__init__(name="PrioritySlaAgent", version="1.0.0", model_name="gemini-3.8-flash")

    async def _execute_core(self, input_data: PrioritySlaInput) -> PrioritySlaOutput:
        return self._fallback_heuristic(input_data, None)

    def _fallback_heuristic(self, input_data: PrioritySlaInput, error: Optional[Exception]) -> PrioritySlaOutput:
        risk_score = input_data.damage_severity_score
        risk_factors = []

        if input_data.is_arterial_or_school_zone:
            risk_score += 2.0
            risk_factors.append("vulnerable_transit_zone")

        hazard_count = len(input_data.hazards)
        if hazard_count > 0:
            risk_score += min(hazard_count * 1.0, 3.0)
            risk_factors.append(f"{hazard_count}_safety_hazards_flagged")

        if input_data.affected_population_estimate in ["HIGH", "CRITICAL"]:
            risk_score += 1.5
            risk_factors.append("high_population_density")

        # Determine priority tier and SLA hours
        if risk_score >= 10.0:
            priority = PriorityLevel.CRITICAL
            sla_hours = 4
            warning_hours = 2
            esc_hours = 4
        elif risk_score >= 7.5:
            priority = PriorityLevel.HIGH
            sla_hours = 24
            warning_hours = 16
            esc_hours = 24
        elif risk_score >= 4.5:
            priority = PriorityLevel.MEDIUM
            sla_hours = 48
            warning_hours = 32
            esc_hours = 48
        else:
            priority = PriorityLevel.LOW
            sla_hours = 96
            warning_hours = 72
            esc_hours = 96

        return PrioritySlaOutput(
            priority=priority,
            sla_hours=sla_hours,
            warning_threshold_hours=warning_hours,
            escalation_hours=esc_hours,
            risk_factors=risk_factors,
            confidence=0.93,
            reasoning_summary=f"Evaluated combined risk score at {risk_score:.1f}/10. Priority assigned as {priority.value} with {sla_hours}h SLA resolution deadline."
        )


priority_agent = PrioritySlaAgent()
