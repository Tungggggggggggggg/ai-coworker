from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from app.agents.graph import app_graph
from app.agents.state import AppState

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    agent_name: str
    reply: str
    latency_ms: float
    estimated_tokens: int
    is_unsafe: bool


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_msg = request.message

    if not user_msg.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    new_human_msg = HumanMessage(content=user_msg)
    
    # Cấu hình Checkpointer với thread_id dựa trên session_id
    config = {"configurable": {"thread_id": session_id}}
    
    # Lấy state hiện tại (trước khi gọi) để tính toán Diff Latency/Tokens (Per-request Metrics)
    current_state = app_graph.get_state(config).values
    prev_latency = current_state.get("latency", 0.0) if current_state else 0.0
    prev_tokens = current_state.get("total_tokens", 0) if current_state else 0

    try:
        # Run graph (Checkpointer sẽ tự merge history nếu operator.add tồn tại trên list attribute)
        final_state = app_graph.invoke({"messages": [new_human_msg]}, config=config)

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
            agent_source = getattr(ai_response, "name", "System") or "System"

        req_lat = final_state.get("latency", 0.0) - prev_latency
        req_tok = final_state.get("total_tokens", 0) - prev_tokens
        is_unsafe = final_state.get("safety_flags", False)

        return ChatResponse(
            agent_name=agent_source,
            reply=reply_text,
            latency_ms=round(req_lat, 2),
            estimated_tokens=req_tok,
            is_unsafe=is_unsafe
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
