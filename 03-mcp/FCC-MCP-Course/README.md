# Model Context Protocol (MCP) - Fundamentals and Concepts

## Table of Contents
- [What is MCP?](#what-is-mcp)
- [MCP Transport Modes](#mcp-transport-modes)
- [Components of MCP](#components-of-mcp)
- [MCP Integrations and Clients](#mcp-integrations-and-clients)
- [OpenAI MCP Tool Usage](#openai-mcp-tool-usage)
- [Project Examples](#project-examples)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how AI applications connect to external data sources and tools. It provides a universal, open standard for connecting AI systems with data sources, replacing fragmented integrations with a single protocol.

### Key Benefits

- **Universal Integration**: One protocol to connect AI applications to any data source or tool
- **Standardized Communication**: Consistent interface between AI models and external systems
- **Simplified Development**: Build once, use everywhere - no need for custom integrations
- **Open Standard**: Free, open-source protocol developed by Anthropic

### Architecture

MCP follows a **client-server architecture**:

```
┌─────────────────┐         ┌──────────────────┐
│   MCP Client    │ ◄─────► │   MCP Server     │
│  (AI Application)│         │  (Tool Provider) │
└─────────────────┘         └──────────────────┘
```

- **MCP Client**: AI applications (Claude Desktop, IDEs, custom agents) that need access to tools/data
- **MCP Server**: Services that expose tools, resources, and prompts to clients
- **Communication**: Clients discover and invoke server capabilities via standardized protocol

---

## MCP Transport Modes

MCP supports three primary transport modes for client-server communication:

### 1. STDIO Transport (Subprocess-Based)

**Use Case**: Local development, desktop applications, subprocess communication

**How It Works**:
- Server runs as a subprocess
- Communication via standard input/output streams
- Client manages server lifecycle (start/stop)

**Example - FastMCP STDIO Server**:
```python
from fastmcp import FastMCP

mcp = FastMCP("My Local Server")

@mcp.tool()
def calculate(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    # Run with STDIO transport (default)
    mcp.run()
```

**Client Configuration** (Claude Desktop):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

### 2. HTTP/SSE Transport (Web Deployment)

**Use Case**: Production deployments, cloud services, web integrations, OpenAI Responses API

**How It Works**:
- Server runs as HTTP web service
- Client connects via HTTP endpoints
- Supports Server-Sent Events (SSE) for real-time updates
- Requires publicly accessible URL

**Example - FastMCP HTTP Server**:
```python
from fastmcp import FastMCP

mcp = FastMCP("My Web Server")

@mcp.tool()
def search_articles(query: str, max_results: int = 5):
    """Search for articles."""
    # Implementation here
    return results

if __name__ == "__main__":
    # Run with HTTP transport on port 8000
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

**Client Connection** (OpenAI Python SDK):
```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    tools=[{
        "type": "mcp",
        "server_label": "my-server",
        "server_url": "https://my-server.example.com/mcp",
        "require_approval": "never"
    }],
    input="Search for React articles"
)
```

### 3. Custom Transports

MCP's architecture allows for custom transport implementations for specialized use cases.

**Comparison Table**:

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **STDIO** | Local, Desktop | Simple, Secure (local only) | Not web-accessible |
| **HTTP/SSE** | Production, Cloud | Scalable, Remote access | Requires hosting, Security config |
| **Custom** | Specialized | Flexible | More complex implementation |

---

## Components of MCP

MCP servers expose three types of capabilities:

### 1. Tools (Callable Functions)

**Purpose**: Enable AI models to perform actions and execute operations

**Characteristics**:
- Invoked by AI models to accomplish tasks
- Accept parameters and return results
- Can have side effects (write files, call APIs, etc.)
- Require explicit descriptions for AI understanding

**Example - FastMCP Tool**:
```python
from fastmcp import FastMCP

mcp = FastMCP("Content Server")

@mcp.tool()
def fcc_news_search(
    query: str,
    max_results: int = 3,
    include_content: bool = False,
    match_all_terms: bool = False
):
    """
    Search FreeCodeCamp's news feed via RSS.

    Supports multi-term queries: "react hooks javascript" finds articles
    with ANY or ALL terms.

    Args:
        query: Search term(s), can be multiple terms separated by spaces
        max_results: Maximum results to return
        include_content: Include full article content in markdown
        match_all_terms: If True, ALL terms must match; if False, ANY term matches

    Returns:
        list: Matching articles with metadata
    """
    import feedparser

    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    results = []

    # Split query into terms for multi-term search
    search_terms = [term.strip().lower() for term in query.split() if term.strip()]

    for entry in feed.entries:
        title = entry.get("title", "")
        description = entry.get("description", "")

        # Search across multiple fields
        searchable_text = f"{title} {description}".lower()

        # Multi-term matching
        if match_all_terms:
            is_match = all(term in searchable_text for term in search_terms)
        else:
            is_match = any(term in searchable_text for term in search_terms)

        if is_match:
            results.append({
                "title": title,
                "url": entry.get("link", ""),
                "description": description
            })

        if len(results) >= max_results:
            break

    return results
```

### 2. Resources (Data Sources)

**Purpose**: Expose data and content to AI models

**Characteristics**:
- Read-only data access (no side effects)
- Can be files, API responses, database queries, etc.
- Identified by URIs (e.g., `file:///path/to/file`, `db://table/id`)
- Support templates and dynamic content

**Example - FastMCP Resource**:
```python
@mcp.resource("config://settings")
def get_settings():
    """Application configuration settings."""
    return {
        "api_version": "v1",
        "max_results": 10,
        "supported_formats": ["json", "markdown", "xml"]
    }

@mcp.resource("file://docs/{filename}")
def get_documentation(filename: str):
    """Get documentation file by name."""
    with open(f"docs/{filename}", "r") as f:
        return f.read()
```

**Usage**: AI models can request resources by URI:
```
AI: "What are the application settings?"
→ Client requests: config://settings

AI: "Show me the installation docs"
→ Client requests: file://docs/installation.md
```

### 3. Prompts (Templates)

**Purpose**: Pre-defined prompt templates for common workflows

**Characteristics**:
- Reusable prompt structures
- Support arguments/parameters
- Help maintain consistency across interactions
- Can include context from resources

**Example - FastMCP Prompt**:
```python
@mcp.prompt()
def code_review_prompt(language: str, code: str):
    """Generate a code review prompt."""
    return f"""Please review this {language} code:

```

```{language}
code
```

Focus on:
- Code quality and best practices
- Potential bugs or security issues
- Performance optimizations
- Readability and maintainability

```python
@mcp.prompt()
def debug_helper_prompt(error_message: str, stack_trace: str):
    """Generate a debugging assistance prompt."""
    return f"""I'm encountering this error:

Error: {error_message}

Stack trace:
{stack_trace}
```


Please help me:
1. Identify the root cause
2. Suggest fixes
3. Explain how to prevent this in the future


**Component Summary**:

| Component | Purpose | Access Pattern | Side Effects |
|-----------|---------|----------------|--------------|
| **Tools** | Execute operations | Function call | Yes (can modify state) |
| **Resources** | Provide data | URI-based read | No (read-only) |
| **Prompts** | Template workflows | Name + arguments | No (just templates) |

---

## MCP Integrations and Clients

### FastMCP Python SDK

**FastMCP** is the official Python framework for building MCP servers with minimal boilerplate.

#### Installation

```bash
pip install fastmcp
```

#### Quick Start - Complete Server

```python
from fastmcp import FastMCP
import feedparser
from markdownify import markdownify as md

# Create MCP server
mcp = FastMCP(name="FreeCodeCamp Content Explorer")

# Define a tool
@mcp.tool()
def search_articles(query: str, max_results: int = 3):
    """Search FreeCodeCamp articles."""
    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    results = []

    for entry in feed.entries:
        if query.lower() in entry.title.lower():
            results.append({
                "title": entry.title,
                "url": entry.link
            })
            if len(results) >= max_results:
                break

    return results

# Define a resource
@mcp.resource("stats://feed")
def get_feed_stats():
    """Get RSS feed statistics."""
    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    return {
        "total_entries": len(feed.entries),
        "feed_title": feed.feed.get("title", ""),
        "last_updated": feed.feed.get("updated", "")
    }

# Define a prompt
@mcp.prompt()
def article_summary_prompt(article_url: str):
    """Generate prompt to summarize an article."""
    return f"""Please read and summarize this article: {article_url}

Provide:
- Key points (3-5 bullets)
- Main takeaways
- Target audience
- Estimated reading time
"""

# Run the server
if __name__ == "__main__":
    # For local development (STDIO)
    mcp.run()

    # For web deployment (HTTP)
    # mcp.run(transport="http", host="0.0.0.0", port=8000)
```

#### FastMCP Cloud Deployment

FastMCP provides a cloud hosting platform for easy deployment:

```bash
# Install CLI
pip install fastmcp

# Deploy server
fastmcp deploy feed_server.py

# Output: https://your-server.fastmcp.app/mcp
```

**Benefits of FastMCP Cloud**:
- ✅ Automatic HTTPS and public URL
- ✅ No infrastructure management
- ✅ Compatible with OpenAI Responses API
- ✅ Built-in monitoring and logs
- ✅ Free tier available

### FastAPI MCP Integration

For existing FastAPI applications, you can integrate MCP capabilities:

```python
from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("My API Server")

# Regular FastAPI endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# MCP tool integrated with FastAPI
@mcp.tool()
def api_search(query: str):
    """Search via API."""
    # Can access FastAPI dependencies, database, etc.
    return {"results": []}

# Mount MCP on FastAPI
@app.post("/mcp")
async def mcp_endpoint(request: dict):
    # Handle MCP protocol messages
    return await mcp.handle_request(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Other MCP Client Libraries

**Official Clients**:
- **Python**: `mcp` package - Low-level MCP client
- **TypeScript/JavaScript**: `@modelcontextprotocol/sdk`
- **Java**: MCP Java SDK (community)

**Client Example** (Python):
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to MCP server
server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")

        # Call a tool
        result = await session.call_tool("search_articles", {
            "query": "python",
            "max_results": 5
        })
        print(result)
```

---

## OpenAI MCP Tool Usage

OpenAI's **Responses API** natively supports MCP servers through the `type: "mcp"` tool configuration.

### Prerequisites

1. **MCP Server**: Must be publicly accessible (HTTP/HTTPS)
   - ❌ Localhost URLs won't work
   - ✅ Use FastMCP Cloud, Heroku, AWS, etc.

2. **OpenAI API Key**: Set `OPENAI_API_KEY` environment variable

3. **Supported Models**: `gpt-4o`, `gpt-5-mini`, `gpt-4-turbo`, etc.

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()

# Configure MCP tool
mcp_tool = {
    "type": "mcp",
    "server_label": "freedcodecamp-content",  # Unique identifier
    "server_url": "https://freedcodecamp-content.fastmcp.app/mcp",
    "require_approval": "never"  # Auto-approve tool calls
}

# Create response with MCP tools
response = client.responses.create(
    model="gpt-5-mini",
    instructions="You are a helpful programming assistant with access to FreeCodeCamp's content library.",
    tools=[mcp_tool],
    input="Find me tutorials about React hooks"
)

print(response.output_text)
```

### Advanced Client with Conversation Management

```python
from openai import OpenAI
from datetime import datetime
import json

class MCPAgentClient:
    def __init__(
        self,
        server_url: str,
        server_label: str,
        model: str = "gpt-5-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # MCP tool configuration
        self.mcp_tool = {
            "type": "mcp",
            "server_label": server_label,
            "server_url": server_url,
            "require_approval": "never"
        }

        # Conversation tracking
        self.conversation_history = []

    def query(self, user_input: str, instructions: str = None):
        """Send query to AI with MCP tools."""

        # Default instructions
        if instructions is None:
            instructions = (
                "You are a helpful programming assistant with access to "
                "FreeCodeCamp's educational content. Use the available tools "
                "to search for relevant articles and videos."
            )

        # Create response
        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            tools=[self.mcp_tool],
            input=user_input,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        # Track conversation
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response.output_text,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        })

        return response.output_text

    def get_conversation_history(self):
        """Get full conversation history."""
        return self.conversation_history

    def export_conversation(self, filepath: str):
        """Export conversation to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation exported to {filepath}")

    def get_usage_stats(self):
        """Calculate total token usage."""
        total_prompt = sum(c['usage']['prompt_tokens'] for c in self.conversation_history)
        total_completion = sum(c['usage']['completion_tokens'] for c in self.conversation_history)
        total_tokens = sum(c['usage']['total_tokens'] for c in self.conversation_history)

        return {
            "total_conversations": len(self.conversation_history),
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "total_tokens": total_tokens,
            "estimated_cost_usd": self._estimate_cost(total_tokens)
        }

    def _estimate_cost(self, total_tokens: int) -> float:
        """Estimate cost based on token usage (approximate)."""
        # Example pricing: $0.50 per 1M tokens for gpt-5-mini
        cost_per_million = 0.50
        return (total_tokens / 1_000_000) * cost_per_million

# Usage example
if __name__ == "__main__":
    # Initialize client
    agent = MCPAgentClient(
        server_url="https://freedcodecamp-content.fastmcp.app/mcp",
        server_label="freedcodecamp-content",
        model="gpt-5-mini"
    )

    # Query 1
    response1 = agent.query("What are the latest Python tutorials?")
    print(f"Response 1: {response1}\n")

    # Query 2
    response2 = agent.query("Find React hooks tutorials")
    print(f"Response 2: {response2}\n")

    # Get stats
    stats = agent.get_usage_stats()
    print(f"Usage stats: {stats}")

    # Export conversation
    agent.export_conversation("conversation_history.json")
```

### MCP Tool Configuration Options

```python
mcp_tool = {
    # Required fields
    "type": "mcp",                    # Must be "mcp"
    "server_label": "my-server",      # Unique identifier for this server
    "server_url": "https://...",      # Public HTTPS URL ending in /mcp

    # Optional fields
    "require_approval": "never",      # "never" | "always" | "on_first_use"
}
```

**Approval Modes**:
- `"never"`: Auto-approve all tool calls (recommended for trusted servers)
- `"always"`: Require user approval for every tool call
- `"on_first_use"`: Ask approval on first use, then auto-approve

### Error Handling

```python
from openai import OpenAI, OpenAIError

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-5-mini",
        tools=[{
            "type": "mcp",
            "server_label": "my-server",
            "server_url": "https://my-server.example.com/mcp",
            "require_approval": "never"
        }],
        input="Search for tutorials"
    )
    print(response.output_text)

except OpenAIError as e:
    print(f"OpenAI API error: {e}")
    # Common errors:
    # - 424 Failed Dependency: Cannot reach MCP server (check URL, ensure public)
    # - 400 Bad Request: Invalid tool configuration
    # - 401 Unauthorized: Invalid API key
```

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **424 Failed Dependency** | MCP server URL not accessible | Deploy to public URL (FastMCP Cloud, etc.) |
| **localhost not working** | OpenAI can't reach local servers | Use tunneling (ngrok) or cloud deployment |
| **Tool not found** | Server label mismatch | Ensure server_label matches server name |
| **Empty responses** | Server not returning data | Check server logs, verify tool implementation |

---

## Project Examples

This repository demonstrates MCP concepts with real working examples:

### 1. MCP Server - [feed_deployment.py](deployment/feed_deployment.py)

**Features**:
- ✅ HTTP transport for web deployment
- ✅ Multi-term search (ANY/ALL matching)
- ✅ RSS feed parsing with full metadata
- ✅ HTML to Markdown conversion
- ✅ Two tools: `fcc_news_search`, `fcc_youtube_search`
- ✅ Deployed to FastMCP Cloud

**Usage**:
```bash
# Run locally
python deployment/feed_deployment.py

# Deploy to cloud
fastmcp deploy deployment/feed_deployment.py
```

### 2. OpenAI Agent Client - [agent_client.py](deployment/agent_client.py)

**Features**:
- ✅ Uses OpenAI Responses API with MCP type
- ✅ Connects to FastMCP Cloud deployment
- ✅ Simple query interface

**Usage**:
```python
from agent_client import FCCAgentClient

agent = FCCAgentClient()
response = agent.query("Find Python tutorials for beginners")
print(response)
```

### 3. Advanced Agent - [agent_client_advanced.py](deployment/agent_client_advanced.py)

**Features**:
- ✅ Conversation history tracking
- ✅ Token usage statistics
- ✅ Cost estimation
- ✅ Export to JSON
- ✅ Configurable temperature and max_tokens

**Usage**:
```python
from agent_client_advanced import AdvancedFCCAgentClient

agent = AdvancedFCCAgentClient(temperature=0.8, max_tokens=1500)

# Multi-turn conversation
agent.query("What are the latest React tutorials?")
agent.query("Show me videos about JavaScript")

# Get stats
stats = agent.get_usage_stats()
print(f"Total tokens used: {stats['total_tokens']}")
print(f"Estimated cost: ${stats['estimated_cost_usd']:.4f}")

# Export conversation
agent.export_conversation("my_conversation.json")
```

### 4. Testing Examples

**Cloud Deployment Test** - [test_cloud_deployment.py](deployment/test_cloud_deployment.py):
```bash
python deployment/test_cloud_deployment.py
# Tests connection to FastMCP Cloud server
```

**Enhanced Feed Test** - [test_enhanced_feed.py](deployment/test_enhanced_feed.py):
```bash
python deployment/test_enhanced_feed.py
# Tests metadata extraction, markdown conversion
```

**Multi-Term Search Test** - [test_multiterm_direct.py](deployment/test_multiterm_direct.py):
```bash
python deployment/test_multiterm_direct.py
# Tests ANY/ALL matching modes with multiple terms
```

---

## Documentation Files

- [CLOUD_DEPLOYMENT_SUCCESS.md](deployment/CLOUD_DEPLOYMENT_SUCCESS.md) - FastMCP Cloud deployment guide
- [ENHANCED_FEED_PARSING.md](deployment/ENHANCED_FEED_PARSING.md) - RSS parsing enhancements
- [MULTI_TERM_SEARCH.md](deployment/MULTI_TERM_SEARCH.md) - Multi-term search implementation

---

## Additional Resources

### Official Documentation
- **MCP Specification**: https://modelcontextprotocol.io/llms.txt
- **FastMCP Docs**: https://github.com/jlowin/fastmcp
- **OpenAI Responses API**: https://platform.openai.com/docs/api-reference/responses

### Community
- **MCP GitHub**: https://github.com/anthropics/model-context-protocol
- **FastMCP Discord**: Community support and discussions
- **OpenAI Community**: https://community.openai.com

### Learning Path
1. Start with STDIO transport for local development
2. Build simple tools with FastMCP decorators
3. Add resources and prompts as needed
4. Deploy to FastMCP Cloud for production
5. Integrate with OpenAI Responses API
6. Implement conversation management and tracking

---

**Last Updated**: January 2026
**MCP Version**: 1.0
**FastMCP Version**: 2.14.2+
