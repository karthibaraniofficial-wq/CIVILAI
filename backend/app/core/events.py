"""
CIVICFLOW AI — Event Bus & Realtime Broadcasting
Provides pub/sub mechanisms for Server-Sent Events (SSE) and audit records.
"""
import asyncio
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List
import json


class EventBus:
    def __init__(self):
        self._subscribers: List[asyncio.Queue] = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue(maxsize=100)
        async with self._lock:
            self._subscribers.append(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue):
        async with self._lock:
            if queue in self._subscribers:
                self._subscribers.remove(queue)

    async def publish(self, event_type: str, data: Dict[str, Any]):
        payload = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        json_data = json.dumps(payload)
        async with self._lock:
            dead_queues = []
            for queue in self._subscribers:
                try:
                    queue.put_nowait(json_data)
                except asyncio.QueueFull:
                    dead_queues.append(queue)
            for dead in dead_queues:
                self._subscribers.remove(dead)


event_bus = EventBus()
