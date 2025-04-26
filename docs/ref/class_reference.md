---
title: FastAgent Class Reference
description: Detailed reference documentation for programmatic usage of the FastAgent class
---

# FastAgent Class Reference

This document provides detailed reference information for programmatically using the `FastAgent` class, which is the core class for creating and running agent applications.

## FastAgent Class

### Constructor

```python
FastAgent(
    name: str,
    config_path: str | None = None,
    ignore_unknown_args: bool = False,
    parse_cli_args: bool = True
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | (required) | Name of the application |
| `config_path` | `str \| None` | `None` | Optional path to config file. If not provided, config is loaded from default locations |
| `ignore_unknown_args` | `bool` | `False` | Whether to ignore unknown command line arguments when `parse_cli_args` is `True` |
| `parse_cli_args` | `bool` | `True` | Whether to parse command line arguments. Set to `False` when embedding FastAgent in frameworks like FastAPI/Uvicorn that handle their own argument parsing |

### Decorator Methods

The `FastAgent` class provides several decorators for creating agents and workflows:

| Decorator | Description |
|-----------|-------------|
| `@fast.agent()` | Create a basic agent |
| `@fast.chain()` | Create a chain workflow |
| `@fast.router()` | Create a router workflow |
| `@fast.parallel()` | Create a parallel workflow |
| `@fast.evaluator_optimizer()` | Create an evaluator-optimizer workflow |
| `@fast.orchestrator()` | Create an orchestrator workflow |

See [Defining Agents](../agents/defining.md) for detailed usage of these decorators.

### Methods

#### `run()`

```python
async with fast.run() as agent:
    # Use agent here
```

An async context manager that initializes all registered agents and returns an `AgentApp` instance that can be used to interact with the agents.

#### `start_server()`

```python
await fast.start_server(
    transport: str = "sse",
    host: str = "0.0.0.0",
    port: int = 8000,
    server_name: Optional[str] = None,
    server_description: Optional[str] = None
)
```

Starts the application as an MCP server.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `transport` | `str` | `"sse"` | Transport protocol to use ("stdio" or "sse") |
| `host` | `str` | `"0.0.0.0"` | Host address for the server when using SSE |
| `port` | `int` | `8000` | Port for the server when using SSE |
| `server_name` | `Optional[str]` | `None` | Optional custom name for the MCP server |
| `server_description` | `Optional[str]` | `None` | Optional description for the MCP server |

#### `main()`

```python
await fast.main()
```

Helper method for checking if server mode was requested. Returns `True` if the `--server` flag is set, `False` otherwise.

## AgentApp Class

The `AgentApp` class is returned from `fast.run()` and provides access to all registered agents and their capabilities.

### Accessing Agents

There are two ways to access agents in the `AgentApp`:

```python
# Attribute access
response = await agent.agent_name.send("Hello")

# Dictionary access
response = await agent["agent_name"].send("Hello")
```

### Methods

#### `send()`

```python
await agent.send(
    message: Union[str, PromptMessage, PromptMessageMultipart],
    agent_name: Optional[str] = None
) -> str
```

Send a message to the specified agent (or the default agent if not specified).

#### `apply_prompt()`

```python
await agent.apply_prompt(
    prompt_name: str,
    arguments: Dict[str, str] | None = None,
    agent_name: str | None = None
) -> str
```

Apply a prompt template to an agent (default agent if not specified).

#### `with_resource()`

```python
await agent.with_resource(
    prompt_content: Union[str, PromptMessage, PromptMessageMultipart],
    resource_uri: str,
    server_name: str | None = None,
    agent_name: str | None = None
) -> str
```

Send a message with an attached MCP resource.

#### `interactive()`

```python
await agent.interactive(
    agent: str | None = None,
    default_prompt: str = ""
) -> str
```

Start an interactive prompt session with the specified agent.

## Example: Integrating with FastAPI

Here's an example of integrating FastAgent with FastAPI:

```python
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from mcp_agent.core.fastagent import FastAgent

# Create the FastAPI app
app = FastAPI()

# Create the FastAgent instance with parse_cli_args=False to avoid conflicts
fast = FastAgent("API Agent", parse_cli_args=False)

@fast.agent(instruction="You are a helpful API assistant")
async def setup_agent():
    # This function is needed for the decorator but not used directly
    pass

# Shared initialization task
agent_app = None

@app.on_event("startup")
async def startup_event():
    global agent_app
    async with fast.run() as agent:
        agent_app = agent
        # Keep the context manager open for the lifetime of the application
        while True:
            await asyncio.sleep(3600)  # Keep alive

# API endpoint for querying the agent
@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    
    if not agent_app:
        return {"error": "Agent not initialized"}
    
    response = await agent_app.send(question)
    return {"response": response}

# To run: uvicorn your_module:app --host 0.0.0.0 --port 8000
```

This example demonstrates how to:
1. Create a FastAgent instance with `parse_cli_args=False` to avoid conflicts with FastAPI
2. Initialize the agent during application startup
3. Use the agent to respond to API requests

## Example: Embedding in a Command-Line Tool

Here's an example of embedding FastAgent in a custom command-line tool:

```python
import asyncio
import argparse
import sys
from mcp_agent.core.fastagent import FastAgent

# Parse our own arguments first
parser = argparse.ArgumentParser(description="Custom AI Tool")
parser.add_argument("--input", help="Input data for analysis")
parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
args, remaining = parser.parse_known_args()

# Create FastAgent with parse_cli_args=False since we're handling our own args
fast = FastAgent("Embedded Agent", parse_cli_args=False)

@fast.agent(instruction="You are a data analysis assistant")
async def analyze():
    async with fast.run() as agent:
        if not args.input:
            print("Error: --input is required")
            sys.exit(1)
            
        result = await agent.send(f"Analyze this data: {args.input}")
        
        if args.format == "json":
            import json
            print(json.dumps({"result": result}))
        else:
            print(result)

if __name__ == "__main__":
    asyncio.run(analyze())
```

This example shows how to:
1. Parse your application's own arguments using `argparse`
2. Create a FastAgent instance with `parse_cli_args=False`
3. Use your own command-line arguments in combination with FastAgent