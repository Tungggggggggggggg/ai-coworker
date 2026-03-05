from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from app.agents.graph import app_graph
from app.agents.state import AppState

router = APIRouter()

# Tạm sử dụng memory dict lưu session history cho assignment
# Trong production có thể dùng Redis / Postgres Checkpointer
SESSION_STORE: Dict[str, AppState] = {}


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    agent_name: str
    reply: str
    latency_ms: float
    estimated_tokens: int


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_msg = request.message

    if not user_msg.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Tạo hoặc gọi state
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = {
            "messages": [],
            "next_node": "",
            "rag_context": "",
            "intent_reasoning": "",
            "latency": 0.0,
            "total_tokens": 0,
        }

    current_state = SESSION_STORE[session_id]

    # Reset latency per request or keep cumulative? Usually metrics are cumulative for session,
    # but frontend might expect per-request metrics. We'll track cumulative in state,
    # and diff for per-request return.
    prev_latency = current_state.get("latency", 0)
    prev_tokens = current_state.get("total_tokens", 0)

    # Append human message
    new_human_msg = HumanMessage(content=user_msg)
    current_state["messages"] = current_state.get("messages", []) + [new_human_msg]

    try:
        # Run graph
        final_state = app_graph.invoke(current_state)
        # Update store
        SESSION_STORE[session_id] = final_state

        # Determine latest answer
        ai_response = final_state["messages"][-1]
        
        # Guard: Nếu message cuối cùng vẫn là HumanMessage (User)
        # Tức là Supervisor đã route thẳng về END mà không trigger Persona nào.
        if isinstance(ai_response, HumanMessage):
            fallback_text = "Tôi là Supervisor. Câu hỏi của bạn chưa có đủ thông tin để định tuyến tới cá nhân nào. Hãy hỏi cụ thể hơn nhé!"
            if final_state.get("intent_hint"):
                fallback_text += f"\n\n💡 **Gợi ý cho bạn:** {final_state['intent_hint']}"
            elif final_state.get("intent_reasoning"):
                fallback_text += f"\n\n*(Ghi chú: {final_state['intent_reasoning']})*"
                
            reply_text = fallback_text
            agent_source = "Supervisor"
        else:
            reply_text = ai_response.content
            agent_source = ai_response.name if hasattr(ai_response, "name") and ai_response.name else "System"

        req_lat = final_state["latency"] - prev_latency
        req_tok = final_state["total_tokens"] - prev_tokens
        return ChatResponse(
            agent_name=agent_source,
            reply=reply_text,
            latency_ms=round(req_lat, 2),
            estimated_tokens=req_tok,
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
