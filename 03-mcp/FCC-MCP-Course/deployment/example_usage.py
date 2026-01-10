"""
Example Usage of FreeCodeCamp MCP Agent Clients

This script demonstrates various ways to use the agent clients
to query FreeCodeCamp's educational content.
"""

from agent_client import FCCAgentClient
from agent_client_advanced import AdvancedFCCAgentClient
import os


def example_1_basic_query():
    """Example 1: Basic single query."""
    print("\n" + "="*70)
    print("📝 Example 1: Basic Query")
    print("="*70 + "\n")

    agent = FCCAgentClient(
        server_url=os.getenv("MCP_SERVER_URL", "http://localhost:8000"),
        model="gpt-4o-mini"
    )

    # Ask a question
    response = agent.query("How do I get started learning React?")

    print("\n✓ Response received successfully!")


def example_2_multiple_topics():
    """Example 2: Query multiple topics."""
    print("\n" + "="*70)
    print("📝 Example 2: Multiple Topic Queries")
    print("="*70 + "\n")

    agent = FCCAgentClient()

    topics = [
        "Python for beginners",
        "JavaScript ES6 features",
        "Machine Learning tutorials"
    ]

    for topic in topics:
        print(f"\n{'─'*70}")
        print(f"Topic: {topic}")
        print(f"{'─'*70}")
        agent.query(topic)


def example_3_conversation():
    """Example 3: Multi-turn conversation with context."""
    print("\n" + "="*70)
    print("📝 Example 3: Contextual Conversation")
    print("="*70 + "\n")

    agent = AdvancedFCCAgentClient()

    # Progressive conversation
    print("💬 Turn 1: Initial question")
    agent.query("I'm completely new to programming. Where should I begin?")

    print("\n💬 Turn 2: Follow-up question")
    agent.query("What programming language should I learn first?")

    print("\n💬 Turn 3: Specific request")
    agent.query("Show me some beginner Python tutorials")

    # Show conversation stats
    print("\n" + "="*70)
    print("📊 Conversation Statistics")
    print("="*70)
    print(agent.conversation.get_summary())


def example_4_specific_search():
    """Example 4: Searching for specific content types."""
    print("\n" + "="*70)
    print("📝 Example 4: Specific Content Search")
    print("="*70 + "\n")

    agent = FCCAgentClient()

    # Search for videos
    agent.query("Find YouTube videos about Node.js")

    # Search for articles
    agent.query("Show me articles about responsive web design")


def example_5_learning_path():
    """Example 5: Getting a learning path recommendation."""
    print("\n" + "="*70)
    print("📝 Example 5: Learning Path Recommendation")
    print("="*70 + "\n")

    agent = AdvancedFCCAgentClient(temperature=0.8)

    query = """
    I want to become a full-stack web developer.
    I know HTML and CSS basics.
    What should I learn next and in what order?
    """

    agent.query(query)


def example_6_export_conversation():
    """Example 6: Export conversation for later review."""
    print("\n" + "="*70)
    print("📝 Example 6: Conversation Export")
    print("="*70 + "\n")

    agent = AdvancedFCCAgentClient()

    # Have a learning session
    agent.query("Explain what REST APIs are")
    agent.query("How do I build a REST API with Node.js?")
    agent.query("Show me REST API tutorials")

    # Export the conversation
    filename = "learning_session_rest_apis.json"
    agent.conversation.export_conversation(filename)

    print(f"\n✓ Conversation exported to {filename}")
    print("You can review this session later!")


def example_7_cost_tracking():
    """Example 7: Track API costs."""
    print("\n" + "="*70)
    print("📝 Example 7: Cost Tracking")
    print("="*70 + "\n")

    agent = AdvancedFCCAgentClient(model="gpt-4o-mini")

    queries = [
        "What is JavaScript?",
        "Explain Python decorators",
        "How does Git work?"
    ]

    print("Running multiple queries and tracking costs...\n")

    for query in queries:
        agent.query(query, verbose=False)

    print("\n" + "="*70)
    print("📊 Total Usage")
    print("="*70)
    print(agent.conversation.get_summary())


def main():
    """Main function to run examples."""
    print("\n" + "="*70)
    print("🎓 FreeCodeCamp MCP Agent - Usage Examples")
    print("="*70)

    print("\nAvailable examples:")
    print("1. Basic Query")
    print("2. Multiple Topic Queries")
    print("3. Contextual Conversation")
    print("4. Specific Content Search")
    print("5. Learning Path Recommendation")
    print("6. Conversation Export")
    print("7. Cost Tracking")
    print("8. Run All Examples")
    print("9. Exit")

    while True:
        try:
            choice = input("\nEnter choice (1-9): ").strip()

            if choice == "1":
                example_1_basic_query()
            elif choice == "2":
                example_2_multiple_topics()
            elif choice == "3":
                example_3_conversation()
            elif choice == "4":
                example_4_specific_search()
            elif choice == "5":
                example_5_learning_path()
            elif choice == "6":
                example_6_export_conversation()
            elif choice == "7":
                example_7_cost_tracking()
            elif choice == "8":
                print("\n🚀 Running all examples...\n")
                example_1_basic_query()
                example_2_multiple_topics()
                example_3_conversation()
                example_4_specific_search()
                example_5_learning_path()
                example_6_export_conversation()
                example_7_cost_tracking()
                print("\n✓ All examples completed!")
                break
            elif choice == "9":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-9.")

            # Ask if user wants to continue
            continue_choice = input("\nRun another example? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Thanks for exploring the examples!")
                break

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    # Check if server is running
    import requests

    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")

    try:
        response = requests.get(server_url, timeout=5)
        print(f"✓ Server is running at {server_url}")
    except:
        print(f"\n⚠️  Warning: Cannot connect to server at {server_url}")
        print("Make sure the MCP server is running:")
        print("  python feed_deployment.py")
        print("\nOr update MCP_SERVER_URL in your .env file\n")

        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Exiting...")
            exit(1)

    main()
