---
title: Command Line Options
description: Command line option reference for fast-agent MCP applications
---

# Command Line Options

**fast-agent** offers flexible command line options for both running agent applications and using built-in CLI utilities.

## Agent Applications

When running a **fast-agent** application (typically `uv run agent.py`), you have access to the following command line options:

| Option | Description | Example |
|--------|-------------|---------|
| `--model MODEL` | Override the default model for the agent | `--model gpt-4o` |
| `--agent AGENT` | Specify which agent to use (default: "default") | `--agent researcher` |
| `-m, --message MESSAGE` | Send a single message to the agent and exit | `--message "Hello world"` |
| `-p, --prompt-file FILE` | Load and apply a prompt file | `--prompt-file conversation.txt` |
| `--quiet` | Disable progress display, tool and message logging | `--quiet` |
| `--version` | Show version and exit | `--version` |
| `--server` | Run as an MCP server | `--server` |
| `--transport {http,sse,stdio}` | Transport protocol when running as server | `--transport http` |
| `--port PORT` | Port for SSE server (default: 8000) | `--port 8080` |
| `--host HOST` | Host for SSE server (default: 0.0.0.0) | `--host localhost` |

### Examples

```bash
# Run interactively with specified model
uv run agent.py --model sonnet

# Run specific agent
uv run agent.py --agent researcher

# Run with specific agent and model
uv run agent.py --agent researcher --model gpt-4o

# Send a message to an agent and exit
uv run agent.py --agent summarizer --message "Summarize this document"

# Apply a prompt file
uv run agent.py --prompt-file my_conversation.txt

# Run as an SSE server on port 8080
uv run agent.py --server --transport sse --port 8080

# Run as a stdio server
uv run agent.py --server --transport stdio

# Get minimal output (for scripting)
uv run agent.py --quiet --message "Generate a report"
```

### Programmatic Control of Command Line Parsing

When embedding FastAgent in other applications (like web frameworks or GUI applications), you can disable command line parsing by setting `parse_cli_args=False` in the constructor:

```python
# Create FastAgent without parsing command line arguments
fast = FastAgent("Embedded Agent", parse_cli_args=False)
```

This is particularly useful when:
- Integrating with frameworks like FastAPI/Uvicorn that have their own argument parsing
- Building GUI applications where command line arguments aren't relevant
- Creating applications with custom argument parsing requirements


## fast-agent go Command

The `fast-agent go` command lets you run an interactive agent directly without creating a Python file. Read the guide [here](go_command.md)

## fast-agent check Command

Use `fast-agent check` to diagnose your configuration:

```bash
# Show configuration summary
fast-agent check

# Display configuration file
fast-agent check show

# Display secrets file
fast-agent check show --secrets
```

## fast-agent setup Command

Create a new agent project with configuration files:

```bash
# Set up in current directory
fast-agent setup

# Set up in a specific directory
fast-agent setup --config-dir ./my-agent

# Force overwrite existing files
fast-agent setup --force
```

## fast-agent quickstart Command

Create example applications to get started quickly:

```bash
# Show available examples
fast-agent quickstart

# Create workflow examples
fast-agent quickstart workflow .

# Create researcher example
fast-agent quickstart researcher .

# Create data analysis example
fast-agent quickstart data-analysis .

# Create state transfer example
fast-agent quickstart state-transfer .
```