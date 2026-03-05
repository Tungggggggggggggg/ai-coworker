import os
import json
from pathlib import Path
from PyPDF2 import PdfReader
from google import genai
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings
from app.core.logger import get_logger
from dotenv import load_dotenv

load_dotenv()

logger = get_logger("rag.data_pipeline")

# Initialize Gemini Client for Semantic Chunking
client = genai.Client(api_key=settings.GEMINI_API_KEY)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

PROMPT_EXTRACT_METADATA = """Bạn là một chuyên gia HR cấp cao của Gucci. 
Người dùng sẽ đưa cho bạn văn bản trích xuất từ tài liệu cấu trúc tổ chức "Gucci 2.0 HRM". 
Nhiệm vụ của bạn là đọc kỹ đoạn văn bản dưới đây và trích xuất TOÀN BỘ thông tin quan trọng. 
Mỗi một ý chính độc lập (Semantic Chunk), hãy phân rã nó ra thành một Document object kèm Metadata.

Yêu cầu định dạng đầu ra BẮT BUỘC LÀ JSON ARRAY có cấu trúc như sau:
[
  {{
    "page_content": "Văn bản chi tiết thể hiện một ý chính, kỹ năng, luật lệ hay quyền tự trị của thương hiệu",
    "metadata": {{
      "sector": "Tên khối (nếu có, ví dụ: Retail, Corporate, Supply Chain, None)",
      "function": "Chức năng/Phòng ban (nếu có, ví dụ: HR, Finance, Store Management, None)",
      "role_level": "Cấp bậc (nếu có, ví dụ: Director, Manager, Staff, None)",
      "primary_skills": "Kỹ năng 1, Kỹ năng 2"
    }}
  }}
]

Chỉ xuất raw JSON array, KHÔNG BAO GỒM markdown format (như ```json) hay bất kỳ văn bản giải thích nào khác.
Nếu trong đoạn văn bản có nhiều loại thông tin, bạn hãy chia thành nhiều object trong mảng.

Văn bản cần xử lý:
---
{text}
---"""


def extract_text_from_pdf(pdf_path: str) -> list[str]:
    """Đọc file PDF, trả về danh sách text theo từng trang."""
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return pages


def generate_chunks_with_gemini(text: str) -> list[dict]:
    """Gửi text qua Gemini để tạo Semantic Chunks và gắn Metadata JSON."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=PROMPT_EXTRACT_METADATA.format(text=text),
        )
        # Clean response if it contains markdown JSON block
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        chunks = json.loads(clean_text)
        return chunks
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return []


def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    pdf_path = root_dir / settings.PDF_DATA_PATH

    if not pdf_path.exists():
        logger.error(f"Không tìm thấy file PDF tại: {pdf_path}")
        return

    logger.info("Bước 1: Giải nén Text từ PDF...")
    pages = extract_text_from_pdf(str(pdf_path))
    logger.info(f"-> Đã đọc {len(pages)} trang.")

    logger.info("Bước 2: Giao tiếp Gemini để Semantic Chunking...")
    all_chunks = []
    for i, page_text in enumerate(pages):
        logger.info(f"  - Xử lý trang {i+1}...")
        chunks = generate_chunks_with_gemini(page_text)
        all_chunks.extend(chunks)

    logger.info(f"-> Trích xuất thành công {len(all_chunks)} semantic chunks.")

    logger.info("Bước 3: Tạo LangChain Documents & Nhúng bằng Embedding Models...")
    documents = []
    for chunk in all_chunks:
        # FAISS metadata values must be str, int, float or bool
        meta = chunk.get("metadata", {})
        if isinstance(meta.get("primary_skills"), list):
            meta["primary_skills"] = ", ".join(meta["primary_skills"])

        doc = Document(page_content=chunk.get("page_content", ""), metadata=meta)
        documents.append(doc)

    logger.info("Bước 4: Khởi tạo FAISS VectorStore...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    vs_dir = root_dir / "app/rag/vectorstore"
    os.makedirs(vs_dir, exist_ok=True)

    logger.info("Bước 5: Lưu index.faiss cục bộ...")
    vectorstore.save_local(str(vs_dir))
    logger.info(f"-> Hoàn tất lưu FAISS VectorStore tại: {vs_dir}")


if __name__ == "__main__":
    main()
