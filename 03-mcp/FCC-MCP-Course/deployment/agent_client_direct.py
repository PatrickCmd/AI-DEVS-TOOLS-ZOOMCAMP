"""
Direct MCP Client with OpenAI Responses API

This client demonstrates:
1. Direct connection to MCP server using FastMCP Python client
2. Dynamic tool retrieval from MCP server
3. Integration with OpenAI Responses API (not chat.completions)
4. Programmatic session management
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json
import asyncio
from fastmcp import Client

# Load environment variables
load_dotenv()


class DirectMCPAgentClient:
    """
    Agent client that directly connects to MCP server and uses OpenAI Responses API.

    This approach:
    - Uses FastMCP client to connect to the MCP server
    - Retrieves tools dynamically from the server
    - Converts MCP tools to OpenAI-compatible format
    - Uses OpenAI Responses API for completions
    """

    def __init__(
        self,
        server_url: str = "http://localhost:8000",
        model: str = "gpt-4.1"
    ):
        """
        Initialize the direct MCP agent client.

        Args:
            server_url (str): URL where the MCP server is running
            model (str): OpenAI model to use with Responses API
        """
        self.server_url = server_url
        self.mcp_endpoint = f"{server_url}/mcp"
        self.model = model
        self.openai_client = OpenAI()
        self.tools = []
        self.mcp_tools_map = {}
        self.mcp_client = None

        print(f"✓ Initializing Direct MCP Client")
        print(f"  Server URL: {self.server_url}")
        print(f"  MCP Endpoint: {self.mcp_endpoint}")
        print(f"  Model: {self.model}")

        # Fetch tools from MCP server
        asyncio.run(self._fetch_mcp_tools())

    async def _fetch_mcp_tools(self):
        """
        Fetch available tools from the MCP server using FastMCP client.
        """
        try:
            print(f"\n🔍 Connecting to MCP server and fetching tools...")

            # Create FastMCP client
            client = Client(self.mcp_endpoint)

            async with client:
                # List available tools
                mcp_tools = await client.list_tools()

                print(f"✓ Connected to MCP server")
                print(f"✓ Found {len(mcp_tools)} tools from MCP server")

                # Convert each MCP tool to OpenAI format
                for tool in mcp_tools:
                    self._add_tool(tool)

        except Exception as e:
            print(f"❌ Error fetching MCP tools: {str(e)}")
            print(f"   Using fallback tool definitions")
            self._use_fallback_tools()

    def _use_fallback_tools(self):
        """
        Use hardcoded tool definitions as fallback if dynamic fetch fails.
        """
        print("\n⚠️  Using fallback tool definitions")

        fallback_tools = [
            {
                "name": "fcc_news_search",
                "description": "Search FreeCodeCamp's news feed via RSS by title/description matching.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to match against article titles and descriptions"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 3
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "fcc_youtube_search",
                "description": "Search FreeCodeCamp's YouTube channel via RSS feed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to match against video titles and descriptions"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 3
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "fcc_secret_message",
                "description": "Get an inspirational secret message from FreeCodeCamp.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

        # Create mock tool objects
        class MockTool:
            def __init__(self, name, description, inputSchema):
                self.name = name
                self.description = description
                self.inputSchema = inputSchema

        for tool_def in fallback_tools:
            mock_tool = MockTool(
                tool_def['name'],
                tool_def['description'],
                tool_def['inputSchema']
            )
            self._add_tool(mock_tool)

    def _add_tool(self, mcp_tool):
        """
        Convert MCP tool format to OpenAI Responses API format and add to tools list.

        Args:
            mcp_tool: Tool object from MCP server
        """
        tool_name = mcp_tool.name

        # Store MCP tool reference for later execution
        self.mcp_tools_map[tool_name] = mcp_tool

        # Convert to OpenAI Responses API function format
        # Note: Responses API has different format than chat.completions
        openai_tool = {
            "type": "function",
            "name": tool_name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema,
            "strict": False
        }

        self.tools.append(openai_tool)
        print(f"  ✓ Added tool: {tool_name}")

    async def _call_mcp_tool_async(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool on the MCP server asynchronously.

        Args:
            tool_name (str): Name of the tool to call
            arguments (dict): Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        try:
            client = Client(self.mcp_endpoint)

            async with client:
                result = await client.call_tool(tool_name, arguments)
                return result.content if hasattr(result, 'content') else result

        except Exception as e:
            return {"error": f"Error calling MCP tool: {str(e)}"}

    def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool on the MCP server (synchronous wrapper).

        Args:
            tool_name (str): Name of the tool to call
            arguments (dict): Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        return asyncio.run(self._call_mcp_tool_async(tool_name, arguments))

    def query(self, user_query: str, instructions: str = None) -> str:
        """
        Query the agent using OpenAI Responses API with MCP tools.

        Args:
            user_query (str): The user's question
            instructions (str, optional): Additional instructions for the agent

        Returns:
            str: The agent's response
        """
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

        print(f"\n{'='*70}")
        print(f"🔍 Query: {user_query}")
        print(f"{'='*70}\n")

        try:
            # Use OpenAI Responses API with our converted tools
            response = self.openai_client.responses.create(
                model=self.model,
                instructions=instructions,
                tools=self.tools,
                input=user_query,
            )

            # Extract the response
            output = response.output_text

            print(f"🤖 Agent Response:\n")
            print(output)
            print(f"\n{'='*70}\n")

            return output

        except Exception as e:
            error_msg = f"Error querying agent: {str(e)}"
            print(f"❌ {error_msg}")

            # Print more detailed error info
            if hasattr(e, 'response'):
                print(f"   Response: {e.response}")

            return error_msg

    def interactive_mode(self):
        """
        Start an interactive session where users can ask multiple questions.
        """
        print("\n" + "="*70)
        print("🎓 FreeCodeCamp Learning Assistant (Direct MCP Mode)")
        print("="*70)
        print("\nAsk me anything about web development, programming, or tech!")
        print("Commands:")
        print("  - Type your question to get started")
        print("  - Type 'quit' or 'exit' to end the session")
        print("  - Type 'help' for suggestions")
        print("  - Type 'tools' to see available tools")
        print("\n" + "="*70 + "\n")

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

                if user_input.lower() == 'tools':
                    self._show_tools()
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

    def _show_tools(self):
        """Show available tools."""
        print("\n🔧 Available Tools:")
        for tool in self.tools:
            func = tool.get('function', {})
            print(f"\n  📌 {func.get('name')}")
            print(f"     {func.get('description')}")
        print()


def main():
    """
    Main function demonstrating usage.
    """
    # Configuration
    SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

    print("\n" + "="*70)
    print("🚀 FreeCodeCamp Direct MCP Agent Client")
    print("="*70)
    print(f"\nServer URL: {SERVER_URL}")
    print(f"OpenAI Model: {MODEL}\n")

    # Initialize the agent client
    agent = DirectMCPAgentClient(server_url=SERVER_URL, model=MODEL)

    # Check if tools were loaded
    if not agent.tools:
        print("\n⚠️  Warning: No tools loaded. Please check MCP server connection.")
        return

    # Example 1: Single query
    print("\n📝 Example 1: Single Query")
    agent.query("I want to learn React. What resources do you have?")

    # Example 2: Interactive mode
    print("\n📝 Starting Interactive Mode...")
    agent.interactive_mode()


if __name__ == "__main__":
    main()
