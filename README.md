# 🛡️ Academic Quartermaster: Multi-Agent CS Assistant
**APAC GenAI Academy Edition - Cohort 1**

Academic Quartermaster is a sophisticated **Multi-Agent Cognitive Architecture** built with the **Google Agent Development Kit (ADK)**. It solves "Academic Fragmentation" by unifying scattered research notes, deadlines, and project tasks into a single, proactive intelligence.

## 🚀 Live Links
* **Interactive Web UI:** [Live on GitHub Pages](https://anushka0626.github.io/Academic_Quartermaster/)
* **Agent API (Swagger):** [Cloud Run Endpoint](https://academics-quartermaster-552903401245.asia-south1.run.app/docs)

---

## 🧠 Core Agent Features

### 📚 The Librarian (Memory & Research)
* **Persistent Knowledge Base:** Uses an optimized SQLite3 backend to archive project-specific research.
* **Contextual Retrieval:** Search through archives for specific project details (e.g., *Veritas Ledger* or *AccessLogix*) using natural language.

### 📅 The Registrar (Schedule & Tasks)
* **Smart Conflict Detection:** Checks Google Calendar for "busy" periods before allowing a task to be scheduled.
* **Task Automation:** Automatically creates action items in Google Tasks once a free slot is confirmed.

### 📝 The Secretary (Workspace Management)
* **Notion Integration:** Generates titled lecture note pages in specified Notion workspaces with one command.
* **Gmail Professional Drafting:** Synthesizes research from your archives into professional email drafts sitting ready in your Gmail "Drafts" folder.

---

## 🛠️ Tech Stack
* **LLM:** Gemini 3 Flash (via Google GenAI SDK)
* **Framework:** Google Agent Development Kit (ADK)
* **Orchestration:** Model Context Protocol (MCP) via Zapier
* **Backend:** FastAPI & Uvicorn (Containerized via Docker)
* **Infrastructure:** Google Cloud Run (Region: `asia-south1`)

---

## ⚙️ Installation & Local Setup

If you wish to run the Academic Quartermaster locally, follow these steps:

### 1. Prerequisites
* Python 3.11+
* A Google Cloud Project with **Vertex AI API** enabled.
* A Zapier account with **MCP** enabled.

### 2. Clone and Install
```bash
git clone [https://github.com/anushka0626/Academic_Quartermaster.git](https://github.com/anushka0626/Academic_Quartermaster.git)
cd Academic_Quartermaster
pip install -r requirements.txt