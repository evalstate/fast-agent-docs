# Prompting Agents

**fast-agent** provides a flexible MCP based API for sending messages to agents, with convenience methods for handling Files, Prompts and Resources.

Read more about the use of MCP types in **fast-agent** [here](/mcp/types/).

## Sending Messages

The simplest way of sending a message to an agent is the `send` method:

```python
response: str = await agent.send("how are you?")
```

Attach files by using the `Prompt.user()` method to construct the message:

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

> Note: use `Prompt.assistant()` to produce messages for the `assistant` role.

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

> If the last message in the conversation is from the `assistant`, it is returned as the response.

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

### Prompt Files

Long prompts can be stored in text files, and loaded with the `load_prompt` utility:

```python
from mcp_agent.mcp.prompts import load_prompt
from mcp.types import PromptMessage

prompt: List[PromptMessage] = load_prompt(Path("two_cities.txt"))
result: str = await agent.send(prompt[0])
```

```markdown title="two_cities.txt"
### The Period

It was the best of times, it was the worst of times, it was the age of
wisdom, it was the age of foolishness, it was the epoch of belief, it was
the epoch of incredulity, ...
```

Prompts files can contain conversations to aid in-context learning or allow you to replay conversations with the Playback LLM:

```markdown title="sizing_conversation.txt"
---USER
the moon
---ASSISTANT
object: MOON
size: 3,474.8
units: KM
---USER
the earth
---ASSISTANT
object: EARTH
size: 12,742
units: KM
---USER
how big is a tiger?
---ASSISTANT
object: TIGER
size: 1.2
units: M
```

Multiple messages (conversations) can be applied with the `generate()` method:

```python
from mcp_agent.mcp.prompts import load_prompt
from mcp.types import PromptMessage

prompt: List[PromptMessage] = load_prompt(Path("sizing_conversation.txt"))
result: PromptMessageMultipart = await agent.generate(prompt)
```

Conversation files can also be used to include resources:

```markdown title="prompt_secret_plans.txt"
---USER
Please review the following documents:
---RESOURCE
secret_plan.pdf
---RESOURCE
repomix.xml
---ASSISTANT
Thank you for those documents, the PDF contains secret plans, and some
source code was attached to achieve those plans. Can I help further?
```

It is usually better (but not necessary) to use `load_prompt_multipart`:

```python
from mcp_agent.mcp.prompts import load_prompt_multipart
from mcp_agent.mcp.PromptMessageMultipart

prompt: List[PromptMessageMultipart] = load_prompt_multipart(Path("prompt_secret_plans.txt"))
result: PromptMessageMultipart = await agent.generate(prompt)
```

!!! Note "File Format / MCP Serialization"

    If the filetype is `json`, then messages are deserialized using the MCP Prompt schema format. The `load_prompt`, `load_prompt_multipart` and `prompt-server` will load either the text or JSON format directly.
    See [History Saving](../models/index.md#history-saving) to learn how to save a conversation to a file for editing or playback.


### Using the MCP prompt-server

Prompt files can also be served using the inbuilt `prompt-server`. The `prompt-server` command is installed with `fast-agent` making it convenient to set up and use:

```yaml title="fastagent.config.yaml"
mcp:
  servers:
    prompts:
      command: "prompt-server"
      args: ["prompt_secret_plans.txt"]
```

This configures an MCP Server that will serve a `prompt_secret_plans` MCP Prompt, and `secret_plan.pdf` and `repomix.xml` as MCP Resources.

If arguments are supplied in the template file, these are also handled by the `prompt-server`

```markdown title="prompt_with_args.txt"
---USER
Hello {{assistant_name}}, how are you?
---ASSISTANT
Great to meet you {{user_name}} how can I be of assistance?
```

<!--
## Structured Outputs

## Multiturn Conversations
-->

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
