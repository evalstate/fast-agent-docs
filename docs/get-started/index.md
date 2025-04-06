---
title: Installation
---

# Getting Started

This guide will help you get up and running quickly with the core features of **fast-agent**.

## Installation

Start by installing the [uv package manager](https://docs.astral.sh/uv/) for Python. Then:

```bash
uv pip install fast-agent-mcp    # install fast-agent!

fast-agent setup                 # create an example agent and config files
uv run agent.py                  # run your first agent
```

After running setup, either edit the `fastagent.secrets.yaml` file to enter your LLM API keys, or set the appropriate environment variables. Read more about model configuration [here](/models/). 

<!-- 
fast-agent bootstrap workflow    # create "building effective agents" examples

Other bootstrap examples include a Researcher Agent (with Evaluator-Optimizer workflow) and Data Analysis Agent (similar to the ChatGPT experience), demonstrating MCP Roots support. -->

### Basic Agents

Defining an agent is as simple as:

```python
@fast.agent(
  instruction="Given an object, respond only with an estimate of its size."
)
```

We can then send messages to the Agent:

```python
async with fast.run() as agent:
  moon_size = await agent("the moon")
  print(moon_size)
```

Or start an interactive chat with the Agent:

```python
async with fast.run() as agent:
  await agent()
```

Here is the complete `sizer.py` Agent application, with boilerplate code:

```python
import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Agent Example")

@fast.agent(
  instruction="Given an object, respond only with an estimate of its size."
)
async def main():
  async with fast.run() as agent:
    await agent()

if __name__ == "__main__":
    asyncio.run(main())
```


!!! note

    Windows Users - there are a couple of configuration changes needed for the Filesystem and Docker MCP Servers - necessary changes are detailed within the configuration files.



The Agent can then be run with `uv run sizer.py`.

Specify a model with the `--model` switch - for example `uv run sizer.py --model sonnet`.

Start by installing the [uv package manager](https://docs.astral.sh/uv/) for Python.

Then from you shell, install [**fast-agent**](https://pypi.org/project/fast-agent-mcp/) from PyPi with:

```bash
uv pip install fast-agent-mcp # install fast-agent!
```

## Running your first agent

Once installed, run `fast-agent setup`. This will create a configuration file, secrets file and

````bash
fast-agent setup              # create an example agent and config files
uv run agent.py               # run your first agent
```

## Creating Your First Agent

FastAgent uses a simple, decorator-based API for creating agents. Here's a minimal example:

```python
from fastagent import FastAgent

# Create an application
fast = FastAgent("my-first-app")

# Define an agent using the decorator
@fast.agent(name="assistant", instruction="You are a helpful AI assistant.")
def main():
    pass

# Run the application
if __name__ == "__main__":
    import asyncio

    async def run():
        async with fast.run() as agent_app:
            # Send a message to the agent
            response = await agent_app.assistant.send("Hello, who are you?")
            print(response)

    asyncio.run(run())
````

## Using the Interactive Console

FastAgent includes a rich interactive console for working with agents. This is great for testing and development:

```python
from fastagent import FastAgent

fast = FastAgent("interactive-demo")

@fast.agent(name="assistant", instruction="You are a helpful AI assistant.")
def main():
    pass

if __name__ == "__main__":
    import asyncio

    async def run():
        async with fast.run() as agent_app:
            # Start an interactive session with the agent
            await agent_app.interactive(agent_name="assistant")

    asyncio.run(run())
```

The interactive console supports:

- Multi-line input (toggle with `Ctrl+T`)
- Command history (navigate with up/down arrows)
- Command completion
- Agent switching with `@agent_name`
- Special commands:
  - `/help` - Show available commands
  - `/clear` - Clear the screen
  - `/agents` - List available agents
  - `/prompts` - List and select MCP prompts
  - `/prompt <name>` - Apply a specific prompt by name

## Configuring Models

You can specify which model to use when creating an agent:

```python
@fast.agent(
    name="assistant",
    instruction="You are a helpful AI assistant.",
    model="gpt-4o"  # Use OpenAI's GPT-4o model
)
def main():
    pass
```

FastAgent supports multiple LLM providers including:

- OpenAI (gpt-4o, gpt-3.5-turbo, etc.)
- Anthropic (claude-3-5-sonnet, claude-3-opus, etc.)
- Open source models through Ollama (llama3, mistral, etc.)

## Working with MCP Servers

### Configuration

Create a `fastagent.config.yaml` file in your project directory:

```yaml
# MCP servers configuration
mcp:
  servers:
    prompt_server:
      transport: stdio
      command: python
      args: ["-m", "mcp_agent.mcp.prompts.prompt_server", "prompts/*.txt"]
```

This configuration sets up an MCP server that can serve prompt templates from text files.

### Using Prompts

Once you've configured an MCP server for prompts, you can use them in your agents:

```python
async def run():
    async with fast.run() as agent_app:
        # List available prompts
        prompts = await agent_app.assistant.list_prompts()
        print(prompts)

        # Apply a prompt template
        result = await agent_app.assistant.apply_prompt(
            "analyze_code",  # Prompt name
            {"language": "Python", "code": "print('Hello World')"}  # Template variables
        )
        print(result)
```

### Accessing Resources

MCP servers can also provide resources like images, documents, or other data:

```python
async def run():
    async with fast.run() as agent_app:
        # List available resources
        resources = await agent_app.assistant.list_resources()
        print(resources)

        # Use a resource in a prompt
        response = await agent_app.assistant.with_resource(
            "Please analyze this image:",  # Text prompt
            "resource://image_server/example.jpg"  # Resource URI
        )
        print(response)
```

## Agent Composition

FastAgent shines when composing multiple agents into workflows. Here's a simple example with two agents:

```python
from fastagent import FastAgent

fast = FastAgent("composition-demo")

@fast.agent(name="researcher", instruction="You research facts and provide accurate information.")
def researcher():
    pass

@fast.agent(name="writer", instruction="You write engaging content based on information.")
def writer():
    pass

async def run():
    async with fast.run() as agent_app:
        # First get research from the researcher
        research = await agent_app.researcher.send("Provide facts about quantum computing")

        # Then have the writer create content based on the research
        content = await agent_app.writer.send(f"Write a blog post based on this research: {research}")

        print(content)
```

## Next Steps

Now that you have a basic understanding of FastAgent, you can explore:

- [Advanced Agent Types](../agents/architecture.md) - Learn about router, chain, orchestrator patterns
- [MCP Integration](../mcp/index.md) - Dive deeper into working with MCP servers
- [Model Configuration](../models/index.md) - Learn more about configuring different LLM providers

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure you've set the appropriate environment variables for your LLM provider:

   ```bash
   export OPENAI_API_KEY=your_key_here
   # Or for Anthropic
   export ANTHROPIC_API_KEY=your_key_here
   ```

2. **MCP Server Connection**: If you're having trouble connecting to an MCP server, check:

   - Server configuration in `fastagent.config.yaml`
   - Server logs for errors
   - Network connectivity if using remote servers

3. **Model Availability**: Ensure you're using a model that's available to you. If you don't have access to a specific model, try using an alternative:
   ```python
   @fast.agent(name="assistant", model="gpt-3.5-turbo")  # Fallback to a more accessible model
   ```

For more help, check the [documentation](https://fast-agent.ai) or raise an issue on our [GitHub repository](https://github.com/evalstate/fast-agent).
