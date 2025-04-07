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

### Format

Model strings follow this format: `provider.model_name.reasoning_effort`

- **provider**: The LLM provider (e.g., `anthropic`, `openai`, `deepseek`, `generic`)
- **model_name**: The specific model to use in API calls
- **reasoning_effort** (optional): Controls the reasoning effort for supported models

Examples:

- `anthropic.claude-3-7-sonnet-latest`
- `openai.gpt-4o`
- `openai.o3-mini.high`
- `generic.llama3.2:latest`

#### Reasoning Effort

For models that support it (`o1`, `o1-preview` and `o3-mini`), you can specify a reasoning effort of **`high`**, **`medium`** or **`low`** - for example `openai.o3-mini.high`. **`medium`** is the default if not specified.

#### Aliases

For convenience, popular models have an alias set such as `gpt-4o` or `sonnet`. These are documented on the [LLM Providers](llm_providers.md) page.

### Default Configuration

You can set a default model for your application in your `fastagent.config.yaml`:

```yaml
default_model: "openai.gpt-4o" # Default model for all agents
```

### History Saving

You can save the conversation history to a file by sending a `***SAVE_HISTORY <filename>` message. This can then be reviewed, edited, loaded, or served with the `prompt-server` or replayed with the `playback` model.

!!! Note "File Format / MCP Serialization"

    If the filetype is `json`, then messages are serialized/deserialized using the MCP Prompt schema. The `load_prompt`, `load_prompt_multipart` and `prompt-server` will load either the text or JSON format directly.

This can be helpful when developing applications to:

* Save a conversation for editing
* Set up in-context learning
* Produce realistic test scenarios to exercise edge conditions etc. with the [Playback model](internal_models.md#playback)