# Context7 MCP Server Guide

Complete guide to installing, configuring, and using Context7 MCP server for accessing up-to-date library documentation and code examples in your development workflow.

## Table of Contents

- [What is Context7 MCP?](#what-is-context7-mcp)
- [Prerequisites](#prerequisites)
- [Getting Your API Key](#getting-your-api-key)
- [Installation & Configuration](#installation--configuration)
  - [Claude Code CLI](#claude-code-cli)
  - [VSCode](#vscode)
  - [GitHub Copilot (via VSCode)](#github-copilot-via-vscode)
  - [Cursor IDE](#cursor-ide)
- [Usage](#usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## What is Context7 MCP?

Context7 MCP (Model Context Protocol) is a server that provides AI coding assistants with **up-to-date, version-specific documentation and code examples** directly from the source. It prevents outdated code examples and hallucinated APIs by fetching real-time documentation.

### Key Benefits

- **Always Current**: Get the latest documentation for any library version
- **No Hallucinations**: Real code examples from official sources
- **Version-Specific**: Access docs for specific library versions
- **Framework Agnostic**: Works with any programming language or framework
- **IDE Integration**: Seamless integration with major IDEs and AI assistants

### How It Works

1. Install Context7 MCP server in your IDE/CLI
2. Add "use context7" or "remember to use context7" to your AI prompts
3. The AI automatically queries Context7 for current documentation
4. You get accurate, up-to-date code examples

## Prerequisites

- **Node.js** (v18 or later) and **npm** installed
- An active **Context7 API key** (free tier available)
- One of the supported tools:
  - Claude Code CLI
  - VSCode with MCP support
  - Cursor IDE
  - Any MCP-compatible AI assistant

## Getting Your API Key

1. Visit [https://context7.com](https://context7.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key (format: `ctx7sk_...`)
5. Copy and save your API key securely

> **Security Note**: Never commit API keys to version control. Use environment variables or secure configuration files.

## Installation & Configuration

### Claude Code CLI

Claude Code has built-in MCP support, making Context7 integration straightforward.

#### Method 1: Direct Installation (Recommended)

```bash
# Add Context7 MCP server to Claude Code
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your actual Context7 API key.

#### Method 2: Using Environment Variables

```bash
# Set environment variable
export CONTEXT7_API_KEY=ctx7sk_your_key

# Add MCP server without exposing key in command
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

#### Verify Installation

```bash
# List installed MCP servers
claude mcp list

# You should see 'context7' in the output
```

#### Configuration File

Claude Code stores MCP configurations in `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
    }
  }
}
```

**Better practice** - Use environment variables:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "ctx7sk_your_key"
      }
    }
  }
}
```

### VSCode

VSCode supports MCP through extensions and configuration.

#### Step 1: Install Required Extension

Install the **MCP Client** extension from VSCode marketplace or a Claude-compatible extension that supports MCP.

#### Step 2: Configure Settings

Open VSCode settings (`Cmd/Ctrl + ,`) and add MCP configuration:

**Option A: Using settings.json**

```json
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
      }
    }
  }
}
```

**Option B: Using Environment Variables (Recommended)**

Create a `.env` file in your project root:

```bash
CONTEXT7_API_KEY=ctx7sk_your_key
```

Then configure in `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"],
        "env": {
          "CONTEXT7_API_KEY": "${env:CONTEXT7_API_KEY}"
        }
      }
    }
  }
}
```

#### Step 3: Restart VSCode

Close and reopen VSCode to activate the MCP server.

### GitHub Copilot (via VSCode)

GitHub Copilot doesn't natively support MCP servers, but you can use Context7 alongside Copilot in VSCode:

1. **Install both**:
   - GitHub Copilot extension
   - MCP-compatible extension (e.g., Claude Code for VSCode)

2. **Configure Context7** as shown in the VSCode section above

3. **Usage pattern**:
   - Use Copilot for code completion
   - Use Claude Code with Context7 for documentation queries and complex implementations

### Cursor IDE

Cursor has built-in MCP support similar to Claude Code.

#### Configuration

1. Open Cursor Settings (`Cmd/Ctrl + ,`)
2. Navigate to **Features** → **MCP Servers**
3. Add new MCP server configuration:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "ctx7sk_your_key"
      }
    }
  }
}
```

4. Restart Cursor

## Usage

### Basic Usage Pattern

When working with AI assistants, simply mention Context7 in your prompts:

```
Use context7 to help me implement JWT authentication with djangorestframework-simplejwt
```

```
Remember to use context7. Show me how to create a Django REST API viewset with pagination
```

```
Using context7, help me set up pytest with Django
```

### The AI Will Automatically:

1. Query Context7 for the latest documentation
2. Retrieve relevant code examples
3. Provide version-specific implementation details
4. Use actual API methods (no hallucinations)

### Example Workflow

**Scenario**: You need to implement GraphQL API with Graphene-Django

**Prompt**:
```
Use context7 to help me set up a GraphQL API with graphene-django for my Pet model.
I need queries, mutations, and proper schema configuration.
```

**What happens**:
- Context7 fetches latest graphene-django documentation
- AI provides current installation steps
- Code examples use actual, current API
- Configuration matches latest version best practices

### Specifying Library Versions

You can request specific versions:

```
Use context7 to show me Django 5.1 middleware configuration
```

```
Using context7, help me with React 18.3 useEffect cleanup patterns
```

## Best Practices

### 1. Always Mention Context7

Make it a habit to include "use context7" in your prompts when:
- Learning new libraries
- Implementing authentication/authorization
- Setting up third-party integrations
- Troubleshooting deprecated APIs
- Working with rapidly evolving frameworks

### 2. Be Specific About Versions

When working on production code, specify exact versions:

```
Use context7 for Django 5.2 and djangorestframework 3.15 to implement JWT authentication
```

### 3. Combine with Your Codebase Context

Provide both Context7 and your project context:

```
Use context7 to help me add GraphQL support to this Django project.
I'm using Django 5.2, PostgreSQL 16, and already have REST API with DRF 3.15.
```

### 4. Use for New Feature Development

Before implementing new features with unfamiliar libraries:

```
Use context7 to research the best approach for implementing real-time
notifications in Django. Compare channels, websockets, and SSE options.
```

### 5. Verify Complex Integrations

For complex setups, ask Context7 to verify:

```
Use context7 to verify this is the correct way to configure Celery
with Django 5.2 and Redis. Are there any deprecated patterns here?
```

### 6. Keep API Key Secure

**DO**:
- Store API key in environment variables
- Use `.env` files (add to `.gitignore`)
- Use secret management tools in production
- Rotate keys periodically

**DON'T**:
- Hardcode keys in configuration files
- Commit keys to version control
- Share keys in team chats
- Use the same key across all environments

### 7. Optimize Query Patterns

Be specific to get better results:

**Good**:
```
Use context7: How to implement pagination with cursor-based approach in DRF 3.15?
```

**Better**:
```
Use context7 for djangorestframework 3.15: Show me how to implement
cursor pagination for a Pet viewset with filtering by status field.
```

### 8. Leverage for Learning

Use Context7 when learning new concepts:

```
I'm new to Django signals. Use context7 to explain signals with
practical examples for sending emails after user registration.
```

### 9. Document Your Dependencies

When Context7 helps you implement features, document the library versions:

```python
# requirements.txt
# Configured with Context7 assistance - 2024-01-03
django==5.2.0
djangorestframework==3.15.0
djangorestframework-simplejwt==5.3.1
```

### 10. Use in Code Reviews

Ask Context7 to review patterns:

```
Use context7 to review if this Django model structure follows
current best practices for Django 5.2
```

## Troubleshooting

### MCP Server Not Found

**Problem**: AI says "Context7 MCP server not available"

**Solutions**:
```bash
# Verify MCP server is installed
claude mcp list  # For Claude Code
# OR check VSCode settings

# Reinstall if needed
claude mcp remove context7
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_KEY

# Verify npx is accessible
which npx
npx --version
```

### Authentication Errors

**Problem**: "Invalid API key" or authentication failures

**Solutions**:
1. Verify API key is correct (check for extra spaces)
2. Ensure API key starts with `ctx7sk_`
3. Check if key has expired or been revoked
4. Generate new key from Context7 dashboard
5. Verify environment variable is set correctly:
   ```bash
   echo $CONTEXT7_API_KEY
   ```

### Node.js/NPM Issues

**Problem**: "npx command not found" or Node.js errors

**Solutions**:
```bash
# Install Node.js (if not installed)
# macOS
brew install node

# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# Verify installation
node --version  # Should be v18+
npm --version

# Update npm
npm install -g npm@latest
```

### Slow Response Times

**Problem**: Context7 queries are slow

**Solutions**:
1. Check internet connection
2. Try more specific queries
3. Verify Context7 service status
4. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

### MCP Server Crashes

**Problem**: MCP server exits unexpectedly

**Solutions**:
```bash
# Check MCP server logs (Claude Code)
cat ~/.claude/logs/mcp.log

# Run server manually to see errors
npx @upstash/context7-mcp --api-key YOUR_KEY

# Reinstall package
npm cache clean --force
npx -y @upstash/context7-mcp --api-key YOUR_KEY
```

### VSCode Integration Issues

**Problem**: MCP not working in VSCode

**Solutions**:
1. Ensure MCP-compatible extension is installed
2. Check settings.json syntax is valid (use JSON validator)
3. Restart VSCode completely
4. Check developer console for errors:
   - `Help` → `Toggle Developer Tools` → `Console` tab
5. Verify extension permissions

### Permission Errors

**Problem**: Permission denied when running npx

**Solutions**:
```bash
# Fix npm permissions (macOS/Linux)
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP ~/.config

# Or use nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

## Examples

### Example 1: Django REST Framework Authentication

**Prompt**:
```
Use context7 to help me implement token refresh functionality
with djangorestframework-simplejwt 5.3.1
```

**Expected Response**:
AI provides current token refresh view configuration, URL patterns, and frontend integration examples using actual simplejwt 5.3.1 API.

### Example 2: Database Migration

**Prompt**:
```
Using context7, show me how to create a custom Django migration
for adding a computed field to my Pet model in Django 5.2
```

**Expected Response**:
AI provides RunPython migration example with current Django 5.2 syntax.

### Example 3: Testing Setup

**Prompt**:
```
Use context7 for pytest-django: Help me set up fixtures and
database configuration for testing Django REST API endpoints
```

**Expected Response**:
AI provides pytest.ini configuration, conftest.py fixtures, and test examples using current pytest-django API.

### Example 4: Third-Party Integration

**Prompt**:
```
Use context7 to help me integrate Stripe payment processing
with my Django store app. Show me webhook handling.
```

**Expected Response**:
AI fetches current Stripe Python SDK documentation and provides up-to-date webhook signature verification and event handling.

### Example 5: Performance Optimization

**Prompt**:
```
Using context7, review my Django queryset and suggest optimizations
using Django 5.2's select_related and prefetch_related
```

**Expected Response**:
AI provides Django 5.2-specific optimization patterns with proper queryset chaining.

## Integration with This Project

For this Petstore API project, you can use Context7 for:

### 1. Adding New Features

```
Use context7 to help me add WebSocket support for real-time pet updates
using Django Channels 4.x with our existing Django 5.2 + PostgreSQL setup
```

### 2. Upgrading Dependencies

```
Use context7 to guide upgrading from Django 5.2 to Django 5.3 when released.
What breaking changes should I watch for?
```

### 3. Implementing Best Practices

```
Using context7, review our Django REST Framework viewsets and suggest
performance optimizations following DRF 3.15 best practices
```

### 4. Troubleshooting

```
Use context7 to help debug this JWT token expiration issue with
djangorestframework-simplejwt 5.3.1
```

### 5. Documentation

```
Use context7 to help me document our API using drf-spectacular
with proper OpenAPI 3.1 annotations
```

## Additional Resources

- **Official Documentation**: [https://context7.com/docs](https://context7.com/docs)
- **GitHub Repository**: [https://github.com/upstash/context7-mcp](https://github.com/upstash/context7-mcp)
- **MCP Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- **API Key Management**: [https://context7.com/dashboard](https://context7.com/dashboard)

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review Context7 documentation
3. Check MCP server logs
4. Visit Context7 support or GitHub issues
5. Ensure you're using latest version:
   ```bash
   npx @upstash/context7-mcp@latest --version
   ```

---

**Last Updated**: January 2026
**Context7 MCP Package**: `@upstash/context7-mcp`
**Supported in**: Claude Code CLI, VSCode, Cursor IDE, and MCP-compatible AI assistants
