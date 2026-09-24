"""
CIVICFLOW AI — Multi-Agent Pipeline Test Suite (10 Realistic Civic Cases)
Tests independent agent execution and the end-to-end autonomous triage pipeline.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.agents.complaint.agent import complaint_agent
from app.agents.vision.agent import vision_agent
from app.agents.routing.agent import routing_agent
from app.agents.priority.agent import priority_agent
from app.agents.core.orchestrator import orchestrator
from app.agents.core.schemas import (
    ComplaintUnderstandingInput, VisionAnalysisInput,
    DepartmentRoutingInput, PrioritySlaInput
)
from app.db.repository import repo
from app.models.entities import Complaint, ComplaintMedia, ComplaintStatus, PriorityLevel


REALISTIC_COMPLAINTS = [
    {
        "title": "Deep dangerous crater and sinkhole outside St. Mary's School gate",
        "description": "A 1.5m wide and 30cm deep asphalt crater right in front of St. Mary's Primary School. Morning school vans swerving dangerously into oncoming traffic.",
        "category": "pothole",
        "address": "Opposite St. Mary School Main Gate, Ring Road, Ward 3",
        "lat": 28.6145, "lng": 77.2105,
        "media": ["https://images.unsplash.com/photo-1515162816999-a0c47dc192f7"],
        "expected_dept": "Roads & Public Infrastructure",
        "expected_min_severity": 7.0,
    },
    {
        "title": "Overflowing untreated medical and hospital bio-waste on pedestrian pathway",
        "description": "Massive pile of discarded syringes, bloody bandages and biohazard trash dumped beside City Hospital back gate. Stray animals scattering refuse.",
        "category": "garbage",
        "address": "Back lane behind City Civil Hospital, Ward 2",
        "lat": 28.6210, "lng": 77.2180,
        "media": ["https://images.unsplash.com/photo-1605600659873-d808a13e4d2a"],
        "expected_dept": "Sanitation & Solid Waste Management",
        "expected_min_severity": 6.0,
    },
    {
        "title": "Dangling snapped 440V live electrical cable sparking near playground",
        "description": "Overhead distribution cable snapped after windstorm. Live sparking cable hanging 4 feet above children's park entrance. Extreme shock danger.",
        "category": "electricity",
        "address": "Sector 4 Community Children Park, Ward 4",
        "lat": 28.6300, "lng": 77.2250,
        "media": ["https://images.unsplash.com/photo-1544724569-5f546fd6f2b5"],
        "expected_dept": "Electricity & Public Lighting",
        "expected_min_severity": 8.0,
    },
    {
        "title": "Ruptured 600mm potable water distribution main flooding neighborhood",
        "description": "Underground trunk line burst creating a 10-meter geyser. Drinking water flooding entire residential block and causing sub-soil subsidence.",
        "category": "water_supply",
        "address": "Crossroad 7, Anand Vihar Block B, Ward 1",
        "lat": 28.6050, "lng": 77.2010,
        "media": ["https://images.unsplash.com/photo-1541888946425-d0fbb1861564"],
        "expected_dept": "Water Supply & Drainage Board",
        "expected_min_severity": 7.5,
    },
    {
        "title": "Black foul-smelling open sewage drain overflowing into residential colony",
        "description": "Main trunk sewer clogged with plastic debris. Raw black sewage backing up into ground floor houses and contaminating shallow tube-wells.",
        "category": "drainage",
        "address": "Lane 12, Subhash Nagar, Ward 5",
        "lat": 28.6410, "lng": 77.2340,
        "media": ["https://images.unsplash.com/photo-1584467735871-8e85353a8413"],
        "expected_dept": "Water Supply & Drainage Board",
        "expected_min_severity": 7.0,
    },
    {
        "title": "Non-functional streetlights causing dark corridor accidents along ring road",
        "description": "Continuous 800-meter stretch of sodium lights dark for 5 days. Two two-wheeler collisions reported due to lack of visibility.",
        "category": "streetlights",
        "address": "Outer Ring Road flyover descent, Ward 3",
        "lat": 28.6180, "lng": 77.2140,
        "media": ["https://images.unsplash.com/photo-1509114397022-ed747cca3f65"],
        "expected_dept": "Electricity & Public Lighting",
        "expected_min_severity": 6.5,
    },
    {
        "title": "Uprooted storm-damaged eucalyptus tree blocking 2 arterial traffic lanes",
        "description": "Massive 40-foot tree fell across double carriage road during monsoon squall. Complete traffic standstill and damaged municipal fence.",
        "category": "park",
        "address": "Kasturba Gandhi Marg, Sector 2, Ward 2",
        "lat": 28.6120, "lng": 77.2080,
        "media": ["https://images.unsplash.com/photo-1542601906990-b4d3fb778b09"],
        "expected_dept": "Horticulture & Urban Forestry",
        "expected_min_severity": 7.0,
    },
    {
        "title": "Missing cast-iron manhole cover on unlit pedestrian footpath",
        "description": "Open storm drain pit 8 feet deep left completely uncovered without barricade. Pedestrians at grave risk of fatal fall at night.",
        "category": "drainage",
        "address": "Footpath outside Metro Station Gate 4, Ward 4",
        "lat": 28.6250, "lng": 77.2200,
        "media": ["https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b"],
        "expected_dept": "Water Supply & Drainage Board",
        "expected_min_severity": 7.5,
    },
    {
        "title": "Industrial chemical waste barrel dumping near public freshwater pond",
        "description": "Unidentified trucks dumped 6 corroded barrels leaking yellow chemical solvent into wetlands adjacent to public drinking water reservoir.",
        "category": "public_health",
        "address": "Wetlands fringe near Hauz Khas Lake, Ward 5",
        "lat": 28.5520, "lng": 77.1940,
        "media": ["https://images.unsplash.com/photo-1611288870280-4a3962b1660f"],
        "expected_dept": "Public Health & Vector Control",
        "expected_min_severity": 8.0,
    },
    {
        "title": "Concrete spalling and exposed rusted rebar under pedestrian overpass bridge",
        "description": "Large concrete chunk fell onto roadway below from footbridge soffit. Heavily corroded tension bars visible overhead.",
        "category": "public_infrastructure",
        "address": "Footbridge 14, Ring Road crossing, Ward 1",
        "lat": 28.6090, "lng": 77.2050,
        "media": ["https://images.unsplash.com/photo-1541888946425-d0fbb1861564"],
        "expected_dept": "Roads & Public Infrastructure",
        "expected_min_severity": 7.5,
    },
]


@pytest.fixture(autouse=True)
def setup_repo():
    repo.reset_demo()


@pytest.mark.asyncio
async def test_independent_complaint_understanding():
    """Validates ComplaintUnderstandingAgent independently."""
    for item in REALISTIC_COMPLAINTS[:3]:
        inp = ComplaintUnderstandingInput(
            title=item["title"],
            description=item["description"],
            raw_category=item["category"],
            location_address=item["address"],
        )
        out = await complaint_agent.execute(inp)
        assert out.standardized_title is not None
        assert out.detected_category is not None
        assert out.confidence >= 0.70
        assert len(out.reasoning_summary) > 10


@pytest.mark.asyncio
async def test_independent_vision_analysis():
    """Validates VisionAnalysisAgent independently."""
    for item in REALISTIC_COMPLAINTS[:3]:
        inp = VisionAnalysisInput(
            media_urls=item["media"],
            claimed_category=item["category"],
            claimed_description=item["description"],
        )
        out = await vision_agent.execute(inp)
        assert out.is_authentic_civic_damage is True
        assert out.damage_severity_score >= item["expected_min_severity"]
        assert len(out.detected_objects) > 0


@pytest.mark.asyncio
async def test_independent_department_routing():
    """Validates DepartmentRoutingAgent independently."""
    for item in REALISTIC_COMPLAINTS[:3]:
        inp = DepartmentRoutingInput(
            category=item["category"],
            description=item["description"],
            location_address=item["address"],
            latitude=item["lat"],
            longitude=item["lng"],
            hazards=["hazard_test"],
        )
        out = await routing_agent.execute(inp)
        assert out.target_department_id is not None
        assert out.confidence >= 0.80


@pytest.mark.asyncio
async def test_independent_priority_and_sla():
    """Validates PrioritySlaAgent independently."""
    inp = PrioritySlaInput(
        category="electricity",
        damage_severity_score=9.0,
        hazards=["live_wire_sparking"],
        location_address="School Zone",
        is_arterial_or_school_zone=True,
        affected_population_estimate="CRITICAL",
    )
    out = await priority_agent.execute(inp)
    assert out.priority == PriorityLevel.CRITICAL
    assert out.sla_hours <= 6
    assert out.confidence >= 0.85


@pytest.mark.asyncio
async def test_end_to_end_pipeline_on_10_realistic_complaints():
    """
    Executes the full autonomous triage pipeline:
    Complaint -> Understanding -> Vision -> Routing -> Priority -> SLA -> Assignment
    on all 10 realistic civic complaints.
    """
    for idx, item in enumerate(REALISTIC_COMPLAINTS, 1):
        complaint = Complaint(
            tracking_number=f"CF-TEST-{idx:04d}",
            citizen_name=f"Citizen {idx}",
            citizen_contact="+91-90000-00000",
            title=item["title"],
            description=item["description"],
            raw_category=item["category"],
            location_address=item["address"],
            latitude=item["lat"],
            longitude=item["lng"],
            status=ComplaintStatus.SUBMITTED,
            media=[ComplaintMedia(
                complaint_id="",
                media_url=item["media"][0]
            )],
        )
        created = repo.create_complaint(complaint)

        # Run multi-agent orchestrator pipeline
        triaged = await orchestrator.process_new_complaint(created.id)
        assert triaged is not None
        assert triaged.status == ComplaintStatus.ASSIGNED
        assert triaged.department_name == item["expected_dept"]
        assert triaged.sla_target_at is not None
        assert triaged.analysis is not None
        assert triaged.analysis.vision_verified is True
        assert triaged.analysis.visual_severity_score >= item["expected_min_severity"]
        assert triaged.analysis.priority_confidence >= 0.80

        # Assert immutable audit trail and agent run records were created
        runs = repo.get_agent_runs(complaint_id=created.id)
        assert len(runs) >= 4 # Complaint, Vision, Routing, Priority agents
