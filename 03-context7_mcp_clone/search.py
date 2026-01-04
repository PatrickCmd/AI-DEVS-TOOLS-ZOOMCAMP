"""
Search Test Script

This script tests the documentation search functionality by:
1. Testing the search_fastmcp_docs tool via MCP Client
2. Running various search queries including "demo"
3. Displaying results and statistics

This is for Question 5 of the homework.
"""

import asyncio
from fastmcp import Client
from main import mcp


async def test_search(query: str, top_k: int = 5):
    """Test searching FastMCP documentation."""
    print(f"\n{'=' * 60}")
    print(f"SEARCH QUERY: '{query}'")
    print(f"TOP K: {top_k}")
    print('=' * 60)

    try:
        async with Client(mcp) as client:
            # Call the search_fastmcp_docs tool
            result = await client.call_tool(
                "search_fastmcp_docs",
                {"query": query, "top_k": top_k}
            )

            # Extract content from result
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0].text
            else:
                content = str(result)

            print(content)

            # Parse first result filename if available
            if "1. " in content:
                lines = content.split('\n')
                for line in lines:
                    if line.strip().startswith("1. "):
                        first_file = line.strip()[3:].strip()
                        return first_file

    except Exception as e:
        print(f"❌ Search failed: {str(e)}")
        import traceback
        traceback.print_exc()

    return None


async def main():
    """Main test function with multiple queries."""
    print("\n" + "=" * 60)
    print("FASTMCP DOCUMENTATION SEARCH TEST")
    print("=" * 60)

    # Test queries
    test_cases = [
        ("demo", 5),              # Question 5 query
        ("getting started", 3),    # Common query
        ("tool decorator", 5),     # Technical term
        ("examples", 3),           # General query
    ]

    results = {}

    for query, top_k in test_cases:
        first_file = await test_search(query, top_k)
        if first_file:
            results[query] = first_file

    # Summary
    print("\n" + "=" * 60)
    print("SEARCH RESULTS SUMMARY")
    print("=" * 60)

    for query, first_file in results.items():
        print(f"Query: '{query}'")
        print(f"  → First result: {first_file}")
        print()

    # Highlight answer to Question 5
    if "demo" in results:
        print("=" * 60)
        print("📊 ANSWER TO QUESTION 5")
        print("=" * 60)
        print(f"First file for 'demo' query: {results['demo']}")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
