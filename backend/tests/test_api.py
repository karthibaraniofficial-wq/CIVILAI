"""
CIVICFLOW AI — Backend Unit & Integration Tests
"""
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from app.db.repository import repo


@pytest.fixture(autouse=True)
def reset_repo():
    repo.reset_demo()


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert len(data["agents"]) == 6
        assert data["stats"]["departments_count"] == 6


@pytest.mark.asyncio
async def test_list_departments():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/departments")
        assert response.status_code == 200
        departments = response.json()
        assert len(departments) == 6
        dept_codes = [d["code"] for d in departments]
        assert "ROAD_INFRA" in dept_codes
        assert "SOLID_WASTE" in dept_codes
        assert "WATER_DRAIN" in dept_codes


@pytest.mark.asyncio
async def test_canonical_demo_complaint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/complaints/track/CF-2026-08912")
        assert response.status_code == 200
        complaint = response.json()
        assert complaint["tracking_number"] == "CF-2026-08912"
        assert complaint["status"] == "IN_PROGRESS"
        assert complaint["priority"] == "HIGH"
        assert len(complaint["media"]) >= 1
        assert complaint["analysis"] is not None
        assert complaint["analysis"]["vision_verified"] is True


@pytest.mark.asyncio
async def test_create_and_triage_complaint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "citizen_name": "Deepa Sundaram",
            "citizen_contact": "+91-99887-76655",
            "title": "Severe sewage water overflow near primary health clinic",
            "description": "Black foul-smelling sewage overflowing across street outside Ward 3 clinic. Patients slipping in water.",
            "raw_category": "drainage",
            "location_address": "Near Ward 3 Health Center, Station Road",
            "latitude": 28.6219,
            "longitude": 77.2185,
            "landmark": "Near Ward 3 Health Center",
            "ward_number": "Ward 3",
            "media_urls": ["https://images.unsplash.com/photo-1541888946425-d0fbb1861564?w=500"]
        }
        create_resp = await ac.post("/api/v1/complaints", json=payload)
        assert create_resp.status_code == 201
        created = create_resp.json()
        assert "CF-2026-" in created["tracking_number"]

        # Manually trigger triage agent to verify pipeline
        triage_resp = await ac.post(f"/api/v1/agents/triage/{created['id']}")
        assert triage_resp.status_code == 200
        triaged = triage_resp.json()["complaint"]
        assert triaged["status"] == "ASSIGNED"
        assert triaged["department_id"] is not None
        assert triaged["analysis"] is not None
        assert triaged["analysis"]["visual_severity_score"] is not None
