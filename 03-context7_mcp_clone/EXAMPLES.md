# Context7 MCP Clone - Usage Examples

## Quick Reference

### Using `search_fastmcp_docs` (MCP Tool - Homework Exercise)

This is the pre-configured tool for searching FastMCP documentation.

**Configuration (in main.py):**
```python
FASTMCP_REPO_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
FASTMCP_CACHE_FILE = "fastmcp-main.zip"
```

**Test with Python:**
```bash
# Run the homework test script
uv run python search.py
```

**Expected Output:**
```
Found 5 result(s) for 'demo':
1. examples/testing_demo/README.md
2. examples/fastmcp_config_demo/README.md
3. examples/atproto_mcp/README.md
4. docs/servers/context.mdx
5. docs/getting-started/welcome.mdx

📊 Answer to Question 5: examples/testing_demo/README.md
```

---

## Using the Flexible CLI

### Example 1: Index and Search FastMCP (Homework)

```bash
# Search FastMCP docs (uses existing cache)
uv run python cli.py search --name fastmcp --query "demo"

# Output:
# 🔎 Searching: fastmcp
# Query: "demo"
# ------------------------------------------------------------
# Found 5 result(s):
# 1. examples/testing_demo/README.md
#    # FastMCP Testing Demo  A comprehensive example demonstrating FastMCP testing patterns...
```

### Example 2: Index a New Repository

```bash
# Index MinSearch documentation
uv run python cli.py index \
  --url https://github.com/alexeygrigorev/minsearch \
  --name minsearch

# Output:
# 🔍 Indexing: minsearch
# URL: https://github.com/alexeygrigorev/minsearch
# ------------------------------------------------------------
# Archive URL: https://github.com/alexeygrigorev/minsearch/archive/refs/heads/main.zip
# Cache file: minsearch-main.zip
#
# Indexing  [####################################]  100%
#
# ✓ Indexing complete!
# Documents indexed: 42
# Total characters: 567,890
```

### Example 3: Search Multiple Repositories

```bash
# Search FastMCP
uv run python cli.py search --name fastmcp --query "tool decorator"

# Search MinSearch
uv run python cli.py search --name minsearch --query "vector search"

# Search Click
uv run python cli.py search --name click --query "options and arguments"
```

### Example 4: Interactive Mode

```bash
# Start interactive session
uv run python cli.py interactive

# Interactive menu:
# ============================================================
#   Documentation Search CLI - Interactive Mode
# ============================================================
#
# What would you like to do?
# 1. Index a new repository
# 2. Search existing index
# 3. Exit
# Your choice [1]: 2
#
# Index name to search: fastmcp
#
# Search 'fastmcp' (or 'quit' to go back) [demo]: how to create tools
#
# Found 5 result(s):
# 1. docs/servers/tools.mdx
#    Tools sidebarTitle: Tools description: Expose functions as executable capabilities...
```

---

## Direct Python Usage

### Example 5: Simple Documentation Search

```python
from doc_indexer import DocumentationIndexer

# Create indexer
indexer = DocumentationIndexer(cache_dir="data")

# Index FastMCP
indexer.load_and_index(
    repo_url="https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip",
    cache_filename="fastmcp-main.zip"
)

# Search
results = indexer.search("demo", top_k=3)

# Display
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc['filename']}")
    print(f"   Preview: {doc['content'][:100]}...")
    print()

# Output:
# 1. examples/testing_demo/README.md
#    Preview: # FastMCP Testing Demo  A comprehensive example demonstrating FastMCP testing patterns with...
```

### Example 6: Index Multiple Repositories

```python
from doc_indexer import DocumentationIndexer

repositories = [
    ("https://github.com/jlowin/fastmcp", "fastmcp"),
    ("https://github.com/alexeygrigorev/minsearch", "minsearch"),
    ("https://github.com/pallets/click", "click"),
]

indexes = {}

for url, name in repositories:
    print(f"Indexing {name}...")

    indexer = DocumentationIndexer(cache_dir="data")
    archive_url = f"{url}/archive/refs/heads/main.zip"
    cache_file = f"{name}-main.zip"

    indexer.load_and_index(archive_url, cache_file)
    indexes[name] = indexer

    stats = indexer.get_stats()
    print(f"  ✓ {stats['num_documents']} documents indexed\n")

# Search across all repositories
query = "getting started"
print(f"Searching for '{query}' across all repositories:\n")

for name, indexer in indexes.items():
    results = indexer.search(query, top_k=1)
    if results:
        print(f"{name}: {results[0]['filename']}")
```

### Example 7: Custom Search with Filters

```python
from doc_indexer import DocumentationIndexer

indexer = DocumentationIndexer(cache_dir="data")

# Load FastMCP
indexer.load_and_index(
    "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip",
    "fastmcp-main.zip"
)

# Search with custom parameters
results = indexer.search(
    query="tool decorator",
    top_k=5
)

# Filter results by filename pattern
filtered = [r for r in results if 'docs/' in r['filename']]

print(f"Found {len(filtered)} documentation files:")
for doc in filtered:
    print(f"  - {doc['filename']}")
```

---

## Homework-Specific Examples

### Question 5: Find First File for "demo" Query

**Using search.py:**
```bash
uv run python search.py
```

**Using CLI:**
```bash
uv run python cli.py search --name fastmcp --query "demo" --top-k 1
```

**Using Python:**
```python
from doc_indexer import DocumentationIndexer

indexer = DocumentationIndexer(cache_dir="data")
indexer.load_and_index(
    "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip",
    "fastmcp-main.zip"
)

results = indexer.search("demo", top_k=1)
print(f"Answer: {results[0]['filename']}")
# Output: Answer: examples/testing_demo/README.md
```

### Question 6: MCP Tool Integration

**Via MCP Client:**
```python
import asyncio
from fastmcp import Client
from main import mcp

async def test():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "search_fastmcp_docs",
            {"query": "demo", "top_k": 5}
        )
        print(result.content[0].text)

asyncio.run(test())
```

**Direct Function Call (for testing):**
```python
from main import get_or_create_indexer

# Get indexer (lazy loading)
indexer = get_or_create_indexer()

# Search directly
results = indexer.search("demo", top_k=5)

for i, doc in enumerate(results, 1):
    print(f"{i}. {doc['filename']}")
```

---

## Batch Operations

### Batch Index Multiple Repositories

Create `batch_index.sh`:
```bash
#!/bin/bash

repos=(
    "https://github.com/jlowin/fastmcp:fastmcp"
    "https://github.com/alexeygrigorev/minsearch:minsearch"
    "https://github.com/pallets/click:click"
)

for repo in "${repos[@]}"; do
    url="${repo%%:*}"
    name="${repo##*:}"

    echo "Indexing $name..."
    uv run python cli.py index --url "$url" --name "$name"
    echo "---"
done

echo "All repositories indexed!"
```

Run:
```bash
chmod +x batch_index.sh
./batch_index.sh
```

### Batch Search Across Repositories

Create `batch_search.py`:
```python
from doc_indexer import DocumentationIndexer
from pathlib import Path

# Find all cached repositories
cache_dir = Path("data")
cache_files = list(cache_dir.glob("*-main.zip"))

query = "getting started"
print(f"Searching for '{query}' across {len(cache_files)} repositories:\n")

for cache_file in cache_files:
    name = cache_file.stem.replace("-main", "")

    indexer = DocumentationIndexer(cache_dir="data")
    docs = indexer.extract_markdown_files(cache_file)
    indexer._documents = docs
    indexer._index = indexer.create_search_index(docs)

    results = indexer.search(query, top_k=1)

    if results:
        print(f"{name:20s}: {results[0]['filename']}")
```

Run:
```bash
uv run python batch_search.py
```

---

## Summary

Three ways to use the system:

1. **MCP Tool** (`search_fastmcp_docs`) - For AI assistants, pre-configured for FastMCP
2. **CLI** (`cli.py`) - For command-line usage, flexible for any repository
3. **Python API** (`doc_indexer.py`) - For programmatic access, full control

Choose based on your use case:
- Homework exercise → Use `search.py` or MCP tool
- Index new repos → Use `cli.py index`
- Build custom tool → Import `DocumentationIndexer`
