---
title: Model Features and History Saving
---

# Model Features and History Saving

Models in **fast-agent** are specified with a model string, that takes the format `provider.model_name.<reasoning_effort>`

### Precedence

Model specifications in fast-agent follow this precedence order (highest to lowest):

1. Explicitly set in agent decorators
1. Command line arguments with `--model` flag
1. Default model in `fastagent.config.yaml`
1. `FAST_AGENT_MODEL` environment variable
1. System default (`gpt-5-mini.low`)

### Format

Model strings follow this format: `provider.model_name.reasoning_effort`

- **provider**: The LLM provider (e.g., `anthropic`, `openai`, `azure`, `deepseek`, `generic`,`openrouter`, `tensorzero`)
- **model_name**: The specific model to use in API calls (for Azure, this is your deployment name)
- **reasoning_effort** (optional): Controls the reasoning effort for supported models

Examples:

- `anthropic.claude-4-5-sonnet-latest`
- `openai.gpt-5.2`
- `openai.o3-mini.high`
- `azure.my-deployment`
- `generic.llama3.2:latest`
- `openrouter.google/gemini-2.5-pro-exp-03-25:free`
- `tensorzero.my_tensorzero_function`

#### Reasoning Effort

For models that support it (e.g. `o1`, and `gpt-5` etc), you can specify a reasoning effort of **`high`**, **`medium`** or **`low`** - for example `openai.o3-mini.high`. **`medium`** is the default if not specified.

`gpt-5` class models additionally support a `minimal` reasoning effort.

#### Aliases

For convenience, popular models have an alias set such as `codex` or `sonnet`. These are documented on the [LLM Providers](llm_providers.md) page.

### Default Configuration

You can set a default model for your application in your `fastagent.config.yaml`:

```yaml
default_model: "openai.gpt-4o" # Default model for all agents
```

### History Saving

You can save the conversation history to a file by sending a `***SAVE_HISTORY <filename>` message. This can then be reviewed, edited, loaded, or served with the `prompt-server` or replayed with the `playback` model.

!!! Note "File Format / MCP Serialization"

    If the filetype is `json`, fast-agent saves a `{"messages": [...]}` JSON container. It can contain either MCP `PromptMessage` objects (legacy) or `PromptMessageExtended` objects (preserves tool calls, channels, etc). `fast_agent.load_prompt` and `prompt-server` will load either the text or JSON format directly.

This can be helpful when developing applications to:

* Save a conversation for editing
* Set up in-context learning
* Produce realistic test scenarios to exercise edge conditions etc. with the [Playback model](internal_models.md#playback)
