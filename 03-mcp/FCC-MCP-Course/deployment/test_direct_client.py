"""
Test script for the Direct MCP Agent Client

This script tests the connection to the MCP server and tool retrieval.
Run this before trying the full agent to ensure everything is working.
"""

import asyncio
from fastmcp import Client
import os
from dotenv import load_dotenv

load_dotenv()

async def test_mcp_connection():
    """Test direct connection to MCP server."""
    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    mcp_endpoint = f"{server_url}/mcp"

    print("="*70)
    print("🧪 Testing MCP Server Connection")
    print("="*70)
    print(f"\nServer URL: {server_url}")
    print(f"MCP Endpoint: {mcp_endpoint}\n")

    try:
        print("🔍 Connecting to MCP server...")
        client = Client(mcp_endpoint)

        async with client:
            print("✓ Connected successfully!\n")

            # List tools
            print("📋 Fetching available tools...")
            tools = await client.list_tools()

            print(f"✓ Found {len(tools)} tools:\n")

            for i, tool in enumerate(tools, 1):
                print(f"{i}. {tool.name}")
                print(f"   Description: {tool.description}")
                print(f"   Input Schema: {tool.inputSchema}")
                print()

            # Test calling a tool
            if tools:
                print("="*70)
                print("🧪 Testing Tool Call: fcc_news_search")
                print("="*70)

                test_tool = "fcc_news_search"
                test_args = {"query": "react", "max_results": 2}

                print(f"\nCalling tool: {test_tool}")
                print(f"Arguments: {test_args}\n")

                result = await client.call_tool(test_tool, test_args)

                print("✓ Tool call successful!")
                print(f"\nResult type: {type(result)}")
                print(f"Result: {result}\n")

                if hasattr(result, 'content'):
                    print(f"Content: {result.content}")

                print("\n" + "="*70)
                print("✅ All tests passed!")
                print("="*70)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"   Type: {type(e).__name__}")

        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
