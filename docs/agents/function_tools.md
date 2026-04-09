# Function Tools

Function tools let you expose ordinary Python functions to an agent without running a separate MCP server.

They are **local Python tools**, distinct from MCP tools loaded from `servers=[...]`.

## When to use function tools

Use function tools when:

- the logic already lives in your Python application
- you want a lightweight tool without packaging an MCP server
- a tool is specific to one app or one agent

Use MCP tools when you need server-based discovery, reuse across processes, remote access, or the wider MCP ecosystem.

## Global tools with `@fast.tool`

`@fast.tool` registers a local Python function tool globally for the application.

Agents that support local function tools receive these global tools unless they declare their own `function_tools`.

```python
import asyncio

from fast_agent import FastAgent

fast = FastAgent("Function Tools Example")


@fast.tool
def get_weather(city: str) -> str:
    """Return the current weather for a city."""
    return f"Sunny in {city}"


@fast.tool(name="add", description="Add two numbers together")
def add_numbers(a: int, b: int) -> int:
    return a + b


@fast.agent(instruction="You are a helpful assistant with access to tools.")
async def main() -> None:
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
```

## Agent-scoped tools with `@agent.tool`

Use `@agent.tool` when a tool should only be available to one agent.

```python
import asyncio

from fast_agent import FastAgent

fast = FastAgent("Tool Scoping Example")


@fast.agent(
    name="writer",
    instruction="You are a writing assistant with translation and summarization tools.",
    default=True,
)
async def writer() -> None:
    pass


@fast.agent(
    name="analyst",
    instruction="You analyse text. You can only count words.",
)
async def analyst() -> None:
    pass


@writer.tool
def translate(text: str, language: str) -> str:
    """Translate text to the given language."""
    return f"[{language}] {text}"


@writer.tool
def summarize(text: str) -> str:
    """Produce a one-line summary."""
    return f"Summary: {text[:80]}..."


@analyst.tool(name="word_count", description="Count words in text")
def count_words(text: str) -> int:
    """Count the number of words in text."""
    return len(text.split())
```

In this example:

- `writer` sees `translate` and `summarize`
- `analyst` sees `word_count`
- neither agent receives tools scoped to the other

## `function_tools=` in decorators

You can also configure local Python function tools directly:

```python
def add(a: int, b: int) -> int:
    return a + b


@fast.agent(
    name="calculator",
    instruction="You can add numbers.",
    function_tools=[add],
)
async def calculator() -> None:
    pass
```

The `function_tools` list may contain:

- Python callables
- string specs like `"tools.py:helper_name"`
- structured specs with display metadata (commonly used in AgentCards)

### Code-style tool call highlighting

Structured `function_tools` entries can opt into syntax-highlighted tool-call
display in the console/TUI. This is especially useful in AgentCards and
ToolCards.

Supported fields:

- `entrypoint` — Python function entrypoint, for example `tools.py:run_query`
- `variant` — currently only `code`
- `code_arg` — which argument should be rendered as the code body
- `language` — syntax highlighter language, for example `python`, `bash`, `sql`

Example:

```yaml
function_tools:
  - entrypoint: tools.py:run_query
    variant: code
    code_arg: code
    language: python
```

Behavior:

- the argument named by `code_arg` is rendered as highlighted code
- other tool arguments are shown as footer metadata
- if `variant: code` is set and you omit the optional fields, defaults are:
  - `code_arg: code`
  - `language: python`

This affects display only. It does not change how the tool executes or what the
LLM sees.

## Scoping and inheritance rules

Function tool inheritance is intentionally simple:

1. If an agent does **not** declare `function_tools`, it receives global `@fast.tool` tools
2. If an agent uses `@agent.tool`, those scoped tools become its explicit tool set
3. If an agent uses `function_tools=[...]`, only those tools are used
4. If an agent uses `function_tools=[]`, it opts out of global function tools entirely

This means global tools are a fallback, not something that is merged into every agent automatically.

## Naming and descriptions

By default:

- tool name = Python function name
- tool description = function docstring

You can override these with `name=` and `description=`:

```python
@fast.tool(name="sum_numbers", description="Add two integers together")
def add(a: int, b: int) -> int:
    return a + b
```

The same applies to `@agent.tool(...)`.

## Reusing helpers across agents

Agent-scoped registrations keep metadata local to each registration. That means the same helper can be reused with different names or descriptions for different agents:

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

## Sync and async functions

Both sync and async Python functions are supported:

```python
@fast.tool
def sync_tool(value: int) -> int:
    return value * 2


@fast.tool
async def async_tool(value: int) -> int:
    return value * 2
```

## Shell tool highlighting

Shell tool calls are highlighted automatically when tool display is enabled.
For example, `execute` calls are rendered using detected shell syntax (`bash`,
`pwsh`, etc.), and `apply_patch` commands use a specialized preview display
when possible.

## Supported agent types

`@agent.tool` is available on:

- `@fast.agent(...)`
- supported `@fast.custom(...)` agents whose constructor accepts `tools=...`

`@agent.tool` is **not** available on workflow decorators such as:

- `@fast.chain(...)`
- `@fast.router(...)`
- `@fast.parallel(...)`
- `@fast.orchestrator(...)`
- `@fast.maker(...)`

For custom agents, `function_tools=` only works when the custom class accepts a `tools=...` constructor argument. Otherwise, fast-agent raises a configuration error.

## Function tools vs MCP tools

These parameters do different things:

- `servers=[...]` connects an agent to MCP servers
- `tools={...}` filters **MCP tools** by server name
- `resources={...}` filters **MCP resources** by server name
- `prompts={...}` filters **MCP prompts** by server name
- `function_tools=[...]` adds **local Python function tools**

So `tools=` and `function_tools=` are related, but they configure different tool sources.

## Examples

Runnable examples in the main repository:

- [`examples/function-tools/basic.py`](https://github.com/evalstate/fast-agent/blob/main/examples/function-tools/basic.py)
- [`examples/function-tools/scoping.py`](https://github.com/evalstate/fast-agent/blob/main/examples/function-tools/scoping.py)
