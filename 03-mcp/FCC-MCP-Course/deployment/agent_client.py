"""
OpenAI Agent Client for FreeCodeCamp MCP Server

This client demonstrates how to consume an MCP server deployed with HTTP transport
using OpenAI's Responses API with MCP integration.

The agent can query development topics and get responses from FreeCodeCamp's
news and YouTube content.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FCCAgentClient:
    """
    Agent client that consumes the FreeCodeCamp MCP server using OpenAI's API.

    The MCP server provides tools for searching:
    - FreeCodeCamp news articles
    - FreeCodeCamp YouTube videos
    - Getting inspirational messages
    """

    def __init__(self, server_url: str = "https://freedcodecamp-content.fastmcp.app/mcp", model: str = "gpt-5-mini"):
        """
        Initialize the agent client.

        Args:
            server_url (str): URL where the MCP server is running
                            Default: FastMCP Cloud deployment
                            For local: "http://localhost:8000/mcp"
            model (str): OpenAI model to use. Must support MCP tools.
                        Recommended: gpt-5-mini (default), gpt-4.1, gpt-4.5, or gpt-5
                        Note: gpt-4o/gpt-4o-mini may not support MCP type tools
        """
        self.server_url = server_url
        self.model = model
        self.client = OpenAI()

        # Warn if using incompatible model
        compatible_models = ["gpt-4.1", "gpt-4.5", "gpt-5", "gpt-5-mini"]
        if not any(m in model for m in compatible_models):
            print(f"⚠️  Warning: Model '{model}' may not support MCP tools.")
            print(f"   Recommended models: {', '.join(compatible_models)}")
            print(f"   If you encounter errors, try: model='gpt-5-mini' or 'gpt-4.1'")

        # Configure MCP tool for OpenAI Responses API
        # Using FastMCP Cloud deployment (publicly accessible)
        self.mcp_tool = {
            "type": "mcp",
            "server_label": "freedcodecamp-content",
            "server_url": server_url,
            "require_approval": "never",
        }

        print(f"✓ Agent initialized with MCP server at {server_url}")
        print(f"✓ Using OpenAI model: {model}")

    def query(self, user_query: str, instructions: str = None) -> str:
        """
        Query the agent with a development topic question.

        The agent will use the MCP server's tools to search FreeCodeCamp content
        and provide relevant responses.

        Args:
            user_query (str): The user's question about a development topic
            instructions (str, optional): Additional instructions for the agent

        Returns:
            str: The agent's response
        """
        # Default instructions if none provided
        if instructions is None:
            instructions = """
            You are a helpful programming and development assistant with access to
            FreeCodeCamp's educational content. When users ask about development topics,
            use the available tools to search for relevant articles and videos from
            FreeCodeCamp's news feed and YouTube channel.

            Always:
            1. Search for relevant content using the provided tools
            2. Summarize the findings
            3. Include direct links to the resources
            4. Be encouraging and supportive

            If no relevant content is found, acknowledge this and provide general guidance.
            """

        print(f"\n{'='*60}")
        print(f"🔍 Query: {user_query}")
        print(f"{'='*60}\n")

        try:
            # Call OpenAI with MCP integration
            response = self.client.responses.create(
                model=self.model,
                instructions=instructions,
                tools=[self.mcp_tool],
                input=user_query,
            )

            # Extract and display the response
            output = response.output_text

            print(f"🤖 Agent Response:\n")
            print(output)
            print(f"\n{'='*60}\n")

            return output

        except Exception as e:
            error_msg = f"Error querying agent: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def interactive_mode(self):
        """
        Start an interactive session where users can ask multiple questions.
        """
        print("\n" + "="*60)
        print("🎓 FreeCodeCamp Learning Assistant (Interactive Mode)")
        print("="*60)
        print("\nAsk me anything about web development, programming, or tech!")
        print("Commands:")
        print("  - Type your question to get started")
        print("  - Type 'quit' or 'exit' to end the session")
        print("  - Type 'help' for suggestions")
        print("\n" + "="*60 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for using FreeCodeCamp Learning Assistant!")
                    break

                if user_input.lower() == 'help':
                    self._show_help()
                    continue

                # Query the agent
                self.query(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using FreeCodeCamp Learning Assistant!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")

    def _show_help(self):
        """Show example questions."""
        print("\n💡 Example questions you can ask:")
        print("  - How do I learn React?")
        print("  - Show me tutorials about Python")
        print("  - What content do you have on machine learning?")
        print("  - Find articles about web development")
        print("  - Search for JavaScript videos")
        print()


def main():
    """
    Main function demonstrating different usage patterns.
    """
    # Configuration
    # Default to FastMCP Cloud deployment (publicly accessible)
    # For local development, set MCP_SERVER_URL=http://localhost:8000/mcp in .env
    SERVER_URL = os.getenv("MCP_SERVER_URL", "https://freedcodecamp-content.fastmcp.app/mcp")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # MCP requires gpt-5-mini, gpt-4.1 or compatible

    print("\n" + "="*60)
    print("🚀 FreeCodeCamp MCP Agent Client")
    print("="*60)
    print(f"\nServer URL: {SERVER_URL}")
    print(f"OpenAI Model: {MODEL}\n")

    # Initialize the agent client
    agent = FCCAgentClient(server_url=SERVER_URL, model=MODEL)

    # Example 1: Single query
    print("\n📝 Example 1: Single Query")
    agent.query("I want to learn React. What resources do you have?")

    # Example 2: Another topic
    print("\n📝 Example 2: Different Topic")
    agent.query("Show me Python tutorials")

    # Example 3: Interactive mode (commented out by default)
    print("\n📝 Starting Interactive Mode...")
    print("(You can comment this out if you just want to test the examples)")
    agent.interactive_mode()


if __name__ == "__main__":
    main()
