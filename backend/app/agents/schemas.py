"""
CIVICFLOW AI — Multi-Agent Input/Output Schemas
Strictly typed Pydantic v2 contracts for all 6 specialized agents.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.models.entities import EscalationLevel, PriorityLevel


# ==========================================
# 1. Complaint Understanding Agent Schemas
# ==========================================
class ComplaintUnderstandingInput(BaseModel):
    title: str = Field(description="Raw citizen complaint title")
    description: str = Field(description="Raw citizen complaint description")
    raw_category: Optional[str] = Field(default=None, description="Optional citizen-selected category")
    location_address: str = Field(description="Address or street description provided by citizen")


class ComplaintUnderstandingOutput(BaseModel):
    standardized_title: str = Field(description="Clean, concise operational title")
    refined_summary: str = Field(description="Executive summary of the issue")
    detected_category: str = Field(description="Standardized civic category (e.g. pothole, garbage, drainage, streetlights, electricity)")
    sentiment_score: float = Field(ge=-1.0, le=1.0, description="Citizen sentiment (-1.0 negative to +1.0 positive)")
    urgency_cues: List[str] = Field(default_factory=list, description="Keywords indicating risk or urgency")
    extracted_entities: Dict[str, Any] = Field(default_factory=dict, description="Named landmarks, road names, wards, etc.")
    confidence: float = Field(ge=0.0, le=1.0, description="Agent confidence score")
    reasoning_summary: str = Field(description="Concise rationale for understanding classification")


# ==========================================
# 2. Vision Analysis Agent Schemas
# ==========================================
class VisionAnalysisInput(BaseModel):
    media_urls: List[str] = Field(description="URLs of submitted photos/media")
    claimed_category: str = Field(description="Claimed or detected category")
    claimed_description: str = Field(description="Claimed grievance description")


class VisionAnalysisOutput(BaseModel):
    is_authentic_civic_damage: bool = Field(description="Whether the image represents legitimate civic infrastructure damage")
    damage_severity_score: float = Field(ge=0.0, le=10.0, description="Visual severity from 0 (negligible) to 10 (catastrophic)")
    detected_objects: List[str] = Field(default_factory=list, description="Identified visual elements, e.g. ['asphalt_fissure', 'standing_water']")
    detected_hazards: List[str] = Field(default_factory=list, description="Specific safety hazards visible in photo")
    image_quality: str = Field(default="GOOD", description="Image quality assessment: GOOD, BLURRY, LOW_RES, INCONCLUSIVE")
    confidence: float = Field(ge=0.0, le=1.0, description="Vision agent confidence")
    reasoning_summary: str = Field(description="Concise rationale based on visual evidence")


# ==========================================
# 3. Department Routing Agent Schemas
# ==========================================
class DepartmentRoutingInput(BaseModel):
    category: str
    description: str
    location_address: str
    ward_number: Optional[str] = None
    latitude: float
    longitude: float
    hazards: List[str] = Field(default_factory=list)


class DepartmentRoutingOutput(BaseModel):
    target_department_id: str = Field(description="UUID of chosen department")
    target_department_code: str = Field(description="Code of chosen department (e.g. ROAD_INFRA)")
    target_department_name: str = Field(description="Name of chosen department")
    assigned_ward: str = Field(description="Assigned municipal ward / zone")
    confidence: float = Field(ge=0.0, le=1.0, description="Routing confidence")
    secondary_departments: List[str] = Field(default_factory=list, description="Secondary depts for cross-jurisdiction notice")
    reasoning_summary: str = Field(description="Concise rationale for department assignment")


# ==========================================
# 4. Priority & SLA Agent Schemas
# ==========================================
class PrioritySlaInput(BaseModel):
    category: str
    damage_severity_score: float = Field(ge=0.0, le=10.0)
    hazards: List[str] = Field(default_factory=list)
    location_address: str
    is_arterial_or_school_zone: bool = False
    affected_population_estimate: str = "MEDIUM" # LOW, MEDIUM, HIGH, CRITICAL


class PrioritySlaOutput(BaseModel):
    priority: PriorityLevel = Field(description="Calculated priority tier: LOW, MEDIUM, HIGH, CRITICAL")
    sla_hours: int = Field(ge=1, description="Target resolution hours")
    warning_threshold_hours: int = Field(ge=1, description="Hours before breach to trigger warning")
    escalation_hours: int = Field(ge=1, description="Hours at which first automated escalation triggers")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk multipliers")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in priority assignment")
    reasoning_summary: str = Field(description="Concise rationale for priority and SLA assignment")


# ==========================================
# 5. Follow-up Agent Schemas
# ==========================================
class FollowupInput(BaseModel):
    complaint_id: str
    tracking_number: str
    status: str
    priority: PriorityLevel
    created_at: str
    sla_target_at: Optional[str] = None
    sla_warning_at: Optional[str] = None
    hours_elapsed: float


class FollowupOutput(BaseModel):
    health_status: str = Field(description="ON_TRACK, AT_RISK, BREACHED, PENDING_CLOSURE")
    recommended_action: str = Field(description="NO_ACTION, SEND_FIELD_REMINDER, CITIZEN_PROGRESS_UPDATE, TRIGGER_ESCALATION")
    action_message: str = Field(description="Human-readable notification text generated by agent")
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_summary: str = Field(description="Concise justification for follow-up intervention")


# ==========================================
# 6. Escalation Agent Schemas
# ==========================================
class EscalationInput(BaseModel):
    complaint_id: str
    tracking_number: str
    title: str
    priority: PriorityLevel
    department_name: str
    ward_number: Optional[str] = None
    hours_elapsed: float
    hours_overdue: float
    current_status: str


class EscalationOutput(BaseModel):
    should_escalate: bool
    escalation_level: EscalationLevel = Field(description="WARD_SUPERVISOR, ZONAL_OFFICER, MUNICIPAL_COMMISSIONER")
    escalated_to_title: str = Field(description="Designation of recipient authority")
    escalation_memo: str = Field(description="Official administrative escalation memorandum")
    priority_boost_recommended: Optional[PriorityLevel] = None
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_summary: str = Field(description="Concise justification for administrative escalation")
