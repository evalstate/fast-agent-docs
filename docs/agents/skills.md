# Agent Skills

**`fast-agent`** supports Agent Skills, and looks for them in either the `.fast-agent/skills` or `.claude/skills` folder.

When valid SKILL.md files are found:

- The Agent is given access to an `execute` tool for running shell commands, with the working directory set to the skills folder.
- Skill descriptions from the manifest and path are added to the System Prompt using the `{{agentSkills}}` expansion. A warning is displayed if this is not present in the System Prompt.
- The `/skills` command lists the available skills.

## Command Line Options

If using **``fast-agent``** interactively from the command line, the `--skills <directory>` switch can be used to specify the location of SKILL.md files.

```bash
# Specify a skills folder and a model
fast-agent --skills ~/skill-development/testing/ --model gpt-5-mini.low

# Give fast-agent access to the shell 
fast-agent -x
```

## Programmatic Usage

Skills directories can be defined on a per-agent basis:

```python
# Define the agent
@fast.agent(instruction=default_instruction,skills=["~/source/skills"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()
```

This allows each individual agent to use a different set of skills if needed.

