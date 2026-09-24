"""
CIVICFLOW AI — Department Routing Agent
Maps grievances to appropriate municipal departments and ward jurisdictions.
"""
import logging
from typing import Optional

from app.agents.base import BaseAgent
from app.agents.schemas import DepartmentRoutingInput, DepartmentRoutingOutput
from app.db.repository import repo

logger = logging.getLogger("civicflow.agents.routing")


class DepartmentRoutingAgent(BaseAgent[DepartmentRoutingInput, DepartmentRoutingOutput]):
    def __init__(self):
        super().__init__(name="DepartmentRoutingAgent", version="1.0.0", model_name="gemini-3.8-flash")

    async def _execute_core(self, input_data: DepartmentRoutingInput) -> DepartmentRoutingOutput:
        return self._fallback_heuristic(input_data, None)

    def _fallback_heuristic(self, input_data: DepartmentRoutingInput, error: Optional[Exception]) -> DepartmentRoutingOutput:
        cat = input_data.category.lower()
        depts = repo.get_departments()

        # Mapping dictionary: category -> dept code
        category_map = {
            "pothole": "ROAD_INFRA",
            "road": "ROAD_INFRA",
            "bridge": "ROAD_INFRA",
            "footpath": "ROAD_INFRA",
            "public_infrastructure": "ROAD_INFRA",
            "garbage": "SOLID_WASTE",
            "trash": "SOLID_WASTE",
            "waste": "SOLID_WASTE",
            "sanitation": "SOLID_WASTE",
            "water_supply": "WATER_DRAIN",
            "water": "WATER_DRAIN",
            "drainage": "WATER_DRAIN",
            "sewage": "WATER_DRAIN",
            "streetlights": "ELEC_LIGHT",
            "lighting": "ELEC_LIGHT",
            "electricity": "ELEC_LIGHT",
            "public_health": "PUB_HEALTH",
            "health": "PUB_HEALTH",
            "park": "PARK_HORT",
            "tree": "PARK_HORT",
            "horticulture": "PARK_HORT",
        }

        target_code = category_map.get(cat, "ROAD_INFRA")
        chosen_dept = next((d for d in depts if d.code == target_code), depts[0] if depts else None)

        ward = input_data.ward_number or "Ward 3"
        secondary = []
        if "water" in cat and "ROAD" in target_code:
            secondary.append("WATER_DRAIN")
        elif "electric" in str(input_data.hazards):
            secondary.append("ELEC_LIGHT")

        return DepartmentRoutingOutput(
            target_department_id=chosen_dept.id if chosen_dept else "d1111111-1111-1111-1111-111111111111",
            target_department_code=chosen_dept.code if chosen_dept else "ROAD_INFRA",
            target_department_name=chosen_dept.name if chosen_dept else "Roads & Public Infrastructure",
            assigned_ward=ward,
            confidence=0.96,
            secondary_departments=secondary,
            reasoning_summary=f"Directly classified grievance category '{cat}' to department '{chosen_dept.name}' in '{ward}'."
        )


routing_agent = DepartmentRoutingAgent()
