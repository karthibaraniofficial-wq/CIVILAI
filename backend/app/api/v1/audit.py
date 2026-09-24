"""
CIVICFLOW AI — Audit Logs API
"""
from typing import List
from fastapi import APIRouter, Query
from app.db.repository import repo
from app.models.entities import AuditLog

router = APIRouter()


@router.get("", response_model=List[AuditLog])
async def list_audit_logs(limit: int = Query(default=100, le=200)):
    return repo.get_audit_logs(limit=limit)
