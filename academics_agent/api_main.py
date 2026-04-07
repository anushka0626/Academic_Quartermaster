import asyncio
import uvicorn
import sys
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

current_dir = Path(__file__).parent.resolve()
sys.path.append(str(current_dir))

try:
    from core_agent import root_agent
except ImportError:
    from academics_agent.core_agent import root_agent

app = FastAPI(title="Academic Quartermaster: Multi-Agent System")
session_service = InMemorySessionService()

class UserPrompt(BaseModel):
    prompt: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For the hackathon, this is the easiest way
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask")
async def ask_quartermaster(item: UserPrompt):
    try:
        import uuid
        session_id = str(uuid.uuid4())
        
        await session_service.create_session(
            app_name="academics_agent", 
            user_id="jury_member", 
            session_id=session_id
        )
        runner = Runner(
            agent=root_agent, 
            app_name="academics_agent", 
            session_service=session_service
        )
        
        message = types.Content(
            role="user", 
            parts=[types.Part(text=item.prompt)]
        )
        
        full_response = ""
        tool_calls_log = []

        async for event in runner.run_async(
            user_id="jury_member", 
            session_id=session_id, 
            new_message=message
        ):
            if hasattr(event, 'content') and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        full_response += part.text
                    elif hasattr(part, 'function_call') and part.function_call:
                        tool_calls_log.append(f"[Tool called: {part.function_call.name}]")
        
        if not full_response:
            full_response = "Agent completed tasks. " + " ".join(tool_calls_log)

        return {
            "status": "success", 
            "agent_response": full_response,
            "tools_used": tool_calls_log
        }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "agent_response": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)