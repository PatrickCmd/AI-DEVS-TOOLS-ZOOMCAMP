# Documentation Search CLI - Usage Guide

## Overview

The Documentation Search CLI provides a flexible command-line interface for indexing and searching documentation from any GitHub repository or website.

## Installation

The CLI tool uses the Click library, which is already included in the project dependencies:

```bash
uv sync
```

## Quick Start

### 1. Index a Repository

```bash
# Index FastMCP documentation (default for homework)
python cli.py index --url https://github.com/jlowin/fastmcp --name fastmcp

# Index MinSearch documentation
python cli.py index --url https://github.com/alexeygrigorev/minsearch --name minsearch

# Index any GitHub repository
python cli.py index --url https://github.com/user/repo --name myrepo
```

### 2. Search Indexed Documentation

```bash
# Search FastMCP docs
python cli.py search --name fastmcp --query "how to create tools"

# Search with custom result count
python cli.py search --name fastmcp --query "getting started" --top-k 3

# Search MinSearch docs
python cli.py search --name minsearch --query "examples"
```

### 3. Interactive Mode

```bash
# Start interactive session
python cli.py interactive
```

Interactive mode provides a menu-driven interface for:
- Indexing new repositories
- Searching existing indexes
- Multiple queries on the same index

---

## Commands

### `index` - Index Documentation

Download and index documentation from a GitHub repository.

**Syntax:**
```bash
python cli.py index [OPTIONS]
```

**Options:**
- `--url TEXT`: Repository or website URL to index (prompts if not provided)
- `--name TEXT`: Friendly name to identify this documentation index (prompts if not provided)
- `--cache-dir TEXT`: Directory to store cached files (default: data)
- `--help`: Show help message

**Examples:**

```bash
# With prompts (interactive)
python cli.py index
# URL: https://github.com/jlowin/fastmcp
# Name: fastmcp

# With all arguments
python cli.py index \
  --url https://github.com/jlowin/fastmcp \
  --name fastmcp

# Custom cache directory
python cli.py index \
  --url https://github.com/user/repo \
  --name myrepo \
  --cache-dir /path/to/cache
```

**What happens:**
1. Converts GitHub URL to archive download URL
2. Downloads repository as ZIP file (with caching)
3. Extracts markdown files (.md and .mdx)
4. Creates searchable index using MinSearch
5. Saves index for future searches

**Output:**
```
🔍 Indexing: fastmcp
URL: https://github.com/jlowin/fastmcp
------------------------------------------------------------
Archive URL: https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip
Cache file: fastmcp-main.zip

Indexing  [####################################]  100%

✓ Indexing complete!
Documents indexed: 266
Total characters: 1,234,567

You can now search with: python cli.py search --name fastmcp --query 'your query'
```

---

### `search` - Search Documentation

Search through previously indexed documentation.

**Syntax:**
```bash
python cli.py search [OPTIONS]
```

**Options:**
- `--name TEXT`: Name of the documentation index to search (prompts if not provided)
- `--query TEXT`: Search query (prompts if not provided)
- `--top-k INTEGER`: Number of results to return, 1-10 (default: 5)
- `--cache-dir TEXT`: Directory where cached files are stored (default: data)
- `--help`: Show help message

**Examples:**

```bash
# With prompts (interactive)
python cli.py search
# Index name: fastmcp
# Search query: demo

# With all arguments
python cli.py search \
  --name fastmcp \
  --query "how to create tools"

# Return only top 3 results
python cli.py search \
  --name fastmcp \
  --query "getting started" \
  --top-k 3

# Search different repository
python cli.py search \
  --name minsearch \
  --query "vector search"
```

**Output:**
```
🔎 Searching: fastmcp
Query: "demo"
------------------------------------------------------------

Found 5 result(s):

1. examples/testing_demo/README.md
   # FastMCP Testing Demo  A comprehensive example demonstrating FastMCP testing patterns with pytest-asyncio.  ## Overview  This example shows how t...

2. examples/fastmcp_config_demo/README.md
   # FastMCP Configuration Demo  This example demonstrates the recommended way to configure FastMCP servers using `fastmcp.json`.  ## Migration from D...

3. examples/atproto_mcp/README.md
   # ATProto MCP Server  This example demonstrates a FastMCP server that provides tools and resources for interacting with the AT Protocol (Bluesky)...
```

---

### `interactive` - Interactive Mode

Interactive mode for indexing and searching documentation.

**Syntax:**
```bash
python cli.py interactive [OPTIONS]
```

**Options:**
- `--cache-dir TEXT`: Directory for cached files (default: data)
- `--help`: Show help message

**Example:**
```bash
python cli.py interactive
```

**Interactive Menu:**
```
============================================================
  Documentation Search CLI - Interactive Mode
============================================================

What would you like to do?
1. Index a new repository
2. Search existing index
3. Exit
Your choice [1]: 1

Repository or website URL [https://github.com/jlowin/fastmcp]:
Name for this index [fastmcp]:

Indexing 'fastmcp' from https://github.com/jlowin/fastmcp...
✓ Indexed 266 documents!

Search 'fastmcp' (or 'quit' to go back) [demo]: how to create tools

Found 5 result(s):
...

Search 'fastmcp' (or 'quit' to go back) [demo]: quit
```

---

## Direct Python Usage

For programmatic access, use the `DocumentationIndexer` class directly:

```python
from doc_indexer import DocumentationIndexer

# Create indexer
indexer = DocumentationIndexer(cache_dir="data")

# Index a repository
indexer.load_and_index(
    repo_url="https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip",
    cache_filename="fastmcp-main.zip",
    text_fields=["content"],
    keyword_fields=["filename"]
)

# Search
results = indexer.search(query="demo", top_k=5)

# Display results
for doc in results:
    print(f"{doc['filename']}: {doc['content'][:100]}...")

# Get stats
stats = indexer.get_stats()
print(f"Indexed {stats['num_documents']} documents")
```

---

## Using with MCP Server (search_fastmcp_docs)

The MCP tool `search_fastmcp_docs` is pre-configured for FastMCP documentation:

### Via MCP Client (for testing)

```python
import asyncio
from fastmcp import Client
from main import mcp

async def test_search():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_fastmcp_docs",
            {"query": "demo", "top_k": 5}
        )
        print(result.content[0].text)

asyncio.run(test_search())
```

### Configuration

The `search_fastmcp_docs` tool uses these constants from `main.py`:

```python
FASTMCP_REPO_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
FASTMCP_CACHE_FILE = "fastmcp-main.zip"
```

To search FastMCP documentation:
1. The index is created lazily on first search
2. Subsequent searches use the cached index
3. Cache persists across server restarts

---

## Use Cases

### 1. Homework Exercise (Question 5 & 6)

```bash
# Index FastMCP (already done if you ran search.py)
python cli.py search --name fastmcp --query "demo"
```

This will return: `examples/testing_demo/README.md` as the first result.

### 2. Index Multiple Repositories

```bash
# Index FastMCP
python cli.py index --url https://github.com/jlowin/fastmcp --name fastmcp

# Index MinSearch
python cli.py index --url https://github.com/alexeygrigorev/minsearch --name minsearch

# Index your own repository
python cli.py index --url https://github.com/yourusername/yourrepo --name myrepo
```

### 3. Compare Documentation

```bash
# Search FastMCP for "demo"
python cli.py search --name fastmcp --query "demo"

# Search MinSearch for "demo"
python cli.py search --name minsearch --query "demo"
```

### 4. Build Your Own Documentation Assistant

```python
from doc_indexer import DocumentationIndexer

# Create custom indexer
indexer = DocumentationIndexer(cache_dir="my_docs_cache")

# Index multiple repositories
repos = [
    ("https://github.com/jlowin/fastmcp", "fastmcp"),
    ("https://github.com/alexeygrigorev/minsearch", "minsearch"),
]

for url, name in repos:
    archive_url = f"{url}/archive/refs/heads/main.zip"
    cache_file = f"{name}-main.zip"
    indexer.load_and_index(archive_url, cache_file)

    # Search each repository
    results = indexer.search("getting started", top_k=3)
    print(f"\n{name} results:")
    for doc in results:
        print(f"  - {doc['filename']}")
```

---

## Troubleshooting

### Index Not Found

**Error:**
```
✗ Index 'myrepo' not found!
```

**Solution:**
Index the repository first:
```bash
python cli.py index --url https://github.com/user/repo --name myrepo
```

### No Results Found

**Possible causes:**
1. Query too specific - try broader terms
2. Documentation doesn't contain those terms
3. Index may need to be rebuilt

### Cache Issues

**Clear cache and re-index:**
```bash
rm data/*.zip
python cli.py index --url <url> --name <name>
```

---

## Performance

- **First index**: 5-10 seconds (downloads + indexes)
- **Subsequent searches**: < 1 second (cached)
- **Cache size**: ~2-5MB per repository
- **Memory usage**: ~50-100MB per indexed repository

---

## Advanced Usage

### Custom Cache Directory

```bash
export CACHE_DIR=/path/to/custom/cache
python cli.py index --cache-dir $CACHE_DIR --url <url> --name <name>
python cli.py search --cache-dir $CACHE_DIR --name <name> --query <query>
```

### Batch Indexing

```bash
#!/bin/bash
# index_multiple.sh

repos=(
    "https://github.com/jlowin/fastmcp:fastmcp"
    "https://github.com/alexeygrigorev/minsearch:minsearch"
    "https://github.com/pallets/click:click"
)

for repo in "${repos[@]}"; do
    url="${repo%%:*}"
    name="${repo##*:}"
    python cli.py index --url "$url" --name "$name"
done
```

Run with:
```bash
chmod +x index_multiple.sh
./index_multiple.sh
```

---

## Summary

The Documentation Search CLI provides three main ways to work with documentation:

1. **CLI Commands** - `python cli.py index/search`
2. **Interactive Mode** - `python cli.py interactive`
3. **Direct Python** - Import and use `DocumentationIndexer`

For the homework exercise, the MCP tool `search_fastmcp_docs` provides a ready-to-use interface for searching FastMCP documentation through AI assistants.
