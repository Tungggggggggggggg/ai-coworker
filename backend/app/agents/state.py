from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage


class AppState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str  # "ceo", "chro", "manager", "END" hoặc "supervisor"
    rag_context: str  # Dữ liệu tài liệu liên quan từ FAISS
    intent_reasoning: str  # Suy nghĩ của Supervisor tại sao chuyển hướng
    intent_hint: str # Gợi ý của Supervisor khi user hỏi mơ hồ
    latency: float  # API latency tính bằng miliseconds
    total_tokens: int  # Ước tính token sử dụng
    safety_flags: bool  # Cờ an toàn, True nếu có vi phạm
