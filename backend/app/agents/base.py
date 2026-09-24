"""
CIVICFLOW AI — Base Agent Interface
Abstract base class governing all 6 specialized agents.
Enforces typed validation, execution metrics, error recovery, and audit tracking.
"""
from abc import ABC, abstractmethod
import asyncio
from datetime import datetime, timezone
import time
from typing import Generic, Optional, Type, TypeVar
import logging
from pydantic import BaseModel

from app.core.config import settings
from app.db.repository import repo
from app.models.entities import AgentRun, AgentRunStatus, AuditLog

logger = logging.getLogger("civicflow.agents")

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class BaseAgent(ABC, Generic[InputT, OutputT]):
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        model_name: str = "gemini-3.8-flash",
        max_retries: int = 2,
        timeout_seconds: float = 15.0,
    ):
        self.name = name
        self.version = version
        self.model_name = model_name
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds

    @abstractmethod
    async def _execute_core(self, input_data: InputT) -> OutputT:
        """Core AI or heuristic reasoning logic implemented by specialized subclass."""
        pass

    @abstractmethod
    def _fallback_heuristic(self, input_data: InputT, error: Exception) -> OutputT:
        """Deterministic, domain-grounded fallback when external AI is unavailable or fails."""
        pass

    async def execute(self, input_data: InputT, complaint_id: Optional[str] = None) -> OutputT:
        """
        Executes the agent with retry policy, timeout handling, timing metrics, and automatic audit logging.
        """
        start_time = time.perf_counter()
        attempt = 0
        last_exception = None
        status = AgentRunStatus.SUCCESS
        error_msg = None

        while attempt <= self.max_retries:
            attempt += 1
            try:
                # Execute with strict timeout
                output = await asyncio.wait_for(
                    self._execute_core(input_data),
                    timeout=self.timeout_seconds
                )
                break
            except Exception as exc:
                last_exception = exc
                logger.warning(
                    f"Agent {self.name} attempt {attempt} failed: {exc}. Retrying..."
                )
                if attempt <= self.max_retries:
                    await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
        else:
            # All retries exhausted, trigger domain-grounded fallback
            logger.error(
                f"Agent {self.name} exhausted all retries. Triggering domain fallback. Error: {last_exception}"
            )
            status = AgentRunStatus.DEGRADED
            error_msg = str(last_exception)
            output = self._fallback_heuristic(input_data, last_exception)

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        # Extract confidence if present in output
        confidence = getattr(output, "confidence", 0.90)

        # Record AgentRun observability record
        agent_run = AgentRun(
            complaint_id=complaint_id,
            agent_name=self.name,
            agent_version=self.version,
            model_name=self.model_name,
            input_payload=input_data.model_dump(),
            output_payload=output.model_dump(),
            confidence=confidence,
            duration_ms=duration_ms,
            status=status,
            error_message=error_msg,
        )
        repo.add_agent_run(agent_run)

        # Record Audit Log
        if complaint_id:
            repo.add_audit_log(AuditLog(
                entity_type="agent_run",
                entity_id=agent_run.id,
                action="AGENT_EXECUTE",
                actor_id=self.name,
                actor_role="AGENT",
                new_values={
                    "complaint_id": complaint_id,
                    "status": status.value,
                    "confidence": confidence,
                    "duration_ms": duration_ms,
                },
                notes=getattr(output, "reasoning_summary", None),
            ))

        return output
