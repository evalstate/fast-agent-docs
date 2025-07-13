---
title: Configuration Reference
description: Complete reference for fast-agent configuration settings
---

# Configuration Reference

**fast-agent** can be configured through the `fastagent.config.yaml` file, which should be placed in your project's root directory. For sensitive information, you can use `fastagent.secrets.yaml` with the same structure - values from both files will be merged, with secrets taking precedence.

Configuration can also be provided through environment variables, with the naming pattern `SECTION__SUBSECTION__PROPERTY` (note the double underscores).

## Configuration File Location

fast-agent automatically searches for configuration files in the current working directory and its parent directories. You can also specify a configuration file path with the `--config` command-line argument.

## General Settings

```yaml
# Default model for all agents
default_model: "haiku"  # Format: provider.model_name.reasoning_effort

# Whether to automatically enable Sampling. Model seletion precedence is Agent > Default.
auto_sampling: true

# Execution engine (only asyncio is currently supported)
execution_engine: "asyncio"
```

## Model Providers

### Anthropic

```yaml
anthropic:
  api_key: "your_anthropic_key"  # Can also use ANTHROPIC_API_KEY env var
  base_url: "https://api.anthropic.com/v1"  # Optional, only include to override
```

### OpenAI

```yaml
openai:
  api_key: "your_openai_key"  # Can also use OPENAI_API_KEY env var
  base_url: "https://api.openai.com/v1"  # Optional, only include to override
  reasoning_effort: "medium"  # Default reasoning effort: "low", "medium", or "high"
```

### Azure OpenAI

```yaml
# Option 1: Using resource_name and api_key (standard method)
azure:
  api_key: "your_azure_openai_key"  # Required unless using DefaultAzureCredential
  resource_name: "your-resource-name"  # Resource name in Azure
  azure_deployment: "deployment-name"  # Required - deployment name from Azure
  api_version: "2023-05-15"  # Optional API version
  # Do NOT include base_url if you use resource_name

# Option 2: Using base_url and api_key (custom endpoints or sovereign clouds)
# azure:
#   api_key: "your_azure_openai_key"
#   base_url: "https://your-endpoint.openai.azure.com/"
#   azure_deployment: "deployment-name"
#   api_version: "2023-05-15"
#   # Do NOT include resource_name if you use base_url

# Option 3: Using DefaultAzureCredential (for managed identity, Azure CLI, etc.)
# azure:
#   use_default_azure_credential: true
#   base_url: "https://your-endpoint.openai.azure.com/"
#   azure_deployment: "deployment-name"
#   api_version: "2023-05-15"
#   # Do NOT include api_key or resource_name in this mode
```

Important configuration notes:
- Use either `resource_name` or `base_url`, not both.
- When using `DefaultAzureCredential`, do NOT include `api_key` or `resource_name` (the `azure-identity` package must be installed).
- When using `base_url`, do NOT include `resource_name`.
- When using `resource_name`, do NOT include `base_url`.
- The model string format is `azure.deployment-name`

### DeepSeek

```yaml
deepseek:
  api_key: "your_deepseek_key"  # Can also use DEEPSEEK_API_KEY env var
  base_url: "https://api.deepseek.com/v1"  # Optional, only include to override
```

### Google

```yaml
google:
  api_key: "your_google_key"  # Can also use GOOGLE_API_KEY env var
  base_url: "https://generativelanguage.googleapis.com/v1beta/openai"  # Optional
```

### Generic (Ollama, etc.)

```yaml
generic:
  api_key: "ollama"  # Default for Ollama, change as needed
  base_url: "http://localhost:11434/v1"  # Default for Ollama
```

### OpenRouter

```yaml
openrouter:
  api_key: "your_openrouter_key"  # Can also use OPENROUTER_API_KEY env var
  base_url: "https://openrouter.ai/api/v1"  # Optional, only include to override
```

### TensorZero

```yaml
tensorzero:
  base_url: "http://localhost:3000"  # Optional, only include to override
```

See the [TensorZero Quick Start](https://tensorzero.com/docs/quickstart) and the [TensorZero Gateway Deployment Guide](https://www.tensorzero.com/docs/gateway/deployment/) for more information on how to deploy the TensorZero Gateway.

### AWS Bedrock

```yaml
bedrock:
  region: "us-east-1"  # Required - AWS region where Bedrock is available
  profile: "default"   # Optional - AWS profile to use (defaults to "default")
```

AWS Bedrock uses standard AWS authentication through the boto3 credential provider chain. You can configure credentials using:

- **AWS CLI**: Run `aws configure` to set up credentials (AWS SSO recommended for local development)
- **Environment variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` (for temporary credentials)
- **IAM roles**: Use IAM roles when running on EC2 or other AWS services
- **AWS profiles**: Use named profiles with the `profile` setting or `AWS_PROFILE` environment variable

Additional environment variables:
- `AWS_REGION` or `AWS_DEFAULT_REGION`: Override the region setting
- `AWS_PROFILE`: Override the profile setting

The model string format is `bedrock.model-id` (e.g., `bedrock.amazon.nova-lite-v1:0`)

## MCP Server Configuration

MCP Servers are defined under the `mcp.servers` section:

```yaml
mcp:
  servers:
    # Example stdio server
    server_name:
      transport: "stdio"  # "stdio" or "sse"
      command: "npx"  # Command to execute
      args: ["@package/server-name"]  # Command arguments as array
      read_timeout_seconds: 60  # Optional timeout in seconds
      env:  # Optional environment variables
        ENV_VAR1: "value1"
        ENV_VAR2: "value2"
      sampling:  # Optional sampling settings
        model: "haiku"  # Model to use for sampling requests

    # Example Stremable HTTP server
    streambale_http__server:
      transport: "http"
      url: "http://localhost:8000/mcp"
      read_transport_sse_timeout_seconds: 300  # Timeout for HTTP connections
      headers:  # Optional HTTP headers
        Authorization: "Bearer token"
      auth:  # Optional authentication
        api_key: "your_api_key"

    # Example SSE server
    sse_server:
      transport: "sse"
      url: "http://localhost:8000/sse"
      read_transport_sse_timeout_seconds: 300  # Timeout for SSE connections
      headers:  # Optional HTTP headers
        Authorization: "Bearer token"
      auth:  # Optional authentication
        api_key: "your_api_key"


    # Server with roots
    file_server:
      transport: "stdio"
      command: "command"
      args: ["arguments"]
      roots:  # Root directories accessible to this server
        - uri: "file:///path/to/dir"  # Must start with file://
          name: "Optional Name"  # Optional display name for the root
          server_uri_alias: "file:///server/path"  # Optional, for consistent paths
```

## OpenTelemetry Settings

```yaml
otel:
  enabled: false  # Enable or disable OpenTelemetry
  service_name: "fast-agent"  # Service name for tracing
  otlp_endpoint: "http://localhost:4318/v1/traces"  # OTLP endpoint for tracing
  console_debug: false  # Log spans to console
  sample_rate: 1.0  # Sample rate (0.0-1.0)
```

## Logging Settings

```yaml
logger:
  type: "file"  # "none", "console", "file", or "http"
  level: "warning"  # "debug", "info", "warning", or "error"
  progress_display: true  # Enable/disable progress display
  path: "fastagent.jsonl"  # Path to log file (for "file" type)
  batch_size: 100  # Events to accumulate before processing
  flush_interval: 2.0  # Flush interval in seconds
  max_queue_size: 2048  # Maximum queue size for events
  
  # HTTP logger settings
  http_endpoint: "https://logging.example.com"  # Endpoint for HTTP logger
  http_headers:  # Headers for HTTP logger
    Authorization: "Bearer token"
  http_timeout: 5.0  # Timeout for HTTP logger requests
  
  # Console display options
  show_chat: true  # Show chat messages on console
  show_tools: true  # Show MCP Server tool calls on console
  truncate_tools: true  # Truncate long tool calls in display
  enable_markup: true # Disable if outputs conflict with rich library markup
```

## Example Full Configuration

```yaml
default_model: "haiku"
execution_engine: "asyncio"

# Model provider settings
anthropic:
  api_key: API_KEY

openai:
  api_key: API_KEY
  reasoning_effort: "high"

# MCP servers
mcp:
  servers:
    fetch:
      transport: "stdio"
      command: "uvx"
      args: ["mcp-server-fetch"]
      
    prompts:
      transport: "stdio"
      command: "prompt-server"
      args: ["prompts/myprompt.txt"]
      
    filesys:
      transport: "stdio"
      command: "uvx"
      args: ["mcp-server-filesystem"]
      roots:
        - uri: "file://./data"
          name: "Data Directory"

# Logging configuration
logger:
  type: "file"
  level: "info"
  path: "logs/fastagent.jsonl"
```

## Environment Variables

All configuration options can be set via environment variables using a nested delimiter:

```
ANTHROPIC__API_KEY=your_key
OPENAI__API_KEY=your_key
LOGGER__LEVEL=debug
```

Environment variables take precedence over values in the configuration files. For nested arrays or complex structures, use the YAML configuration file.

The `fastagent.config.yaml` file supports referencing environment variables inline using the `${ENV_VAR}` syntax. When the configuration is loaded, any value specified as `${ENV_VAR}` will be automatically replaced with the value of the corresponding environment variable. This allows you to securely inject sensitive or environment-specific values into your configuration files without hardcoding them.

For example:

```yaml
openai:
  api_key: "${OPENAI_API_KEY}"
```

In this example, the `api_key` value will be set to the value of the `OPENAI_API_KEY` environment variable at runtime.

