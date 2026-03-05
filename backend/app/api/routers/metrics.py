from fastapi import APIRouter
from app.api.routers.chat import SESSION_STORE

router = APIRouter()


@router.get("/metrics/{session_id}")
async def get_metrics(session_id: str):
    if session_id not in SESSION_STORE:
        return {"total_latency_ms": 0.0, "total_tokens": 0}

    state = SESSION_STORE[session_id]
    return {
        "total_latency_ms": round(state.get("latency", 0), 2),
        "total_tokens": state.get("total_tokens", 0),
    }
