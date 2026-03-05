from fastapi import APIRouter
from app.agents.graph import app_graph

router = APIRouter()


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    config = {"configurable": {"thread_id": session_id}}
    state_snap = app_graph.get_state(config)
    
    if not state_snap or not state_snap.values:
        return {"messages": []}

    state = state_snap.values
    messages = state.get("messages", [])

    # Format messages for frontend
    history = []
    for msg in messages:
        role = "OD Director" if msg.type == "human" else getattr(msg, "name", "AI")
        history.append({"role": role, "content": msg.content})

    return {"messages": history}
