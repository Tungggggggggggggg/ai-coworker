# 🤖 AI Co-Worker Engine (Gucci HR Simulation)

This project simulates a fully functional AI-enabled workplace environment where users can collaborate with AI-driven co-workers (NPCs) that possess unique personas, memories, and business functions. 

Developed as part of the **AI Engineer Intern Assignment** for Edtronaut's Job Simulation Platform.

## 🌟 Key Features
* **Role-Playing AI Agents:** Interact with distinctive AI personas (e.g., Gucci Group CEO, CHRO, Regional Manager) constrained by specific system instructions and business goals.
* **Retrieval-Augmented Generation (RAG):** AI agents retrieve context from vector databases (FAISS) based on external knowledge (e.g., PDF documents like the Gucci Competency Framework) to provide highly accurate, domain-specific responses.
* **Contextual Memory & State Management:** Maintain dialogue history and context across multiple conversational turns using LangGraph state management.
* **Supervisor Orchestration:** A hidden "Director" agent monitors the conversation to ensure the user stays on track with the simulation's learning objectives.
* **Modern Tech Stack:** 
  * **Backend:** Python, FastAPI, LangChain/LangGraph, FAISS, LLM APIs (Gemini/OpenAI).
  * **Frontend:** Next.js (React), Tailwind CSS, Framer Motion.

## 📂 Project Structure

This repository is organized into a mono-repo structure containing both the frontend client and the AI backend services:

```text
ai-coworker/
├── backend/               # Python FastAPI backend & AI Agents logic
│   ├── app/               # FastAPI application, routers, services
│   ├── agents/            # LangGraph agent definitions & prompts
│   ├── rag/               # Retrieval-Augmented Generation (FAISS, Chunking)
│   └── data/              # Source PDFs and Vector DB storage
│
├── frontend/              # Next.js web application
│   ├── src/components/    # React functional components
│   ├── src/app/           # Next.js App Router pages
│   └── package.json       # Frontend dependencies
│
└── README.md              # Project documentation
```

## 🚀 Getting Started

### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv

# Kích hoạt môi trường ảo (Virtual Environment):
# Đối với Windows (Command Prompt / PowerShell):
venv\Scripts\activate
# Đối với macOS / Linux:
source venv/bin/activate

# Cài đặt thư viện:
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload
```

### 2. Frontend Setup (Next.js)
```bash
cd frontend
npm install

# Start the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## ☁️ Deployment Guide (Vercel)

Since the Next.js application is located in the `frontend` subdirectory, please follow these steps when deploying to Vercel:
1. Import the Git repository in Vercel.
2. In the "Configure Project" section, set the **Framework Preset** to `Next.js`.
3. Set the **Root Directory** to `frontend`.
4. Add any necessary Environment Variables (e.g., API keys).
5. Click **Deploy**.