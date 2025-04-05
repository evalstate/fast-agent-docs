# Getting Started with FastAgent

This guide will help you install and set up FastAgent, create your first agent, and understand the basic workflow.

## Installation

You can install FastAgent using pip:

```bash
pip install fast-agent-mcp
```

Or using a virtual environment tool like `uv`:

```bash
uv pip install fast-agent-mcp
```

## Setting Up Your Environment

FastAgent requires configuration for API keys and MCP servers. You can either set environment variables or use configuration files.

### Using the CLI to Create a New Project

FastAgent comes with a CLI tool that helps you scaffold a new project:

```bash
fastagent setup
```

This will create the following files in your current directory:
- `fastagent.config.yaml`: Configuration for MCP servers and defaults
- `fastagent.secrets.yaml`: Configuration for API keys
- `agent.py`: A simple example agent
- `.gitignore`: Configured to ignore secrets

### Configuration

Edit `fastagent.secrets.yaml` to add your API keys:

```yaml
# FastAgent Secrets Configuration
# WARNING: Keep this file secure and never commit to version control

anthropic:
  api_key: your-anthropic-api-key

openai:
  api_key: your-openai-api-key
```

Edit `fastagent.config.yaml` to configure MCP servers:

```yaml
# Default model configuration
default_model: haiku  # Alias for Claude 3.5 Haiku

# Logging and Console Configuration
logger:
  progress_display: true
  show_chat: true
  show_tools: true

# MCP Servers
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
```

## Creating Your First Agent

Here's a simple example of creating an agent using the FastAgent framework:

```python
import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("My First Agent")

# Define an agent
@fast.agent(
    instruction="You are a helpful AI assistant with a great sense of humor",
    servers=["fetch"]
)
async def main():
    async with fast.run() as agent:
        # Start an interactive session with the agent
        await agent()

if __name__ == "__main__":
    asyncio.run(main())
```

Save this code as `agent.py` and run it:

```bash
python agent.py
```

This will start an interactive session with your agent that has access to the fetch server for web searches.

## Using Different Models

You can specify different LLM models by using the `model` parameter:

```python
@fast.agent(
    instruction="You are a helpful AI assistant",
    servers=["fetch"],
    model="gpt-4o"  # Use OpenAI's GPT-4o model
)
```

Or by using the command line:

```bash
python agent.py --model=gpt-4o
```

FastAgent supports various models through aliases:
- `haiku`: Claude 3.5 Haiku
- `sonnet`: Claude 3.5 Sonnet
- `opus`: Claude 3 Opus
- `gpt-4o`: OpenAI's GPT-4o
- `o3-mini`: OpenAI's o3-mini

## Next Steps

Now that you have a basic agent running, explore these next steps:

1. Learn how to [compose agents using workflow patterns](patterns/router.md)
2. Add [resource handling](advanced/resource-handling.md) capabilities
3. Integrate [human input](advanced/human-input.md) for interactive agents
4. Create [prompts](advanced/prompt-management.md) for consistent behavior
