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
