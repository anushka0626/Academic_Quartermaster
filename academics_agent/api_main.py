import asyncio
import uvicorn
import sys
import traceback
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

        # Replace your current event loop with this:
        async for event in runner.run_async(
            user_id="jury_member", 
            session_id=session_id, 
            new_message=message
        ):
            # Safe check: Only try to read text if the event has content and parts
            if event.is_final_response():
                if event.content and event.content.parts and len(event.content.parts) > 0:
                    part = event.content.parts[0]
                    # Only assign if the part actually contains text
                    if hasattr(part, 'text') and part.text:
                        full_response = part.text
            
            # 2. Log tool calls for debugging
            if hasattr(event, 'tool_call') and event.tool_call:
                tool_calls_log.append(f"Calling: {event.tool_call.function_name}")
                
            # 3. Log tool results (this confirms the tool actually finished)
            if hasattr(event, 'tool_result') and event.tool_result:
                tool_calls_log.append(f"Result received from: {event.tool_result.function_name}")
        return {
            "status": "success", 
            "agent_response": full_response if full_response else "No verbal response, but tools may have run.",
            "tools_used": tool_calls_log
        }
    except Exception as e:
        error_str = str(e)
        if "503" in error_str or "UNAVAILABLE" in error_str:
            user_message = "Gemini is under high demand right now. Please retry in 30 seconds."
        else:
            user_message = error_str
        return {
            "status": "error",
            "agent_response": user_message,
            "traceback": traceback.format_exc()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)