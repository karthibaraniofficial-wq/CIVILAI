"""
CIVICFLOW AI — Hackathon Presentation & Safe Demo Mode API
Allows judges and presenters to load realistic demo cases, accelerate SLA clocks,
demonstrate multi-agent escalation triggers, and reset demo state safely.
"""
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter
from app.agents.followup_agent import followup_agent
from app.agents.orchestrator import orchestrator
from app.agents.schemas import FollowupInput
from app.core.events import event_bus
from app.db.repository import repo
from app.models.entities import ComplaintStatus, PriorityLevel

router = APIRouter()


@router.post("/reset")
async def reset_demo_state():
    """Resets repository to clean initial seed dataset."""
    repo.reset_demo()
    await event_bus.publish("DEMO_RESET", {"message": "Demo state reset successfully."})
    return {"status": "success", "message": "Demo state successfully reset to seed baseline."}


@router.post("/load-scenario")
async def load_demo_scenario():
    """Ensures canonical scenario CIVIC-DEMO-01 is loaded and ready for walkthrough."""
    demo_case = repo.get_complaint_by_tracking("CF-2026-08912")
    if not demo_case:
        repo.reset_demo()
        demo_case = repo.get_complaint_by_tracking("CF-2026-08912")
        
    await event_bus.publish("DEMO_SCENARIO_LOADED", {
        "tracking_number": demo_case.tracking_number,
        "title": demo_case.title,
    })
    return {
        "status": "success",
        "scenario_code": "CIVIC-DEMO-01",
        "complaint": demo_case,
        "presentation_flow": [
            "1. Citizen submits hazardous grievance with photo outside school",
            "2. Autonomous multi-agent triage: Vision verifies severity (8.2/10), Routing assigns Roads Infra",
            "3. Dynamic SLA calculated (24h) due to vulnerable school transit zone",
            "4. Field crew acknowledged; simulate SLA acceleration to trigger escalation demo",
            "5. Escalation Agent alerts Zonal Officer & Municipal Commissioner"
        ]
    }


@router.post("/accelerate-sla/{complaint_id}")
async def accelerate_sla(complaint_id: str):
    """
    Simulates time acceleration: advances elapsed time so grievance enters SLA breach,
    invokes the Follow-up Agent and triggers Escalation Agent.
    """
    c = repo.get_complaint_by_id(complaint_id)
    if not c:
        return {"error": "Complaint not found"}

    now = datetime.now(timezone.utc)
    # Artificially set target to past to trigger overdue state
    c.sla_target_at = now - timedelta(hours=4)
    c.sla_warning_at = now - timedelta(hours=12)

    # Invoke Follow-up Agent
    follow_input = FollowupInput(
        complaint_id=c.id,
        tracking_number=c.tracking_number,
        status=c.status.value,
        priority=c.priority,
        created_at=c.created_at.isoformat(),
        hours_elapsed=28.0,
    )
    follow_out = await followup_agent.execute(follow_input, complaint_id=c.id)

    # If breached, trigger escalation
    if follow_out.health_status == "BREACHED":
        from app.agents.escalation_agent import escalation_agent
        from app.agents.schemas import EscalationInput
        from app.models.entities import Escalation
        
        esc_input = EscalationInput(
            complaint_id=c.id,
            tracking_number=c.tracking_number,
            title=c.title,
            priority=c.priority,
            department_name=c.department_name or "Roads & Public Infrastructure",
            ward_number=c.ward_number,
            hours_elapsed=28.0,
            hours_overdue=4.0,
            current_status=c.status.value,
        )
        esc_out = await escalation_agent.execute(esc_input, complaint_id=c.id)

        escalation = Escalation(
            complaint_id=c.id,
            escalation_level=esc_out.escalation_level,
            reason="Accelerated Simulated SLA Breach (4.0h overdue)",
            triggered_by="ESCALATION_AGENT",
            previous_priority=c.priority,
            new_priority=esc_out.priority_boost_recommended or c.priority,
            escalated_to_name=esc_out.escalated_to_title,
        )
        repo.create_escalation(escalation)

    await event_bus.publish("SLA_ACCELERATED", {
        "complaint_id": complaint_id,
        "new_status": c.status.value,
        "health": follow_out.health_status,
    })

    return {
        "status": "success",
        "health_status": follow_out.health_status,
        "action_taken": follow_out.recommended_action,
        "complaint": c,
    }
