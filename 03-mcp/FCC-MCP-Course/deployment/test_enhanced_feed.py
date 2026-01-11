"""
Test script for enhanced RSS feed parsing

This script tests the improved feed parsing with comprehensive metadata
including content, categories, authors, dates, and markdown formatting.
"""

import feedparser
from markdownify import markdownify as md
from datetime import datetime
import json

def test_news_feed_parsing():
    """Test enhanced news feed parsing."""
    print("="*70)
    print("🧪 Testing Enhanced FreeCodeCamp News Feed Parsing")
    print("="*70)

    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")

    print(f"\n✓ Feed loaded: {feed.feed.get('title', 'Unknown')}")
    print(f"✓ Total entries: {len(feed.entries)}")

    if feed.entries:
        print("\n" + "="*70)
        print("📄 Sample Entry (First Result)")
        print("="*70)

        entry = feed.entries[0]

        # Title
        title = entry.get("title", "")
        print(f"\nTitle: {title}")

        # URL
        url = entry.get("link", "")
        print(f"URL: {url}")

        # Description
        description = entry.get("description", "")
        print(f"\nDescription: {description[:150]}...")

        # Author
        author = entry.get('author', 'Unknown')
        if hasattr(entry, 'author_detail'):
            author = entry.author_detail.get('name', author)
        print(f"\nAuthor: {author}")

        # Publication date
        pub_date = ""
        if hasattr(entry, 'published'):
            pub_date = entry.published
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    dt = datetime(*entry.published_parsed[:6])
                    pub_date = dt.strftime("%B %d, %Y at %I:%M %p UTC")
                except:
                    pass
        print(f"Published: {pub_date}")

        # Categories/Tags
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]
        print(f"\nCategories ({len(categories)}): {', '.join(categories[:5])}")
        if len(categories) > 5:
            print(f"  ... and {len(categories) - 5} more")

        # Content
        content_html = ""
        if hasattr(entry, 'content'):
            content_html = entry.content[0].value if entry.content else ""
        elif 'content' in entry:
            content_html = entry.content[0].get('value', '') if entry.content else ""

        if content_html:
            print(f"\nContent HTML length: {len(content_html)} characters")

            # Convert to markdown
            content_markdown = md(
                content_html,
                heading_style="ATX",
                strip=['script', 'style']
            ).strip()

            print(f"Content Markdown length: {len(content_markdown)} characters")
            print(f"\nMarkdown preview (first 300 chars):")
            print("-" * 70)
            print(content_markdown[:300] + "...")
            print("-" * 70)

        # Media/Image
        if hasattr(entry, 'media_content') and entry.media_content:
            image = entry.media_content[0].get('url', '')
            print(f"\nFeatured Image: {image}")

        # Complete result object
        result = {
            "title": title,
            "url": url,
            "description": description,
            "author": author,
            "published": pub_date,
            "categories": categories,
            "content_length": len(content_html),
            "markdown_length": len(content_markdown) if content_html else 0,
        }

        print("\n" + "="*70)
        print("📊 Complete Result Object")
        print("="*70)
        print(json.dumps(result, indent=2))

    print("\n" + "="*70)
    print("✅ Test Complete!")
    print("="*70)


def test_youtube_feed_parsing():
    """Test YouTube feed parsing."""
    print("\n\n" + "="*70)
    print("🎥 Testing FreeCodeCamp YouTube Feed Parsing")
    print("="*70)

    feed = feedparser.parse(
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ"
    )

    print(f"\n✓ Feed loaded: {feed.feed.get('title', 'Unknown')}")
    print(f"✓ Total entries: {len(feed.entries)}")

    if feed.entries:
        print("\n" + "="*70)
        print("🎬 Sample Entry (First Video)")
        print("="*70)

        entry = feed.entries[0]

        # Title
        title = entry.get("title", "")
        print(f"\nTitle: {title}")

        # URL
        url = entry.get("link", "")
        print(f"URL: {url}")

        # Description
        description = ""
        if hasattr(entry, 'summary'):
            description = entry.summary
        elif 'summary' in entry:
            description = entry.get('summary', '')

        if description:
            # Convert HTML to markdown if needed
            if '<' in description and '>' in description:
                description = md(description, strip=['script', 'style']).strip()
            print(f"\nDescription: {description[:200]}...")

        # Author
        author = entry.get('author', 'freeCodeCamp.org')
        if hasattr(entry, 'author_detail'):
            author = entry.author_detail.get('name', author)
        print(f"\nAuthor: {author}")

        # Publication date
        pub_date = ""
        if hasattr(entry, 'published'):
            pub_date = entry.published
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    dt = datetime(*entry.published_parsed[:6])
                    pub_date = dt.strftime("%B %d, %Y at %I:%M %p UTC")
                except:
                    pass
        print(f"Published: {pub_date}")

        # Video ID
        video_id = entry.get("yt_videoid", "")
        print(f"Video ID: {video_id}")

        # Thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            thumbnail = entry.media_thumbnail[0].get('url', '')
            print(f"Thumbnail: {thumbnail}")

    print("\n" + "="*70)
    print("✅ YouTube Test Complete!")
    print("="*70)


if __name__ == "__main__":
    test_news_feed_parsing()
    test_youtube_feed_parsing()
