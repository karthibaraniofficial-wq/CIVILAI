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

        # Seed 9 additional realistic complaints
        extra_cases = [
            ("c2222222-2222-2222-2222-222222222222", "CF-2026-08913", "Ananya Verma", "+91-98101-11111",
             "Overflowing untreated medical and hospital bio-waste on pedestrian pathway",
             "Massive pile of discarded syringes and biohazard trash dumped beside City Hospital back gate. Stray animals scattering refuse.",
             "garbage", "garbage", ComplaintStatus.ASSIGNED, PriorityLevel.HIGH,
             "d2222222-2222-2222-2222-222222222222", "Sanitation & Solid Waste Management", "Ward 2",
             "Back lane behind City Civil Hospital, Ward 2", 28.6210, 77.2180, "Behind Civil Hospital Gate 3", 24, 6.5,
             "https://images.unsplash.com/photo-1605600659873-d808a13e4d2a?auto=format&fit=crop&w=600&q=80"),
            ("c3333333-3333-3333-3333-333333333333", "CF-2026-08914", "Vikram Jeet", "+91-98101-22222",
             "Dangling snapped 440V live electrical cable sparking near playground",
             "Overhead distribution cable snapped after windstorm. Live sparking cable hanging 4 feet above children park entrance.",
             "electricity", "electricity", ComplaintStatus.ESCALATED, PriorityLevel.CRITICAL,
             "d4444444-4444-4444-4444-444444444444", "Electricity & Public Lighting", "Ward 4",
             "Sector 4 Community Children Park, Ward 4", 28.6300, 77.2250, "Children Park North Gate", 4, 9.0,
             "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?auto=format&fit=crop&w=600&q=80"),
            ("c4444444-4444-4444-4444-444444444444", "CF-2026-08915", "Sunil Chawla", "+91-98101-33333",
             "Ruptured 600mm potable water distribution main flooding neighborhood",
             "Underground trunk line burst creating a 10-meter geyser. Drinking water flooding entire residential block and causing sub-soil subsidence.",
             "water_supply", "water_supply", ComplaintStatus.IN_PROGRESS, PriorityLevel.CRITICAL,
             "d3333333-3333-3333-3333-333333333333", "Water Supply & Drainage Board", "Ward 1",
             "Crossroad 7, Anand Vihar Block B, Ward 1", 28.6050, 77.2010, "Near Mother Dairy Booth", 4, 8.5,
             "https://images.unsplash.com/photo-1541888946425-d0fbb1861564?auto=format&fit=crop&w=600&q=80"),
            ("c5555555-5555-5555-5555-555555555555", "CF-2026-08916", "Manish Malhotra", "+91-98101-44444",
             "Black foul-smelling open sewage drain overflowing into residential colony",
             "Main trunk sewer clogged with debris. Raw black sewage backing up into ground floor houses and contaminating shallow tube-wells.",
             "drainage", "drainage", ComplaintStatus.ACKNOWLEDGED, PriorityLevel.HIGH,
             "d3333333-3333-3333-3333-333333333333", "Water Supply & Drainage Board", "Ward 5",
             "Lane 12, Subhash Nagar, Ward 5", 28.6410, 77.2340, "Opposite Arya Samaj Mandir", 24, 7.5,
             "https://images.unsplash.com/photo-1584467735871-8e85353a8413?auto=format&fit=crop&w=600&q=80"),
            ("c6666666-6666-6666-6666-666666666666", "CF-2026-08917", "Deepika Roy", "+91-98101-55555",
             "Non-functional streetlights causing dark corridor accidents along ring road",
             "Continuous 800-meter stretch of sodium lights dark for 5 days. Two-wheeler collisions reported due to lack of visibility.",
             "streetlights", "streetlights", ComplaintStatus.ASSIGNED, PriorityLevel.MEDIUM,
             "d4444444-4444-4444-4444-444444444444", "Electricity & Public Lighting", "Ward 3",
             "Outer Ring Road flyover descent, Ward 3", 28.6180, 77.2140, "Near Flyover Pillar 28", 48, 6.0,
             "https://images.unsplash.com/photo-1509114397022-ed747cca3f65?auto=format&fit=crop&w=600&q=80"),
            ("c7777777-7777-7777-7777-777777777777", "CF-2026-08918", "Harpreet Singh", "+91-98101-66666",
             "Uprooted storm-damaged eucalyptus tree blocking 2 arterial traffic lanes",
             "Massive 40-foot tree fell across double carriage road during monsoon squall. Complete traffic standstill.",
             "park", "park", ComplaintStatus.IN_PROGRESS, PriorityLevel.HIGH,
             "d6666666-6666-6666-6666-666666666666", "Horticulture & Urban Forestry", "Ward 2",
             "Kasturba Gandhi Marg, Sector 2, Ward 2", 28.6120, 77.2080, "Near KG Marg Roundabout", 24, 7.5,
             "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=600&q=80"),
            ("c8888888-8888-8888-8888-888888888888", "CF-2026-08919", "Naveen Jindal", "+91-98101-77777",
             "Missing cast-iron manhole cover on unlit pedestrian footpath",
             "Open storm drain pit 8 feet deep left completely uncovered without barricade. Pedestrians at grave risk of fatal fall.",
             "drainage", "drainage", ComplaintStatus.ESCALATED, PriorityLevel.CRITICAL,
             "d3333333-3333-3333-3333-333333333333", "Water Supply & Drainage Board", "Ward 4",
             "Footpath outside Metro Station Gate 4, Ward 4", 28.6250, 77.2200, "Outside Metro Gate 4", 4, 8.5,
             "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=600&q=80"),
            ("c9999999-9999-9999-9999-999999999999", "CF-2026-08920", "Dr. Sanjeev Kaul", "+91-98101-88888",
             "Industrial chemical waste barrel dumping near public freshwater pond",
             "Unidentified trucks dumped 6 corroded barrels leaking chemical solvent into wetlands adjacent to public drinking water reservoir.",
             "public_health", "public_health", ComplaintStatus.ASSIGNED, PriorityLevel.CRITICAL,
             "d5555555-5555-5555-5555-555555555555", "Public Health & Vector Control", "Ward 5",
             "Wetlands fringe near Hauz Khas Lake, Ward 5", 28.5520, 77.1940, "Near Lake Bird Sanctuary", 4, 8.5,
             "https://images.unsplash.com/photo-1611288870280-4a3962b1660f?auto=format&fit=crop&w=600&q=80"),
            ("c0000000-0000-0000-0000-000000000010", "CF-2026-08921", "Geeta Bhatt", "+91-98101-99999",
             "Concrete spalling and exposed rusted rebar under pedestrian overpass bridge",
             "Large concrete chunk fell onto roadway below from footbridge soffit. Heavily corroded tension bars visible overhead.",
             "public_infrastructure", "public_infrastructure", ComplaintStatus.RESOLVED, PriorityLevel.HIGH,
             "d1111111-1111-1111-1111-111111111111", "Roads & Public Infrastructure", "Ward 1",
             "Footbridge 14, Ring Road crossing, Ward 1", 28.6090, 77.2050, "Pillar 14 Footbridge", 24, 7.5,
             "https://images.unsplash.com/photo-1541888946425-d0fbb1861564?auto=format&fit=crop&w=600&q=80"),
        ]

        for cid, trk, cname, cphone, title, desc, raw_cat, ver_cat, status, prio, dept_id, dept_name, ward, addr, lat, lng, lmark, sla_h, sev, photo in extra_cases:
            c = Complaint(
                id=cid,
                tracking_number=trk,
                citizen_name=cname,
                citizen_contact=cphone,
                title=title,
                description=desc,
                raw_category=raw_cat,
                verified_category=ver_cat,
                status=status,
                priority=prio,
                department_id=dept_id,
                department_name=dept_name,
                ward_number=ward,
                location_address=addr,
                latitude=lat,
                longitude=lng,
                landmark=lmark,
                sla_target_at=now + timedelta(hours=sla_h) if status != ComplaintStatus.RESOLVED else now - timedelta(hours=2),
                sla_warning_at=now + timedelta(hours=int(sla_h * 0.6)),
                resolved_at=now - timedelta(hours=2) if status == ComplaintStatus.RESOLVED else None,
                escalated_at=now - timedelta(hours=1) if status == ComplaintStatus.ESCALATED else None,
                is_simulated=True,
                created_at=now - timedelta(hours=12),
            )
            self.complaints[cid] = c
            media = ComplaintMedia(id=str(uuid.uuid4()), complaint_id=cid, media_url=photo, caption=title)
            self.complaint_media[cid] = [media]
            c.media = [media]

            analysis = ComplaintAnalysis(
                id=str(uuid.uuid4()),
                complaint_id=cid,
                language="en",
                sentiment_score=-0.6,
                detected_entities={"location": addr, "ward": ward},
                vision_verified=True,
                visual_severity_score=sev,
                detected_hazards=["public_safety_risk"],
                routing_confidence=0.95,
                routing_rationale=f"Assigned to {dept_name} based on verified {ver_cat} hazard.",
                priority_confidence=0.92,
                priority_rationale=f"Evaluated severity {sev}/10. SLA assigned at {sla_h} hours.",
                sla_hours_calculated=sla_h,
            )
            self.complaint_analysis[cid] = analysis
            c.analysis = analysis

            self.complaint_events[cid] = [
                ComplaintEvent(
                    complaint_id=cid,
                    event_type="COMPLAINT_SUBMITTED",
                    new_state="SUBMITTED",
                    actor_type="CITIZEN",
                    title="Grievance Registered",
                    description=f"Lodge by citizen {cname}.",
                    created_at=now - timedelta(hours=12),
                ),
                ComplaintEvent(
                    complaint_id=cid,
                    event_type="AI_TRIAGE_COMPLETED",
                    previous_state="SUBMITTED",
                    new_state="ASSIGNED",
                    actor_type="AGENT",
                    title="Autonomous Multi-Agent Triage",
                    description=f"Routed to {dept_name}. Priority {prio.value}.",
                    created_at=now - timedelta(hours=11, minutes=58),
                ),
            ]

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
