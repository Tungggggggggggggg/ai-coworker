from fastapi import APIRouter
from app.agents.graph import app_graph

router = APIRouter()


@router.get("/metrics/{session_id}")
async def get_metrics(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    state_snap = app_graph.get_state(config)
    
    if not state_snap or not state_snap.values:
        return {"total_latency_ms": 0.0, "total_tokens": 0}

    state = state_snap.values
    return {
        "total_latency_ms": round(state.get("latency", 0), 2),
        "total_tokens": state.get("total_tokens", 0),
    }
