from fastmcp import FastMCP
import requests
from doc_indexer import DocumentationIndexer

mcp = FastMCP("Context7 Clone 🔍")

# Global indexer instance (lazy loading)
_indexer = None

# FastMCP repository configuration
FASTMCP_REPO_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
FASTMCP_CACHE_FILE = "fastmcp-main.zip"


def get_or_create_indexer() -> DocumentationIndexer:
    """
    Get existing indexer or create and initialize a new one.

    This implements lazy loading:
    - Index is created on first search request
    - Subsequent searches use the cached index
    - Improves server startup time
    """
    global _indexer

    if _indexer is None:
        print("🔨 Initializing documentation indexer...")
        _indexer = DocumentationIndexer(cache_dir="data")

        # Load and index FastMCP documentation
        _indexer.load_and_index(
            repo_url=FASTMCP_REPO_URL,
            cache_filename=FASTMCP_CACHE_FILE,
            text_fields=["content"],
            keyword_fields=["filename"]
        )

        stats = _indexer.get_stats()
        print(f"✓ Indexer ready: {stats['num_documents']} documents indexed")

    return _indexer

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def scrape_web(url: str) -> str:
    """
    Download web page content as markdown using Jina Reader.

    Args:
        url: The URL to scrape

    Returns:
        Markdown content of the page
    """
    try:
        # Prepend Jina reader URL
        jina_url = f"https://r.jina.ai/{url}"

        # Make HTTP request with timeout
        response = requests.get(jina_url, timeout=30)

        # Raise exception for bad status codes
        response.raise_for_status()

        # Return markdown content
        return response.text

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while accessing {url}"
    except requests.exceptions.RequestException as e:
        return f"Error downloading {url}: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool
def search_fastmcp_docs(query: str, top_k: int = 5) -> str:
    """
    Search FastMCP documentation for relevant information.

    This tool searches through the FastMCP repository documentation
    including README files, guides, tutorials, and API references.

    **Note**: This tool is configured to search FastMCP documentation only.
    For flexible indexing and searching of any repository, use the CLI tool:
        python cli.py index --url <repo_url> --name <name>
        python cli.py search --name <name> --query <query>

    Or for direct Python usage:
        from doc_indexer import DocumentationIndexer
        indexer = DocumentationIndexer()
        indexer.load_and_index(repo_url, cache_file)
        results = indexer.search(query, top_k=5)

    Args:
        query: Search query (e.g., "how to create tools", "getting started", "demo")
        top_k: Number of results to return (default: 5, max: 10)

    Returns:
        Formatted search results with filenames and content snippets

    Examples:
        - search_fastmcp_docs("tool decorator")
        - search_fastmcp_docs("getting started", top_k=3)
        - search_fastmcp_docs("demo examples")

    Configuration:
        Repository: https://github.com/jlowin/fastmcp
        Cache file: fastmcp-main.zip (in data/ directory)
        Documents indexed: 266 markdown files
    """
    try:
        # Validate inputs
        if not query or not query.strip():
            return "Error: Query cannot be empty"

        if top_k < 1 or top_k > 10:
            return "Error: top_k must be between 1 and 10"

        # Get or create indexer (lazy loading)
        indexer = get_or_create_indexer()

        # Perform search
        results = indexer.search(query=query.strip(), top_k=top_k)

        if not results:
            return f"No results found for query: '{query}'"

        # Format results for display
        output = [f"Found {len(results)} result(s) for '{query}':\n"]

        for i, doc in enumerate(results, 1):
            filename = doc.get('filename', 'Unknown')
            content = doc.get('content', '')

            # Get first 200 characters as preview
            preview = content[:200].replace('\n', ' ').strip()
            if len(content) > 200:
                preview += "..."

            output.append(f"{i}. {filename}")
            output.append(f"   Preview: {preview}")
            output.append("")

        return "\n".join(output)

    except Exception as e:
        return f"Error searching documentation: {str(e)}"

if __name__ == "__main__":
    mcp.run()