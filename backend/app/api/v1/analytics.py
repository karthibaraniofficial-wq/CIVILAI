"""
CIVICFLOW AI — Analytics API
Exposes aggregated civic performance metrics with date and department filtering.
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query
from app.services.analytics_service import analytics_service, AnalyticsSummary

router = APIRouter()


@router.get("", response_model=AnalyticsSummary)
async def get_analytics(
    start_date: Optional[str] = Query(default=None, description="ISO format start date"),
    end_date: Optional[str] = Query(default=None, description="ISO format end date"),
    department_id: Optional[str] = Query(default=None),
):
    start_dt = datetime.fromisoformat(start_date) if start_date else None
    end_dt = datetime.fromisoformat(end_date) if end_date else None
    return analytics_service.get_analytics(start_date=start_dt, end_date=end_dt, department_id=department_id)
