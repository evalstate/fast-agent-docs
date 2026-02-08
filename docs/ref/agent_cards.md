---
title: AgentCards and ToolCards
description: How fast-agent loads AgentCards as runnable agents vs attached tools, including defaults for agent-cards and tool-cards directories.
---

# AgentCards and ToolCards

## Quick answer

In fast-agent, **ToolCards are AgentCards**. There is no separate card schema.

The distinction is **how cards are loaded**:

- `--agent-cards` (or `--card`) loads cards as runnable agents.
- `--card-tool` loads cards, then attaches those loaded agents as tools to a parent agent.

## Card file format

AgentCards can be Markdown+frontmatter or YAML:

- `.md`
- `.markdown`
- `.yaml`
- `.yml`

## Default directories

By default, `fast-agent go` discovers cards from your environment directory:

- `<env>/agent-cards/`
- `<env>/tool-cards/`

`<env>` defaults to `.fast-agent/` in your current project root.
Use `--env` to point to a different environment directory.
Use `--noenv` to disable implicit default directory discovery entirely.

## Recommended usage

Use `--agent-cards` for agents you want to run directly.

Use `--card-tool` for agents you primarily want to invoke as tools from another agent.

If a card should not appear in normal interactive agent lists, set:

```yaml
tool_only: true
```

## Examples

```bash
# Load runnable agents
fast-agent go --agent-cards ./agents

# Load cards as tools attached to the default/selected agent
fast-agent go --card-tool ./tool-cards

# Mix both
fast-agent go --agent-cards ./agents --card-tool ./tool-cards

# Ephemeral/noenv run: only explicit paths are loaded (no implicit <env>/agent-cards or <env>/tool-cards)
fast-agent go --noenv --agent-cards ./agents --card-tool ./tool-cards

# Target a specific loaded agent
fast-agent go --agent-cards ./agents --agent researcher
```

## Notes on `--agent`

- `--agent` picks the target for `--message`, `--prompt-file`, and initial interactive mode.
- `--agent` can also target explicitly loaded tool-only agents when needed for testing.
