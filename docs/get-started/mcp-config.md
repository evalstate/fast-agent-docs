---
title: Configuring MCP Servers
---

# Configuring MCP Servers

Model Context Protocol (MCP) servers provide additional capabilities to your agents, such as access to tools, resources, and prompt templates. This guide will help you configure and use MCP servers with FastAgent.

## Understanding MCP Servers

MCP servers provide several capabilities:

- **Prompts**: Reusable prompt templates
- **Tools**: Functions that can be called by your agents
- **Resources**: External data like images, documents, or databases
- **Sampling**: Text generation services

FastAgent can connect to multiple MCP servers simultaneously, giving your agents access to a wide range of capabilities.

## Configuration File

MCP servers are configured in the `fastagent.config.yaml` file in your project directory:

```yaml
# Basic configuration for FastAgent
default_model: "gpt-4o"  # Default model if not specified on agent

# MCP servers configuration
mcp:
  servers:
    # Prompt server - serves prompt templates from text files
    prompt_server:
      transport: stdio  # Communication method (stdio or sse)
      command: python   # Command to run the server
      args: ["-m", "mcp_agent.mcp.prompts.prompt_server", "prompts/*.txt"]
      
    # Tool server - provides mathematical tools
    math_server:
      transport: stdio
      command: python
      args: ["-m", "math_tools.server"]
      
    # Resource server - provides access to files and images
    resource_server:
      transport: sse    # Server-Sent Events over HTTP
      url: "http://localhost:8000"  # URL for SSE connection
```

### Server Configuration Options

Each server configuration can include:

- `transport`: Communication method (`stdio` or `sse`)
- `command`: Command to run the server (for `stdio`)
- `args`: Arguments for the command (for `stdio`)
- `url`: URL for SSE connection (for `sse`)
- `env`: Environment variables for the server process
- `sampling`: Configuration for sampling capabilities
- `read_timeout_seconds`: Timeout for server responses
- `roots`: Resource root configurations

## Built-in MCP Servers

FastAgent includes several built-in MCP servers:

### Prompt Server

The prompt server serves prompt templates from text files:

```yaml
prompt_server:
  transport: stdio
  command: python
  args: ["-m", "mcp_agent.mcp.prompts.prompt_server", "prompts/*.txt"]
```

This server loads all `.txt` files in the `prompts` directory as prompt templates.

#### Creating Prompt Templates

Prompt templates use a simple delimiter format:

```
---USER
I need you to analyze the following {{language}} code:

{{code}}
---ASSISTANT
Here's my analysis of the {{language}} code:

1. Purpose: 
2. Structure:
3. Potential issues:
```

The template contains variables in double curly braces (`{{variable}}`) that can be filled in when the prompt is applied.

## Connecting to MCP Servers

FastAgent automatically connects to all configured MCP servers when your application starts. You specify which servers an agent can access in its decorator:

```python
@fast.agent(
    name="coder",
    instruction="You are a coding assistant.",
    servers=["prompt_server", "resource_server"]  # Servers this agent can access
)
def code_agent():
    pass
```

## Using MCP Features in Your Agents

### Working with Prompts

```python
# List available prompts
prompts = await agent.list_prompts()
print(prompts)

# Apply a prompt template
result = await agent.apply_prompt(
    "analyze_code",  # Prompt name
    {
        "language": "Python", 
        "code": "print('Hello World')"
    }  # Template variables
)
```

### Working with Resources

```python
# List available resources
resources = await agent.list_resources()
print(resources)

# Use a resource in a prompt
response = await agent.with_resource(
    "Please analyze this image:",  # Text prompt
    "resource://image_server/example.jpg"  # Resource URI
)
```

### Calling Tools

```python
# List available tools
tools = await agent.list_tools()
print(tools)

# Call a tool
result = await agent.call_tool(
    "math_server-calculate",  # Tool name with server prefix
    {"expression": "2 + 2 * 3"}  # Tool arguments
)
```

## Creating a Basic Prompt Server

The simplest way to add capabilities to your agents is through a prompt server. Here's how to set one up:

1. Create a `prompts` directory in your project
2. Add prompt template files (`.txt`) to this directory
3. Configure the prompt server in your config file:

```yaml
mcp:
  servers:
    prompt_server:
      transport: stdio
      command: python
      args: ["-m", "mcp_agent.mcp.prompts.prompt_server", "prompts/*.txt"]
```

4. Access prompts in your agent:

```python
@fast.agent(name="assistant", servers=["prompt_server"])
def main():
    pass

async def run():
    async with fast.run() as agent_app:
        # Apply a prompt template
        result = await agent_app.assistant.apply_prompt(
            "explain_topic",
            {"topic": "quantum computing"}
        )
        print(result)
```

## Advanced: Creating Custom MCP Servers

You can create custom MCP servers to provide specialized tools or resources:

1. Create a new Python file for your server:

```python
# math_tools.py
from mcp.server.fastmcp import FastMCP

app = FastMCP("Math Tools Server")

@app.tool
async def calculate(expression: str) -> float:
    """Calculate the result of a mathematical expression."""
    return eval(expression)

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_stdio_async())
```

2. Configure your server in `fastagent.config.yaml`:

```yaml
mcp:
  servers:
    math_server:
      transport: stdio
      command: python
      args: ["math_tools.py"]
```

3. Use the tool in your agent:

```python
@fast.agent(name="calculator", servers=["math_server"])
def main():
    pass

async def run():
    async with fast.run() as agent_app:
        result = await agent_app.calculator.call_tool(
            "math_server-calculate",
            {"expression": "2 + 2 * 3"}
        )
        print(result)  # Output: 8.0
```

## Troubleshooting MCP Servers

If you encounter issues with MCP servers:

1. **Check Configuration**: Ensure your `fastagent.config.yaml` is correctly formatted.

2. **Verify File Paths**: Make sure the paths to your prompt files or server scripts are correct.

3. **Check Permissions**: Ensure the command has permission to execute.

4. **Monitor Server Output**: FastAgent logs server output to help with debugging.

5. **Test Servers Independently**: You can run MCP servers directly to test them:
   ```bash
   python -m mcp_agent.mcp.prompts.prompt_server prompts/*.txt
   ```

6. **Check for Port Conflicts**: If using SSE transport, ensure the specified port is available.

By properly configuring MCP servers, you can significantly enhance your agents' capabilities with tools, prompts, and resources.