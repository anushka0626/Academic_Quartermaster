# 🛡️ Academic Quartermaster: Multi-Agent CS Assistant
**APAC GenAI Academy Edition - Cohort 1**

The Academic Quartermaster is a sophisticated **Multi-Agent Cognitive Architecture** designed to solve "Academic Fragmentation." As a CS student, research notes, deadlines, and project tasks are often scattered. This system unifies them using specialized sub-agents.

## 🚀 Live Links
* **Interactive UI:** [Insert Your GitHub Pages Link Here]
* **Agent API (Swagger):** https://academics-quartermaster-552903401245.asia-south1.run.app/docs

## 🧠 The Architecture
The system utilizes a **Coordinator-Specialist** pattern:
1. **The Registrar (Registrar Agent):** Manages time-sensitive data via Google Calendar and Classroom (Zapier MCP).
2. **The Librarian (Librarian Agent):** Manages a persistent SQLite knowledge base for project research like *Veritas Ledger* and *AccessLogix*.
3. **The Secretary (Secretary Agent):** Executes workflow tasks, including creating Notion workspace pages and Google Tasks.

## 🛠️ Tech Stack
* **LLM:** Gemini 3 Flash
* **Framework:** Google Agent Development Kit (ADK)
* **API:** FastAPI & Uvicorn
* **Deployment:** Google Cloud Run (Containerized via Docker)
* **Orchestration:** Model Context Protocol (MCP) via Zapier
* **Database:** SQLite3

## 📦 Project Structure
```text
├── academics_agent/
│   ├── core_agent.py   # Root Agent Logic & Tool definitions
│   ├── database.py     # SQLite Librarian logic
│   └── quartermaster.db
├── main.py             # FastAPI Entry point
├── index.html          # Custom Web UI (GitHub Pages)
├── Procfile            # Cloud Run Deployment instructions
└── requirements.txt    # Dependency Manifest