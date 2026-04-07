import asyncio
import dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from core_agent import root_agent

dotenv.load_dotenv()

async def main():
    print("🧠 Quartermaster is thinking...\n")
    
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="academics_agent",
        user_id="test_user",
        session_id="test_session"
    )
    
    runner = Runner(
        agent=root_agent,
        app_name="academics_agent",
        session_service=session_service
    )
    
    message = types.Content(
        role="user",
        parts=[types.Part(text="I'm heading into an AccessLogix lab now. Create my Notion notes with my previous RFID pin-out data, then check if I'm free at 9 PM to review them. If I am, set a Task.")]
    )
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=message
    ):
        # Print ALL event types so we can see what's happening
        print(f"📡 Event type: {type(event).__name__}")
        
        # Check for text content in the event
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"🤖 Agent: {part.text}")
                elif hasattr(part, 'function_call') and part.function_call:
                    print(f"🔧 Calling tool: {part.function_call.name}")
                    print(f"   Args: {part.function_call.args}")
                elif hasattr(part, 'function_response') and part.function_response:
                    print(f"✅ Tool result: {str(part.function_response.response)[:200]}")

if __name__ == "__main__":
    asyncio.run(main())