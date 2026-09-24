"""
CIVICFLOW AI — Backend Entrypoint
FastAPI application with autonomous multi-agent orchestration,
dual-persistence support, and realtime streaming.
"""
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    agents, audit, complaints, demo, departments, escalations, events, health
)
from app.core.config import settings

# Structured logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("civicflow.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    logger.info("Initializing multi-agent registry and local persistence repository...")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Community Grievance Resolution Orchestrator — Autonomous Multi-Agent AI System",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
api_prefix = settings.API_V1_STR
app.include_router(health.router, prefix=api_prefix)
app.include_router(complaints.router, prefix=f"{api_prefix}/complaints", tags=["Complaints"])
app.include_router(departments.router, prefix=f"{api_prefix}/departments", tags=["Departments"])
app.include_router(agents.router, prefix=f"{api_prefix}/agents", tags=["Multi-Agent System"])
app.include_router(escalations.router, prefix=f"{api_prefix}/escalations", tags=["Escalations"])
app.include_router(audit.router, prefix=f"{api_prefix}/audit", tags=["Audit Trail"])
app.include_router(events.router, prefix=f"{api_prefix}/events", tags=["Realtime Events"])
app.include_router(demo.router, prefix=f"{api_prefix}/demo", tags=["Demo Mode"])


@app.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_v1": api_prefix,
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
