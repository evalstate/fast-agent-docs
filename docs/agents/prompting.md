# Prompting Agents

## Introduction

**fast-agent** provides a flexible MCP based API for sending messages to Agent, with convenience methods for handling Files, Prompts and Resources. Read more about the use of MCP types in **fast-agent** [here](/mcp/types/).

## Sending Messages

The simplest way of sending a message to an agent is the `send` method:

```python
response: str = await agent.send("how are you?")
```

You can also use the MCP PromptMessage directly:

```python
from mcp.types import PromptMessage, TextContent

mcp_prompt: PromptMessage = PromptMessage(
    role="user", content=TextContent(type="text", text="how are you?")
)
result: str = await agent.send(mcp_prompt)
```

## Multipart Messages

Prompts can contain a mixture of content types (dependent on model support). You can use `Prompt.user()` to easily attach files and resources to your message:

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

`Prompt.user()` also accepts MCP Native types for constructing messages.

This makes working with MCP Resources simple:

```python
resource: ReadResourceResult = agent.openai.get_resource(
    "server_name", "resource://images/cat.png"
)
response: str = agent.haiku.send(
    Prompt.user("What is in this image?", resource)
)
```

Alternatively, there is a convenience method to send a message with a resource:

```python
response: str = agent.haiku.with_resource(
    "What is in this image?",
    "server_name",
    "resource://images/cat/png"
)

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

## Prompt Files
