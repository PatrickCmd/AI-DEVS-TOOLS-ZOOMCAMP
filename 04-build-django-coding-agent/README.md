# Building a Django Coding Agent with OpenAI 🤖🐍

A comprehensive guide to building an AI-powered coding agent that can autonomously develop Django applications using OpenAI's API and function calling capabilities.

## Table of Contents
- [Overview](#overview)
- [What is a Coding Agent?](#what-is-a-coding-agent)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How It Works](#how-it-works)
- [Building the Agent Step-by-Step](#building-the-agent-step-by-step)
- [Example: Pets Store Application](#example-pets-store-application)
- [Agent Tools](#agent-tools)
- [Developer Prompt](#developer-prompt)
- [Usage](#usage)
- [Advanced Features](#advanced-features)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## Overview

This project demonstrates how to build an **autonomous coding agent** that can:
- 📝 Understand natural language instructions
- 🔧 Write and modify Django application code
- 🗂️ Navigate and manage project files
- ⚙️ Execute bash commands for testing and validation
- 🎨 Create beautiful UIs with TailwindCSS
- 🤖 Make intelligent decisions about code structure

The agent uses **OpenAI's function calling** feature to interact with the codebase through a set of defined tools, orchestrated using the [ToyAIKit](https://github.com/alexeygrigorev/toyaikit) framework.

### Example Output

The agent successfully built a **Pets Store** Django application with:
- Pet adoption browsing 🐶🐱🐰
- Product catalog 🧸🍖🎁
- Beautiful TailwindCSS UI
- Admin dashboard
- Database models and migrations
- Template rendering

See the complete implementation in [pets-store/](./pets-store/)

---

## What is a Coding Agent?

A **coding agent** is an AI system that can autonomously write, modify, and manage code based on natural language instructions. Unlike traditional code generation tools that provide one-time code snippets, a coding agent:

1. **Maintains context** across multiple interactions
2. **Makes decisions** about code structure and implementation
3. **Uses tools** to interact with the filesystem and execute commands
4. **Validates** its changes through testing
5. **Iterates** based on errors and feedback

### Key Capabilities

- **Autonomous Development**: Agent works independently with minimal human intervention
- **Multi-Step Planning**: Breaks down complex tasks into sequential steps
- **Tool Usage**: Reads files, writes code, executes commands
- **Error Handling**: Detects and fixes issues autonomously
- **Best Practices**: Follows Django conventions and patterns

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Instruction                      │
│        "Build a pet store with products"                 │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              OpenAI Responses API (GPT-4o)              │
│        - Function calling                                │
│        - Reasoning                                       │
│        - Code generation                                 │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                  ToyAIKit Framework                      │
│        - Message orchestration                           │
│        - Tool management                                 │
│        - Response handling                               │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                    Agent Tools                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ read_file   │  │ write_file  │  │ execute_bash│    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌─────────────┐  ┌─────────────┐                      │
│  │see_file_tree│  │search_files │                      │
│  └─────────────┘  └─────────────┘                      │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│               Django Project Files                       │
│        - Models                                          │
│        - Views                                           │
│        - Templates                                       │
│        - URLs                                            │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required Software
- **Python 3.12+**
- **uv** (Python package manager)
- **OpenAI API Key** with access to GPT-4o or GPT-4o-mini

### Python Packages
```bash
pip install openai python-dotenv toyaikit
```

Or with uv:
```bash
uv add openai python-dotenv toyaikit
```

### Knowledge Prerequisites
- Basic understanding of Django
- Familiarity with OpenAI API
- Understanding of function calling
- Python async/await patterns

---

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd 04-build-django-coding-agent
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Set Up Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. Clone Django Template

The agent uses a base Django template as a starting point:

```bash
git clone https://github.com/alexeygrigorev/django_template.git
```

---

## How It Works

### The Agent Loop

```
1. User provides instruction
   ↓
2. Agent analyzes request & plans steps
   ↓
3. Agent calls appropriate tools (read_file, write_file, etc.)
   ↓
4. Tools execute and return results
   ↓
5. Agent processes results & decides next action
   ↓
6. Repeat steps 3-5 until task complete
   ↓
7. Agent provides final response
```

### Function Calling Flow

The agent uses OpenAI's function calling to interact with tools:

```python
# 1. Define tools
tools = [
    {
        "type": "function",
        "name": "read_file",
        "description": "Read contents of a file",
        "parameters": {...}
    }
]

# 2. Send request with tools
response = client.responses.create(
    model="gpt-4o",
    input=messages,
    tools=tools
)

# 3. Process function calls
if response.output has function_call:
    result = execute_function(function_call)
    messages.append(function_result)

# 4. Continue conversation
response = client.responses.create(
    model="gpt-4o",
    input=messages  # includes function results
)
```

---

## Building the Agent Step-by-Step

### Step 1: Understanding OpenAI Function Calling

First, let's understand the basics with a simple joke-making example:

```python
from openai import OpenAI

client = OpenAI()

# Define a tool
make_joke_description = {
    "type": "function",
    "name": "make_joke",
    "description": "Generates a random personalized joke",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name to personalize the joke"
            }
        },
        "required": ["name"]
    }
}

# Call API with tool
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {"role": "developer", "content": "You make personalized jokes"},
        {"role": "user", "content": "Tell me a joke about Patrick"}
    ],
    tools=[make_joke_description]
)

# Agent will call the make_joke function
# You execute it and return results
```

### Step 2: Setting Up ToyAIKit for Orchestration

[ToyAIKit](https://github.com/alexeygrigorev/toyaikit) simplifies the agent loop:

```python
from toyaikit.tools import Tools
from toyaikit.chat import IPythonChatInterface
from toyaikit.llm import OpenAIClient
from toyaikit.chat.runners import OpenAIResponsesRunner

# Initialize components
tools_obj = Tools()
tools_obj.add_tool(make_joke, make_joke_description)

chat_interface = IPythonChatInterface()
llm_client = OpenAIClient(client=OpenAI())

# Create runner
runner = OpenAIResponsesRunner(
    tools=tools_obj,
    developer_prompt="You make personalized jokes",
    chat_interface=chat_interface,
    llm_client=llm_client
)

# Run the agent
runner.run()
```

**Note**: ToyAIKit is great for learning but not production-ready. For production, use [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk) or [PydanticAI](https://ai.pydantic.dev/).

### Step 3: Creating Agent Tools

Define tools the agent can use to interact with the codebase:

```python
from pathlib import Path
import subprocess
import os

class AgentTools:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def read_file(self, filepath: str) -> str:
        """Read file contents"""
        abs_path = self.project_dir / filepath
        with open(abs_path, 'r') as f:
            return f.read()

    def write_file(self, filepath: str, content: str):
        """Write content to file"""
        abs_path = self.project_dir / filepath
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(abs_path, 'w') as f:
            f.write(content)

    def execute_bash_command(self, command: str, cwd: str = None):
        """Execute bash command"""
        # Block dangerous commands
        if "runserver" in command:
            return "", "Error: runserver not allowed", 1

        abs_cwd = (self.project_dir / cwd) if cwd else self.project_dir
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=abs_cwd,
            timeout=15
        )
        return result.stdout, result.stderr, result.returncode

    def see_file_tree(self, root_dir: str = ".") -> list[str]:
        """List all files in directory"""
        # Implementation in tools.py
        pass

    def search_in_files(self, pattern: str, root_dir: str = "."):
        """Search for pattern in files"""
        # Implementation in tools.py
        pass
```

See complete implementation in [tools.py](./tools.py)

### Step 4: Crafting the Developer Prompt

The developer prompt is crucial - it defines the agent's behavior:

```python
DEVELOPER_PROMPT = """
You are a coding agent. Your task is to modify the provided Django project template
according to user instructions. You don't tell the user what to do; you do it yourself
using the available tools. First, think about the sequence of steps you will do, and
then execute the sequence.

## Project Overview

The project is a Django 5.2.4 web application scaffolded with standard best practices.
It uses:
- Python 3.12+
- Django 5.2.4
- uv for dependency management
- SQLite as default database
- TailwindCSS for styling (via CDN)
- Font Awesome for icons

## Available Tools

You have access to:
- read_file: Read any file in the project
- write_file: Create or modify files
- execute_bash_command: Run commands (migrations, checks, etc.)
- see_file_tree: List project files
- search_in_files: Search for patterns in code

## Best Practices

- Follow Django conventions
- Use TailwindCSS for styling
- Use emojis and Font Awesome icons
- Keep logic in views, not templates
- Test changes with Django check command
- Don't run runserver (blocked)

## Workflow

1. Analyze user request
2. Plan implementation steps
3. Read relevant files
4. Make changes
5. Test with Django check
6. Report completion
"""
```

### Step 5: Initializing the Project

Create a function to copy the Django template:

```python
import shutil
import os

def start(project_name: str) -> bool:
    """Copy Django template to new project directory"""
    if not project_name:
        print("Project name cannot be empty.")
        return False

    if os.path.exists(project_name):
        print(f"Directory '{project_name}' already exists.")
        return False

    shutil.copytree('django_template', project_name)
    print(f"Django template copied to '{project_name}' directory.")
    return True
```

### Step 6: Assembling the Complete Agent

Put it all together:

```python
from openai import OpenAI
from pathlib import Path
from toyaikit.tools import Tools
from toyaikit.llm import OpenAIClient
from toyaikit.chat import IPythonChatInterface
from toyaikit.chat.runners import OpenAIResponsesRunner
import tools

# 1. Create project from template
project_name = input("Enter the new Django project name: ").strip()
start(project_name)

# 2. Initialize agent tools
project_path = Path(project_name)
agent_tools = tools.AgentTools(project_path)

# 3. Register tools
tools_obj = Tools()
tools_obj.add_tools(agent_tools)

# 4. Set up chat interface
chat_interface = IPythonChatInterface()
openai_client = OpenAIClient(model="gpt-4o", client=OpenAI())

# 5. Create assistant
chat_assistant = OpenAIResponsesRunner(
    tools=tools_obj,
    developer_prompt=DEVELOPER_PROMPT,
    chat_interface=chat_interface,
    llm_client=openai_client
)

# 6. Run the agent
chat_assistant.run()
```

### Step 7: Interacting with the Agent

Once running, you can give instructions:

```
User: Create a pets store application with a Pet model that has name,
      type, breed, age, and price fields. Also add a Product model for
      pet supplies. Make it look beautiful with TailwindCSS.

Agent: I'll create the pets store application. Let me break this down:
       1. Create Pet and Product models
       2. Configure admin interface
       3. Create views and templates
       4. Add URL routing
       5. Style with TailwindCSS

       [Agent starts executing...]
```

The agent will:
1. Read existing code
2. Create models in `models.py`
3. Register models in `admin.py`
4. Create views and templates
5. Update URLs
6. Run migrations
7. Test with `python manage.py check`

---

## Example: Pets Store Application

The agent successfully built a complete **Pets Store** application. See [pets-store/README.md](./pets-store/README.md) for details.

### What the Agent Created

**Models** (`myapp/models.py`):
```python
class Pet(models.Model):
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age_years = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    emoji = models.CharField(max_length=10)
    description = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    icon = models.CharField(max_length=50)
    description = models.TextField()
```

**Views** (`myapp/views.py`):
- Home page with stats and featured items
- Catalog page with search and filters
- Pet detail page
- Product detail page

**Templates** with TailwindCSS:
- `base.html` - Base layout with navigation
- `home.html` - Landing page
- `catalog.html` - Browse pets and products
- `pet_detail.html` - Individual pet details
- `product_detail.html` - Individual product details

**Admin Dashboard**:
- Branded as "Pets Store Admin"
- Custom list displays
- Search and filter capabilities

**Management Command**:
- `seed_store` - Generates synthetic data for testing

### Running the Pets Store App

```bash
cd pets-store

# Install dependencies
make install

# Run migrations
make migrate

# Seed sample data
make seed

# Create admin user
make createsuperuser-admin

# Run server
make run
```

Visit:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/ (admin/admin123)

---

## Agent Tools

### Tool Reference

| Tool | Purpose | Parameters | Returns |
|------|---------|------------|---------|
| `read_file` | Read file contents | `filepath: str` | File content as string |
| `write_file` | Create/modify file | `filepath: str`, `content: str` | None |
| `execute_bash_command` | Run shell command | `command: str`, `cwd: str` (optional) | stdout, stderr, returncode |
| `see_file_tree` | List files | `root_dir: str` (optional) | List of file paths |
| `search_in_files` | Search for pattern | `pattern: str`, `root_dir: str` (optional) | List of matches |

### Tool Implementation Details

**read_file**:
- Reads UTF-8 encoded files
- Returns complete file content
- Handles relative paths from project root

**write_file**:
- Creates directories if needed
- Overwrites existing files
- UTF-8 encoding

**execute_bash_command**:
- 15-second timeout
- Blocks `runserver` command
- Captures stdout and stderr
- Returns exit code

**see_file_tree**:
- Recursive directory listing
- Skips common directories (`.venv`, `__pycache__`, `.git`, etc.)
- Returns relative paths

**search_in_files**:
- Simple string matching (not regex)
- Returns (filepath, line_number, line_content) tuples
- Handles encoding errors gracefully

---

## Developer Prompt

The developer prompt is the agent's instruction manual. Key sections:

### 1. Role Definition
```
You are a coding agent. Your task is to modify the provided Django project
template according to user instructions. You don't tell the user what to do;
you do it yourself using the available tools.
```

### 2. Project Context
- Python/Django versions
- Dependency management (uv)
- Database (SQLite)
- Styling (TailwindCSS)
- File structure

### 3. Behavioral Guidelines
- Think before acting (plan steps)
- Use tools autonomously
- Follow Django best practices
- Make things beautiful
- Use emojis and icons

### 4. Constraints
- Don't run `runserver`
- Keep logic in views, not templates
- Use TailwindCSS classes
- Test with `python manage.py check`

---

## Usage

### Starting a New Project

```python
# In Jupyter Notebook or Python script
from openai import OpenAI
from pathlib import Path
import tools

# Initialize
project_name = "my-django-app"
start(project_name)

project_path = Path(project_name)
agent_tools = tools.AgentTools(project_path)

# Set up agent (see Step 6 above)
# ...

# Run
chat_assistant.run()
```

### Example Instructions

**Simple Task**:
```
User: Add a Contact model with name, email, and message fields.
```

**Complex Task**:
```
User: Create a blog application with:
      - Post model (title, content, author, published_date)
      - Comment model (post, author, content, created_at)
      - List view showing all posts
      - Detail view with comments
      - Beautiful UI with cards and typography
      - Admin interface
```

**Modification Task**:
```
User: Update the Pet model to include a 'featured' boolean field
      and show featured pets on the home page.
```

---

## Advanced Features

### Auto-Reloading During Development

When developing the agent itself, use Jupyter's auto-reload:

```python
%load_ext autoreload
%autoreload 2

import tools  # Changes to tools.py will auto-reload
```

### Cost Tracking

ToyAIKit provides automatic cost tracking:

```python
result = chat_assistant.run()

print(f"Total tokens: {result.tokens.total_tokens}")
print(f"Cost: ${result.cost.total_cost}")
```

### Custom Tool Creation

Add your own tools:

```python
class AgentTools:
    # ... existing tools ...

    def run_tests(self) -> str:
        """Run Django tests"""
        stdout, stderr, code = self.execute_bash_command(
            "python manage.py test"
        )
        return stdout if code == 0 else stderr

# Register with description
test_description = {
    "type": "function",
    "name": "run_tests",
    "description": "Run Django test suite",
    "parameters": {...}
}

tools_obj.add_tool(agent_tools.run_tests, test_description)
```

### Multi-Turn Conversations

The agent maintains context across turns:

```
User: Create a Blog model
Agent: [Creates model]

User: Now add a Comment model that references Blog
Agent: [Creates Comment model with ForeignKey to Blog]

User: Add admin interface for both
Agent: [Updates admin.py]
```

---

## Best Practices

### For Agent Prompts

1. **Be Specific**: "Create a Pet model with name, breed, age" is better than "Create a pet thing"

2. **Include Requirements**: Mention UI requirements, validation rules, etc.

3. **One Task at a Time**: For complex projects, break into phases

4. **Provide Context**: If modifying existing code, explain the goal

### For Tool Design

1. **Clear Descriptions**: Tools should have unambiguous descriptions

2. **Safety First**: Block dangerous commands (rm -rf, etc.)

3. **Timeouts**: Prevent hanging on long-running commands

4. **Error Handling**: Return useful error messages

### For Developer Prompts

1. **Set Expectations**: What the agent should and shouldn't do

2. **Provide Context**: Project structure, conventions, constraints

3. **Give Examples**: Show the desired behavior

4. **Define Workflow**: Step-by-step process the agent should follow

---

## Troubleshooting

### Common Issues

**Issue: Agent keeps reading the same file**
- **Cause**: Circular reasoning or unclear instructions
- **Solution**: Provide more specific guidance in user prompt

**Issue: Agent creates incorrect code**
- **Cause**: Insufficient context or unclear requirements
- **Solution**: Improve developer prompt with better examples and guidelines

**Issue: Commands timeout**
- **Cause**: Long-running command (migrations on large DB)
- **Solution**: Increase timeout in `execute_bash_command` or run manually

**Issue: Agent doesn't use tools**
- **Cause**: Tool descriptions unclear or model doesn't see relevance
- **Solution**: Improve tool descriptions and developer prompt

**Issue: Encoding errors in files**
- **Cause**: Non-UTF-8 files
- **Solution**: Handle encoding errors in `read_file` with `errors='replace'`

### Debug Tips

1. **Print Messages**: Add logging to see what agent is thinking

```python
for msg in chat_assistant.all_messages:
    print(f"{msg.role}: {msg.content[:100]}...")
```

2. **Check Tool Calls**: See what functions agent called

```python
for msg in result.all_messages:
    if hasattr(msg, 'type') and msg.type == 'function_call':
        print(f"Tool: {msg.name}, Args: {msg.arguments}")
```

3. **Validate Output**: Use Django's check command

```bash
cd your-project
python manage.py check
```

4. **Test in Isolation**: Test tools independently before agent integration

```python
agent_tools = AgentTools(Path("test-project"))
content = agent_tools.read_file("models.py")
print(content)
```

---

## Resources

### Documentation
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [ToyAIKit GitHub](https://github.com/alexeygrigorev/toyaikit)
- [Django Documentation](https://docs.djangoproject.com/)

### Templates & Examples
- [Django Template](https://github.com/alexeygrigorev/django_template)
- [Coding Agent Workshop](https://github.com/alexeygrigorev/workshops/tree/main/coding-agent)
- [Pets Store Example](./pets-store/)

### Production-Ready Alternatives
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk) - Official OpenAI framework
- [PydanticAI](https://ai.pydantic.dev/) - Type-safe agent framework
- [LangChain](https://python.langchain.com/) - Comprehensive LLM framework
- [CrewAI](https://www.crewai.com/) - Multi-agent orchestration

### Related Projects
- [Aider](https://aider.chat/) - AI pair programming in terminal
- [GitHub Copilot](https://github.com/features/copilot) - AI code completion
- [Cursor](https://cursor.sh/) - AI-first code editor

---

## Project Structure

```
04-build-django-coding-agent/
├── README.md                   # This file
├── agents.ipynb                # Complete agent implementation notebook
├── tools.py                    # Agent tools (read, write, execute, search)
├── .gitignore                  # Python/Django gitignore
├── django_template/            # Base Django template (cloned)
│   ├── manage.py
│   ├── myapp/
│   ├── myproject/
│   └── templates/
└── pets-store/                 # Example app built by agent
    ├── README.md               # Pets Store documentation
    ├── Makefile                # Convenience commands
    ├── manage.py
    ├── myapp/
    │   ├── models.py           # Pet & Product models
    │   ├── views.py            # View logic
    │   ├── admin.py            # Admin configuration
    │   ├── management/
    │   │   └── commands/
    │   │       └── seed_store.py
    │   └── templates/          # Beautiful TailwindCSS templates
    └── myproject/
        ├── settings.py
        └── urls.py
```

---

## Next Steps

1. **Experiment**: Try building different types of Django apps
2. **Extend Tools**: Add more capabilities (git operations, API calls, etc.)
3. **Improve Prompts**: Refine developer prompt for better results
4. **Add Safety**: Implement code review and validation layers
5. **Production**: Migrate to production-ready frameworks (OpenAI Agents SDK)

---

## Contributing

Contributions are welcome! Areas for improvement:

- Additional agent tools
- Better error handling
- Code validation/linting integration
- Test generation capabilities
- Documentation generation
- Git integration for version control

---

## License

This project is for educational purposes. Use the concepts and code freely for learning and experimentation.

---

## Acknowledgments

- [Alexey Grigorev](https://github.com/alexeygrigorev) for ToyAIKit and Django template
- [DataTalks.Club](https://datatalks.club/) for AI Dev Tools Zoomcamp
- OpenAI for the Responses API and function calling capabilities

---

**Built with ❤️ for AI Dev Tools Zoomcamp Week 4**
