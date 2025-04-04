# Files and Resources

## Attaching Files

You can include files in a conversation using Paths:

```python
from mcp_agent.core.prompt import Prompt
from pathlib import Path

plans = agent.send(
    Prompt.user(
        "Summarise this PDF",
        Path("secret-plans.pdf")
    )
)
```

This works for any mime type that can be tokenized by the model.

## MCP Resources

MCP Server resources can be conveniently included in a message with:

```python
description = agent.with_resource(
    "What is in this image?",
    "mcp_image_server",
    "resource://images/cat.png"
)
```

## Prompt Files

Prompt Files can include Resources:

```md title="agent_script.txt"
---USER
Please extract the major colours from this CSS file:
---RESOURCE
index.css
```

They can either be loaded with the `load_prompt_multipart` function, or delivered via the built-in `prompt-server`.
