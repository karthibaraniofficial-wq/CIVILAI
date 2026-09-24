"""
CIVICFLOW AI — Escalations API
"""
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.escalation_agent import escalation_agent
from app.agents.schemas import EscalationInput
from app.db.repository import repo
from app.models.entities import Escalation, EscalationLevel

router = APIRouter()


class TriggerEscalationRequest(BaseModel):
    complaint_id: str
    reason: str
    hours_overdue: float = 6.0


@router.get("", response_model=List[Escalation])
async def list_escalations():
    return repo.get_escalations()


@router.post("/trigger", response_model=Escalation)
async def trigger_escalation(req: TriggerEscalationRequest):
    c = repo.get_complaint_by_id(req.complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    esc_input = EscalationInput(
        complaint_id=c.id,
        tracking_number=c.tracking_number,
        title=c.title,
        priority=c.priority,
        department_name=c.department_name or "Municipal Board",
        ward_number=c.ward_number,
        hours_elapsed=30.0,
        hours_overdue=req.hours_overdue,
        current_status=c.status.value,
    )
    esc_out = await escalation_agent.execute(esc_input, complaint_id=c.id)

    escalation = Escalation(
        complaint_id=c.id,
        escalation_level=esc_out.escalation_level,
        reason=req.reason,
        triggered_by="ESCALATION_AGENT",
        previous_priority=c.priority,
        new_priority=esc_out.priority_boost_recommended or c.priority,
        escalated_to_name=esc_out.escalated_to_title,
    )
    return repo.create_escalation(escalation)
