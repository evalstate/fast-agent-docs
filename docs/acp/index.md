# Agent Client Protocol

**`fast-agent`** has comprehensive support for Zed Industries [Agent Client Protocol](https://zed.dev/acp). Why use **`fast-agent`**?

- Robust, native LLM Provider infrastructure, with Streaming and Structured outputs.
- Comprehensive MCP and Agent Skills support, including Tool Progress Notifications and Sampling.
- Extend and build custom multi-agent experiences in a few lines of code.
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

### Installing 


 uvx fast-agent-mcp@latest check

