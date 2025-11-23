---
title: FastAgent Class Reference
description: Detailed reference documentation for programmatic usage of the FastAgent class
---

# fast-agent Class Reference

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

Helper method for checking if server mode was requested. Returns `True` if server mode was triggered via `--transport` (or the legacy `--server` flag).
`--transport` also implies server mode for direct CLI runs; `--server` remains as a deprecated alias.

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
    message: Union[str, PromptMessage, PromptMessageExtended],
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
    prompt_content: Union[str, PromptMessage, PromptMessageExtended],
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

See [here](https://github.com/evalstate/fast-agent/tree/main/examples/fastapi) for more examples of using FastAPI with **`fast-agent`**. 

```python title="fastapi-simple.py"
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fast_agent.core.fastagent import FastAgent

# Create FastAgent without parsing CLI args (plays nice with uvicorn)
fast = FastAgent("fast-agent demo", parse_cli_args=False, quiet=True)


# Register a simple default agent via decorator
@fast.agent(name="helper", instruction="You are a helpful AI Agent.", default=True)
async def decorator():
    pass


# Keep FastAgent running for the app lifetime
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with fast.run() as agents:
        app.state.agents = agents
        yield


app = FastAPI(lifespan=lifespan)


class AskRequest(BaseModel):
    message: str


class AskResponse(BaseModel):
    response: str


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    try:
        result = await app.state.agents.send(req.message)
        return AskResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```


## Example: Embedding in a Command-Line Tool

Here's an example of embedding FastAgent in a custom command-line tool:

```python
import asyncio
import argparse
import sys
from fast_agent.core.fastagent import FastAgent

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
3. Use your own command-line arguments in combination with **`fast-agent`**
