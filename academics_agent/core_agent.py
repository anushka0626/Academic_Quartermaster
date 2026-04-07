import os
from dotenv import load_dotenv          
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from academics_agent.database import save_snippet, search_notes, init_db
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from datetime import datetime
import tenacity 
from anyio import BrokenResourceError

load_dotenv()                           
init_db()


raw_token = os.getenv('ZAPIER_MCP_ACCESS_TOKEN', '')
clean_token = raw_token.strip().replace("\n", "").replace("\r", "")

zapier_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.zapier.com/api/v1/connect",
        headers={
            "Authorization": f"Bearer {clean_token}"
        }
    )
)

async def get_calendar_events(query: str):
    """Searches the user's Google Calendar for events or meetings."""
    TOKEN = clean_token
    MCP_URL = "https://mcp.zapier.com/api/v1/connect"
    
    try:
        transport = StreamableHttpTransport(
            url=MCP_URL,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        async with Client(transport) as client:
            result = await client.call_tool(
                "google_calendar_find_events", 
                arguments={"instructions": query}
            )
            return str(result)
    except Exception as e:
        return f"Calendar tool unavailable: {str(e)}"
    
async def search_academic_archives(query: str):
    words = query.split()
    all_results = []
    
    for word in words:
        if len(word) > 2: # Ignore tiny words like 'is', 'on', 'the'
            all_results.extend(search_notes(word))
    unique_results = list(set(all_results))
    
    if not unique_results:
        return "I checked your archives but couldn't find any notes on that topic."
    
    formatted_results = "\n".join([f"[{r[0]}]: {r[1]}" for r in unique_results])
    return f"Here is what I found in your archives:\n{formatted_results}"

async def create_study_reminder(task_title: str):
    """Creates a new task in Google Tasks to remind the user to study."""
    TOKEN = clean_token
    MCP_URL = "https://mcp.zapier.com/api/v1/connect"
    
    try:
        transport = StreamableHttpTransport(
            url=MCP_URL,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        async with Client(transport,timeout=30) as client:
            result = await client.call_tool(
                "google_tasks_create_task", 
                arguments={
                    "instructions": f"Create a task titled '{task_title}'",
                    "title": task_title
                }
            )
            return f"Task created: {task_title}"
    except Exception as p:
        return f"task creation failed:{str(p)}"

async def create_lecture_notes_page(subject: str):
    context = search_notes(subject)
    summary = "New lecture started."
    if context:
        summary = f"Related Research: {context[0][1]}" 

    TOKEN = clean_token
    PARENT_ID = os.getenv("NOTION_PAGE_ID")
    
    try:
        async with Client(StreamableHttpTransport(url="https://mcp.zapier.com/api/v1/connect", 
                        headers={"Authorization": f"Bearer {TOKEN}"})) as client:
            title = f"{subject} - {datetime.now().strftime('%d %b')}"
            
            result = await client.call_tool(
                "notion_create_page", 
                arguments={
                    "instructions": f"Create a page titled '{title}' in {PARENT_ID}. Add this content: {summary}",
                    "parent_id": PARENT_ID,
                    "title": title
                }
            )
            return f"Notion page created with context: {summary[:50]}..."
    except Exception as c:
        return f"notion page create failed:{str(c)}"

async def check_schedule_and_remind(task_title: str, preferred_time: str):
    TOKEN = clean_token
    
    try:
        async with Client(StreamableHttpTransport(url="https://mcp.zapier.com/api/v1/connect", 
                        headers={"Authorization": f"Bearer {TOKEN}"})) as client:
            
            busy_check = await client.call_tool(
                "google_calendar_find_busy_periods_in_calendar",
                arguments={"instructions": f"Check my schedule for {preferred_time}. Am I busy?"}
            )
            
            # IMPROVED CHECK:
            # Most MCP tools return an empty list or a specific "no conflict" string.
            # Instead of checking for the word 'busy', check if the result contains actual event details.
            response_text = str(busy_check).lower()
            
            # If the response explicitly mentions a specific event or a non-empty list
            if "busy" in response_text and "no busy" not in response_text and "free" not in response_text:
                return f"⚠️ Conflict detected: {busy_check}. Suggesting a different time."
            
            # If it's free, proceed to create the task
            await client.call_tool("google_tasks_create_task", 
                                   arguments={"instructions": task_title, "title": task_title})
            return f"Slot is free! Task '{task_title}' created for {preferred_time}."
        
    except Exception as s:
        return f"schedule check faile:{str(s)}"
    
async def draft_professional_email(recipient: str, subject: str, context: str):
    TOKEN = clean_token
    
    try:
        async with Client(StreamableHttpTransport(url="https://mcp.zapier.com/api/v1/connect", 
                        headers={"Authorization": f"Bearer {TOKEN}"})) as client:
            
            # Simplified arguments to avoid 'invalid_type' errors
            result = await client.call_tool(
                "gmail_create_draft", 
                arguments={
                    "instructions": f"Create a draft to {recipient} with subject '{subject}'. Body: {context}"
                }
            )
            return f"✅ Draft created in your Gmail for {recipient}!"
    except Exception as e:
        return f"❌ Email drafting failed: {str(e)}"

async def save_academic_note(category: str, content: str):
    #from .database import save_snippet
    try:
        save_snippet(category, content)
        return f"Successfully archived in Librarian: [{category}] {content[:30]}..."
    except Exception as e:
        return f"Failed to save note: {e}"


#ROOT AGENT heree
root_agent = Agent(
    model='gemini-1.5-flash', 
    name='academics_agent',
    description='Multi-agent system for academics managing',
    instruction="""You are the Academic Quartermaster, a decisive multi-agent coordinator for a CS student managing two projects: 'Veritas Ledger' (Blockchain/NLP research paper) and 'AccessLogix' (Arduino/RFID lab system).

    CORE RULES - FOLLOW STRICTLY:
    1. NEVER ask for confirmation before taking action. If the user says "yes", "okay", "sure" — just DO IT immediately 
    using the right tool.
    2. NEVER say "Would you like me to...?" — just do it and report back.
    3. If a tool fails, say so briefly and offer ONE alternative. Don't explain the technical error.
    4. Always search archives FIRST before saying notes don't exist.
    5. When user says "yes" or "okay" to your last suggestion, remember what you suggested and execute it.

    TOOLS & WHEN TO USE THEM:
    - search_academic_archives: ANY question about notes, projects, topics
    - save_academic_note: When user shares ANY new info or asks to save something
    - get_calendar_events: When user asks about schedule, deadlines, free time
    - check_schedule_and_remind: When setting a timed reminder — ALWAYS check calendar first
    - create_study_reminder: Fallback if calendar check fails — still create the task
    - create_lecture_notes_page: When starting a lab or lecture session
    - draft_professional_email: Only for email drafting

    RESPONSE STYLE:
    - Be concise. Max 3 sentences unless listing results.
    - Use bullet points for multiple results.
    - Always confirm what action you took, not what you plan to do.
    CRITICAL: You must EXECUTELY call the tool. Do not just describe what you will do""",
    tools=[zapier_tools, get_calendar_events,search_academic_archives, create_study_reminder,create_lecture_notes_page,check_schedule_and_remind,draft_professional_email,save_academic_note]
)