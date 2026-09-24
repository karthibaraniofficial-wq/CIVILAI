"""
CIVICFLOW AI — Health & Diagnostic API
"""
from datetime import datetime, timezone
import time
from fastapi import APIRouter
from app.core.config import settings
from app.db.repository import repo

router = APIRouter()
start_time = time.time()


@router.get("/health", tags=["System"])
async def get_health():
    complaints = repo.get_complaints()
    departments = repo.get_departments()
    
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": int(time.time() - start_time),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "persistence": "SUPABASE" if settings.SUPABASE_URL else "EMBEDDED_LOCAL_PERSISTENCE",
        "ai_engine": "GEMINI_3.8_FLASH" if settings.GEMINI_API_KEY else "HEURISTIC_INTELLIGENCE_ENGINE",
        "stats": {
            "departments_count": len(departments),
            "complaints_count": len(complaints),
            "agent_runs_count": len(repo.agent_runs),
            "audit_logs_count": len(repo.audit_logs),
        },
        "agents": [
            {"name": "ComplaintUnderstandingAgent", "status": "ONLINE", "version": "1.0.0"},
            {"name": "VisionAnalysisAgent", "status": "ONLINE", "version": "1.0.0"},
            {"name": "DepartmentRoutingAgent", "status": "ONLINE", "version": "1.0.0"},
            {"name": "PrioritySlaAgent", "status": "ONLINE", "version": "1.0.0"},
            {"name": "FollowupAgent", "status": "ONLINE", "version": "1.0.0"},
            {"name": "EscalationAgent", "status": "ONLINE", "version": "1.0.0"},
        ]
    }
