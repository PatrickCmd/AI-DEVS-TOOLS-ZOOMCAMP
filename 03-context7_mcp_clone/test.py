"""
Test script for scrape_web tool.

This script tests the web scraping functionality using FastMCP's in-memory testing.
It tests the actual scrape_web function from main.py using the MCP Client.
"""

import asyncio
from fastmcp import Client
from main import mcp

async def test_scrape_minsearch():
    """Test scraping the minsearch repository using the MCP tool."""
    print("Testing scrape_web tool with minsearch repository...")
    print("-" * 60)

    # Test URL from homework
    url = "https://github.com/alexeygrigorev/minsearch"

    print(f"Testing URL: {url}")
    print("Please wait, this may take a few seconds...\n")

    try:
        # Use in-memory transport to test the tool
        async with Client(mcp) as client:
            # Call the scrape_web tool
            result = await client.call_tool("scrape_web", {"url": url})

            # Extract content from result
            # MCP tool results are returned as a list of TextContent objects
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0].text
            else:
                content = str(result)

            # Check if error occurred
            if content.startswith("Error"):
                print(f"❌ Scraping failed: {content}")
                return None

            # Count characters
            char_count = len(content)

            print("✅ Scraping successful!")
            print(f"Character count: {char_count}")
            print("-" * 60)
            print("\nFirst 500 characters of content:")
            print(content[:500])
            print("\n...")
            print("\nLast 500 characters of content:")
            print(content[-500:])
            print("-" * 60)

            # Verify content contains expected information
            if "minsearch" in content.lower():
                print("✅ Content verification: 'minsearch' found in content")
            else:
                print("⚠️  Warning: 'minsearch' not found in content")

            return char_count

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Main async test function."""
    print("\n" + "=" * 60)
    print("MCP SERVER - WEB SCRAPING TOOL TEST")
    print("=" * 60 + "\n")

    char_count = await test_scrape_minsearch()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    if char_count:
        print(f"\n📊 Answer to Question 3: {char_count} characters")
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
