import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from app.core.config import settings
from app.agents.state import AppState
from app.rag.retriever import query_rag_context

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage, SystemMessage
from app.rag.retriever import query_rag_context, search_gucci_knowledge_base, lookup_employee_kpi

llm_persona = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    temperature=0.7,
    google_api_key=settings.GEMINI_API_KEY
)
tools = [search_gucci_knowledge_base, lookup_employee_kpi]
llm_with_tools = llm_persona.bind_tools(tools)

# Khởi tạo Gemini Web Client (Dành cho Supervisor JSON xuất)
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Đường dẫn folder chứa prompts
PROMPT_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    with open(PROMPT_DIR / filename, "r", encoding="utf-8") as f:
        return f.read()


def estimate_tokens(text: str) -> int:
    # 1 token roughly 4 ký tự (mock metric rất đơn giản, vì SDK chưa hỗ trợ đếm số raw str gọn nhẹ)
    return len(str(text)) // 4


def _invoke_llm_json(prompt: str, user_query: str) -> dict[str, any]:
    """Hàm wrapper cho Supervisor để xuất Intent JSON."""
    start_time = time.time()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"{prompt}\nUser nói: {user_query}",
    )
    latency = (time.time() - start_time) * 1000  # ms

    raw_out = response.text.strip()
    if raw_out.startswith("```json"):
        raw_out = raw_out[7:]
    if raw_out.endswith("```"):
        raw_out = raw_out[:-3]
    try:
        data = json.loads(raw_out.strip())
    except Exception as e:
        print("Json Parse Error:", e)
        data = {
            "next_node": "END",
            "reasoning": "Parse json fail",
            "guardrail_message": "Hệ thống gặp lỗi phân giải Intent.",
        }

    return data, latency, estimate_tokens(prompt + user_query + raw_out)


def _invoke_persona_llm(prompt_template: str, messages_history: list) -> tuple[str, float, int]:
    """Hàm wrapper cho Persona Agents text-generation with Tool Calling."""
    start_time = time.time()
    
    msgs = [SystemMessage(content=prompt_template)] + messages_history
    
    # Lần call đầu tiên
    response = llm_with_tools.invoke(msgs)
    
    # Loop xử lý tools nếu LLM yêu cầu gọi hàm
    while response.tool_calls:
        msgs.append(response)
        for tc in response.tool_calls:
            if tc["name"] == "search_gucci_knowledge_base":
                tool_res = search_gucci_knowledge_base.invoke(tc["args"])
            elif tc["name"] == "lookup_employee_kpi":
                tool_res = lookup_employee_kpi.invoke(tc["args"])
            else:
                tool_res = "Tool không tồn tại"
                
            msgs.append(ToolMessage(content=str(tool_res), tool_call_id=tc["id"], name=tc["name"]))
            
        # Call lại LLM kèm theo kết quả của Tool
        response = llm_with_tools.invoke(msgs)
        
    latency = (time.time() - start_time) * 1000
    tok = estimate_tokens(str(msgs)) + estimate_tokens(response.content)
    
    return response.content, latency, tok


# --- NODES LOGIC ---


def supervisor_node(state: AppState) -> AppState:
    messages = state.get("messages", [])
    if not messages:
        return state

    current_human_msg = messages[-1].content
    
    history_str = "\n".join([f"{'User' if isinstance(m, HumanMessage) else (getattr(m, 'name', 'AI') or 'AI')}: {m.content}" for m in messages[-21:-1]])
    if history_str:
         msg_with_history = f"[LỊCH SỬ HỘI THOẠI GẦN ĐÂY]\n{history_str}\n\n[TIN NHẮN MỚI NHẤT CỦA USER]\n{current_human_msg}"
    else:
         msg_with_history = current_human_msg

    sup_prompt = load_prompt("supervisor.txt")

    data, lat, tok = _invoke_llm_json(sup_prompt, msg_with_history)

    # Track update
    state["latency"] = state.get("latency", 0) + lat
    state["total_tokens"] = state.get("total_tokens", 0) + tok

    if data.get("guardrail_message"):
        error_msg = AIMessage(
            content=f"[SUPERVISOR GUARDRAIL] {data.get('guardrail_message')}",
            name="supervisor",
        )
        state["messages"] = [error_msg]
        state["next_node"] = "END"
        state["intent_reasoning"] = "Guardrail triggered"
        state["safety_flags"] = True
        return state

    state["next_node"] = data.get("next_node", "END").lower()
    state["intent_reasoning"] = data.get("reasoning", "")
    state["intent_hint"] = data.get("hint", "")
    state["safety_flags"] = False
    return state


def ceo_node(state: AppState) -> AppState:
    return _run_persona("ceo", load_prompt("ceo.txt"), state)


def chro_node(state: AppState) -> AppState:
    return _run_persona("chro", load_prompt("chro.txt"), state)


def manager_node(state: AppState) -> AppState:
    return _run_persona("manager", load_prompt("manager.txt"), state)


def _run_persona(name: str, prompt: str, state: AppState) -> AppState:
    messages = state.get("messages", [])
    history_msgs = messages[-21:]  # Trích xuất 20 Human/AIMessage Objects cho Tool Calling
    
    answer_text, lat, tok = _invoke_persona_llm(prompt, history_msgs)

    state["latency"] = state.get("latency", 0) + lat
    state["total_tokens"] = state.get("total_tokens", 0) + tok
    state["safety_flags"] = state.get("safety_flags", False)

    agent_msg = AIMessage(content=answer_text, name=name)
    state["messages"] = [agent_msg]
    state["next_node"] = "END"
    return state
