"""
CIVICFLOW AI — Agents API
Observability, registry inspection, and manual triage trigger.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.agents.orchestrator import orchestrator
from app.db.repository import repo
from app.models.entities import AgentRun

router = APIRouter()


@router.get("/runs", response_model=List[AgentRun])
async def list_agent_runs(
    complaint_id: Optional[str] = Query(default=None),
    limit: int = Query(default=50, le=100)
):
    return repo.get_agent_runs(complaint_id=complaint_id, limit=limit)


@router.post("/triage/{complaint_id}")
async def trigger_triage(complaint_id: str):
    complaint = repo.get_complaint_by_id(complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    processed = await orchestrator.process_new_complaint(complaint_id)
    return {"message": "Autonomous multi-agent triage completed", "complaint": processed}
