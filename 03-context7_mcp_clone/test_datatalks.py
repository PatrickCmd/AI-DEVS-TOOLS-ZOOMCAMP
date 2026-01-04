"""
Test script for Question 4: Count "data" occurrences on datatalks.club.

This script:
1. Uses the scrape_web tool to fetch https://datatalks.club/
2. Counts how many times the word "data" appears (case-insensitive)
3. Reports the result
"""

import asyncio
import re
from fastmcp import Client
from main import mcp

async def test_datatalks_word_count():
    """Test scraping datatalks.club and counting 'data' occurrences."""
    print("Testing scrape_web with datatalks.club...")
    print("-" * 60)

    # Test URL from homework
    url = "https://datatalks.club/"

    print(f"Testing URL: {url}")
    print("Searching for word: 'data' (case-insensitive)")
    print("Please wait, this may take a few seconds...\n")

    try:
        # Use in-memory transport to test the tool
        async with Client(mcp) as client:
            # Call the scrape_web tool
            result = await client.call_tool("scrape_web", {"url": url})

            # Extract content from result
            if hasattr(result, 'content') and len(result.content) > 0:
                content = result.content[0].text
            else:
                content = str(result)

            # Check if error occurred
            if content.startswith("Error"):
                print(f"❌ Scraping failed: {content}")
                return None

            # Count occurrences of "data" (case-insensitive)
            # Using word boundaries to match whole words only
            data_pattern = r'\bdata\b'
            matches = re.findall(data_pattern, content, re.IGNORECASE)
            data_count = len(matches)

            # Also count total characters for reference
            char_count = len(content)

            print("✅ Scraping successful!")
            print(f"Total characters: {char_count}")
            print(f"Occurrences of 'data': {data_count}")
            print("-" * 60)

            # Show some examples of where "data" appears
            print("\nFirst few occurrences of 'data' in context:")
            lines_with_data = [line.strip() for line in content.split('\n') if re.search(data_pattern, line, re.IGNORECASE)]
            for i, line in enumerate(lines_with_data[:5], 1):
                # Truncate long lines
                if len(line) > 100:
                    line = line[:100] + "..."
                print(f"{i}. {line}")

            print("-" * 60)

            # Verify content contains expected information
            if "datatalks" in content.lower():
                print("✅ Content verification: 'datatalks' found in content")
            else:
                print("⚠️  Warning: 'datatalks' not found in content")

            return data_count

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Main async test function."""
    print("\n" + "=" * 60)
    print("MCP SERVER - WORD COUNTING TEST (QUESTION 4)")
    print("=" * 60 + "\n")

    data_count = await test_datatalks_word_count()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    if data_count is not None:
        print(f"\n📊 Answer to Question 4: {data_count} occurrences of 'data'")
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())
