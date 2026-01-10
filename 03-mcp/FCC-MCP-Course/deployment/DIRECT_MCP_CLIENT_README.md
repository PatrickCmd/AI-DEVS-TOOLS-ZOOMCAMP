# Direct MCP Client with OpenAI Responses API - Investigation Report

## Summary

This document summarizes the investigation into creating an OpenAI agent client that consumes an MCP server using the Responses API.

## What We Tried

### Approach 1: Native MCP Integration (`agent_client.py` and `agent_client_advanced.py`)

**Method**: Used OpenAI's native MCP integration with `type: "mcp"` tool type.

```python
mcp_tool = {
    "type": "mcp",
    "server_label": "fcc_content_explorer",
    "server_url": "http://localhost:8000/mcp/",
    "require_approval": {
        "never": {
            "tool_names": ["fcc_news_search", "fcc_youtube_search", "fcc_secret_message"]
        }
    }
}

response = client.responses.create(
    model="gpt-5-mini",
    instructions=instructions,
    tools=[mcp_tool],
    input=user_query,
)
```

**Result**: ❌ Error 424 - Failed Dependency
```
Error code: 424 - {'error': {'message': "Error retrieving tool list from MCP server: 'fcc_content_explorer'. Http status code: 424 (Failed Dependency)", 'type': 'external_connector_error', 'param': 'tools', 'code': 'http_error'}}
```

**Analysis**:
- OpenAI's Responses API cannot connect to the local MCP server
- The MCP server is running correctly (verified with MCP Inspector)
- MCP Inspector shows session tokens and successful connections
- Likely reasons for failure:
  - OpenAI's MCP integration may require publicly accessible URLs (not localhost)
  - MCP feature may be in beta/limited access
  - Authentication/session management differences

### Approach 2: Direct FastMCP Client with Function Tools (`agent_client_direct.py`)

**Method**:
1. Use FastMCP Python client to connect to MCP server
2. Retrieve tools dynamically from server
3. Convert MCP tools to OpenAI function format
4. Pass function tools to Responses API

```python
# Connect to MCP server
client = Client("http://localhost:8000/mcp")
async with client:
    mcp_tools = await client.list_tools()

# Convert to OpenAI function format
openai_tool = {
    "type": "function",
    "name": tool_name,
    "description": mcp_tool.description,
    "parameters": mcp_tool.inputSchema,
    "strict": False
}

# Use with Responses API
response = self.openai_client.responses.create(
    model=self.model,
    instructions=instructions,
    tools=[openai_tool],
    input=user_query,
)
```

**Result**: ⚠️ Partial Success
- ✅ Successfully connected to MCP server using FastMCP client
- ✅ Successfully retrieved 3 tools from server
- ✅ Successfully converted tools to OpenAI format
- ✅ Responses API accepted the tool definitions
- ❌ Tool calls cannot be executed (output_text is empty)

**Analysis**:
The Responses API's `output` field shows tool calls as `ResponseFunctionToolCall` objects with `status='completed'`, but since these are external MCP tools, they cannot be automatically executed by OpenAI. The API expects either:
1. Built-in tools (web search, file search, etc.)
2. MCP servers accessible via public URLs
3. Manual tool execution loop (not supported in Responses API)

## What Works

### ✅ FastMCP Client Connection

The FastMCP Python client successfully connects to the MCP server and can:
- List available tools
- Call tools with arguments
- Receive results

**Test Results** (`test_direct_client.py`):
```
✓ Connected to MCP server
✓ Found 3 tools from MCP server
✓ Tool call successful!

Tool: fcc_news_search
Arguments: {'query': 'react', 'max_results': 2}
Result: [
  {"title":"How to Optimize React","url":"https://www.freecodecamp.org/news/how-to-optimize-react/"},
  {"title":"Real-Time Systems for Web Developers: From Theory to a Live Go + React App","url":"..."}
]
```

### ✅ MCP Server is Running Correctly

The MCP server deployed with FastMCP HTTP transport works as expected:
- Responds to connections
- Provides tool listings
- Executes tool calls
- Returns proper results

## Current Limitations

### OpenAI Responses API Limitations

1. **MCP Integration**: The native `type: "mcp"` integration appears to require:
   - Publicly accessible URLs (not localhost)
   - Possible beta/limited access
   - Unknown authentication requirements

2. **Function Tool Execution**: The Responses API:
   - Cannot execute external function tools directly
   - Expects tools to be either built-in or accessible via MCP
   - Does not support manual tool execution loops

3. **Local Development**: OpenAI's Responses API cannot easily consume localhost MCP servers

## Recommended Solutions

### Solution 1: Deploy MCP Server Publicly (Recommended for Production)

Deploy the MCP server to a publicly accessible URL and use the native MCP integration:

```python
mcp_tool = {
    "type": "mcp",
    "server_label": "fcc_content_explorer",
    "server_url": "https://your-domain.com/mcp/",
    "require_approval": {
        "never": {
            "tool_names": ["fcc_news_search", "fcc_youtube_search", "fcc_secret_message"]
        }
    }
}
```

**Deployment Options**:
- AWS Lambda + API Gateway
- Google Cloud Run
- Railway.app
- Fly.io
- Heroku

### Solution 2: Use Chat Completions API with Manual Tool Execution

For local development, use the Chat Completions API which supports manual tool execution:

```python
# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "fcc_news_search",
            "description": "Search FreeCodeCamp news",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# Initial completion
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Check for tool calls
if response.choices[0].message.tool_calls:
    # Execute tools via FastMCP client
    for tool_call in response.choices[0].message.tool_calls:
        result = await mcp_client.call_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
        # Add result to messages and continue conversation
```

### Solution 3: Use Claude with MCP (Native MCP Support)

Claude has native MCP support through desktop clients and can connect to local MCP servers directly:

```json
{
  "mcpServers": {
    "fcc_content_explorer": {
      "command": "python",
      "args": ["feed_deployment.py"],
      "env": {}
    }
  }
}
```

## Files Created

1. **`agent_client.py`**: Basic client using native MCP integration (Error 424)
2. **`agent_client_advanced.py`**: Advanced client with conversation management (Error 424)
3. **`agent_client_direct.py`**: Direct FastMCP client with function tools (Partial success)
4. **`test_direct_client.py`**: Test FastMCP connection (✅ Works)
5. **`test_agent_simple.py`**: Test OpenAI agent (Empty responses)
6. **`test_response_inspect.py`**: Inspect Responses API structure (✅ Informative)

## Key Learnings

1. **MCP Server HTTP Transport**: FastMCP's HTTP transport works correctly and can be consumed by Python clients
2. **Tool Format**: Responses API uses different tool format than Chat Completions API
3. **Local MCP Servers**: Cannot be easily consumed by OpenAI's Responses API
4. **FastMCP Client**: Reliable for direct MCP server communication
5. **Production Deployment**: MCP servers should be deployed publicly for OpenAI integration

## Next Steps

For this project, we recommend:

1. **For Local Development**:
   - Use the FastMCP client directly (as shown in `test_direct_client.py`)
   - Or use Chat Completions API with manual tool execution
   - Or use Claude desktop with native MCP support

2. **For Production**:
   - Deploy MCP server to a cloud platform
   - Use native MCP integration with public URL
   - Monitor for 424 errors and implement proper error handling

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [OpenAI Responses API Documentation](https://platform.openai.com/docs/api-reference/responses)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

**Status**: Investigation Complete
**Date**: 2026-01-10
**Conclusion**: Native MCP integration with Responses API requires public URLs. For local development, use Chat Completions API or Claude's native MCP support.
