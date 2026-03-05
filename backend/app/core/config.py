from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    FAISS_INDEX_PATH: str = "app/rag/vectorstore/index.faiss"
    FAISS_PKL_PATH: str = "app/rag/vectorstore/index.pkl"
    PDF_DATA_PATH: str = (
        "app/rag/data/08. HRM Talent & Leadership Development - Gucci 2.0.pdf"
    )

    class Config:
        env_file = ".env"


settings = Settings()
