"""
Simple test for the Direct MCP Agent Client with OpenAI Responses API

This script tests a single query without entering interactive mode.
"""

from agent_client_direct import DirectMCPAgentClient
import os
from dotenv import load_dotenv

load_dotenv()

def test_simple_query():
    """Test a simple query to the agent."""
    SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    print("\n" + "="*70)
    print("🧪 Testing Direct MCP Agent Client")
    print("="*70)
    print(f"\nServer URL: {SERVER_URL}")
    print(f"Model: {MODEL}\n")

    # Initialize the agent client
    print("Initializing agent...")
    agent = DirectMCPAgentClient(server_url=SERVER_URL, model=MODEL)

    # Check if tools were loaded
    if not agent.tools:
        print("\n❌ No tools loaded. Test failed.")
        return

    print(f"\n✓ Agent initialized with {len(agent.tools)} tools")

    # Test a simple query
    print("\n" + "="*70)
    print("Testing query: 'What React tutorials do you have?'")
    print("="*70)

    response = agent.query("What React tutorials do you have?")

    print("\n" + "="*70)
    print("✅ Test completed!")
    print("="*70)

if __name__ == "__main__":
    test_simple_query()
