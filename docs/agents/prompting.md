# Prompting Agents

**fast-agent** provides a flexible MCP based API for sending messages to agents, with convenience methods for handling Files, Prompts and Resources.

Read more about the use of MCP types in **fast-agent** [here](/mcp/types/).

## Sending Messages

The simplest way of sending a message to an agent is the `send` method:

```python
response: str = await agent.send("how are you?")
```

To attach files, use `Prompt.user()`:

```python
from mcp_agent.core.prompt import Prompt
from pathlib import Path

plans: str = await agent.send(
    Prompt.user(
        "Summarise this PDF",
        Path("secret-plans.pdf")
    )
)
```

Attached files are converted to the appropriate MCP Type (e.g. ImageContent for Images, EmbeddedResource for PDF and TextResource).

> Note there is also `Prompt.assistant()` which produces messages for the `assistant` role.

### MCP Prompts

Apply a Prompt from an MCP Server to the agent with:

```python
response: str = await agent.apply_prompt(
    "setup_sizing",
    arguments: {"units","metric"}
)
```

You can list and get Prompts from attached MCP Servers:
```python
from mcp.types import GetPromptResult, PromptMessage

prompt: GetPromptResult = await agent.get_prompt("setup_sizing")
first_message: PromptMessage = prompt[0]
```

and send the native MCP `PromptMessage` to the agent with:
```python
response: str = agent.send(first_message)
```

> If the last message in the conversation is from the `assistant`, that content is returned as the response.

### MCP Resources

You can use `Prompt.user` to work with MCP Resources:

```python
from mcp.types import ReadResourceResult

resource: ReadResourceResult = agent.get_resource(
    "mcp_server_name", "resource://images/cat.png"
)
response: str = agent.send(
    Prompt.user("What is in this image?", resource)
)
```

Alternatively, use the _with_resource_ convenience method:

```python
response: str = agent.with_resource(
    "What is in this image?",
    "mcp_server_name",
    "resource://images/cat.png"
)

```

## Structured Outputs



## Multiturn Conversations

<!-- make this a table generated from the mime type logic? -->

<!--

from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart

# Create conversation history

messages = [
Prompt.user("What is the capital of France?"),
Prompt.assistant("The capital of France is Paris."),
Prompt.user("And what is its population?")
]

# Send all messages at once

response = await agent.generate(messages, None)
print(response.first_text())

The generate() method provides more control over the conversation flow and returns a PromptMessageMultipart object with the full model
response.

```

```

-->
