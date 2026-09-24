"""
CIVICFLOW AI — Complaints API
Handles citizen submission, listing, filtering, tracking, and operational status transitions.
"""
import asyncio
from datetime import datetime, timezone
import random
from typing import List, Optional
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel, Field

from app.agents.orchestrator import orchestrator
from app.db.repository import repo
from app.models.entities import (
    Complaint, ComplaintEvent, ComplaintMedia, ComplaintStatus, PriorityLevel
)

router = APIRouter()


class ComplaintCreateRequest(BaseModel):
    citizen_name: str = Field(min_length=2, max_length=150)
    citizen_contact: Optional[str] = Field(default=None)
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(min_length=10)
    raw_category: Optional[str] = Field(default="pothole")
    location_address: str = Field(min_length=3)
    latitude: float
    longitude: float
    landmark: Optional[str] = None
    ward_number: Optional[str] = "Ward 3"
    media_urls: List[str] = Field(default_factory=list)


class StatusUpdateRequest(BaseModel):
    status: ComplaintStatus
    actor_id: Optional[str] = None
    actor_type: str = "OPERATOR"
    notes: Optional[str] = None


@router.get("", response_model=List[Complaint])
async def list_complaints(
    status: Optional[ComplaintStatus] = Query(default=None),
    department_id: Optional[str] = Query(default=None),
    priority: Optional[PriorityLevel] = Query(default=None),
    limit: int = Query(default=50, le=100),
):
    return repo.get_complaints(status=status, department_id=department_id, priority=priority, limit=limit)


@router.post("", response_model=Complaint, status_code=201)
async def create_complaint(
    req: ComplaintCreateRequest,
    background_tasks: BackgroundTasks
):
    # Generate unique civic tracking number: e.g. CF-2026-XXXXX
    tracking_num = f"CF-2026-{random.randint(10000, 99999)}"
    complaint_id = str(uuid4())

    media_items = [
        ComplaintMedia(
            complaint_id=complaint_id,
            media_url=url,
            media_type="image/jpeg",
        ) for url in req.media_urls
    ]

    complaint = Complaint(
        id=complaint_id,
        tracking_number=tracking_num,
        citizen_name=req.citizen_name,
        citizen_contact=req.citizen_contact,
        title=req.title,
        description=req.description,
        raw_category=req.raw_category,
        location_address=req.location_address,
        latitude=req.latitude,
        longitude=req.longitude,
        landmark=req.landmark,
        ward_number=req.ward_number,
        status=ComplaintStatus.SUBMITTED,
        media=media_items,
    )

    created = repo.create_complaint(complaint)

    # Trigger autonomous multi-agent pipeline in background
    background_tasks.add_task(orchestrator.process_new_complaint, created.id)

    return created


@router.get("/{complaint_id}", response_model=Complaint)
async def get_complaint(complaint_id: str):
    c = repo.get_complaint_by_id(complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return c


@router.get("/track/{tracking_number}", response_model=Complaint)
async def track_complaint(tracking_number: str):
    c = repo.get_complaint_by_tracking(tracking_number)
    if not c:
        raise HTTPException(status_code=404, detail=f"No grievance found with tracking number '{tracking_number}'")
    return c


@router.get("/{complaint_id}/events", response_model=List[ComplaintEvent])
async def get_complaint_timeline(complaint_id: str):
    c = repo.get_complaint_by_id(complaint_id)
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return repo.get_complaint_events(complaint_id)


@router.patch("/{complaint_id}/status", response_model=Complaint)
async def update_status(complaint_id: str, req: StatusUpdateRequest):
    updated = repo.update_complaint_status(
        complaint_id=complaint_id,
        new_status=req.status,
        actor_type=req.actor_type,
        actor_id=req.actor_id,
        reason=req.notes,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated
