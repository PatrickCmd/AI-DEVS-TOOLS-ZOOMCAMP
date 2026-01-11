# Tutorial: Deploying an MCP Service with HTTP Transport
# This example shows how to deploy an MCP service using HTTP transport

# Step 1: Import required libraries
from fastmcp import FastMCP
import feedparser
from markdownify import markdownify as md
from datetime import datetime

# Step 2: Create the MCP service
# Note: This is similar to our previous feed service, but configured for HTTP deployment
mcp = FastMCP(name="FreeCodeCamp Content Explorer (Deployed)")

# Step 3: Define the service tools
@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3, include_content: bool = False, match_all_terms: bool = False):
    """
    Search FreeCodeCamp's news feed via RSS with comprehensive metadata.

    This tool searches through title, description, content, and categories,
    returning rich metadata including authors, publication dates, categories,
    and optionally full content in markdown format.

    Supports multi-term queries: "react hooks javascript" finds articles with ANY or ALL terms.

    Args:
        query (str): The search term(s) to look for. Can be multiple terms separated by spaces.
        max_results (int, optional): Maximum results to return. Defaults to 3.
        include_content (bool, optional): Include full article content in markdown. Defaults to False.
        match_all_terms (bool, optional): If True, ALL terms must be present. If False, ANY term matches. Defaults to False.

    Returns:
        list: Matching articles with metadata or a "no results" message
    """
    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    results = []

    # Split query into individual terms for multi-term search
    search_terms = [term.strip().lower() for term in query.split() if term.strip()]

    # If single term or empty, use original query
    if len(search_terms) <= 1:
        search_terms = [query.lower()]
        match_all_terms = False  # Single term doesn't need AND logic

    for entry in feed.entries:
        # Extract basic fields
        title = entry.get("title", "")
        description = entry.get("description", "")

        # Extract content (full article HTML)
        content_html = ""
        if hasattr(entry, 'content'):
            content_html = entry.content[0].value if entry.content else ""
        elif 'content' in entry:
            content_html = entry.content[0].get('value', '') if entry.content else ""

        # Extract categories/tags
        categories = []
        if hasattr(entry, 'tags'):
            categories = [tag.term for tag in entry.tags]

        # Search in multiple fields
        searchable_text = f"{title} {description} {content_html} {' '.join(categories)}".lower()

        # Multi-term search logic
        is_match = False
        if match_all_terms:
            # ALL terms must be present
            is_match = all(term in searchable_text for term in search_terms)
        else:
            # ANY term must be present
            is_match = any(term in searchable_text for term in search_terms)

        if is_match:
            # Parse publication date
            pub_date = ""
            if hasattr(entry, 'published'):
                pub_date = entry.published
                # Try to format it nicely
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        dt = datetime(*entry.published_parsed[:6])
                        pub_date = dt.strftime("%B %d, %Y at %I:%M %p UTC")
                    except:
                        pass

            # Extract author
            author = entry.get('author', 'Unknown')
            if hasattr(entry, 'author_detail'):
                author = entry.author_detail.get('name', author)

            # Build result object
            result = {
                "title": title,
                "url": entry.get("link", ""),
                "description": description,
                "author": author,
                "published": pub_date,
                "categories": categories,
            }

            # Add media/image if available
            if hasattr(entry, 'media_content') and entry.media_content:
                result["image"] = entry.media_content[0].get('url', '')

            # Optionally include full content in markdown
            if include_content and content_html:
                # Convert HTML content to markdown
                content_markdown = md(
                    content_html,
                    heading_style="ATX",  # Use # style headings
                    strip=['script', 'style']  # Remove script and style tags
                )
                result["content_markdown"] = content_markdown.strip()

            results.append(result)

        if len(results) >= max_results:
            break

    return results or [{"message": "No results found for your query"}]

@mcp.tool()
def fcc_youtube_search(query: str, max_results: int = 3, include_content: bool = True, match_all_terms: bool = False):
    """
    Search FreeCodeCamp's YouTube channel via RSS with comprehensive metadata.

    This tool searches through video titles and descriptions,
    returning metadata including authors, publication dates, thumbnails,
    and video statistics.

    Supports multi-term queries: "python tutorial beginner" finds videos with ANY or ALL terms.

    Args:
        query (str): The search term(s) to look for. Can be multiple terms separated by spaces.
        max_results (int, optional): Maximum results to return. Defaults to 3.
        include_content (bool, optional): Include video descriptions. Defaults to True.
        match_all_terms (bool, optional): If True, ALL terms must be present. If False, ANY term matches. Defaults to False.

    Returns:
        list: Matching videos with metadata or a "no videos found" message
    """
    feed = feedparser.parse(
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ"
    )
    results = []

    # Split query into individual terms for multi-term search
    search_terms = [term.strip().lower() for term in query.split() if term.strip()]

    # If single term or empty, use original query
    if len(search_terms) <= 1:
        search_terms = [query.lower()]
        match_all_terms = False  # Single term doesn't need AND logic

    for entry in feed.entries:
        title = entry.get("title", "")

        # Get description/summary
        description = ""
        if hasattr(entry, 'summary'):
            description = entry.summary
        elif 'summary' in entry:
            description = entry.get('summary', '')

        # Search in title and description
        searchable_text = f"{title} {description}".lower()

        # Multi-term search logic
        is_match = False
        if match_all_terms:
            # ALL terms must be present
            is_match = all(term in searchable_text for term in search_terms)
        else:
            # ANY term must be present
            is_match = any(term in searchable_text for term in search_terms)

        if is_match:
            # Parse publication date
            pub_date = ""
            if hasattr(entry, 'published'):
                pub_date = entry.published
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        dt = datetime(*entry.published_parsed[:6])
                        pub_date = dt.strftime("%B %d, %Y at %I:%M %p UTC")
                    except:
                        pass

            # Extract author/channel
            author = entry.get('author', 'freeCodeCamp.org')
            if hasattr(entry, 'author_detail'):
                author = entry.author_detail.get('name', author)

            # Build result object
            result = {
                "title": title,
                "url": entry.get("link", ""),
                "author": author,
                "published": pub_date,
                "video_id": entry.get("yt_videoid", ""),
            }

            # Add description if requested
            if include_content and description:
                # Convert HTML to markdown if needed
                if '<' in description and '>' in description:
                    description = md(description, strip=['script', 'style']).strip()
                result["description"] = description

            # Add thumbnail if available
            if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                result["thumbnail"] = entry.media_thumbnail[0].get('url', '')

            results.append(result)

        if len(results) >= max_results:
            break

    return results or [{"message": "No videos found for your query"}]

@mcp.tool()
def fcc_secret_message():
    """Returns an inspirational message."""
    return "Keep exploring! The journey of learning never ends! 🌟"

# Step 4: Run the service with HTTP transport
if __name__ == "__main__":
    print("Starting the FreeCodeCamp Content Explorer with HTTP transport...")
    print("The service will be accessible via HTTP endpoints")
    print("This deployment configuration allows the service to:")
    print("1. Be accessed over HTTP")
    print("2. Handle multiple concurrent requests")
    print("3. Be integrated with web services")
    
    # The key difference is here - we use HTTP transport instead of STDIO
    # mcp.run(transport="http", host="0.0.0.0", port=8000)
    mcp.run(transport="http")

# Deployment Notes:
# 1. This service uses HTTP transport instead of STDIO
# 2. It can be accessed through HTTP endpoints
# 3. Suitable for production deployment
# 4. Can be containerized and deployed to cloud platforms