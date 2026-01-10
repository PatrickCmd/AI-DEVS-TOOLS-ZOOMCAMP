# FreeCodeCamp MCP Server Deployment & OpenAI Agent Client

Complete guide for deploying an MCP server with HTTP transport and consuming it with OpenAI agents.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [MCP Server](#mcp-server)
- [OpenAI Agent Clients](#openai-agent-clients)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [Using the Clients](#using-the-clients)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

---

## Overview

This project demonstrates:

1. **MCP Server with HTTP Transport**: A FastMCP server that provides tools to search FreeCodeCamp's educational content
2. **OpenAI Agent Integration**: Clients that consume the MCP server using OpenAI's Responses API
3. **Production-Ready Patterns**: Authentication, error handling, conversation management

### Key Features

✅ HTTP-based MCP server (deployable to cloud)
✅ OpenAI Responses API integration
✅ Automatic tool discovery and invocation
✅ Multi-turn conversations with context
✅ Cost tracking and usage statistics
✅ Conversation export and replay
✅ Interactive and programmatic modes

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User / Application                     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              OpenAI Agent Client                         │
│  - Sends queries to OpenAI                              │
│  - Includes MCP server as tool                          │
│  - Manages conversation context                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              OpenAI Responses API                        │
│  - Processes natural language                           │
│  - Decides when to call MCP tools                       │
│  - Synthesizes responses                                │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼ (HTTP Request to /mcp/ endpoint)
┌─────────────────────────────────────────────────────────┐
│            FastMCP Server (HTTP Transport)               │
│  ┌─────────────────────────────────────────────┐       │
│  │ Tools:                                       │       │
│  │  • fcc_news_search()                        │       │
│  │  • fcc_youtube_search()                     │       │
│  │  • fcc_secret_message()                     │       │
│  └─────────────────────────────────────────────┘       │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│            External Content Sources                      │
│  • FreeCodeCamp RSS Feed (news)                         │
│  • YouTube RSS Feed (videos)                            │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

1. **User** asks a question: "How do I learn React?"
2. **Agent Client** sends request to OpenAI with MCP server configured as a tool
3. **OpenAI API** analyzes the query and decides to call MCP tools
4. **MCP Server** receives HTTP request, executes tools, returns results
5. **OpenAI API** synthesizes final response using tool results
6. **Agent Client** displays response to user

---

## MCP Server

### Server Implementation (`feed_deployment.py`)

The MCP server provides three tools:

#### 1. `fcc_news_search`
Searches FreeCodeCamp's news feed by title/description.

```python
@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3):
    """Search FreeCodeCamp's news articles"""
    # Returns list of matching articles with titles and URLs
```

#### 2. `fcc_youtube_search`
Searches FreeCodeCamp's YouTube channel by video title.

```python
@mcp.tool()
def fcc_youtube_search(query: str, max_results: int = 3):
    """Search FreeCodeCamp's YouTube videos"""
    # Returns list of matching videos with titles and URLs
```

#### 3. `fcc_secret_message`
Returns an inspirational message.

```python
@mcp.tool()
def fcc_secret_message():
    """Returns an inspirational message"""
    return "Keep exploring! The journey of learning never ends! 🌟"
```

### HTTP Transport Configuration

```python
if __name__ == "__main__":
    # Run with HTTP transport instead of STDIO
    mcp.run(transport="http")
```

This makes the server accessible via HTTP endpoints, suitable for:
- Production deployment
- Cloud hosting (AWS, GCP, Azure, etc.)
- Containerization (Docker, Kubernetes)
- Multiple concurrent clients

---

## OpenAI Agent Clients

### Basic Client (`agent_client.py`)

Simple, straightforward client for quick usage.

**Features**:
- Single query execution
- Interactive mode
- Basic error handling

**Usage**:
```python
from agent_client import FCCAgentClient

# Initialize
agent = FCCAgentClient(
    server_url="http://localhost:8000",
    model="gpt-4o-mini"
)

# Single query
agent.query("How do I learn React?")

# Interactive mode
agent.interactive_mode()
```

### Advanced Client (`agent_client_advanced.py`)

Production-ready client with enhanced features.

**Features**:
- ✅ Conversation history tracking
- ✅ Multi-turn conversations with context
- ✅ Tool call tracking for debugging
- ✅ Cost estimation
- ✅ Conversation export (JSON)
- ✅ Streaming support (optional)
- ✅ Usage statistics

**Usage**:
```python
from agent_client_advanced import AdvancedFCCAgentClient

# Initialize with custom settings
agent = AdvancedFCCAgentClient(
    server_url="http://localhost:8000",
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000
)

# Query with context awareness
agent.query("I'm new to programming. Where should I start?")
agent.query("What about Python?")  # Maintains context
agent.query("Show me Python tutorials")  # Context-aware

# Interactive chat
agent.chat()
```

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- OpenAI API key with access to GPT-4o or GPT-4o-mini
- Internet connection (for RSS feeds)

### 1. Install Dependencies

```bash
cd 03-mcp/FCC-MCP-Course/deployment

# Install required packages
pip install fastmcp>=2.14.2 feedparser>=6.0.12 openai python-dotenv

# Or use the requirements file
pip install -r requirements_deploy.txt
```

### 2. Set Up Environment Variables

Create a `.env` file:

```bash
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-api-key-here

# Optional configurations
MCP_SERVER_URL=http://localhost:8000
OPENAI_MODEL=gpt-4o-mini
```

### 3. Verify Installation

```bash
# Check FastMCP
python -c "import fastmcp; print(fastmcp.__version__)"

# Check OpenAI
python -c "import openai; print(openai.__version__)"
```

---

## Running the Server

### Method 1: Direct Execution

```bash
python feed_deployment.py
```

Output:
```
Starting the FreeCodeCamp Content Explorer with HTTP transport...
The service will be accessible via HTTP endpoints
This deployment configuration allows the service to:
1. Be accessed over HTTP
2. Handle multiple concurrent requests
3. Be integrated with web services
```

The server will start on `http://localhost:8000` by default.

### Method 2: Using FastMCP CLI

```bash
fastmcp run feed_deployment.py:mcp --transport http --port 8000
```

### Method 3: With Custom Port

```python
# In feed_deployment.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.app, host="0.0.0.0", port=8080)
```

### Verify Server is Running

```bash
# Check server health
curl http://localhost:8000/

# List available tools
curl http://localhost:8000/mcp/tools
```

---

## Using the Clients

### Basic Client

#### Example 1: Single Query

```python
from agent_client import FCCAgentClient

agent = FCCAgentClient()
response = agent.query("How do I learn React?")
print(response)
```

#### Example 2: Multiple Queries

```python
agent = FCCAgentClient()

queries = [
    "Show me Python tutorials",
    "What content do you have on machine learning?",
    "Find articles about web development"
]

for query in queries:
    agent.query(query)
```

#### Example 3: Interactive Mode

```python
agent = FCCAgentClient()
agent.interactive_mode()
```

### Advanced Client

#### Example 1: Context-Aware Conversation

```python
from agent_client_advanced import AdvancedFCCAgentClient

agent = AdvancedFCCAgentClient(temperature=0.8)

# Multi-turn conversation with context
agent.query("I'm a complete beginner in programming")
agent.query("Should I start with Python or JavaScript?")
agent.query("Show me some beginner tutorials")

# Get conversation stats
print(agent.conversation.get_summary())
```

#### Example 2: Export Conversation

```python
agent = AdvancedFCCAgentClient()

# Have a conversation
agent.query("How do I learn React?")
agent.query("What about Next.js?")

# Export to file
agent.conversation.export_conversation("my_learning_session.json")
```

#### Example 3: Cost Tracking

```python
agent = AdvancedFCCAgentClient(model="gpt-4o-mini")

response = agent.query("Explain REST APIs", verbose=True)

# Usage stats will be printed:
# 📊 Usage Stats:
#   - Input tokens: 150
#   - Output tokens: 250
#   - Total tokens: 400
#   - Estimated cost: $0.000090
```

---

## Examples

### Example 1: Learning Path Query

**User Query**: "I want to become a web developer. What should I learn first?"

**Expected Flow**:
1. Agent calls `fcc_news_search("web development beginner")`
2. Agent calls `fcc_youtube_search("web development tutorial")`
3. Agent synthesizes response with links to resources

**Response**:
```
Great question! Let me help you get started on your web development journey.

Based on FreeCodeCamp's resources, here's what I found:

📚 Recommended Articles:
1. "How to Become a Web Developer - A Complete Guide"
   https://www.freecodecamp.org/news/...

2. "HTML and CSS for Beginners - Full Course"
   https://www.freecodecamp.org/news/...

🎥 Video Tutorials:
1. "Web Development Tutorial for Beginners"
   https://www.youtube.com/watch?v=...

2. "Learn HTML & CSS - Full Course"
   https://www.youtube.com/watch?v=...

I recommend starting with:
1. HTML basics
2. CSS for styling
3. JavaScript fundamentals
4. Then move to frameworks like React

Keep exploring! The journey of learning never ends! 🌟
```

### Example 2: Specific Technology Query

**User Query**: "Show me Python machine learning tutorials"

**Expected Flow**:
1. Agent calls `fcc_news_search("Python machine learning")`
2. Agent calls `fcc_youtube_search("Python machine learning")`

**Response**:
```
Here are some excellent Python machine learning resources from FreeCodeCamp:

📚 Articles:
1. "Python Machine Learning Course for Beginners"
   https://www.freecodecamp.org/news/...

2. "Machine Learning with Python - Full Course"
   https://www.freecodecamp.org/news/...

🎥 Videos:
1. "Python Machine Learning Tutorial - 10 Hours"
   https://www.youtube.com/watch?v=...

These resources cover:
- NumPy and Pandas
- Scikit-learn basics
- Building ML models
- Real-world projects

Happy learning! 🚀
```

---

## Troubleshooting

### Issue 1: Server Not Starting

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python feed_deployment.py --port 8080
```

### Issue 2: OpenAI API Error

**Error**: `Invalid API key`

**Solution**:
1. Check `.env` file has correct API key
2. Verify environment variable is loaded:
   ```python
   import os
   print(os.getenv("OPENAI_API_KEY"))
   ```
3. Reload environment:
   ```bash
   source .env  # or restart terminal
   ```

### Issue 3: MCP Server Not Reachable

**Error**: `Connection refused to http://localhost:8000` or `Error code: 424 - Failed Dependency`

**Solution**:
1. Verify server is running:
   ```bash
   curl http://localhost:8000/
   ```
2. Check the MCP endpoint specifically:
   ```bash
   # Test the MCP endpoint
   curl http://localhost:8000/mcp

   # Or with trailing slash
   curl http://localhost:8000/mcp/
   ```
3. Check firewall settings
4. Try explicit host binding:
   ```python
   mcp.run(transport="http", host="0.0.0.0", port=8000)
   ```
5. Verify the endpoint path in your client matches the server:
   ```python
   # Client should use: server_url + "/mcp"
   server_url = "http://localhost:8000/mcp"
   ```

### Issue 4: No Results from Tools

**Error**: Tools return empty results

**Possible Causes**:
1. RSS feeds are down (check manually)
2. Search query too specific
3. Network issues

**Solution**:
```python
# Test tools directly
import feedparser

feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
print(f"Found {len(feed.entries)} entries")
```

### Issue 5: High API Costs

**Problem**: OpenAI API costs too high

**Solutions**:
1. Use `gpt-4o-mini` instead of `gpt-4o`:
   ```python
   agent = FCCAgentClient(model="gpt-4o-mini")
   ```
2. Reduce max_tokens:
   ```python
   agent = AdvancedFCCAgentClient(max_tokens=500)
   ```
3. Cache frequently asked questions
4. Implement request throttling

---

## Advanced Usage

### 1. Authentication

Add authentication to your MCP server:

```python
# In OpenAI client
mcp_tool = {
    "type": "mcp",
    "server_label": "fcc_content_explorer",
    "server_url": f"{server_url}/mcp/",
    "require_approval": "never",
    "headers": {
        "Authorization": f"Bearer {access_token}"
    }
}
```

### 2. Custom Instructions

Customize agent behavior:

```python
custom_instructions = """
You are a React expert. When users ask about React:
1. Always search for official React content first
2. Provide code examples
3. Explain concepts step-by-step
4. Recommend project-based learning
"""

agent.query(
    "How do I use React hooks?",
    instructions=custom_instructions
)
```

### 3. Streaming Responses

Enable streaming for better UX:

```python
response = client.responses.create(
    model="gpt-4o",
    tools=[mcp_tool],
    input=query,
    stream=True  # Enable streaming
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

### 4. Deploy to Cloud

#### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_deploy.txt .
RUN pip install -r requirements_deploy.txt

COPY feed_deployment.py .

EXPOSE 8000

CMD ["python", "feed_deployment.py"]
```

Build and run:
```bash
docker build -t fcc-mcp-server .
docker run -p 8000:8000 fcc-mcp-server
```

#### AWS Lambda

Use FastMCP's deployment features:

```bash
fastmcp deploy feed_deployment.py:mcp --platform aws-lambda
```

### 5. Monitoring & Logging

Add logging to track usage:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3):
    logger.info(f"News search: query='{query}', max={max_results}")
    # ... existing code ...
    logger.info(f"Found {len(results)} results")
    return results
```

---

## Performance Optimization

### 1. Caching

Implement caching for frequently requested content:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_fcc_feed(feed_url: str, cache_time: int = 3600):
    """Cache feed results for 1 hour"""
    return feedparser.parse(feed_url)

@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3):
    feed = get_fcc_feed("https://www.freecodecamp.org/news/rss/")
    # ... rest of code ...
```

### 2. Rate Limiting

Protect your server from abuse:

```python
from fastapi import HTTPException
from collections import defaultdict
import time

# Simple rate limiter
request_counts = defaultdict(list)
RATE_LIMIT = 10  # requests
TIME_WINDOW = 60  # seconds

def check_rate_limit(client_id: str):
    now = time.time()
    # Remove old requests
    request_counts[client_id] = [
        t for t in request_counts[client_id]
        if now - t < TIME_WINDOW
    ]

    if len(request_counts[client_id]) >= RATE_LIMIT:
        raise HTTPException(429, "Rate limit exceeded")

    request_counts[client_id].append(now)
```

### 3. Connection Pooling

Reuse HTTP connections for better performance:

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Create session with retry logic
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Use session for all requests
def fetch_feed(url):
    return session.get(url, timeout=10)
```

---

## Testing

### Unit Tests

```python
import pytest
from agent_client import FCCAgentClient

def test_agent_initialization():
    agent = FCCAgentClient()
    assert agent.server_url == "http://localhost:8000"
    assert agent.model == "gpt-4o"

def test_query_execution():
    agent = FCCAgentClient()
    response = agent.query("Test query")
    assert response is not None
    assert isinstance(response, str)

@pytest.mark.asyncio
async def test_multiple_queries():
    agent = FCCAgentClient()
    queries = ["Python", "JavaScript", "React"]

    for query in queries:
        response = agent.query(query)
        assert response is not None
```

### Integration Tests

```bash
# Start server in test mode
python feed_deployment.py --test &

# Run tests
pytest test_agent_client.py

# Cleanup
pkill -f feed_deployment.py
```

---

## Resources

### Documentation
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

### Related Projects
- [FreeCodeCamp](https://www.freecodecamp.org/)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

---

## License

This project is for educational purposes. Use freely for learning and experimentation.

---

## Contributing

Contributions welcome! Areas for improvement:
- Additional content sources
- Better error handling
- Caching strategies
- Authentication mechanisms
- Deployment templates

---

**Built for AI Dev Tools Zoomcamp - MCP Module** 🚀
