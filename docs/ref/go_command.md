---
title: fast-agent go command
description: Describes how to use the fast-agent go command to quickly connect to and test MCP Servers, including STDIO, SSE and Streaming support.
---

## `fast-agent go` command

The `go` command allows you to run an interactive agent directly from the command line without
creating a dedicated agent.py file.

### Usage

```bash
fast-agent go [OPTIONS]
```

### Options

- `--name TEXT`: Name for the workflow (default: "FastAgent CLI")
- `--instruction`, `-i <path or url>`: File name or URL for [System Prompt](../agents/instructions.md) (default: "You are a helpful AI Agent.")
- `--config-path`, `-c <path>`: Path to config file
- `--servers <server1>,<server2>`: Comma-separated list of server names to enable from config
- `--url TEXT`: Comma-separated list of HTTP/SSE URLs to connect to directly
- `--auth TEXT`: Bearer token for authorization with URL-based servers
- `--model <model_string>`: Override the default model (e.g., haiku, sonnet, gpt-4)
- `--model <model_string1>,<model_string2>,...`: Set up a `parallel` containing each model
- `--message`, `-m TEXT`: Message to send to the agent (skips interactive mode)
- `--prompt-file`, `-p <path>`: Path to a prompt file to use (either text or JSON)
- `--quiet`: Disable progress display and logging
- `--stdio "<command> <options>"`: Run the command to attach a STDIO server (enclose arguments in quotes)
- `--npx "@package/name <options>"`: Run an NPX package as a STDIO server (enclose arguments in quotes)
- `--uvx "@package/name <options>"`: Run an UVX package as a STDIO server (enclose arguments in quotes)

### Examples

Note - you may omit `go` when supplying command line options.

```bash
# Basic usage with interactive mode
fast-agent go --model=haiku

# Basic usage with interactive mode (go omitted)
fast-agent --model haiku

# Send commands to different LLMs in Parallel
fast-agent --model kimi,gpt-5-mini.low

# Specifying servers from configuration
fast-agent go --servers=fetch,filesystem --model=haiku

# Directly connecting to HTTP/SSE servers via URLs
fast-agent go --url=http://localhost:8001/mcp,http://api.example.com/sse

# Connecting to an authenticated API endpoint
fast-agent go --url=https://api.example.com/mcp --auth=YOUR_API_TOKEN

# Run an NPX package directly
fast-agent --npx @modelcontextprotocol/server-everything 

# Non-interactive mode with a single message
fast-agent go --message="What is the weather today?" --model=haiku

# Using a prompt file
fast-agent go --prompt-file=my-prompt.txt --model=haiku

# Specify a system prompt file
fast-agent go -i my_system_prompt.md

# Specify a skills directory
fast-agent --skills ~/my-skills/

# Provider LLM shell access (use at your own risk)
fast-agent -x

```

### URL Connection Details

The `--url` parameter allows you to connect directly to HTTP or SSE servers using URLs.

- URLs must have http or https scheme
- The transport type is determined by the URL path:
  - URLs ending with `/sse` are treated as SSE transport
  - URLs ending with `/mcp` or automatically appended with `/mcp` are treated as HTTP transport
- Server names are generated automatically based on the hostname, port, and path
- The URL-based servers are added to the agent's configuration and enabled

### Authentication

The `--auth` parameter provides authentication for URL-based servers:

- When provided, it creates an `Authorization: Bearer TOKEN` header for all URL-based servers
- This is commonly used with API endpoints that require authentication
- Example: `fast-agent go --url=https://api.example.com/mcp --auth=12345abcde`