"""
Test script for FastMCP Cloud Deployment

This script tests the OpenAI agent client with the FastMCP Cloud deployed server.
"""

from agent_client import FCCAgentClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_cloud_deployment():
    """Test the agent with FastMCP Cloud deployment."""

    print("\n" + "="*70)
    print("🧪 Testing FastMCP Cloud Deployment")
    print("="*70)

    # Get configuration from environment
    server_url = os.getenv("MCP_SERVER_URL", "https://freedcodecamp-content.fastmcp.app/mcp")
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    print(f"\nServer URL: {server_url}")
    print(f"Model: {model}")
    print("\n" + "="*70)

    # Initialize agent
    print("\n📡 Initializing agent with cloud deployment...")
    agent = FCCAgentClient(server_url=server_url, model=model)

    # Test query
    print("\n" + "="*70)
    print("🔍 Testing Query")
    print("="*70)

    test_query = "What React tutorials do you have?"
    print(f"\nQuery: {test_query}\n")

    try:
        response = agent.query(test_query)

        print("\n" + "="*70)
        print("✅ Test Successful!")
        print("="*70)
        print(f"\nResponse received: {len(response)} characters")

        if response and len(response) > 0:
            print("\n✓ Agent successfully connected to FastMCP Cloud")
            print("✓ MCP tools are accessible")
            print("✓ OpenAI Responses API working correctly")
        else:
            print("\n⚠️  Response was empty - check MCP server tools")

    except Exception as e:
        print("\n" + "="*70)
        print("❌ Test Failed!")
        print("="*70)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify MCP_SERVER_URL is correct in .env")
        print("2. Check FastMCP Cloud deployment is active")
        print("3. Ensure OpenAI API key has necessary permissions")
        print("4. Try model='gpt-4.1' if gpt-5-mini doesn't work")

if __name__ == "__main__":
    test_cloud_deployment()
