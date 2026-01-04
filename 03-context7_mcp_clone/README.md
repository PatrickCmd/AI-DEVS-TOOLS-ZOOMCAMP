# Context7 MCP Server Clone

A Model Context Protocol (MCP) server that clones Context7's functionality - providing documentation search capabilities through AI assistants.

## Project Overview

This project implements an MCP server that:
- Downloads documentation from GitHub repositories
- Processes and indexes documentation using MinSearch
- Provides search capabilities through MCP tools
- Integrates with AI assistants (Claude Code, VSCode, Cursor)

## Documentation

- **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** - Complete step-by-step implementation guide
- **[Homework Assignment](docs/homework.md)** - Original homework requirements

---

## Progress

### ✅ Question 1: Create a New Project

**Objective**: Set up Python project with uv dependency manager and install FastMCP.

**Steps Completed**:
1. Installed `uv` package manager
2. Initialized project with `uv init`
3. Installed FastMCP dependency with `uv add fastmcp`
4. Verified `uv.lock` file generation

**Answer**:
The first hash in the `wheels` section of `fastmcp` in `uv.lock`:

```
sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca
```

**Verification**:
```bash
# Check uv.lock for fastmcp wheels section
grep -A 30 "name = \"fastmcp\"" uv.lock | grep -A 3 "wheels = \["
```

**Files Created**:
- `pyproject.toml` - Project configuration
- `uv.lock` - Dependency lock file
- `.python-version` - Python version specification (3.12)

---

### ✅ Question 2: FastMCP Transport

**Objective**: Create a basic MCP server and identify the transport protocol.

**Implementation** (`main.py`):
```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

**Running the Server**:
```bash
uv run python main.py
```

**Output** (Welcome Screen):
```
╭─ MCP Server ─────────────────────────────────────────────────╮
│                                                               │
│  Server: Demo 🚀                                              │
│  Status: Running                                              │
│  Transport: STDIO                                             │
│                                                               │
│  Tools: 1                                                     │
│   • add: Add two numbers                                      │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

**Answer**: **STDIO** (Standard Input/Output)

**Explanation**:
- STDIO transport uses standard input/output for communication
- Perfect for local AI assistant integration
- No network configuration required
- Secure and simple for single-user scenarios

**Verification**:
```bash
# Run the server to see the welcome screen
uv run python main.py

# The transport type is displayed in the welcome screen
```

---

### ✅ Question 3: Scrape Web Tool

**Objective**: Implement a web scraping tool using Jina Reader API.

**Steps Completed**:
1. Installed `requests` library with `uv add requests`
2. Implemented `scrape_web` tool with Jina Reader integration
3. Added comprehensive error handling (timeout, network errors, general exceptions)
4. Created `test.py` using FastMCP's in-memory testing
5. Tested with minsearch repository URL

**Implementation** ([main.py:11-40](main.py#L11-L40)):
```python
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
```

**Testing** ([test.py](test.py)):
- Created async test using FastMCP's `Client` for in-memory testing
- Test URL: `https://github.com/alexeygrigorev/minsearch`
- Verified content contains "minsearch"
- Character count validation

**Running the Test**:
```bash
uv run python test.py
```

**Test Results**:
```
✅ Scraping successful!
Character count: 31361
✅ Content verification: 'minsearch' found in content
```

**Answer**: **31,361 characters**

**Key Features**:
- ✅ Jina Reader API integration (`https://r.jina.ai/{url}`)
- ✅ 30-second timeout for requests
- ✅ Proper error handling for network issues
- ✅ Returns markdown-formatted content
- ✅ In-memory testing with FastMCP Client

---

## Current Project Structure

```
03-context7_mcp_clone/
├── main.py                 # MCP server with all tools
├── doc_indexer.py          # Documentation indexer module (reusable)
├── cli.py                  # CLI for flexible doc indexing/search
├── test.py                 # Test script for scrape_web (minsearch)
├── test_datatalks.py       # Test script for word counting (datatalks.club)
├── search.py               # Test script for documentation search
├── SUMMARY.md              # Project summary
├── .gitignore              # Git ignore file
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Dependency lock file
├── .python-version         # Python version (3.12)
├── docs/
│   ├── homework.md         # Homework assignment
│   ├── IMPLEMENTATION_PLAN.md  # Complete implementation guide
│   ├── minsearch-docs.md   # MinSearch library documentation
│   └── CLI_USAGE.md        # CLI usage guide (NEW!)
├── data/                   # Cache directory (auto-created)
│   └── fastmcp-main.zip    # Cached FastMCP repository
└── .venv/                  # Virtual environment (auto-created)
```

---

### ✅ Question 4: MCP Integration

**Objective**: Integrate the MCP server with AI assistants and test the scrape_web tool.

**Steps Completed**:
1. Added MCP server to VSCode workspace configuration
2. Added MCP server to Claude Code CLI
3. Verified MCP server connection
4. Documented testing instructions

**VSCode Configuration** ([.vscode/mcp.json](../.vscode/mcp.json)):
```json
{
  "servers": {
    "context7-clone": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/Users/patrickwalukagga/Projects/personal/ai-dev-tools-zoomcamp/03-context7_mcp_clone",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**Claude Code CLI Configuration**:
```bash
claude mcp add context7-clone -- uv --directory /Users/patrickwalukagga/Projects/personal/ai-dev-tools-zoomcamp/03-context7_mcp_clone run python main.py
```

**Verification**:
```bash
# List MCP servers
claude mcp list

# Output:
# context7-clone: uv --directory /path/to/03-context7_mcp_clone run python main.py - ✓ Connected
```

**Testing Instructions**:

**Test Prompt**:
```
Count how many times the word "data" appears on https://datatalks.club/
Use available MCP tools for that
```

**Expected Behavior**:
1. AI assistant discovers the `scrape_web` tool from the MCP server
2. AI calls `scrape_web(url="https://datatalks.club/")`
3. Tool returns markdown content of the page
4. AI processes the content and counts occurrences of "data"
5. AI reports the count

---

#### Testing with VSCode

1. **Restart VSCode** to reload MCP configuration
2. **Start a new Claude conversation**
3. Use the test prompt above
4. Approve tool usage when prompted

---

#### Testing with Claude Code CLI

**Option 1: Interactive Mode** (Recommended for first-time testing)

Launch Claude Code and paste the prompt:

```bash
claude
```

Then type or paste the test prompt. This allows you to approve the tool when prompted, and the permission will be remembered for future runs.

**Option 2: One-Shot with `-p` Flag**

Run a single prompt and get the output:

```bash
claude -p 'Count how many times the word "data" appears on https://datatalks.club/ Use available MCP tools for that'
```

**Option 3: One-Shot with Auto-Approval**

Skip all permission prompts (use cautiously):

```bash
claude -p --dangerously-skip-permissions 'Count how many times the word "data" appears on https://datatalks.club/ Use available MCP tools for that'
```

**Option 4: Pre-Approve Specific Tools** (Recommended for automation)

Pre-approve only the `scrape_web` tool:

```bash
claude -p --allowedTools 'mcp__context7-clone__scrape_web' 'Count how many times the word "data" appears on https://datatalks.club/ Use available MCP tools for that'
```

**Option 5: Piping from File**

Save the prompt to a file and pipe it:

```bash
echo 'Count how many times the word "data" appears on https://datatalks.club/ Use available MCP tools for that' > prompt.txt
cat prompt.txt | claude -p --dangerously-skip-permissions
```

**Claude Code CLI Useful Flags**:

| Flag | Purpose |
|------|---------|
| `-p, --print` | Run one prompt then exit (non-interactive) |
| `--dangerously-skip-permissions` | Auto-approve all tool usage |
| `--allowedTools` | Pre-approve specific tools |
| `--verbose` | Show more detailed output |
| `--output-format json` | Get structured JSON output |

**Permanent Tool Approval**:

Create or edit `~/.claude/settings.json` to permanently allow the scrape_web tool:

```json
{
  "allowedTools": [
    "mcp__context7-clone__scrape_web"
  ]
}
```

**Test Script**: [test_datatalks.py](test_datatalks.py)

**Running the Test**:
```bash
uv run python test_datatalks.py
```

**Test Results**:
```
✅ Scraping successful!
Total characters: 5679
Occurrences of 'data': 10
✅ Content verification: 'datatalks' found in content
```

**Answer**: **10 occurrences of "data"**

**Key Features**:
- ✅ VSCode workspace integration
- ✅ Claude Code CLI integration
- ✅ STDIO transport verified
- ✅ MCP tools discoverable by AI assistants
- ✅ Ready for end-to-end testing

---

### ✅ Question 5: Documentation Indexing

**Objective**: Download, index, and search FastMCP documentation using MinSearch.

**Steps Completed**:
1. Installed `minsearch` library
2. Created modular `DocumentationIndexer` class
3. Implemented repository download with caching
4. Implemented markdown file extraction
5. Created MinSearch index with 266 documents
6. Tested search functionality

**Implementation** ([doc_indexer.py](doc_indexer.py)):

Created a reusable `DocumentationIndexer` class with the following features:

```python
class DocumentationIndexer:
    """Handle documentation indexing for GitHub repositories."""

    def download_repo(repo_url, cache_filename) -> Path
        # Downloads GitHub repo as ZIP with caching

    def extract_markdown_files(zip_path) -> List[Dict]
        # Extracts .md and .mdx files from ZIP

    def create_search_index(documents) -> Index
        # Creates MinSearch index

    def search(query, top_k=5) -> List[Dict]
        # Searches indexed documents

    def load_and_index(repo_url, cache_filename) -> Index
        # Complete workflow: download + extract + index
```

**Key Features**:
- ✅ Automatic caching (avoids re-downloading)
- ✅ Modular and reusable design
- ✅ Path normalization (removes repo prefix)
- ✅ Full-text search on content
- ✅ Keyword filtering on filenames
- ✅ Proper error handling

**Test Script**: [search.py](search.py)

**Running the Test**:
```bash
uv run python search.py
```

**Test Results**:
```
🔨 Initializing documentation indexer...
⬇ Downloading repository from https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip...
✓ Repository downloaded and cached: data/fastmcp-main.zip
📄 Extracting markdown files from fastmcp-main.zip...
✓ Extracted 266 markdown files
🔍 Creating search index...
✓ Index created with 266 documents

Found 5 result(s) for 'demo':
1. examples/testing_demo/README.md
2. examples/fastmcp_config_demo/README.md
3. examples/atproto_mcp/README.md
4. docs/servers/context.mdx
5. docs/getting-started/welcome.mdx
```

**Answer**: **examples/testing_demo/README.md**

---

### ✅ Question 6: Search Tool Integration

**Objective**: Expose search functionality as an MCP tool for AI assistants.

**Steps Completed**:
1. Implemented `search_fastmcp_docs` MCP tool
2. Added lazy loading for index initialization
3. Integrated with main.py MCP server
4. Tested end-to-end workflow

**Implementation** ([main.py:79-135](main.py#L79-L135)):

```python
@mcp.tool
def search_fastmcp_docs(query: str, top_k: int = 5) -> str:
    """
    Search FastMCP documentation for relevant information.

    Args:
        query: Search query (e.g., "how to create tools", "getting started", "demo")
        top_k: Number of results to return (default: 5, max: 10)

    Returns:
        Formatted search results with filenames and content snippets
    """
    # Get or create indexer (lazy loading)
    indexer = get_or_create_indexer()

    # Perform search
    results = indexer.search(query=query.strip(), top_k=top_k)

    # Format and return results
    # ...
```

**Lazy Loading Strategy**:
```python
def get_or_create_indexer() -> DocumentationIndexer:
    """
    Lazy loading:
    - Index created on first search request
    - Subsequent searches use cached index
    - Improves server startup time
    """
    global _indexer

    if _indexer is None:
        _indexer = DocumentationIndexer(cache_dir="data")
        _indexer.load_and_index(FASTMCP_REPO_URL, FASTMCP_CACHE_FILE)

    return _indexer
```

**Configuration**:
- Repository: `https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip`
- Cache directory: `data/`
- Cache file: `fastmcp-main.zip`
- Indexed documents: 266 markdown files

**Usage Examples**:

Via AI assistant:
```
"Search FastMCP docs for information about tools"
"How do I create a new FastMCP server?"
"Find examples of using demo in FastMCP"
```

Direct test:
```python
# Via MCP Client (in search.py)
result = await client.call_tool(
    "search_fastmcp_docs",
    {"query": "demo", "top_k": 5}
)
```

**Key Features**:
- ✅ Lazy index initialization (fast server startup)
- ✅ Persistent cache across searches
- ✅ Input validation (query, top_k)
- ✅ Formatted output with previews
- ✅ Error handling
- ✅ 266 documents indexed
- ✅ Full MCP integration

**Performance**:
- First search: ~5-10 seconds (downloads + indexes)
- Subsequent searches: < 1 second (uses cached index)
- Cache persists across server restarts

---

## Installation & Setup

### Prerequisites
- Python 3.12+
- uv package manager

### Installation

1. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Clone the repository**:
   ```bash
   cd ai-dev-tools-zoomcamp/03-context7_mcp_clone
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

### Running the Server

```bash
# Run the MCP server
uv run python main.py

# Or with full path for AI assistant integration
uv --directory ~/path/to/03-context7_mcp_clone run python main.py
```

---

## Usage

### Available Tools

The server provides three main tools:

**`add` tool** - Adds two numbers (testing/demo tool)
```python
# AI assistant can call this tool
add(a=5, b=3)  # Returns: 8
```

**`scrape_web` tool** - Downloads web page content as markdown
```python
# AI assistant can call this tool
scrape_web(url="https://github.com/alexeygrigorev/minsearch")
# Returns: Markdown content of the page
```

**`search_fastmcp_docs` tool** - Searches FastMCP documentation
```python
# AI assistant can call this tool
search_fastmcp_docs(query="how to create tools", top_k=5)
# Returns: Formatted search results with filenames and content previews
```

### Flexible Documentation Search (NEW!)

For searching ANY repository or website, use the new CLI tool:

**Command-Line Interface:**
```bash
# Index any GitHub repository
uv run python cli.py index --url https://github.com/user/repo --name myrepo

# Search indexed documentation
uv run python cli.py search --name myrepo --query "your question"

# Interactive mode
uv run python cli.py interactive
```

**Direct Python Usage:**
```python
from doc_indexer import DocumentationIndexer

# Create indexer
indexer = DocumentationIndexer(cache_dir="data")

# Index any repository
indexer.load_and_index(
    repo_url="https://github.com/user/repo/archive/refs/heads/main.zip",
    cache_filename="repo-main.zip"
)

# Search
results = indexer.search("your query", top_k=5)
for doc in results:
    print(f"{doc['filename']}: {doc['content'][:100]}...")
```

See **[CLI Usage Guide](docs/CLI_USAGE.md)** for complete documentation.

### Integrating with AI Assistant

To use this MCP server with your AI assistant, add the following configuration:

**For Claude Code CLI**:
```bash
# Add the MCP server
claude mcp add context7-clone -- uv --directory ~/path/to/03-context7_mcp_clone run python main.py
```

**For VSCode** (in settings.json):
```json
{
  "mcp": {
    "servers": {
      "context7-clone": {
        "type": "stdio",
        "command": "uv",
        "args": [
          "--directory",
          "/absolute/path/to/03-context7_mcp_clone",
          "run",
          "python",
          "main.py"
        ]
      }
    }
  }
}
```

---

## Development

### Project Dependencies

**Core**:
- `fastmcp` - MCP server framework
- `requests` - HTTP client for web scraping
- `minsearch` - Document search engine (with scikit-learn, pandas, numpy)
- `click` - Command-line interface creation toolkit

### Running Tests

```bash
# Test web scraping tool (Question 3)
uv run python test.py

# Test word counting (Question 4)
uv run python test_datatalks.py

# Test documentation search (Questions 5 & 6)
uv run python search.py
```

---

## Technical Details

### MCP Protocol
- **Transport**: STDIO (Standard Input/Output)
- **Communication**: JSON-RPC based messages
- **Tools**: Discoverable functions exposed to AI assistants
- **Security**: Local execution, no network exposure

### FastMCP Features
- Simple decorator-based tool creation
- Automatic schema generation
- Built-in validation
- Error handling
- Type hints support

---

## Homework Answers Summary

| Question | Answer | Status |
|----------|--------|--------|
| Q1: First hash in fastmcp wheels | `sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca` | ✅ Complete |
| Q2: Transport protocol | STDIO | ✅ Complete |
| Q3: Character count for minsearch | **31,361 characters** | ✅ Complete |
| Q4: "data" word count | **10 occurrences** | ✅ Complete |
| Q5: First file for "demo" query | **examples/testing_demo/README.md** | ✅ Complete |
| Q6: Search tool integration | **Implemented and tested** | ✅ Complete |

---

## Resources

- [FastMCP Repository](https://github.com/jlowin/fastmcp)
- [MinSearch Repository](https://github.com/alexeygrigorev/minsearch)
- [Jina Reader API](https://jina.ai/reader)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [UV Package Manager](https://github.com/astral-sh/uv)

---

## License

This project is part of the AI Dev Tools Zoomcamp coursework.

---

**Created**: January 2026
**Last Updated**: January 2026
