"""
CIVICFLOW AI — SLA Monitoring, Escalation Subsystem & Analytics Tests
Tests:
1. Normal workflow: Assigned -> In Progress -> Resolved
2. Escalation workflow: Assigned -> SLA Breached -> Escalation Created -> Authority & Citizen Notified
3. Analytics: Real aggregated database statistics
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta, timezone
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from app.db.repository import repo
from app.models.entities import Complaint, ComplaintStatus, PriorityLevel
from app.services.sla_engine import sla_engine


@pytest.fixture(autouse=True)
def reset_repo():
    repo.reset_demo()


@pytest.mark.asyncio
async def test_normal_resolution_lifecycle():
    """
    Tests: Normal complaint -> assigned -> progressing -> resolved
    """
    now = datetime.now(timezone.utc)
    complaint = Complaint(
        tracking_number="CF-TEST-NORMAL-01",
        citizen_name="Rajiv Sethi",
        citizen_contact="+91-98765-11111",
        title="Routine streetlight bulb replacement",
        description="Single sodium lamp out on internal colony lane 4.",
        raw_category="streetlights",
        verified_category="streetlights",
        location_address="Lane 4, Model Town",
        latitude=28.6190,
        longitude=77.2140,
        status=ComplaintStatus.ASSIGNED,
        priority=PriorityLevel.LOW,
        sla_target_at=now + timedelta(hours=72),
        sla_warning_at=now + timedelta(hours=48),
    )
    repo.create_complaint(complaint)

    # 1. Evaluate: should be ON_TRACK
    eval_res = sla_engine.evaluate_complaint(complaint)
    assert eval_res["status"] == "ON_TRACK"
    assert eval_res["action"] == "NONE"

    # 2. Field Team starts work: transition to IN_PROGRESS
    repo.update_complaint_status(complaint.id, ComplaintStatus.IN_PROGRESS, actor_type="OPERATOR")
    c_updated = repo.get_complaint_by_id(complaint.id)
    assert c_updated.status == ComplaintStatus.IN_PROGRESS

    # 3. Work completed: transition to RESOLVED
    repo.update_complaint_status(complaint.id, ComplaintStatus.RESOLVED, actor_type="OPERATOR")
    c_resolved = repo.get_complaint_by_id(complaint.id)
    assert c_resolved.status == ComplaintStatus.RESOLVED
    assert c_resolved.resolved_at is not None

    # 4. Evaluate: resolved complaint is not evaluated for breach
    eval_after = sla_engine.evaluate_complaint(c_resolved)
    assert eval_after["status"] == "RESOLVED_OR_CLOSED"


@pytest.mark.asyncio
async def test_sla_breach_and_escalation_workflow():
    """
    Tests: Complaint -> assigned -> SLA breached -> escalation -> authority notification -> citizen notification
    """
    now = datetime.now(timezone.utc)
    # Create complaint whose SLA target was 2 hours ago (breached)
    complaint = Complaint(
        tracking_number="CF-TEST-BREACH-01",
        citizen_name="Kavita Krishnan",
        citizen_contact="+91-98765-22222",
        title="High pressure gas line bubbling into puddle",
        description="Hazardous gas odor and bubbling water puddle near public park.",
        raw_category="public_infrastructure",
        verified_category="public_infrastructure",
        location_address="Park Road Junction, Ward 3",
        latitude=28.6180,
        longitude=77.2130,
        status=ComplaintStatus.ASSIGNED,
        priority=PriorityLevel.CRITICAL,
        sla_target_at=now - timedelta(hours=2), # Overdue by 2 hours
        sla_warning_at=now - timedelta(hours=4),
    )
    repo.create_complaint(complaint)

    # Run deterministic SLA engine evaluation
    eval_res = sla_engine.evaluate_complaint(complaint)
    assert eval_res["status"] == "BREACHED"
    assert eval_res["action"] == "ESCALATED"
    assert eval_res["hours_overdue"] >= 2.0

    # Verify escalation entity was created
    escalations = repo.get_escalations()
    assert len(escalations) >= 1
    recent_esc = next((e for e in escalations if e.complaint_id == complaint.id), None)
    assert recent_esc is not None
    assert recent_esc.triggered_by == "SLA_ENGINE"

    # Verify Authority Notification
    auth_notif = next(
        (n for n in repo.notifications if n.complaint_id == complaint.id and n.notification_type == "AUTHORITY_SLA_BREACH"),
        None
    )
    assert auth_notif is not None
    assert "URGENT ESCALATION" in auth_notif.title

    # Verify Citizen Notification
    cit_notif = next(
        (n for n in repo.notifications if n.complaint_id == complaint.id and n.notification_type == "CITIZEN_ESCALATION_UPDATE"),
        None
    )
    assert cit_notif is not None

    # Verify complaint status transitioned to ESCALATED
    c_escalated = repo.get_complaint_by_id(complaint.id)
    assert c_escalated.status == ComplaintStatus.ESCALATED


@pytest.mark.asyncio
async def test_analytics_endpoint():
    """
    Tests: Real analytics aggregation endpoint returns valid metrics
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "total_complaints" in data
        assert "sla_compliance_rate" in data
        assert "department_workload" in data
        assert "category_distribution" in data
        assert len(data["department_workload"]) >= 6
