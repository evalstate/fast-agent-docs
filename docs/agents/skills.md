# Agent Skills

**`fast-agent`** supports Agent Skills, and by default searches the directories listed in `DEFAULT_SKILLS_PATHS`:

- `.fast-agent/skills`
- `.claude/skills`

When valid SKILL.md files are found:

- The Agent is given access to an `execute` tool for running shell commands, with the working directory set to the workspace root.
- Skill descriptions from the manifest and path are added to the System Prompt using the `{{agentSkills}}` expansion. A warning is displayed if this is not present in the System Prompt.
- The `/skills` command lists the available skills.
- If duplicate skill names exist across directories, later directories override earlier ones. Warnings are surfaced in `/status` (ACP).

## Command Line Options

If using **`fast-agent`** interactively from the command line, the `--skills <directory>` switch can be used to specify a single skills directory. When supplied, the default search paths are not used.

```bash
# Specify a skills folder and a model
fast-agent go --skills ~/skill-development/testing/ --model gpt-5-mini.low

# Give fast-agent access to the shell
fast-agent go -x
```

## Config File

Use `skills.directories` to set multiple skills directories. When provided (even as an empty list), the default search paths are not used.

```yaml
skills:
  directories:
    - ~/skills/team
    - ./skills/local
```

## Programmatic Usage

Skills directories can be defined on a per-agent basis:

```python
from fast_agent.constants import DEFAULT_SKILLS_PATHS

# Define the agent
@fast.agent(instruction=default_instruction, skills=DEFAULT_SKILLS_PATHS + ["~/source/skills"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()
```

This allows each individual agent to use a different set of skills if needed. To disable skills for an agent, pass `skills=[]`.
