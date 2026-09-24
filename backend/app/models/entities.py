"""
CIVICFLOW AI — Domain Entities & Enums
Pydantic v2 domain models corresponding to PostgreSQL / Supabase schema.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


# --- Enums ---
class ComplaintStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    ANALYZING = "ANALYZING"
    CLASSIFIED = "CLASSIFIED"
    ASSIGNED = "ASSIGNED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING = "WAITING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"
    REJECTED = "REJECTED"


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class UserRole(str, Enum):
    CITIZEN = "CITIZEN"
    OPERATOR = "OPERATOR"
    SUPERVISOR = "SUPERVISOR"
    ADMIN = "ADMIN"


class EscalationLevel(str, Enum):
    WARD_SUPERVISOR = "WARD_SUPERVISOR"
    ZONAL_OFFICER = "ZONAL_OFFICER"
    MUNICIPAL_COMMISSIONER = "MUNICIPAL_COMMISSIONER"


class AgentRunStatus(str, Enum):
    SUCCESS = "SUCCESS"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


# --- Core Entities ---
class Department(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    code: str
    name: str
    description: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    head_officer_name: Optional[str] = None
    ward_zones: List[str] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    full_name: str
    email: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CITIZEN
    department_id: Optional[str] = None
    ward_number: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SlaRule(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    department_id: str
    category: str
    priority: PriorityLevel
    max_resolution_hours: int
    warning_threshold_hours: int
    escalation_tier_1_hours: int
    escalation_tier_2_hours: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ComplaintMedia(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: str
    media_url: str
    media_type: str = "image/jpeg"
    caption: Optional[str] = None
    is_resolution_proof: bool = False
    file_size_bytes: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ComplaintAnalysis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: str
    language: str = "en"
    sentiment_score: Optional[float] = None
    detected_entities: Dict[str, Any] = Field(default_factory=dict)
    vision_verified: bool = False
    visual_severity_score: Optional[float] = None
    detected_hazards: List[str] = Field(default_factory=list)
    routing_confidence: Optional[float] = None
    routing_rationale: Optional[str] = None
    priority_confidence: Optional[float] = None
    priority_rationale: Optional[str] = None
    sla_hours_calculated: Optional[int] = None
    full_analysis_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Complaint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tracking_number: str
    citizen_id: Optional[str] = None
    citizen_name: str
    citizen_contact: Optional[str] = None
    title: str
    description: str
    raw_category: Optional[str] = None
    verified_category: Optional[str] = None
    status: ComplaintStatus = ComplaintStatus.SUBMITTED
    priority: PriorityLevel = PriorityLevel.MEDIUM
    department_id: Optional[str] = None
    ward_number: Optional[str] = None
    location_address: str
    latitude: float
    longitude: float
    landmark: Optional[str] = None
    sla_target_at: Optional[datetime] = None
    sla_warning_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    escalated_at: Optional[datetime] = None
    is_simulated: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Populated joins for client convenience
    media: List[ComplaintMedia] = Field(default_factory=list)
    analysis: Optional[ComplaintAnalysis] = None
    department_name: Optional[str] = None


class Assignment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: str
    department_id: str
    assigned_to_user_id: Optional[str] = None
    crew_name: Optional[str] = None
    assignment_notes: Optional[str] = None
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    acknowledged_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "ASSIGNED"


class ComplaintEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: str
    event_type: str
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    actor_id: Optional[str] = None
    actor_type: str = "SYSTEM" # CITIZEN, AGENT, OPERATOR, SYSTEM
    title: str
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AgentRun(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: Optional[str] = None
    agent_name: str
    agent_version: str = "1.0.0"
    model_name: str = "gemini-3.8-flash"
    input_payload: Dict[str, Any] = Field(default_factory=dict)
    output_payload: Dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = None
    duration_ms: int = 0
    status: AgentRunStatus = AgentRunStatus.SUCCESS
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    complaint_id: Optional[str] = None
    notification_type: str
    severity: str = "INFO"
    title: str
    message: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Escalation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    complaint_id: str
    escalation_level: EscalationLevel
    reason: str
    triggered_by: str = "ESCALATION_AGENT"
    previous_priority: Optional[PriorityLevel] = None
    new_priority: Optional[PriorityLevel] = None
    escalated_to_name: Optional[str] = None
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    entity_type: str
    entity_id: str
    action: str
    actor_id: Optional[str] = None
    actor_role: Optional[str] = None
    ip_address: Optional[str] = None
    previous_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    status: str = "SUCCESS"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
