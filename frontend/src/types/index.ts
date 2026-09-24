export type ComplaintStatus =
  | 'SUBMITTED'
  | 'ANALYZING'
  | 'CLASSIFIED'
  | 'ASSIGNED'
  | 'ACKNOWLEDGED'
  | 'IN_PROGRESS'
  | 'WAITING'
  | 'RESOLVED'
  | 'CLOSED'
  | 'ESCALATED'
  | 'REJECTED';

export type PriorityLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type UserRole = 'CITIZEN' | 'OPERATOR' | 'SUPERVISOR' | 'ADMIN';

export type EscalationLevel = 'WARD_SUPERVISOR' | 'ZONAL_OFFICER' | 'MUNICIPAL_COMMISSIONER';

export interface Department {
  id: string;
  code: string;
  name: string;
  description?: string;
  contact_email?: string;
  contact_phone?: string;
  head_officer_name?: string;
  ward_zones: string[];
  is_active: boolean;
  created_at: string;
}

export interface ComplaintMedia {
  id: string;
  complaint_id: string;
  media_url: string;
  media_type: string;
  caption?: string;
  is_resolution_proof?: boolean;
}

export interface ComplaintAnalysis {
  id: string;
  complaint_id: string;
  language: string;
  sentiment_score?: number;
  detected_entities: Record<string, any>;
  vision_verified: boolean;
  visual_severity_score?: number;
  detected_hazards: string[];
  routing_confidence?: number;
  routing_rationale?: string;
  priority_confidence?: number;
  priority_rationale?: string;
  sla_hours_calculated?: number;
  full_analysis_json?: Record<string, any>;
}

export interface Complaint {
  id: string;
  tracking_number: string;
  citizen_id?: string;
  citizen_name: string;
  citizen_contact?: string;
  title: string;
  description: string;
  raw_category?: string;
  verified_category?: string;
  status: ComplaintStatus;
  priority: PriorityLevel;
  department_id?: string;
  department_name?: string;
  ward_number?: string;
  location_address: string;
  latitude: number;
  longitude: number;
  landmark?: string;
  sla_target_at?: string;
  sla_warning_at?: string;
  resolved_at?: string;
  closed_at?: string;
  escalated_at?: string;
  is_simulated: boolean;
  created_at: string;
  updated_at: string;
  media?: ComplaintMedia[];
  analysis?: ComplaintAnalysis;
}

export interface ComplaintEvent {
  id: string;
  complaint_id: string;
  event_type: string;
  previous_state?: string;
  new_state?: string;
  actor_id?: string;
  actor_type: string;
  title: string;
  description?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface AgentRun {
  id: string;
  complaint_id?: string;
  agent_name: string;
  agent_version: string;
  model_name: string;
  input_payload: Record<string, any>;
  output_payload: Record<string, any>;
  confidence?: number;
  duration_ms: number;
  status: 'SUCCESS' | 'DEGRADED' | 'FAILED';
  error_message?: string;
  created_at: string;
}

export interface Escalation {
  id: string;
  complaint_id: string;
  escalation_level: EscalationLevel;
  reason: string;
  triggered_by: string;
  previous_priority?: PriorityLevel;
  new_priority?: PriorityLevel;
  escalated_to_name?: string;
  is_resolved: boolean;
  created_at: string;
}

export interface AuditLog {
  id: string;
  correlation_id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  actor_id?: string;
  actor_role?: string;
  status: string;
  notes?: string;
  created_at: string;
}

export interface DepartmentWorkload {
  department: Department;
  active_complaints_count: number;
  critical_count: number;
  sla_compliance_rate: number;
}
