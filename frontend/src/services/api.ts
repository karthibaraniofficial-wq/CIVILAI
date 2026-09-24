import { 
  Complaint, Department, DepartmentWorkload, AgentRun, 
  ComplaintEvent, Escalation, AuditLog, ComplaintStatus 
} from '../types';

const API_BASE = '/api/v1';

export async function fetchHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch system health');
  return res.json();
}

export async function fetchComplaints(params?: {
  status?: string;
  department_id?: string;
  priority?: string;
  limit?: number;
}): Promise<Complaint[]> {
  const query = new URLSearchParams();
  if (params?.status) query.set('status', params.status);
  if (params?.department_id) query.set('department_id', params.department_id);
  if (params?.priority) query.set('priority', params.priority);
  if (params?.limit) query.set('limit', params.limit.toString());

  const res = await fetch(`${API_BASE}/complaints?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch complaints');
  return res.json();
}

export async function fetchComplaintById(id: string): Promise<Complaint> {
  const res = await fetch(`${API_BASE}/complaints/${id}`);
  if (!res.ok) throw new Error('Failed to fetch complaint details');
  return res.json();
}

export async function trackComplaint(trackingNumber: string): Promise<Complaint> {
  const res = await fetch(`${API_BASE}/complaints/track/${encodeURIComponent(trackingNumber)}`);
  if (!res.ok) throw new Error('Grievance not found');
  return res.json();
}

export async function createComplaint(data: {
  citizen_name: string;
  citizen_contact?: string;
  title: string;
  description: string;
  raw_category?: string;
  location_address: string;
  latitude: number;
  longitude: number;
  landmark?: string;
  ward_number?: string;
  media_urls?: string[];
}): Promise<Complaint> {
  const res = await fetch(`${API_BASE}/complaints`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to submit grievance');
  return res.json();
}

export async function updateComplaintStatus(
  id: string, 
  status: ComplaintStatus, 
  notes?: string
): Promise<Complaint> {
  const res = await fetch(`${API_BASE}/complaints/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status, notes, actor_type: 'OPERATOR' }),
  });
  if (!res.ok) throw new Error('Failed to update status');
  return res.json();
}

export async function fetchComplaintEvents(id: string): Promise<ComplaintEvent[]> {
  const res = await fetch(`${API_BASE}/complaints/${id}/events`);
  if (!res.ok) throw new Error('Failed to fetch timeline');
  return res.json();
}

export async function fetchDepartments(): Promise<Department[]> {
  const res = await fetch(`${API_BASE}/departments`);
  if (!res.ok) throw new Error('Failed to fetch departments');
  return res.json();
}

export async function fetchDepartmentWorkloads(): Promise<DepartmentWorkload[]> {
  const res = await fetch(`${API_BASE}/departments/workload`);
  if (!res.ok) throw new Error('Failed to fetch department workloads');
  return res.json();
}

export async function fetchAgentRuns(complaintId?: string): Promise<AgentRun[]> {
  const url = complaintId 
    ? `${API_BASE}/agents/runs?complaint_id=${complaintId}` 
    : `${API_BASE}/agents/runs`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch agent runs');
  return res.json();
}

export async function triggerAgentTriage(complaintId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/agents/triage/${complaintId}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to trigger agent triage');
  return res.json();
}

export async function fetchEscalations(): Promise<Escalation[]> {
  const res = await fetch(`${API_BASE}/escalations`);
  if (!res.ok) throw new Error('Failed to fetch escalations');
  return res.json();
}

export async function fetchAuditLogs(): Promise<AuditLog[]> {
  const res = await fetch(`${API_BASE}/audit`);
  if (!res.ok) throw new Error('Failed to fetch audit logs');
  return res.json();
}

// Demo Controls
export async function resetDemoState(): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/reset`, { method: 'POST' });
  return res.json();
}

export async function loadDemoScenario(): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/load-scenario`, { method: 'POST' });
  return res.json();
}

export async function accelerateSla(complaintId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/accelerate-sla/${complaintId}`, { method: 'POST' });
  return res.json();
}
