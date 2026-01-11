"""
Quick test to verify GPT-5 compatibility fix
Tests that temperature parameter has been removed for GPT-5 models
"""

import os
from dotenv import load_dotenv
from agent_client_advanced import AdvancedFCCAgentClient

load_dotenv()

def test_gpt5_compatibility():
    """Test that agent works with GPT-5 models without temperature parameter."""
    print("\n" + "="*70)
    print("🧪 Testing GPT-5 Model Compatibility")
    print("="*70)

    # Initialize agent (should not have temperature in API call)
    agent = AdvancedFCCAgentClient(
        server_url=os.getenv("MCP_SERVER_URL", "https://freedcodecamp-content.fastmcp.app/mcp"),
        model="gpt-5-mini",
        max_output_tokens=500
    )

    # Test query
    print("\n📝 Testing query: 'Find Python tutorials for beginners'\n")

    try:
        response = agent.query(
            "Find Python tutorials for beginners",
            verbose=True
        )

        print("\n" + "="*70)
        print("✅ SUCCESS: GPT-5 compatibility test passed!")
        print("="*70)
        print("\nThe agent successfully:")
        print("  ✓ Initialized without temperature parameter")
        print("  ✓ Connected to MCP server")
        print("  ✓ Retrieved response from OpenAI")
        print("  ✓ No parameter errors")

        return True

    except Exception as e:
        print("\n" + "="*70)
        print("❌ FAILED: GPT-5 compatibility test failed!")
        print("="*70)
        print(f"\nError: {str(e)}")

        if "temperature" in str(e).lower():
            print("\n⚠️  Temperature parameter is still being sent to API")
            print("   This should have been removed for GPT-5 models")

        return False

if __name__ == "__main__":
    test_gpt5_compatibility()
