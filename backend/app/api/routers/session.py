from fastapi import APIRouter
from app.api.routers.chat import SESSION_STORE

router = APIRouter()


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    if session_id not in SESSION_STORE:
        return {"messages": []}

    state = SESSION_STORE[session_id]
    messages = state.get("messages", [])

    # Format messages for frontend
    history = []
    for msg in messages:
        role = "OD Director" if msg.type == "human" else getattr(msg, "name", "AI")
        history.append({"role": role, "content": msg.content})

    return {"messages": history}
