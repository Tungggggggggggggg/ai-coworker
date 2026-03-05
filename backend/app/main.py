from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import chat, session, metrics

app = FastAPI(
    title="Gucci AI Co-Worker Engine API",
    description="Multi-agent Orchestrator cho OD Director HR Simulation",
    version="1.0.0",
)

# Cấu hình CORS (Frontend gửi request từ localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên setup domain cụ thể
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route Mounting
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(session.router, prefix="/api", tags=["Session"])
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Gucci AI HR Engine is running"}
