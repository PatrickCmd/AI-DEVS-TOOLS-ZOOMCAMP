# Quick Start Guide - FreeCodeCamp MCP Agent

Get up and running in 5 minutes! 🚀

## Prerequisites

- Python 3.12+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

### 1. Install Dependencies

```bash
# Install server dependencies
pip install fastmcp>=2.14.2 feedparser>=6.0.12

# Install client dependencies
pip install openai>=1.12.0 python-dotenv>=1.0.0
```

Or use requirements files:

```bash
pip install -r requirements_deploy.txt requirements_client.txt
```

### 2. Set Up Environment

Create `.env` file in this directory:

```bash
OPENAI_API_KEY=sk-your-api-key-here
MCP_SERVER_URL=http://localhost:8000
OPENAI_MODEL=gpt-4o-mini
```

## Running

### Option 1: Using Quick Start Script

```bash
# Make executable (Linux/Mac)
chmod +x quickstart.sh

# Run
./quickstart.sh
```

### Option 2: Manual Steps

**Terminal 1 - Start Server:**

```bash
python feed_deployment.py
```

Wait for:
```
Starting the FreeCodeCamp Content Explorer with HTTP transport...
The service will be accessible via HTTP endpoints
```

**Terminal 2 - Run Client:**

```bash
# Basic client
python agent_client.py

# Or advanced client
python agent_client_advanced.py

# Or run examples
python example_usage.py
```

## Usage Examples

### Quick Test

```python
from agent_client import FCCAgentClient

agent = FCCAgentClient()
agent.query("How do I learn React?")
```

### Interactive Mode

```python
agent = FCCAgentClient()
agent.interactive_mode()
```

Then type your questions:
```
You: I want to learn Python
You: Show me beginner tutorials
You: What about machine learning?
```

## Example Questions

Try asking:
- "How do I get started with web development?"
- "Show me Python tutorials for beginners"
- "Find articles about JavaScript ES6"
- "What content do you have on machine learning?"
- "I want to learn React, where should I start?"

## Troubleshooting

### Server won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
python feed_deployment.py --port 8080
```

### Can't connect to server

```bash
# Verify server is running
curl http://localhost:8000/

# Check your .env file
cat .env
```

### OpenAI API errors

1. Verify API key in `.env`
2. Check API key permissions at [OpenAI Platform](https://platform.openai.com/)
3. Ensure you have credits available

## Next Steps

1. ✅ Explore [example_usage.py](./example_usage.py) for more examples
2. ✅ Read [README.md](./README.md) for complete documentation
3. ✅ Try the advanced client with conversation export
4. ✅ Deploy to cloud (see README.md)

## Files Overview

```
deployment/
├── feed_deployment.py          # MCP server (HTTP transport)
├── agent_client.py             # Basic OpenAI agent client
├── agent_client_advanced.py    # Advanced client with features
├── example_usage.py            # Usage examples
├── README.md                   # Complete documentation
├── QUICKSTART.md              # This file
├── quickstart.sh              # Automated setup script
├── requirements_deploy.txt    # Server dependencies
└── requirements_client.txt    # Client dependencies
```

## Cost Estimation

Using `gpt-4o-mini` (recommended):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Average query: ~$0.0001 - $0.001

Tips to reduce costs:
1. Use `gpt-4o-mini` instead of `gpt-4o`
2. Set lower `max_tokens`
3. Cache frequently asked questions

## Support

- 📖 [Full Documentation](./README.md)
- 🐛 [Report Issues](https://github.com/jlowin/fastmcp/issues)
- 💬 [Community Discussion](https://github.com/jlowin/fastmcp/discussions)

---

**Happy Learning! 🎓**
