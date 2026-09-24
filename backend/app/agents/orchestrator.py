"""
CIVICFLOW AI — Multi-Agent Orchestrator Pipeline
Coordinates the autonomous execution sequence:
Complaint Agent -> Vision Agent -> Routing Agent -> Priority & SLA Engine -> Assignment.
"""
from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from app.agents.complaint_agent import complaint_agent
from app.agents.vision_agent import vision_agent
from app.agents.routing_agent import routing_agent
from app.agents.priority_agent import priority_agent
from app.agents.schemas import (
    ComplaintUnderstandingInput, VisionAnalysisInput, 
    DepartmentRoutingInput, PrioritySlaInput
)
from app.core.events import event_bus
from app.db.repository import repo
from app.models.entities import (
    Complaint, ComplaintAnalysis, ComplaintEvent, ComplaintStatus
)

logger = logging.getLogger("civicflow.orchestrator")


class AgentOrchestrator:
    async def process_new_complaint(self, complaint_id: str) -> Optional[Complaint]:
        """
        Executes the end-to-end multi-agent triage pipeline for a newly submitted grievance.
        """
        complaint = repo.get_complaint_by_id(complaint_id)
        if not complaint:
            logger.error(f"Cannot process non-existent complaint {complaint_id}")
            return None

        # Transition status to ANALYZING
        repo.update_complaint_status(
            complaint_id=complaint_id,
            new_status=ComplaintStatus.ANALYZING,
            actor_type="SYSTEM",
            reason="Autonomous multi-agent triage pipeline initiated.",
        )
        await event_bus.publish("COMPLAINT_ANALYZING", {"complaint_id": complaint_id})

        # Step 1: Complaint Understanding Agent
        under_input = ComplaintUnderstandingInput(
            title=complaint.title,
            description=complaint.description,
            raw_category=complaint.raw_category,
            location_address=complaint.location_address,
        )
        under_out = await complaint_agent.execute(under_input, complaint_id=complaint_id)

        # Step 2: Vision Analysis Agent
        media_urls = [m.media_url for m in complaint.media]
        vision_input = VisionAnalysisInput(
            media_urls=media_urls,
            claimed_category=under_out.detected_category,
            claimed_description=complaint.description,
        )
        vision_out = await vision_agent.execute(vision_input, complaint_id=complaint_id)

        # Step 3: Department Routing Agent
        routing_input = DepartmentRoutingInput(
            category=under_out.detected_category,
            description=complaint.description,
            location_address=complaint.location_address,
            ward_number=complaint.ward_number,
            latitude=complaint.latitude,
            longitude=complaint.longitude,
            hazards=vision_out.detected_hazards,
        )
        routing_out = await routing_agent.execute(routing_input, complaint_id=complaint_id)

        # Step 4: Priority & SLA Agent
        is_vulnerable = any("school" in str(v).lower() for v in under_out.extracted_entities.values())
        priority_input = PrioritySlaInput(
            category=under_out.detected_category,
            damage_severity_score=vision_out.damage_severity_score,
            hazards=vision_out.detected_hazards,
            location_address=complaint.location_address,
            is_arterial_or_school_zone=is_vulnerable,
            affected_population_estimate="HIGH" if is_vulnerable else "MEDIUM",
        )
        priority_out = await priority_agent.execute(priority_input, complaint_id=complaint_id)

        # Step 5: Consolidate Analysis & Update Complaint
        now = datetime.now(timezone.utc)
        sla_target = now + timedelta(hours=priority_out.sla_hours)
        sla_warning = now + timedelta(hours=priority_out.warning_threshold_hours)

        analysis = ComplaintAnalysis(
            complaint_id=complaint_id,
            language="en",
            sentiment_score=under_out.sentiment_score,
            detected_entities=under_out.extracted_entities,
            vision_verified=vision_out.is_authentic_civic_damage,
            visual_severity_score=vision_out.damage_severity_score,
            detected_hazards=vision_out.detected_hazards,
            routing_confidence=routing_out.confidence,
            routing_rationale=routing_out.reasoning_summary,
            priority_confidence=priority_out.confidence,
            priority_rationale=priority_out.reasoning_summary,
            sla_hours_calculated=priority_out.sla_hours,
            full_analysis_json={
                "understanding": under_out.model_dump(),
                "vision": vision_out.model_dump(),
                "routing": routing_out.model_dump(),
                "priority_sla": priority_out.model_dump(),
            },
        )
        repo.save_complaint_analysis(analysis)

        # Update core complaint properties
        complaint.verified_category = under_out.detected_category
        complaint.department_id = routing_out.target_department_id
        complaint.department_name = routing_out.target_department_name
        complaint.priority = priority_out.priority
        complaint.sla_target_at = sla_target
        complaint.sla_warning_at = sla_warning
        complaint.status = ComplaintStatus.ASSIGNED

        # Record assignment event
        repo.add_complaint_event(ComplaintEvent(
            complaint_id=complaint_id,
            event_type="AI_TRIAGE_COMPLETED",
            previous_state="ANALYZING",
            new_state="ASSIGNED",
            actor_type="AGENT",
            title="Multi-Agent Triage Complete",
            description=(
                f"Classified as '{under_out.detected_category}'. Routed to {routing_out.target_department_name}. "
                f"Priority set to {priority_out.priority.value} ({priority_out.sla_hours}h SLA)."
            ),
            metadata={"sla_hours": priority_out.sla_hours, "severity": vision_out.damage_severity_score},
        ))

        await event_bus.publish("COMPLAINT_ASSIGNED", {
            "complaint_id": complaint_id,
            "department": routing_out.target_department_name,
            "priority": priority_out.priority.value,
            "sla_hours": priority_out.sla_hours,
        })

        return complaint


orchestrator = AgentOrchestrator()
