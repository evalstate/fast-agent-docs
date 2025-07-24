# Defining Agents and Workflows

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

The Agent can then be run with `uv run sizer.py`.

Specify a model with the `--model` switch - for example `uv run sizer.py --model sonnet`.

You can also pass a `Path` for the instruction - e.g. 

```python
from pathlib import Path

@fast.agent(
  instruction=Path("./sizing_prompt.md")
)

```

## Workflows and MCP Servers

_To generate examples use `fast-agent quickstart workflow`. This example can be run with `uv run workflow/chaining.py`. fast-agent looks for configuration files in the current directory before checking parent directories recursively._

Agents can be chained to build a workflow, using MCP Servers defined in the `fastagent.config.yaml` file:

```yaml title="fastagent.config.yaml"
# Example of a STDIO sever named "fetch"
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
```


```python title="social.py"
@fast.agent(
    "url_fetcher",
    "Given a URL, provide a complete and comprehensive summary",
    servers=["fetch"], # Name of an MCP Server defined in fastagent.config.yaml
)
@fast.agent(
    "social_media",
    """
    Write a 280 character social media post for any given text.
    Respond only with the post, never use hashtags.
    """,
)
@fast.chain(
    name="post_writer",
    sequence=["url_fetcher", "social_media"],
)
async def main():
    async with fast.run() as agent:
        # using chain workflow
        await agent.post_writer("http://fast-agent.ai")
```

All Agents and Workflows respond to `.send("message")`. The agent app responds to `.interactive()` to start a chat session.

Saved as `social.py` we can now run this workflow from the command line with:

```bash
uv run workflow/chaining.py --agent post_writer --message "<url>"
```

Add the `--quiet` switch to disable progress and message display and return only the final response - useful for simple automations. 

Read more about running **fast-agent** agents [here](running.md)

## Workflow Types

**fast-agent** has built-in support for the patterns referenced in  Anthropic's [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) paper.

### Chain

The `chain` workflow offers a declarative approach to calling Agents in sequence:

```python

@fast.chain(
  "post_writer",
  sequence=["url_fetcher","social_media"]
)

# we can them prompt it directly:
async with fast.run() as agent:
  await agent.interactive(agent="post_writer")

```

This starts an interactive session, which produces a short social media post for a given URL. If a _chain_ is prompted it returns to a chat with last Agent in the chain. You can switch agents by typing `@agent-name`.

Chains can be incorporated in other workflows, or contain other workflow elements (including other Chains). You can set an `instruction` to describe it's capabilities to other workflow steps if needed.

Chains are also helpful for capturing content before being dispatched by a `router`, or summarizing content before being used in the downstream workflow.

### Human Input

Agents can request Human Input to assist with a task or get additional context:

```python
@fast.agent(
    instruction="An AI agent that assists with basic tasks. Request Human Input when needed.",
    human_input=True,
)

await agent("print the next number in the sequence")
```

In the example `human_input.py`, the Agent will prompt the User for additional information to complete the task.

### Parallel

The Parallel Workflow sends the same message to multiple Agents simultaneously (`fan-out`), then uses the `fan-in` Agent to process the combined content.

```python
@fast.agent("translate_fr", "Translate the text to French")
@fast.agent("translate_de", "Translate the text to German")
@fast.agent("translate_es", "Translate the text to Spanish")

@fast.parallel(
  name="translate",
  fan_out=["translate_fr","translate_de","translate_es"]
)

@fast.chain(
  "post_writer",
  sequence=["url_fetcher","social_media","translate"]
)
```

If you don't specify a `fan-in` agent, the `parallel` returns the combined Agent results verbatim.

`parallel` is also useful to ensemble ideas from different LLMs.

When using `parallel` in other workflows, specify an `instruction` to describe its operation.

### Evaluator-Optimizer

Evaluator-Optimizers combine 2 agents: one to generate content (the `generator`), and the other to judge that content and provide actionable feedback (the `evaluator`). Messages are sent to the generator first, then the pair run in a loop until either the evaluator is satisfied with the quality, or the maximum number of refinements is reached. The final result from the Generator is returned.

If the Generator has `use_history` off, the previous iteration is returned when asking for improvements - otherwise conversational context is used.

```python
@fast.evaluator_optimizer(
  name="researcher",
  generator="web_searcher",
  evaluator="quality_assurance",
  min_rating="EXCELLENT",
  max_refinements=3
)

async with fast.run() as agent:
  await agent.researcher.send("produce a report on how to make the perfect espresso")
```

When used in a workflow, it returns the last `generator` message as the result.

See the `evaluator.py` workflow example, or `fast-agent quickstart researcher` for a more complete example.

### Router

Routers use an LLM to assess a message, and route it to the most appropriate Agent. The routing prompt is automatically generated based on the Agent instructions and available Servers.

```python
@fast.router(
  name="route",
  agents=["agent1","agent2","agent3"]
)
```

NB - If only one agent is supplied to the router, it forwards directly.

Look at the `router.py` workflow for an example.

### Orchestrator

Given a complex task, the Orchestrator uses an LLM to generate a plan to divide the task amongst the available Agents. The planning and aggregation prompts are generated by the Orchestrator, which benefits from using more capable models. Plans can either be built once at the beginning (`plantype="full"`) or iteratively (`plantype="iterative"`).

```python
@fast.orchestrator(
  name="orchestrate",
  agents=["task1","task2","task3"]
)
```

See the `orchestrator.py` or `agent_build.py` workflow example.

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
from mcp_agent.core.request_params import RequestParams

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
| `max_iterations`      | `int`    | `20`    | The maximum number of tool calls allowed in a conversation turn                        |
| `parallel_tool_calls` | `bool`   | `True`  | Whether to allow simultaneous tool calls   |
| `response_format`     | `Any`    | `None`  | Response format for structured calls (advanced use). Prefer to use `structured` with a Pydantic model instead                |
| `template_vars` | `Dict[str,Any]` | `{}` | Dictionary of template values for dynamic templates. Currently only supported for TensorZero provider |
| `temperature` | `float` | `None` | Temperature to use for the completion request |



### Defining Agents

#### Basic Agent

```python
@fast.agent(
  name="agent",                          # name of the agent
  instruction="You are a helpful Agent", # base instruction for the agent
  servers=["filesystem"],                # list of MCP Servers for the agent
  #tools={"filesystem": ["tool_1", "tool_2"]  # Filter the tools available to the agent. Defaults to all
  #resources={"filesystem: ["resource_1", "resource_2"]} # Filter the resources available to the agent. Defaults to all
  #prompts={"filesystem": ["prompt_1", "prompt_2"]}  # Filter the prompts available to the agent. Defaults to all.
  model="o3-mini.high",                  # specify a model for the agent
  use_history=True,                      # agent maintains chat history
  request_params=RequestParams(temperature= 0.7), # additional parameters for the LLM (or RequestParams())
  human_input=True,                      # agent can request human input
  elicitation_handler=ElicitationFnT,    # custom elicitation handler (from mcp.client.session)
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```

#### Chain

```python
@fast.chain(
  name="chain",                          # name of the chain
  sequence=["agent1", "agent2", ...],    # list of agents in execution order
  instruction="instruction",             # instruction to describe the chain for other workflows
  cumulative=False,                      # whether to accumulate messages through the chain
  continue_with_final=True,              # open chat with agent at end of chain after prompting
)
```

#### Parallel

```python
@fast.parallel(
  name="parallel",                       # name of the parallel workflow
  fan_out=["agent1", "agent2"],          # list of agents to run in parallel
  fan_in="aggregator",                   # name of agent that combines results (optional)
  instruction="instruction",             # instruction to describe the parallel for other workflows
  include_request=True,                  # include original request in fan-in message
)
```

#### Evaluator-Optimizer

```python
@fast.evaluator_optimizer(
  name="researcher",                     # name of the workflow
  generator="web_searcher",              # name of the content generator agent
  evaluator="quality_assurance",         # name of the evaluator agent
  min_rating="GOOD",                     # minimum acceptable quality (EXCELLENT, GOOD, FAIR, POOR)
  max_refinements=3,                     # maximum number of refinement iterations
)
```

#### Router

```python
@fast.router(
  name="route",                          # name of the router
  agents=["agent1", "agent2", "agent3"], # list of agent names router can delegate to
  instruction="routing instruction",     # any extra routing instructions
  servers=["filesystem"],                # list of servers for the routing agent
  #tools={"filesystem": ["tool_1", "tool_2"]  # Filter the tools available to the agent. Defaults to all
  #resources={"filesystem: ["resource_1", "resource_2"]} # Filter the resources available to the agent. Defaults to all
  #prompts={"filesystem": ["prompt_1", "prompt_2"]}  # Filter the prompts available to the agent. Defaults to all
  model="o3-mini.high",                  # specify routing model
  use_history=False,                     # router maintains conversation history
  human_input=False,                     # whether router can request human input
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```

#### Orchestrator

```python
@fast.orchestrator(
  name="orchestrator",                   # name of the orchestrator
  instruction="instruction",             # base instruction for the orchestrator
  agents=["agent1", "agent2"],           # list of agent names this orchestrator can use
  model="o3-mini.high",                  # specify orchestrator planning model
  use_history=False,                     # orchestrator doesn't maintain chat history (no effect).
  human_input=False,                     # whether orchestrator can request human input
  plan_type="full",                      # planning approach: "full" or "iterative"
  max_iterations=5,                      # maximum number of full plan attempts, or iterations
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```

#### Custom

```python
@fast.custom(
  cls=Custom                             # agent class
  name="custom",                         # name of the custom agent
  instruction="instruction",             # base instruction for the orchestrator
  servers=["filesystem"],                # list of MCP Servers for the agent
  MCP Servers for the agent
  #tools={"filesystem": ["tool_1", "tool_2"]  # Filter the tools available to the agent. Defaults to all
  #resources={"filesystem: ["resource_1", "resource_2"]} # Filter the resources available to the agent. Defaults to all
  #prompts={"filesystem": ["prompt_1", "prompt_2"]}  # Filter the prompts available to the agent. Defaults to all
  model="o3-mini.high",                  # specify a model for the agent
  use_history=True,                      # agent maintains chat history
  request_params=RequestParams(temperature= 0.7), # additional parameters for the LLM (or RequestParams())
  human_input=True,                      # agent can request human input
  elicitation_handler=ElicitationFnT,    # custom elicitation handler (from mcp.client.session)
  api_key="programmatic-api-key",        # specify the API KEY programmatically, it will override which provided in config file or env var
)
```

