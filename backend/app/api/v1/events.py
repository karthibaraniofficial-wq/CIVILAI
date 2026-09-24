"""
CIVICFLOW AI — Realtime Events Streaming (SSE)
"""
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.core.events import event_bus

router = APIRouter()


@router.get("/stream")
async def event_stream():
    """Server-Sent Events endpoint streaming live platform events to frontend."""
    async def sse_generator():
        queue = await event_bus.subscribe()
        try:
            # Send initial keep-alive
            yield f"event: ping\ndata: {{\"connected\": true}}\n\n"
            while True:
                msg = await queue.get()
                yield f"data: {msg}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            await event_bus.unsubscribe(queue)

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
