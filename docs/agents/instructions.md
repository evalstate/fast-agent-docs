# Instructions

Agents can have their System Instructions set in a number of flexible ways to make building useful .



When defining an Agent, you can load the instruction as either a `String`, `Path` or `AnyUrl`.

Instructions support embedding the current date, as well as content from other URLs. This is really helpful if you want to refer to files on GitHub, or assemble useful prompts/content in Gists etc.

```python title="Simple String"
@fast.agent(name="example",
    instruction="""
You are a helpful AI Agent.
""")
```

```python title="With current date"
@fast.agent(name="example",
    instruction="""
You are a helpful AI Agent. 
Your reliable knowledge cut-off date is December 2024. 
Todays date is {{currentDate}}.
""")
```

Will produce: `You are a helpful AI Agent. Your reliable knowledge cut-off date is December 2024. Todays date is 25 July 2025.`

```python title="With URL"
@fast.agent(name="mcp-expert",
    instruction="""
You are have expert knowledge of the 
MCP (Model Context Protocol) schema.

{{url:https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/refs/heads/main/schema/2025-06-18/schema.ts}}

Answer any questions about the protocol by referring
to and quoting the schema where necessary.
""")
```

You can store the prompt in an external file for easy editing - including template variables:

```python title="From file"
from pathlib import Path

@fast.agent(name="mcp-expert",
    instruction=Path("./mcp-expert.md"))
""")
```

```md title="mcp-expert.md"
You are have expert knowledge of the MCP (Model Context Protocol) schema.

{{url:https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/refs/heads/main/schema/2025-06-18/schema.ts}}

Answer any questions about the protocol by referring to and quoting the schema where necessary.
Your knowledge cut-off is December 2024, todays date is {{currentDate}}

```

Or you can load the prompt directly from a URL:

```python title="From URL"
from pydantic import AnyUrl

@fast.agent(name="mcp-expert",
    instruction=AnyUrl("https://gist.githubusercontent.com/evalstate/d432921aaaee2c305cf46ae320840360/raw/eb9c7ff93adc780171bfb0ae2560be2178304f16/gistfile1.txt"))

# --> fast-agent system prompt demo
```

You can start an agent with instructions from a file using the `fast-agent` commmand:

```bash
fast-agent --instructions=mcp-expert.md
```

This can be combined with other options to specify model and available servers:

```bash
fast-agent -i mcp-expert.md --model sonnet --url https://hf.co/mcp
```

Starts an interactive agent session, with the MCP Schema loaded, attached to Sonnet with the Hugging Face MCP Server. 

![Instructions](instructions.png)

You can even specify multiple models to directly compare their outputs:

![Instructions Parallel](instructions_parallel.png)

Read more about the `fast-agent` command [here](../ref/go_command.md). 