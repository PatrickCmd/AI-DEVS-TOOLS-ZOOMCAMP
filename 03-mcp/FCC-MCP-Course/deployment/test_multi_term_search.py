"""
Test multi-term search behavior

This script tests how the search handles queries with multiple topics/terms.
"""

import feedparser

def test_current_search(query: str, max_results: int = 3):
    """Test the current search implementation."""
    print(f"\n{'='*70}")
    print(f"🔍 Testing Query: '{query}'")
    print(f"{'='*70}")

    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    results = []
    query_lower = query.lower()

    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        # Current implementation: simple substring search
        if query_lower in title.lower() or query_lower in description.lower():
            results.append({
                "title": title,
                "url": entry.get("link", "")
            })

        if len(results) >= max_results:
            break

    print(f"\n✓ Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['url']}")

    return results


def test_improved_search(query: str, max_results: int = 3, match_all: bool = False):
    """Test improved multi-term search."""
    print(f"\n{'='*70}")
    print(f"🔍 Testing Improved Query: '{query}' (match_all={match_all})")
    print(f"{'='*70}")

    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    results = []

    # Split query into terms
    terms = [term.strip().lower() for term in query.split() if term.strip()]

    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        # Get categories
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]

        # Combine searchable text
        searchable_text = f"{title} {description} {' '.join(categories)}".lower()

        # Check if entry matches
        if match_all:
            # ALL terms must be present
            if all(term in searchable_text for term in terms):
                results.append({
                    "title": title,
                    "url": entry.get("link", ""),
                    "categories": categories
                })
        else:
            # ANY term must be present
            if any(term in searchable_text for term in terms):
                results.append({
                    "title": title,
                    "url": entry.get("link", ""),
                    "categories": categories
                })

        if len(results) >= max_results:
            break

    print(f"\n✓ Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Categories: {', '.join(result['categories'][:3])}")
        print(f"   {result['url']}")

    return results


if __name__ == "__main__":
    print("="*70)
    print("🧪 Multi-Term Search Testing")
    print("="*70)

    # Test 1: Single term
    print("\n\n" + "="*70)
    print("TEST 1: Single Term")
    print("="*70)
    test_current_search("react", max_results=2)

    # Test 2: Multiple terms as phrase (current implementation)
    print("\n\n" + "="*70)
    print("TEST 2: Multiple Terms as Exact Phrase (Current)")
    print("="*70)
    test_current_search("react hooks", max_results=2)

    # Test 3: Multiple terms - ANY match (improved)
    print("\n\n" + "="*70)
    print("TEST 3: Multiple Terms - ANY Match (Improved)")
    print("="*70)
    test_improved_search("react python javascript", max_results=5, match_all=False)

    # Test 4: Multiple terms - ALL match (improved)
    print("\n\n" + "="*70)
    print("TEST 4: Multiple Terms - ALL Match (Improved)")
    print("="*70)
    test_improved_search("react hooks", max_results=5, match_all=True)

    # Test 5: Topic combinations
    print("\n\n" + "="*70)
    print("TEST 5: Multiple Topics - ANY Match")
    print("="*70)
    test_improved_search("machine learning ai python", max_results=5, match_all=False)

    print("\n\n" + "="*70)
    print("✅ All Tests Complete!")
    print("="*70)
