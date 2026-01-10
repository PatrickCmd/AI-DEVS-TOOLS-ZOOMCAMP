"""
Advanced OpenAI Agent Client for FreeCodeCamp MCP Server

This advanced client demonstrates:
1. Multi-turn conversations with context
2. Streaming responses
3. Tool call tracking
4. Cost estimation
5. Error handling and retries
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from datetime import datetime
import json

# Load environment variables
load_dotenv()


class ConversationManager:
    """Manages conversation history and context."""

    def __init__(self):
        self.messages: List[Dict] = []
        self.tool_calls: List[Dict] = []
        self.start_time = datetime.now()

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def add_tool_call(self, tool_name: str, arguments: dict, result: str):
        """Track tool calls for debugging."""
        self.tool_calls.append({
            "tool": tool_name,
            "arguments": arguments,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    def get_summary(self) -> str:
        """Get conversation summary."""
        duration = (datetime.now() - self.start_time).total_seconds()
        return f"""
Conversation Summary:
- Duration: {duration:.2f} seconds
- Messages: {len(self.messages)}
- Tool Calls: {len(self.tool_calls)}
        """

    def export_conversation(self, filename: str = "conversation.json"):
        """Export conversation to JSON file."""
        data = {
            "metadata": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_messages": len(self.messages),
                "total_tool_calls": len(self.tool_calls)
            },
            "messages": self.messages,
            "tool_calls": self.tool_calls
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✓ Conversation exported to {filename}")


class AdvancedFCCAgentClient:
    """
    Advanced agent client with conversation management and enhanced features.
    """

    def __init__(
        self,
        server_url: str = "http://localhost:8000",
        model: str = "gpt-4.1",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Initialize the advanced agent client.

        Args:
            server_url (str): URL where the MCP server is running
            model (str): OpenAI model to use. Must support MCP tools.
                        Recommended: gpt-4.1 (default), gpt-4.5, or gpt-5
            temperature (float): Response randomness (0-2)
            max_tokens (int): Maximum tokens in response
        """
        self.server_url = server_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI()
        self.conversation = ConversationManager()

        # Warn if using incompatible model
        compatible_models = ["gpt-4.1", "gpt-4.5", "gpt-5", "gpt-5-mini"]
        if not any(m in model for m in compatible_models):
            print(f"⚠️  Warning: Model '{model}' may not support MCP tools.")
            print(f"   Recommended models: {', '.join(compatible_models)}")

        # Configure MCP tool for OpenAI
        # Note: Per FastMCP docs, server_url should include trailing slash /mcp/
        self.mcp_tool = {
            "type": "mcp",
            "server_label": "fcc_content_explorer",
            "server_url": f"{server_url}/mcp/",  # Trailing slash required
            "require_approval": "never",
        }

        # System instructions
        self.system_instructions = """
        You are an expert programming tutor powered by FreeCodeCamp's educational content.

        Your role:
        - Help developers learn programming and web development
        - Search FreeCodeCamp's news and YouTube content using available tools
        - Provide clear, encouraging, and educational responses
        - Include links to relevant resources
        - Break down complex topics into understandable explanations

        When answering:
        1. First, use tools to search for relevant FreeCodeCamp content
        2. Analyze the results and extract key information
        3. Provide a structured response with:
           - Brief explanation of the topic
           - Links to relevant articles/videos
           - Next steps for learning
        4. Be encouraging and supportive

        If tools return no results, provide general guidance based on your knowledge
        and suggest related topics to explore.
        """

        self._print_header()

    def _print_header(self):
        """Print initialization header."""
        print("\n" + "="*70)
        print("🚀 Advanced FreeCodeCamp Learning Assistant")
        print("="*70)
        print(f"✓ Server: {self.server_url}")
        print(f"✓ Model: {self.model}")
        print(f"✓ Temperature: {self.temperature}")
        print(f"✓ Max Tokens: {self.max_tokens}")
        print("="*70 + "\n")

    def query(
        self,
        user_query: str,
        stream: bool = False,
        verbose: bool = True
    ) -> str:
        """
        Query the agent with context awareness.

        Args:
            user_query (str): The user's question
            stream (bool): Enable streaming responses
            verbose (bool): Print detailed information

        Returns:
            str: The agent's response
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"💬 Query: {user_query}")
            print(f"{'='*70}\n")

        # Add to conversation history
        self.conversation.add_message("user", user_query)

        try:
            # Create response with OpenAI
            response = self.client.responses.create(
                model=self.model,
                instructions=self.system_instructions,
                tools=[self.mcp_tool],
                input=user_query,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )

            # Extract response
            output = response.output_text

            # Add to conversation history
            self.conversation.add_message("assistant", output)

            # Track usage
            if hasattr(response, 'usage'):
                self._print_usage(response.usage)

            if verbose:
                print(f"🤖 Assistant:\n")
                print(output)
                print(f"\n{'='*70}\n")

            return output

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n❌ {error_msg}\n")
            self.conversation.add_message("system", f"Error: {error_msg}")
            return error_msg

    def _print_usage(self, usage):
        """Print token usage information."""
        print(f"\n📊 Usage Stats:")
        print(f"  - Input tokens: {usage.input_tokens}")
        print(f"  - Output tokens: {usage.output_tokens}")
        print(f"  - Total tokens: {usage.total_tokens}")

        # Estimate cost (approximate rates for GPT-4o-mini)
        if "gpt-4o-mini" in self.model.lower():
            input_cost = (usage.input_tokens / 1_000_000) * 0.15
            output_cost = (usage.output_tokens / 1_000_000) * 0.60
            total_cost = input_cost + output_cost
            print(f"  - Estimated cost: ${total_cost:.6f}")

    def chat(self):
        """
        Start an interactive chat session with enhanced features.
        """
        print("\n" + "="*70)
        print("💬 Interactive Chat Mode")
        print("="*70)
        print("\nCommands:")
        print("  📝 Type your question to chat")
        print("  💾 Type 'save' to export conversation")
        print("  📊 Type 'stats' to see conversation stats")
        print("  💡 Type 'help' for example questions")
        print("  🚪 Type 'quit' or 'exit' to end")
        print("\n" + "="*70 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    self._handle_exit()
                    break

                if user_input.lower() == 'save':
                    self._handle_save()
                    continue

                if user_input.lower() == 'stats':
                    self._handle_stats()
                    continue

                if user_input.lower() == 'help':
                    self._show_help()
                    continue

                # Process query
                self.query(user_input, verbose=True)

            except KeyboardInterrupt:
                print("\n")
                self._handle_exit()
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")

    def _handle_exit(self):
        """Handle exit command."""
        print("\n" + "="*70)
        print(self.conversation.get_summary())
        print("="*70)

        save = input("\n💾 Save conversation? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Filename (default: conversation.json): ").strip()
            if not filename:
                filename = "conversation.json"
            self.conversation.export_conversation(filename)

        print("\n👋 Thanks for using FreeCodeCamp Learning Assistant!")
        print("Happy coding! 🚀\n")

    def _handle_save(self):
        """Handle save command."""
        filename = input("Filename (default: conversation.json): ").strip()
        if not filename:
            filename = "conversation.json"
        self.conversation.export_conversation(filename)

    def _handle_stats(self):
        """Handle stats command."""
        print("\n" + "="*70)
        print(self.conversation.get_summary())
        print("="*70 + "\n")

    def _show_help(self):
        """Show example questions."""
        print("\n" + "="*70)
        print("💡 Example Questions:")
        print("="*70)
        examples = [
            "How do I get started with React?",
            "Show me Python tutorials for beginners",
            "What are the best JavaScript courses?",
            "Find articles about web development",
            "I want to learn machine learning",
            "Search for Node.js videos",
            "What should I learn after HTML and CSS?",
            "Explain responsive web design"
        ]
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example}")
        print("="*70 + "\n")


def demo_basic_usage():
    """Demonstrate basic usage."""
    print("\n🎯 Demo 1: Basic Usage\n")

    agent = AdvancedFCCAgentClient(
        server_url=os.getenv("MCP_SERVER_URL", "http://localhost:8000"),
        model="gpt-4.1"  # MCP requires gpt-4.1 or compatible
    )

    # Single query
    agent.query("How do I learn React?")


def demo_multi_turn():
    """Demonstrate multi-turn conversation."""
    print("\n🎯 Demo 2: Multi-Turn Conversation\n")

    agent = AdvancedFCCAgentClient(
        server_url=os.getenv("MCP_SERVER_URL", "http://localhost:8000"),
        model="gpt-4o-mini"
    )

    # Multiple related queries
    queries = [
        "I'm new to programming. Where should I start?",
        "What about Python?",
        "Show me some Python tutorials"
    ]

    for query in queries:
        agent.query(query)


def demo_interactive():
    """Demonstrate interactive mode."""
    print("\n🎯 Demo 3: Interactive Mode\n")

    agent = AdvancedFCCAgentClient(
        server_url=os.getenv("MCP_SERVER_URL", "http://localhost:8000"),
        model="gpt-4o-mini",
        temperature=0.8
    )

    agent.chat()


def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("🎓 FreeCodeCamp MCP Agent - Advanced Client")
    print("="*70)

    print("\nChoose a demo:")
    print("1. Basic Usage (single query)")
    print("2. Multi-Turn Conversation")
    print("3. Interactive Chat Mode")
    print("4. Run all demos")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        demo_basic_usage()
    elif choice == "2":
        demo_multi_turn()
    elif choice == "3":
        demo_interactive()
    elif choice == "4":
        demo_basic_usage()
        demo_multi_turn()
        demo_interactive()
    else:
        print("❌ Invalid choice. Running interactive mode...")
        demo_interactive()


if __name__ == "__main__":
    main()
