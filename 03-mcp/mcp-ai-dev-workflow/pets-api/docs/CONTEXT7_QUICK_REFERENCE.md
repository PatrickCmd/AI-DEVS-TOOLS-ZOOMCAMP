# Context7 MCP Quick Reference

Quick reference guide for using Context7 MCP in your daily development workflow.

## Installation Commands

### Claude Code CLI
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

### VSCode settings.json
```json
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"],
        "env": {
          "CONTEXT7_API_KEY": "ctx7sk_your_key"
        }
      }
    }
  }
}
```

### Cursor IDE
Add to MCP Servers configuration:
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

## Common Prompt Patterns

### Basic Usage
```
Use context7 to help me [task description]
```

### Version-Specific
```
Use context7 for Django 5.2 to show me [feature]
```

### Multiple Libraries
```
Use context7: I need to integrate Django 5.2 with Celery 5.3 for background tasks
```

### Best Practice Check
```
Use context7 to verify if this [pattern/code] follows current best practices
```

### Troubleshooting
```
Use context7 to help debug this [issue] with [library version]
```

## Example Prompts for This Project

### Django REST Framework
```
Use context7 to help me add filtering and search to my Pet viewset using DRF 3.15
```

### Authentication
```
Use context7 for djangorestframework-simplejwt 5.3.1: How to implement token blacklisting on logout?
```

### Testing
```
Use context7 for pytest-django: Show me how to test authenticated endpoints with JWT tokens
```

### Database
```
Use context7 to help me optimize this Django queryset for PostgreSQL 16
```

### GraphQL (if adding)
```
Use context7 to add GraphQL API with graphene-django to my existing Django REST project
```

### Background Tasks (if adding)
```
Use context7: Integrate Celery 5.3 with Django 5.2 for sending email notifications
```

### WebSockets (if adding)
```
Use context7 for Django Channels 4.x: Implement real-time pet updates with WebSockets
```

## Verification Commands

### Check MCP Installation
```bash
# Claude Code
claude mcp list

# Manual test
npx @upstash/context7-mcp --api-key YOUR_KEY
```

### Verify Environment Variable
```bash
echo $CONTEXT7_API_KEY
```

### Check Node.js/npm
```bash
node --version  # Should be v18+
npm --version
which npx
```

## Common Issues & Quick Fixes

### "MCP server not found"
```bash
claude mcp remove context7
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_KEY
```

### "Invalid API key"
- Check for extra spaces in API key
- Verify key starts with `ctx7sk_`
- Generate new key at https://context7.com/dashboard

### "npx command not found"
```bash
# Install Node.js
brew install node  # macOS
# or
sudo apt install nodejs npm  # Ubuntu
```

### Slow responses
- Make queries more specific
- Check internet connection
- Verify Context7 service status

## Best Practices Checklist

- ✅ Always mention "use context7" in prompts for library-related tasks
- ✅ Specify exact versions when working on production code
- ✅ Store API key in environment variables, not in config files
- ✅ Add `.env` to `.gitignore` if using .env files
- ✅ Be specific in queries for better results
- ✅ Use Context7 when learning new libraries or frameworks
- ✅ Verify complex integrations with Context7 before implementing
- ✅ Document library versions when Context7 helps with implementation
- ✅ Use Context7 in code reviews to check for deprecated patterns
- ✅ Keep npx and Node.js updated

## Library-Specific Templates

### Django
```
Use context7 for Django [version] to [task]
```

### Django REST Framework
```
Use context7 for djangorestframework [version]: [specific feature]
```

### pytest
```
Use context7 for pytest-django: [testing scenario]
```

### PostgreSQL/Database
```
Use context7 to optimize Django ORM queries for PostgreSQL [version]
```

### Authentication
```
Use context7 for djangorestframework-simplejwt [version]: [auth feature]
```

## Resources

- **Full Guide**: [CONTEXT7_MCP_GUIDE.md](CONTEXT7_MCP_GUIDE.md)
- **Get API Key**: https://context7.com/dashboard
- **Documentation**: https://context7.com/docs
- **MCP Protocol**: https://modelcontextprotocol.io

---

**Pro Tip**: Create a shell alias for quick Context7 testing:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias ctx7test='npx @upstash/context7-mcp --api-key $CONTEXT7_API_KEY'
```
