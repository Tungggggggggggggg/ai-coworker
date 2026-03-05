from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings


def get_faiss_retriever():
    root_dir = Path(__file__).resolve().parent.parent.parent
    vs_dir = root_dir / "app/rag/vectorstore"

    if not vs_dir.exists():
        raise FileNotFoundError(
            f"Chưa build FAISS db. Vui lòng chạy `python -m app.rag.data_pipeline` trước."
        )

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load vector store from local index files
    vectorstore = FAISS.load_local(
        str(vs_dir), embeddings, allow_dangerous_deserialization=True
    )

    # Return a retriever
    # Trả về kết quả search default để framework LLM dựa trên system prompt tự lọc
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})


def query_rag_context(query: str) -> str:
    """Truy vấn Vector DB, nếu list docs trống thì fallback chống Ảo giác."""
    try:
        retriever = get_faiss_retriever()
        docs = retriever.invoke(query)

        if not docs:
            return "Tôi không có thông tin về vấn đề này trong dữ liệu của Gucci."

        context_text = "\n\n".join([doc.page_content for doc in docs])
        return context_text

    except Exception as e:
        print(f"RAG Error: {e}")
        return "Tôi đang gặp khó khăn khi truy cập dữ liệu Gucci. Vui lòng thử lại sau."


from langchain_core.tools import tool

@tool
def search_gucci_knowledge_base(query: str) -> str:
    """Tra cứu cơ sở trí thức (Knowledge base) của tập đoàn Gucci bằng RAG (Vector DB) để lấy thông tin nội bộ cực kỳ quan trọng về chính sách, Competency Framework, v.v. Lưu ý: Luôn dùng tool này nếu người dùng hỏi về kiến thức chuyên môn, định nghĩa của tổ chức."""
    return query_rag_context(query)

@tool
def lookup_employee_kpi(employee_id: str) -> str:
    """Sử dụng khi cần tra cứu điểm số đánh giá KPI cá nhân hoặc bảng điểm năng lực của một nhân sự cụ thể theo mã số nhân viên."""
    fake_db = {
        "NV01": "Nguyễn Văn A - Passion: 4.5/5, Vision: 3.5/5 - Đạt KPI",
        "NV02": "Trần Thị B - Passion: 2.0/5, Vision: 4.0/5 - Trượt KPI",
    }
    eid = employee_id.upper().strip()
    return fake_db.get(eid, f"Không tìm thấy dữ liệu KPI cho nhân sự có mã {employee_id}.")
