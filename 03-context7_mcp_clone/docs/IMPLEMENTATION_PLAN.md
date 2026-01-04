# Context7 MCP Clone - Implementation Plan

**Project Goal**: Build a Model Context Protocol (MCP) server that clones Context7's functionality - providing documentation search capabilities through an AI assistant.

**Target Repository**: [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

## Overview

We will build an MCP server that:
1. Downloads documentation from GitHub repositories
2. Processes and indexes the documentation using MinSearch
3. Provides search capabilities through MCP tools
4. Integrates seamlessly with AI assistants (Claude Code, VSCode, etc.)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Assistant (Client)                     │
│              (Claude Code / VSCode / Cursor)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ MCP Protocol (STDIO)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   MCP Server (main.py)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Web Scraper │  │   Document   │  │  Search Engine  │   │
│  │     Tool     │  │   Indexer    │  │   (MinSearch)   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                        │
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              Local Storage / Cache                           │
│  ┌────────────────────┐  ┌──────────────────────────────┐   │
│  │  fastmcp-main.zip  │  │  MinSearch Index (in-memory) │   │
│  │  (Documentation)   │  │  (content + filenames)       │   │
│  └────────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### ✅ Phase 1: Project Setup (Questions 1-2)

**Status**: COMPLETED

#### Step 1.1: Project Initialization
- **Goal**: Set up Python project with uv dependency manager
- **Tools**: uv (Python package manager)
- **Actions**:
  - Initialize empty project with `uv init`
  - Install FastMCP dependency
  - Verify uv.lock file generation
- **Deliverable**: Working Python project with FastMCP installed
- **Homework Question 1**: Extract first hash from uv.lock wheels section

#### Step 1.2: Basic MCP Server
- **Goal**: Create minimal working MCP server
- **Tools**: FastMCP framework
- **Actions**:
  - Create main.py with basic FastMCP server
  - Implement simple `add` tool for testing
  - Run server and verify STDIO transport
- **Deliverable**: Functional MCP server with one test tool
- **Homework Question 2**: Identify transport protocol (STDIO)

---

### 🔨 Phase 2: Web Scraping Tool (Question 3)

#### Step 2.1: Jina Reader Integration
- **Goal**: Create tool to download and convert web pages to markdown
- **API**: Jina Reader API (`https://r.jina.ai/{url}`)
- **Libraries**:
  - `requests` for HTTP calls
  - `fastmcp` for tool decoration

**Implementation Requirements**:
```python
@mcp.tool()
def scrape_web(url: str) -> str:
    """
    Download web page content as markdown using Jina Reader.

    Args:
        url: The URL to scrape

    Returns:
        Markdown content of the page
    """
    # Prepend Jina reader URL
    # Make HTTP request
    # Return markdown content
```

**Testing**:
- Create `test.py` to verify functionality
- Test URL: `https://github.com/alexeygrigorev/minsearch`
- Verify character count in response
- **Homework Question 3**: Count characters returned (~19184)

**Error Handling**:
- Handle network errors
- Handle invalid URLs
- Handle API failures

---

### 🔌 Phase 3: MCP Integration (Question 4)

#### Step 3.1: Configure AI Assistant
- **Goal**: Integrate MCP server with AI assistant
- **AI Assistants**: Claude Code / VSCode / Cursor
- **Configuration**:
  - Add MCP server to assistant configuration
  - Use full path to project directory
  - Test tool invocation from assistant

**MCP Server Command**:
```bash
uv --directory ~/path/to/homework run python main.py
```

**Platform-Specific Paths**:
- **macOS/Linux**: `~/path/to/homework`
- **Windows**: `C:/Users/username/path/to/homework`

#### Step 3.2: Integration Testing
- **Test Prompt**: "Count how many times the word 'data' appears on https://datatalks.club/ Use available MCP tools for that"
- **Expected Behavior**:
  1. AI calls scrape_web tool
  2. Tool returns markdown content
  3. AI processes content and counts "data" occurrences
- **Homework Question 4**: Word count result (~111)

**Verification Checklist**:
- [ ] MCP server starts correctly
- [ ] AI assistant can discover tools
- [ ] scrape_web tool executes successfully
- [ ] AI can process tool results
- [ ] Error messages are clear and helpful

---

### 📚 Phase 4: Documentation Indexing (Question 5)

#### Step 4.1: Download GitHub Repository
- **Goal**: Download and cache FastMCP documentation
- **Source**: https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip
- **Implementation**:

```python
def download_repo(repo_url: str, cache_path: str) -> str:
    """
    Download GitHub repo as ZIP if not already cached.

    Args:
        repo_url: GitHub archive URL
        cache_path: Local path to save ZIP

    Returns:
        Path to downloaded/cached ZIP file
    """
    # Check if already downloaded
    # If not, download using requests
    # Save to cache_path
    # Return path
```

**Caching Strategy**:
- Check if file exists before downloading
- Avoid unnecessary downloads
- Store in project directory or temp folder

#### Step 4.2: Extract and Process Markdown Files
- **Goal**: Extract only markdown documentation files
- **File Types**: `.md` and `.mdx` files
- **Processing**:

```python
def extract_markdown_files(zip_path: str) -> List[Dict[str, str]]:
    """
    Extract markdown files from ZIP archive.

    Args:
        zip_path: Path to ZIP file

    Returns:
        List of dicts with 'filename' and 'content' keys
    """
    documents = []

    # Open ZIP file
    # Iterate through all files
    # Filter for .md and .mdx files
    # Remove path prefix (e.g., "fastmcp-main/")
    # Read file content
    # Append to documents list

    return documents
```

**Path Transformation**:
- Original: `fastmcp-main/docs/getting-started/welcome.mdx`
- Processed: `docs/getting-started/welcome.mdx`

**Data Structure**:
```python
{
    "filename": "docs/getting-started/welcome.mdx",
    "content": "# Welcome to FastMCP\n\n..."
}
```

#### Step 4.3: MinSearch Integration
- **Goal**: Index documents with MinSearch for fast searching
- **Library**: https://github.com/alexeygrigorev/minsearch
- **Installation**: `uv add minsearch` (or include in requirements)

**Index Setup**:
```python
from minsearch import Index

def create_search_index(documents: List[Dict]) -> Index:
    """
    Create MinSearch index from documents.

    Args:
        documents: List of dicts with 'filename' and 'content'

    Returns:
        Configured MinSearch index
    """
    # Initialize Index with text_fields and keyword_fields
    # Fit index with documents
    # Return index
```

**Index Configuration**:
- **text_fields**: `["content"]` - for full-text search
- **keyword_fields**: `["filename"]` - for exact filename matching

#### Step 4.4: Search Function Implementation
- **Goal**: Query indexed documents and return top results
- **Implementation**:

```python
def search_docs(query: str, top_k: int = 5) -> List[Dict]:
    """
    Search documentation using MinSearch.

    Args:
        query: Search query string
        top_k: Number of results to return (default: 5)

    Returns:
        List of most relevant documents with scores
    """
    # Use index.search() method
    # Return top K results
    # Include filename and content snippet
```

**Search Parameters**:
- Default: Return 5 most relevant documents
- Ranking: Based on MinSearch's BM25 algorithm
- Result format: Include filename, content preview, relevance score

#### Step 4.5: Testing Search Implementation
- **Create**: `search.py` test file
- **Test Query**: "demo"
- **Verification**:
  - Check first result filename
  - Verify search ranking
  - Test multiple queries
- **Homework Question 5**: First file returned for "demo" query

**Expected Result Options**:
- README.md
- docs/servers/context.mdx
- examples/testing_demo/README.md
- docs/python-sdk/fastmcp-settings.mdx

**Test Cases**:
```python
# test_search.py
test_queries = [
    ("demo", 5),           # Basic query
    ("getting started", 3), # Multi-word query
    ("installation", 5),    # Common topic
    ("tool decorator", 5),  # Technical term
]

for query, top_k in test_queries:
    results = search_docs(query, top_k)
    print(f"Query: {query}")
    print(f"Top result: {results[0]['filename']}")
    print("---")
```

---

### 🔧 Phase 5: Search Tool Integration (Question 6)

#### Step 5.1: Implement Search as MCP Tool
- **Goal**: Expose search functionality through MCP protocol
- **Implementation**:

```python
@mcp.tool()
def search_fastmcp_docs(query: str, top_k: int = 5) -> str:
    """
    Search FastMCP documentation for relevant information.

    Args:
        query: Search query (e.g., "how to create tools")
        top_k: Number of results to return (default: 5)

    Returns:
        Formatted search results with filenames and content
    """
    # Call search_docs function
    # Format results for display
    # Return formatted string
```

**Result Formatting**:
```python
# Example output format
"""
Found 5 results for "demo":

1. examples/testing_demo/README.md
   Content: This example demonstrates how to create...

2. docs/getting-started/welcome.mdx
   Content: FastMCP makes it easy to build...

...
"""
```

#### Step 5.2: Index Initialization Strategy
- **When to Build Index**:
  - Option 1: On server startup (slow start, fast queries)
  - Option 2: Lazy loading on first search (fast start, slow first query)
  - Option 3: Background initialization

**Recommended Approach** (Lazy Loading):
```python
_search_index = None  # Global cache

def get_or_create_index() -> Index:
    """Get existing index or create new one."""
    global _search_index

    if _search_index is None:
        print("Building search index...")
        zip_path = download_repo(FASTMCP_REPO_URL, "fastmcp-main.zip")
        documents = extract_markdown_files(zip_path)
        _search_index = create_search_index(documents)
        print(f"Indexed {len(documents)} documents")

    return _search_index
```

#### Step 5.3: End-to-End Testing
- **Test with AI Assistant**:
  - Restart MCP server
  - Ask: "Search FastMCP docs for information about tools"
  - Ask: "How do I create a new FastMCP server?"
  - Ask: "Find examples of using context in FastMCP"

**Success Criteria**:
- [ ] AI can invoke search tool
- [ ] Search returns relevant results
- [ ] AI can interpret and use search results
- [ ] Response time is acceptable (<5 seconds)
- [ ] Error handling works correctly

---

## Project Structure

```
03-context7_mcp_clone/
├── main.py                 # MCP server with all tools
├── search.py               # Search testing script
├── test.py                 # Web scraping test
├── pyproject.toml          # Project dependencies
├── uv.lock                 # Dependency lock file
├── .python-version         # Python version specification
├── docs/
│   ├── homework.md         # Homework assignment
│   └── IMPLEMENTATION_PLAN.md  # This file
├── data/                   # Created automatically
│   └── fastmcp-main.zip    # Cached repository
└── .venv/                  # Virtual environment
```

---

## Dependencies

### Core Dependencies
```toml
[project]
dependencies = [
    "fastmcp",      # MCP server framework
    "requests",     # HTTP client for web scraping
    "minsearch",    # Document search engine
]
```

### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest",       # Testing framework
    "ipython",      # Interactive shell
]
```

---

## Implementation Checklist

### Phase 1: Setup ✅
- [x] Initialize project with uv
- [x] Install FastMCP
- [x] Create basic MCP server
- [x] Verify STDIO transport

### Phase 2: Web Scraping 🔨
- [ ] Implement scrape_web tool
- [ ] Add Jina Reader integration
- [ ] Create test.py
- [ ] Test with minsearch repo URL
- [ ] Verify character count

### Phase 3: MCP Integration 🔌
- [ ] Configure AI assistant
- [ ] Test tool discovery
- [ ] Verify tool execution
- [ ] Test word counting use case

### Phase 4: Documentation Indexing 📚
- [ ] Implement repo download function
- [ ] Create ZIP extraction logic
- [ ] Add path transformation
- [ ] Install MinSearch
- [ ] Create search index
- [ ] Implement search function
- [ ] Create search.py test file
- [ ] Test "demo" query

### Phase 5: Search Tool 🔧
- [ ] Create search MCP tool
- [ ] Implement lazy index loading
- [ ] Format search results
- [ ] Test with AI assistant
- [ ] Verify end-to-end workflow

---

## Testing Strategy

### Unit Tests
```python
# Test web scraping
def test_scrape_web():
    content = scrape_web("https://github.com/alexeygrigorev/minsearch")
    assert len(content) > 10000
    assert "minsearch" in content.lower()

# Test document extraction
def test_extract_markdown_files():
    docs = extract_markdown_files("fastmcp-main.zip")
    assert len(docs) > 0
    assert all("filename" in doc and "content" in doc for doc in docs)

# Test search
def test_search_docs():
    results = search_docs("demo", top_k=5)
    assert len(results) <= 5
    assert "filename" in results[0]
```

### Integration Tests
```python
# Test full workflow
def test_full_workflow():
    # 1. Download repo
    zip_path = download_repo(REPO_URL, "test.zip")

    # 2. Extract docs
    docs = extract_markdown_files(zip_path)

    # 3. Create index
    index = create_search_index(docs)

    # 4. Search
    results = index.search("demo", top_k=5)

    assert len(results) > 0
```

### Manual Tests
- Test with AI assistant
- Verify all MCP tools are discoverable
- Test error scenarios (network failures, invalid URLs)
- Test with different queries

---

## Error Handling

### Network Errors
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    return f"Error downloading: {str(e)}"
```

### File Processing Errors
```python
try:
    with zipfile.ZipFile(zip_path) as zf:
        # Process files
        pass
except zipfile.BadZipFile:
    return "Error: Invalid ZIP file"
```

### Search Errors
```python
if not query or not query.strip():
    return "Error: Query cannot be empty"

if top_k < 1:
    return "Error: top_k must be at least 1"
```

---

## Performance Considerations

### Caching
- Download repo once and cache locally
- Build search index once per session
- Use global variable for index persistence

### Optimization
- Load index lazily (on first search)
- Limit search results (default: 5)
- Use MinSearch for efficient retrieval

### Resource Management
- Clean up temporary files
- Limit memory usage for large repos
- Stream large file downloads

---

## Future Enhancements

### Multi-Repository Support
- Index multiple repositories
- Switch between documentation sources
- Aggregate search results

### Advanced Search Features
- Filter by file type
- Search in code vs documentation
- Semantic search with embeddings

### Caching Improvements
- Persistent index storage (pickle/json)
- Update index incrementally
- Configurable cache expiration

### Better Results
- Include code snippets
- Highlight matched terms
- Provide context around matches

---

## Homework Submission

### Deliverables
1. **Code**: Complete implementation in GitHub repository
2. **Structure**: Code in `03-mcp/` folder
3. **Documentation**: This implementation plan
4. **Tests**: Working test files (test.py, search.py)

### GitHub Repository Structure
```
ai-dev-tools-zoomcamp/
├── 03-mcp/
│   ├── context7_mcp_clone/
│   │   ├── main.py
│   │   ├── search.py
│   │   ├── test.py
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   └── docs/
│   │       ├── homework.md
│   │       └── IMPLEMENTATION_PLAN.md
│   └── mcp-ai-dev-workflow/  # Previous work
└── README.md
```

### Submission Checklist
- [ ] All code committed to GitHub
- [ ] Code in correct folder structure
- [ ] Implementation plan documented
- [ ] Tests pass successfully
- [ ] README updated with usage instructions
- [ ] Homework answers documented

---

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MinSearch Repository](https://github.com/alexeygrigorev/minsearch)
- [Jina Reader API](https://jina.ai/reader)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [UV Package Manager](https://github.com/astral-sh/uv)

---

**Created**: January 2026
**Last Updated**: January 2026
