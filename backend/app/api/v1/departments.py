"""
CIVICFLOW AI — Departments API
"""
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from app.db.repository import repo
from app.models.entities import Department

router = APIRouter()


class DepartmentWorkloadResponse(BaseModel):
    department: Department
    active_complaints_count: int
    critical_count: int
    sla_compliance_rate: float


@router.get("", response_model=List[Department])
async def list_departments():
    return repo.get_departments()


@router.get("/workload", response_model=List[DepartmentWorkloadResponse])
async def get_department_workloads():
    depts = repo.get_departments()
    all_complaints = repo.get_complaints()
    result = []

    for d in depts:
        dept_complaints = [c for c in all_complaints if c.department_id == d.id]
        active = [c for c in dept_complaints if c.status.value not in ["RESOLVED", "CLOSED", "REJECTED"]]
        critical = [c for c in active if c.priority.value == "CRITICAL"]
        
        # Calculate simulated SLA compliance rate
        rate = 94.5 if len(dept_complaints) > 0 else 100.0
        
        result.append(DepartmentWorkloadResponse(
            department=d,
            active_complaints_count=len(active),
            critical_count=len(critical),
            sla_compliance_rate=rate,
        ))
    return result
