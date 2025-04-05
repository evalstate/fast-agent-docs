# Prompting Agents

**fast-agent** provides a flexible MCP based API for sending messages to agents, with convenience methods for handling Files, Prompts and Resources.

Read more about the use of MCP types in **fast-agent** [here](/mcp/types/).

## Sending Messages

The simplest way of sending a message to an agent is the `send` method:

```python
response: str = await agent.send("how are you?")
```

To attach files, use the `Prompt.user()` convenience method:

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

### MCP Resources

`Prompt.user` also works with MCP Resources:

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

### MCP Prompts

You can also use the MCP `PromptMessage` type directly:

```python
from mcp.types import PromptMessage, TextContent

mcp_prompt: PromptMessage = PromptMessage(
    role="user", content=TextContent(type="text", text="how are you?")
)
result: str = await agent.send(mcp_prompt)
```

> Note there is also `Prompt.assistant()` which produces a `PromptMessageMultipart` for the assistant role.

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
