# Agent Client Protocol

**`fast-agent`** has comprehensive support for Zed Industries [Agent Client Protocol](https://zed.dev/acp). Why use **`fast-agent`**?:

- Robust, native LLM Provider infrastructure, with Streaming and Structured outputs.
- Comprehensive MCP and Agent Skills support, including Tool Progress Notifications and Sampling.
- Build custom, multi-agent experiences in a few lines of code.
- Each Agent or Workflow appears as a "Mode" and transmits workflow events to the your ACP Client.

## Getting Started

### No Install Quick Start:
To try it out straight away with your Client, set an API Key environment variable and add:

**Hugging Face**

export HF_TOKEN=hf_.......

`uvx fast-agent-mcp@latest serve --transport acp --model <your_model>` 

**Open AI**

export OPENAI_API_KEY=......

`uvx fast-agent-mcp@latest serve --transport acp --model <your_model>` 

**Anthropic**

export ANTHROPIC_API_KEY=......

`uvx fast-agent-mcp@latest serve --transport acp --model <your_model>` 

Tip: Use `uvx fast-agent-mcp check` to help diagnose issues.

Note: OAuth keys are stored in your keyring, so `check` may prompt to read the credential store.

### Installing 

`uv tool install -U fast-agent-mcp`

Documentation in Progress.

## Shell and File Access

**`fast-agent`** adds the shell tool, read and write tools from the Client to allow "follow-along" functionality.