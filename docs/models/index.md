# Models

## Specifying Models

Models in fast-agent are specified using a model string, that takes the format `provider.model_name.<reasoning_effort>`

### Precedence

Model specifications in fast-agent follow this precedence order (highest to lowest):

1. Command line arguments with `--model` flag
2. Explicitly set in agent decorators
3. Configuration in `fastagent.config.yaml`
4. Default model configured in the application

### Format

Model strings follow this format: `provider.model_name.reasoning_effort`

- **provider**: The LLM provider (e.g., `anthropic`, `openai`, `deepseek`, `generic`)
- **model_name**: The specific model to use
- **reasoning_effort** (optional): Controls the reasoning effort (`low`, `high`) for supported models

Examples:
- `anthropic.claude-3-5-sonnet`
- `openai.gpt-4o`
- `openai.o3-mini.high`
- `generic.llama3:latest`

### Reasoning Effort

For models that support it, you can specify a reasoning effort:

- **high**: More thorough reasoning, typically resulting in more detailed, accurate responses
- **low**: Less thorough reasoning, typically faster but potentially less detailed

Example: `openai.o3-mini.high`

## Parameters

For each model provider, you can configure parameters either through environment variables or in your `fastagent.config.yaml` file.

### Common Configuration Format

In your `fastagent.config.yaml`:

```yaml
models:
  <provider>:
    api_key: "your_api_key"  # Override with API_KEY env var
    base_url: "https://api.example.com"  # Base URL for API calls
    timeout_seconds: 60  # Request timeout in seconds
```

## Providers

### Anthropic

Anthropic's Claude models provide strong reasoning and instruction-following capabilities.

**YAML Configuration:**
```yaml
models:
  anthropic:
    api_key: "your_anthropic_key"
    base_url: "https://api.anthropic.com"  # Default, rarely needs changing
    timeout_seconds: 60
```

**Environment Variables:**
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `ANTHROPIC_BASE_URL`: Override the API endpoint

**Model Name Aliases:**
- `claude`: Maps to `claude-3-5-sonnet-20240620`
- `claude-3-haiku`: Maps to `claude-3-haiku-20240307`
- `claude-3-opus`: Maps to `claude-3-opus-20240229`
- `claude-3-sonnet`: Maps to `claude-3-sonnet-20240229`
- `claude-3-5-sonnet`: Maps to `claude-3-5-sonnet-20240620`

### OpenAI

fast-agent supports OpenAI's GPT-4o and o1/o3 series models with full tool calling capabilities.

**YAML Configuration:**
```yaml
models:
  openai:
    api_key: "your_openai_key"
    base_url: "https://api.openai.com/v1"  # Default OpenAI endpoint
    timeout_seconds: 60
```

**Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_BASE_URL`: Override the API endpoint

**Model Name Aliases:**
- `gpt-4`: Maps to `gpt-4-turbo-preview`
- `gpt-4o`: Maps to `gpt-4o-2024-05-13`
- `o1`: Maps to `o1-preview`
- `o1-mini`: Maps to `o1-mini-2024-07-18`
- `o3`: Maps to `o3`
- `o3-mini`: Maps to `o3-mini`

### DeepSeek

DeepSeek offers cost-effective models with strong capabilities.

**YAML Configuration:**
```yaml
models:
  deepseek:
    api_key: "your_deepseek_key"
    base_url: "https://api.deepseek.com/v1"
    timeout_seconds: 60
```

**Environment Variables:**
- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `DEEPSEEK_BASE_URL`: Override the API endpoint

**Model Names:**
- `deepseek-chat`
- `deepseek-coder`

### Generic OpenAI LLM

!!! warning

    Use the Generic Provider to connect to OpenAI compatible models (including Ollama).
    Tool Calling and other modalities for generic models are not included in the e2e test suite, and should be used at your own risk.

Models prefixed with `generic` will use a generic OpenAI endpoint, with the defaults configured to work with Ollama. For example, to run with Llama 3.2 latest you can specify `generic.llama3.2:latest`. 

**YAML Configuration:**
```yaml
models:
  generic:
    api_key: "ollama"  # Default for Ollama, change as needed
    base_url: "http://localhost:11434/v1"  # Default for Ollama
    timeout_seconds: 60
```

**Environment Variables:**
- `GENERIC_API_KEY`: Your API key (defaults to `ollama` for Ollama)
- `GENERIC_BASE_URL`: Override the API endpoint

**Usage with Ollama:**
If you're using `ollama serve`, you can use any model available in Ollama by specifying:
```
generic.model_name
```

For example: `generic.llama3:latest` or `generic.mistral:latest`

**Usage with other OpenAI API compatible providers:**
By configuring the `base_url` and appropriate `api_key`, you can connect to any OpenAI API-compatible provider, such as:

- Self-hosted models (LM Studio, vLLM, etc.)
- Azure OpenAI Services
- Other providers with OpenAI-compatible APIs

## Default Configuration

You can set a default model for your application in your `fastagent.config.yaml`:

```yaml
default_model: "openai.gpt-4o"  # Default model for all agents
```
