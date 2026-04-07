# test_mcp.py
import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

load_dotenv()

MCP_URL = "https://mcp.zapier.com/api/v1/connect"  

TOKEN = os.getenv("ZAPIER_MCP_ACCESS_TOKEN")

async def test():
    print(f"Token present: {'✅ YES' if TOKEN else '❌ NO - check .env'}\n")

    transport = StreamableHttpTransport(
        url=MCP_URL,
        headers={"Authorization": f"Bearer {TOKEN}"}
    )

    async with Client(transport) as client:
        # tools = await client.list_tools()
        # print(f"Connected! Found {len(tools)} tools:\n")
        # for tool in tools:
        #     print(f"  🔧 {tool.name}")

        print("🔍 Searching for upcoming events...")
        result = await client.call_tool(
            "google_calendar_find_events", 
            arguments={"instructions": "Find my next meeting for today"}
        )
        print(f"📅 Calendar Result: {result}")

asyncio.run(test())