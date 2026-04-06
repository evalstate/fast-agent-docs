# Defining Agents

## Basic Agents

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
  await agent.interactive()
```

Here is the complete `sizer.py` Agent application, with boilerplate code:

```python title="sizer.py"
import asyncio
from fast_agent.core.fastagent import FastAgent

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

The Agent can then be run with `uv run sizer.py`.

Specify a model with the `--model` switch - for example `uv run sizer.py --model sonnet`.

You can also pass a `Path` for the instruction - e.g. 

```python
from pathlib import Path

@fast.agent(
  instruction=Path("./sizing_prompt.md")
)

```

See [Workflows](workflows.md) for chaining, routing, parallelism, orchestrators, and MAKER.

## Human Input

Agents can request Human Input to assist with a task or get additional context:

```python
@fast.agent(
    instruction="An AI agent that assists with basic tasks. Request Human Input when needed.",
    human_input=True,
)

await agent("print the next number in the sequence")
```

In the example `human_input.py`, the agent will prompt the user for additional information to complete the task.

## Function Tools

`fast-agent` supports two kinds of tools:

- **MCP tools** provided by configured servers via `servers=[...]`
- **Local Python function tools** provided directly in your application with `function_tools=`, `@fast.tool`, or `@agent.tool`

Use local function tools when you want to expose ordinary Python functions to an agent without running an MCP server.

### Global function tools with `@fast.tool`

For convenience, `@fast.tool` registers a local Python function tool that is available to agents that support function tools and do **not** declare an explicit `function_tools` list.

```python
from fast_agent import FastAgent

fast = FastAgent("Function Tools Example")


@fast.tool
def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    return f"Sunny in {city}"


@fast.tool(name="add", description="Add two whole numbers")
def add_numbers(a: int, b: int) -> int:
    return a + b


@fast.agent(name="assistant", instruction="You are helpful.")
async def main() -> None:
    pass
```

Both sync and async functions are supported. By default, the tool name comes from the Python function name and the description comes from the function docstring.

### Agent-scoped tools with `@agent.tool`

`@agent.tool` registers a local Python function tool on one specific agent:

```python
@fast.agent(name="writer", instruction="You write and translate text.")
async def writer() -> None:
    pass


@writer.tool
def translate(text: str, language: str) -> str:
    """Translate text to the given language."""
    return f"[{language}] {text}"


@writer.tool(name="summarize", description="Produce a one-line summary")
def summarize_text(text: str) -> str:
    return f"Summary: {text[:80]}..."
```

This is useful when different agents should see different local tools.

### Scoping rules

Function tool scoping is explicit:

- Agents with no explicit `function_tools` receive global `@fast.tool` registrations
- Agents with `@agent.tool` registrations only see their own scoped tools
- Agents with `function_tools=[...]` only see the tools in that list
- Agents with `function_tools=[]` explicitly opt out of global function tools

### Reusing the same helper with different metadata

Per-agent metadata is scoped to each registration, so you can reuse the same helper function across agents with different names or descriptions:

```python
@fast.agent(name="support", instruction="Help support users.")
async def support() -> None:
    pass


@fast.agent(name="billing", instruction="Help billing users.")
async def billing() -> None:
    pass


def lookup_customer(customer_id: str) -> str:
    """Fetch customer details."""
    return f"customer:{customer_id}"


support.tool(name="support_lookup", description="Lookup a support customer")(lookup_customer)
billing.tool(name="billing_lookup", description="Lookup a billing customer")(lookup_customer)
```

### Supported decorators

- `@fast.agent(...)` supports `@agent.tool`
- Some `@fast.custom(...)` agents support local function tools if the custom class constructor accepts `tools=...`
- Workflow decorators such as router, chain, parallel, orchestrator, and maker do **not** expose `.tool`

If a custom agent class does not accept `tools=...`, using `function_tools=` with that class raises a configuration error.

For more examples, see:

- [`examples/function-tools/basic.py`](https://github.com/evalstate/fast-agent/blob/main/examples/function-tools/basic.py)
- [`examples/function-tools/scoping.py`](https://github.com/evalstate/fast-agent/blob/main/examples/function-tools/scoping.py)
- [Function Tools](function_tools.md)

## Agent and Workflow Reference

### Calling Agents

All definitions allow omitting the name and instructions arguments for brevity:

```python
@fast.agent("You are a helpful agent")          # Create an agent with a default name.
@fast.agent("greeter","Respond cheerfully!")    # Create an agent with the name "greeter"

moon_size = await agent("the moon")             # Call the default (first defined agent) with a message

result = await agent.greeter("Good morning!")   # Send a message to an agent by name using dot notation
result = await agent.greeter.send("Hello!")     # You can call 'send' explicitly

agent["greeter"].send("Good Evening!")          # Dictionary access to agents is also supported
```

Read more about prompting agents [here](prompting.md)

## Configuring Agent Request Parameters

You can customize how an agent interacts with the LLM by passing `request_params=RequestParams(...)` when defining it.

### Example

```python
from fast_agent.types import RequestParams

@fast.agent(
  name="CustomAgent",                              # name of the agent
  instruction="You have my custom configurations", # base instruction for the agent
  request_params=RequestParams(
    maxTokens=8192,
    use_history=False,
    max_iterations=20
  )
)
```

### Available RequestParams Fields

| Field                 | Type     | Default | Description                                                                |
| --------------------- | -------- | ------- | -------------------------------------------------------------------------- |
| `maxTokens`           | `int`    | `2048`  | The maximum number of tokens to sample, as requested by the server         |
| `model`               | `string` | `None`  | The model to use for the LLM generation. Can only be set at Agent creation time                                    |
| `use_history`         | `bool`   | `True`  | Agent/LLM maintains conversation history. Does not include applied Prompts                        |
| `max_iterations`      | `int`    | `99`    | The maximum number of tool calls allowed in a conversation turn                        |
| `parallel_tool_calls` | `bool`   | `True`  | Whether to allow simultaneous tool calls   |
| `response_format`     | `Any`    | `None`  | Response format for structured calls (advanced use). Prefer to use `structured` with a Pydantic model instead                |
| `template_vars` | `Dict[str,Any]` | `{}` | Dictionary of template values for dynamic templates. Currently only supported for TensorZero provider |
| `mcp_metadata` | `Optional[Dict[str,Any]]` | `None` | Metadata to pass through to MCP tool calls via the _meta field |
| `temperature` | `float` | `None` | Temperature to use for the completion request |



### Defining Agents

#### Basic Agent

```python
@fast.agent(
  name="agent",                          # name of the agent
  instruction="You are a helpful Agent", # base instruction for the agent
  servers=["filesystem"],                # list of MCP Servers for the agent
  #tools={"filesystem": ["tool_1", "tool_2"]}  # Filter MCP tools by server. Defaults to all
  #resources={"filesystem": ["resource_1", "resource_2"]}  # Filter MCP resources by server. Defaults to all
  #prompts={"filesystem": ["prompt_1", "prompt_2"]}  # Filter MCP prompts by server. Defaults to all
  #function_tools=[helper_fn, "tools.py:other_helper"],  # Local Python function tools for this agent
  model="o3-mini.high",                  # specify a model for the agent
  use_history=True,                      # agent maintains chat history
  request_params=RequestParams(temperature= 0.7), # additional parameters for the LLM (or RequestParams())
  human_input=True,                      # agent can request human input
  elicitation_handler=ElicitationFnT,    # custom elicitation handler (from mcp.client.session)
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```

Workflow definitions (chain/parallel/router/orchestrator/maker) are documented on the [Workflows](workflows.md) page.

#### Custom

```python
@fast.custom(
  cls=Custom,                            # agent class
  name="custom",                         # name of the custom agent
  instruction="instruction",             # base instruction for the orchestrator
  servers=["filesystem"],                # list of MCP Servers for the agent
  #tools={"filesystem": ["tool_1", "tool_2"]}  # Filter MCP tools by server. Defaults to all
  #resources={"filesystem": ["resource_1", "resource_2"]}  # Filter MCP resources by server. Defaults to all
  #prompts={"filesystem": ["prompt_1", "prompt_2"]}  # Filter MCP prompts by server. Defaults to all
  #function_tools=[helper_fn],            # Local Python function tools, if Custom accepts tools=...
  model="o3-mini.high",                  # specify a model for the agent
  use_history=True,                      # agent maintains chat history
  request_params=RequestParams(temperature= 0.7), # additional parameters for the LLM (or RequestParams())
  human_input=True,                      # agent can request human input
  elicitation_handler=ElicitationFnT,    # custom elicitation handler (from mcp.client.session)
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```
