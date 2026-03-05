from typing import Literal
from langgraph.graph import StateGraph, START, END
from app.agents.state import AppState
from app.agents.nodes import supervisor_node, ceo_node, chro_node, manager_node


def supervisor_router(state: AppState) -> Literal["ceo", "chro", "manager", "END"]:
    next_n = state.get("next_node", "END")
    if next_n in ["ceo", "chro", "manager"]:
        return next_n
    return "END"


# 1. Khởi tạo Graph
workflow = StateGraph(AppState)

# 2. Thêm Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("ceo", ceo_node)
workflow.add_node("chro", chro_node)
workflow.add_node("manager", manager_node)

# 3. Định nghĩa Edges & Routing
workflow.add_edge(START, "supervisor")

workflow.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {"ceo": "ceo", "chro": "chro", "manager": "manager", "END": END},
)

# Các agent trả kết quả xong là kết thúc chu trình của lượt chat đó
workflow.add_edge("ceo", END)
workflow.add_edge("chro", END)
workflow.add_edge("manager", END)

from langgraph.checkpoint.memory import MemorySaver

# 4. Biên dịch (Compile) với Checkpointer
memory = MemorySaver()
app_graph = workflow.compile(checkpointer=memory)
