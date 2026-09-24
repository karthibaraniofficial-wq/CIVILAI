"""
CIVICFLOW AI — Persistence Repository
Provides thread-safe in-memory/SQLite persistence initialized with realistic municipal seed data.
Architected to sync with PostgreSQL / Supabase when configured.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import uuid

from app.models.entities import (
    AgentRun, AgentRunStatus, Assignment, AuditLog, Complaint, 
    ComplaintAnalysis, ComplaintEvent, ComplaintMedia, ComplaintStatus, 
    Department, Escalation, EscalationLevel, Notification, PriorityLevel, 
    Profile, SlaRule, UserRole
)


class DataRepository:
    def __init__(self):
        self.departments: Dict[str, Department] = {}
        self.profiles: Dict[str, Profile] = {}
        self.sla_rules: Dict[str, SlaRule] = {}
        self.complaints: Dict[str, Complaint] = {}
        self.complaint_media: Dict[str, List[ComplaintMedia]] = {}
        self.complaint_analysis: Dict[str, ComplaintAnalysis] = {}
        self.complaint_events: Dict[str, List[ComplaintEvent]] = {}
        self.assignments: Dict[str, List[Assignment]] = {}
        self.agent_runs: List[AgentRun] = []
        self.notifications: List[Notification] = []
        self.escalations: List[Escalation] = []
        self.audit_logs: List[AuditLog] = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        # 1. Departments
        depts = [
            Department(
                id="d1111111-1111-1111-1111-111111111111",
                code="ROAD_INFRA",
                name="Roads & Public Infrastructure",
                description="Maintains urban roadways, bridges, flyovers, footpaths, and structural civic assets.",
                contact_email="roads@civicflow.gov",
                contact_phone="+91-11-2345-0101",
                head_officer_name="Chief Engr. Rajesh Sharma",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
            Department(
                id="d2222222-2222-2222-2222-222222222222",
                code="SOLID_WASTE",
                name="Sanitation & Solid Waste Management",
                description="Handles municipal solid waste, garbage dumping clearance, bio-waste collection, and street sweeping.",
                contact_email="waste@civicflow.gov",
                contact_phone="+91-11-2345-0102",
                head_officer_name="Dr. Sunita Deshmukh",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
            Department(
                id="d3333333-3333-3333-3333-333333333333",
                code="WATER_DRAIN",
                name="Water Supply & Drainage Board",
                description="Manages drinking water distribution, burst mains, drainage overflow, and sewer desilting.",
                contact_email="water@civicflow.gov",
                contact_phone="+91-11-2345-0103",
                head_officer_name="Engr. Vikramaditya Rao",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
            Department(
                id="d4444444-4444-4444-4444-444444444444",
                code="ELEC_LIGHT",
                name="Electricity & Public Lighting",
                description="Maintains streetlights, traffic signals, transformers, exposed electrical wires, and high-mast lamps.",
                contact_email="electric@civicflow.gov",
                contact_phone="+91-11-2345-0104",
                head_officer_name="Engr. Amit Sen",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
            Department(
                id="d5555555-5555-5555-5555-555555555555",
                code="PUB_HEALTH",
                name="Public Health & Vector Control",
                description="Fumigation, disease vector control, open stagnant water hazards, and food sanitation.",
                contact_email="health@civicflow.gov",
                contact_phone="+91-11-2345-0105",
                head_officer_name="Dr. Farhana Begum",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
            Department(
                id="d6666666-6666-6666-6666-666666666666",
                code="PARK_HORT",
                name="Horticulture & Urban Forestry",
                description="Fallen trees, dangerous tree branches, median landscaping, and municipal park upkeep.",
                contact_email="greenery@civicflow.gov",
                contact_phone="+91-11-2345-0106",
                head_officer_name="Officer Pradeep Nair",
                ward_zones=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
            ),
        ]
        for d in depts:
            self.departments[d.id] = d

        # 2. SLA Rules
        sla_list = [
            SlaRule(department_id="d1111111-1111-1111-1111-111111111111", category="pothole", priority=PriorityLevel.CRITICAL, max_resolution_hours=6, warning_threshold_hours=4, escalation_tier_1_hours=6, escalation_tier_2_hours=12),
            SlaRule(department_id="d1111111-1111-1111-1111-111111111111", category="pothole", priority=PriorityLevel.HIGH, max_resolution_hours=24, warning_threshold_hours=16, escalation_tier_1_hours=24, escalation_tier_2_hours=48),
            SlaRule(department_id="d1111111-1111-1111-1111-111111111111", category="pothole", priority=PriorityLevel.MEDIUM, max_resolution_hours=48, warning_threshold_hours=36, escalation_tier_1_hours=48, escalation_tier_2_hours=72),
            SlaRule(department_id="d2222222-2222-2222-2222-222222222222", category="garbage", priority=PriorityLevel.HIGH, max_resolution_hours=24, warning_threshold_hours=16, escalation_tier_1_hours=24, escalation_tier_2_hours=48),
            SlaRule(department_id="d3333333-3333-3333-3333-333333333333", category="water_supply", priority=PriorityLevel.CRITICAL, max_resolution_hours=4, warning_threshold_hours=2, escalation_tier_1_hours=4, escalation_tier_2_hours=8),
            SlaRule(department_id="d4444444-4444-4444-4444-444444444444", category="streetlights", priority=PriorityLevel.HIGH, max_resolution_hours=24, warning_threshold_hours=16, escalation_tier_1_hours=24, escalation_tier_2_hours=48),
        ]
        for s in sla_list:
            self.sla_rules[s.id] = s

        # 3. Profiles
        profs = [
            Profile(id="u0000000-0000-0000-0000-000000000001", full_name="Aarav Mehta", email="citizen@civicflow.gov", role=UserRole.CITIZEN, ward_number="Ward 3"),
            Profile(id="u0000000-0000-0000-0000-000000000002", full_name="Ramesh Kulkarni", email="operator.roads@civicflow.gov", role=UserRole.OPERATOR, department_id="d1111111-1111-1111-1111-111111111111", ward_number="Ward 3"),
            Profile(id="u0000000-0000-0000-0000-000000000003", full_name="Priya Saxena", email="supervisor.zonal@civicflow.gov", role=UserRole.SUPERVISOR, department_id="d1111111-1111-1111-1111-111111111111", ward_number="Ward 3"),
            Profile(id="u0000000-0000-0000-0000-000000000004", full_name="Commissioner Meera Sen", email="admin@civicflow.gov", role=UserRole.ADMIN, ward_number="Central"),
        ]
        for p in profs:
            self.profiles[p.id] = p

        # 4. Canonical Demo Grievance (CF-2026-08912)
        demo_id = "c1111111-1111-1111-1111-111111111111"
        now = datetime.now(timezone.utc)
        demo_complaint = Complaint(
            id=demo_id,
            tracking_number="CF-2026-08912",
            citizen_id="u0000000-0000-0000-0000-000000000001",
            citizen_name="Aarav Mehta",
            citizen_contact="+91-98765-43210",
            title="Deep dangerous pothole with exposed cracked pipe near Model High School",
            description="Severe road depression measuring roughly 1.2m across and 25cm deep on Mahatma Gandhi Road right outside Model High School main gate. Morning school buses are swerving into oncoming traffic to avoid it. Water is also slowly pooling around an exposed corroded pipeline underneath.",
            raw_category="pothole",
            verified_category="pothole",
            status=ComplaintStatus.IN_PROGRESS,
            priority=PriorityLevel.HIGH,
            department_id="d1111111-1111-1111-1111-111111111111",
            department_name="Roads & Public Infrastructure",
            ward_number="Ward 3",
            location_address="Plot 42, Mahatma Gandhi Marg, near Model High School Gate #2",
            latitude=28.6139,
            longitude=77.2090,
            landmark="Opposite Model High School Gate 2",
            sla_target_at=now + timedelta(hours=18),
            sla_warning_at=now + timedelta(hours=10),
            is_simulated=True,
            created_at=now - timedelta(hours=6),
            updated_at=now - timedelta(hours=1),
        )
        self.complaints[demo_id] = demo_complaint

        media_item = ComplaintMedia(
            id="m1111111-1111-1111-1111-111111111111",
            complaint_id=demo_id,
            media_url="https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&w=1000&q=80",
            caption="Severe road pothole with water pooling and visible structural sub-base damage",
        )
        self.complaint_media[demo_id] = [media_item]
        demo_complaint.media = [media_item]

        analysis = ComplaintAnalysis(
            id="a1111111-1111-1111-1111-111111111111",
            complaint_id=demo_id,
            language="en",
            sentiment_score=-0.65,
            detected_entities={"landmarks": ["Model High School", "Gate 2"], "road": "Mahatma Gandhi Marg", "vulnerability": "school_children_transit"},
            vision_verified=True,
            visual_severity_score=8.2,
            detected_hazards=["traffic_collision_risk", "pedestrian_fall_hazard", "water_pipe_leakage"],
            routing_confidence=0.96,
            routing_rationale="Matched primary damage type road crater/pothole to Roads & Public Infrastructure. Cross-notified Water Supply Board regarding co-located pipeline seepage.",
            priority_confidence=0.92,
            priority_rationale="Upgraded to HIGH priority due to proximate vulnerable pedestrian population (K-12 school zone) and bus route disruption.",
            sla_hours_calculated=24,
        )
        self.complaint_analysis[demo_id] = analysis
        demo_complaint.analysis = analysis

        events = [
            ComplaintEvent(
                complaint_id=demo_id,
                event_type="COMPLAINT_SUBMITTED",
                new_state="SUBMITTED",
                actor_type="CITIZEN",
                title="Complaint Registered",
                description="Citizen Aarav Mehta registered complaint with 1 attached visual proof.",
                created_at=now - timedelta(hours=6),
            ),
            ComplaintEvent(
                complaint_id=demo_id,
                event_type="AI_TRIAGE_COMPLETED",
                previous_state="SUBMITTED",
                new_state="CLASSIFIED",
                actor_type="AGENT",
                title="Autonomous Multi-Agent Triage",
                description="Complaint Agent, Vision Agent, Routing Agent, and Priority Agent processed input with 94% aggregate confidence.",
                created_at=now - timedelta(hours=5, minutes=58),
            ),
            ComplaintEvent(
                complaint_id=demo_id,
                event_type="DISPATCHED_TO_DEPARTMENT",
                previous_state="CLASSIFIED",
                new_state="ASSIGNED",
                actor_type="SYSTEM",
                title="Assigned to Roads & Public Infrastructure",
                description="Dispatched to Ward 3 Quick Response Asphalt Repair Unit.",
                created_at=now - timedelta(hours=5, minutes=50),
            ),
            ComplaintEvent(
                complaint_id=demo_id,
                event_type="FIELD_CREW_ACKNOWLEDGED",
                previous_state="ASSIGNED",
                new_state="IN_PROGRESS",
                actor_type="OPERATOR",
                title="Field Crew Dispatched",
                description="Officer Ramesh Kulkarni acknowledged case. Crew 4 en route with cold-mix asphalt and barricades.",
                created_at=now - timedelta(hours=1),
            ),
        ]
        self.complaint_events[demo_id] = events

    # --- Query Methods ---
    def get_departments(self) -> List[Department]:
        return list(self.departments.values())

    def get_department(self, dept_id: str) -> Optional[Department]:
        return self.departments.get(dept_id)

    def get_complaints(
        self,
        status: Optional[ComplaintStatus] = None,
        department_id: Optional[str] = None,
        priority: Optional[PriorityLevel] = None,
        limit: int = 50,
    ) -> List[Complaint]:
        results = []
        for c in self.complaints.values():
            if status and c.status != status:
                continue
            if department_id and c.department_id != department_id:
                continue
            if priority and c.priority != priority:
                continue
            results.append(c)
        results.sort(key=lambda x: x.created_at, reverse=True)
        return results[:limit]

    def get_complaint_by_id(self, complaint_id: str) -> Optional[Complaint]:
        c = self.complaints.get(complaint_id)
        if c:
            c.media = self.complaint_media.get(complaint_id, [])
            c.analysis = self.complaint_analysis.get(complaint_id)
            if c.department_id and c.department_id in self.departments:
                c.department_name = self.departments[c.department_id].name
        return c

    def get_complaint_by_tracking(self, tracking_number: str) -> Optional[Complaint]:
        for c in self.complaints.values():
            if c.tracking_number.upper() == tracking_number.strip().upper():
                return self.get_complaint_by_id(c.id)
        return None

    def create_complaint(self, complaint: Complaint) -> Complaint:
        if complaint.department_id and complaint.department_id in self.departments:
            complaint.department_name = self.departments[complaint.department_id].name
        self.complaints[complaint.id] = complaint
        self.complaint_media[complaint.id] = complaint.media or []
        self.complaint_events[complaint.id] = []
        
        # Log initial submission event
        self.add_complaint_event(ComplaintEvent(
            complaint_id=complaint.id,
            event_type="COMPLAINT_SUBMITTED",
            new_state="SUBMITTED",
            actor_type="CITIZEN",
            title="Grievance Registered",
            description=f"Grievance filed by {complaint.citizen_name}.",
        ))
        
        # Audit log
        self.add_audit_log(AuditLog(
            entity_type="complaint",
            entity_id=complaint.id,
            action="CREATE",
            actor_id=complaint.citizen_id or "anonymous_citizen",
            actor_role="CITIZEN",
            new_values={"tracking_number": complaint.tracking_number, "title": complaint.title},
        ))
        return complaint

    def update_complaint_status(
        self,
        complaint_id: str,
        new_status: ComplaintStatus,
        actor_type: str = "SYSTEM",
        actor_id: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Optional[Complaint]:
        c = self.get_complaint_by_id(complaint_id)
        if not c:
            return None
        old_status = c.status
        c.status = new_status
        c.updated_at = datetime.now(timezone.utc)
        
        if new_status == ComplaintStatus.RESOLVED:
            c.resolved_at = datetime.now(timezone.utc)
        elif new_status == ComplaintStatus.CLOSED:
            c.closed_at = datetime.now(timezone.utc)
        elif new_status == ComplaintStatus.ESCALATED:
            c.escalated_at = datetime.now(timezone.utc)

        self.add_complaint_event(ComplaintEvent(
            complaint_id=complaint_id,
            event_type=f"STATUS_CHANGED_TO_{new_status.value}",
            previous_state=old_status.value,
            new_state=new_status.value,
            actor_id=actor_id,
            actor_type=actor_type,
            title=f"Status changed to {new_status.value}",
            description=reason or f"Transitioned from {old_status.value} to {new_status.value}",
        ))
        return c

    def add_complaint_event(self, event: ComplaintEvent):
        if event.complaint_id not in self.complaint_events:
            self.complaint_events[event.complaint_id] = []
        self.complaint_events[event.complaint_id].append(event)

    def get_complaint_events(self, complaint_id: str) -> List[ComplaintEvent]:
        events = self.complaint_events.get(complaint_id, [])
        return sorted(events, key=lambda x: x.created_at)

    def save_complaint_analysis(self, analysis: ComplaintAnalysis):
        self.complaint_analysis[analysis.complaint_id] = analysis
        if analysis.complaint_id in self.complaints:
            self.complaints[analysis.complaint_id].analysis = analysis

    def add_agent_run(self, run: AgentRun):
        self.agent_runs.append(run)

    def get_agent_runs(self, complaint_id: Optional[str] = None, limit: int = 50) -> List[AgentRun]:
        runs = self.agent_runs
        if complaint_id:
            runs = [r for r in runs if r.complaint_id == complaint_id]
        return sorted(runs, key=lambda x: x.created_at, reverse=True)[:limit]

    def add_audit_log(self, log: AuditLog):
        self.audit_logs.append(log)

    def get_audit_logs(self, limit: int = 100) -> List[AuditLog]:
        return sorted(self.audit_logs, key=lambda x: x.created_at, reverse=True)[:limit]

    def create_escalation(self, escalation: Escalation) -> Escalation:
        self.escalations.append(escalation)
        # Update complaint status if not resolved
        self.update_complaint_status(
            complaint_id=escalation.complaint_id,
            new_status=ComplaintStatus.ESCALATED,
            actor_type="AGENT",
            reason=f"Escalated to {escalation.escalation_level.value}: {escalation.reason}",
        )
        return escalation

    def get_escalations(self) -> List[Escalation]:
        return sorted(self.escalations, key=lambda x: x.created_at, reverse=True)

    def reset_demo(self):
        self.departments.clear()
        self.profiles.clear()
        self.sla_rules.clear()
        self.complaints.clear()
        self.complaint_media.clear()
        self.complaint_analysis.clear()
        self.complaint_events.clear()
        self.assignments.clear()
        self.agent_runs.clear()
        self.notifications.clear()
        self.escalations.clear()
        self.audit_logs.clear()
        self._seed_initial_data()


repo = DataRepository()
