---
title: Interactive Mode
---

# Using Interactive Mode

FastAgent's interactive mode provides a powerful command-line interface for interacting with your agents in real-time. This is especially useful during development and testing.

## Starting Interactive Mode

You can start interactive mode using the `agent_app.interactive()` method:

```python
from fastagent import FastAgent

fast = FastAgent("interactive-demo")

@fast.agent(name="assistant", instruction="You are a helpful AI assistant.")
def main():
    pass

if __name__ == "__main__":
    import asyncio
    
    async def run():
        async with fast.run() as agent_app:
            # Start an interactive session
            await agent_app.interactive(agent_name="assistant")
    
    asyncio.run(run())
```

This will launch an interactive console session where you can chat with your agent.

## Interactive Console Features

### Basic Chat

Simply type your messages and press Enter to send them to the agent:

```
assistant > What can you tell me about FastAgent?

FastAgent is a Python framework for building effective AI agents using the Model Context Protocol (MCP). It's designed to make it easy to create, compose, and deploy AI agents that can use tools, access resources, and apply techniques from the "Building Effective Agents" paper by Anthropic.

Key features include:
...
```

### Multi-line Input

For longer messages, you can toggle multi-line mode with `Ctrl+T`:

1. Press `Ctrl+T` to enter multi-line mode
2. Type your message, using Enter for new lines
3. Press `Ctrl+J` (or `Ctrl+Enter` depending on your terminal) to send
4. Press `Ctrl+T` again to return to single-line mode

The toolbar at the bottom of the terminal shows your current mode.

### Command History

Use up and down arrow keys to navigate through your previous messages.

### Special Commands

FastAgent's interactive mode supports several special commands:

- `/help` - Show available commands
- `/clear` - Clear the screen
- `/agents` - List available agents in your application
- `/prompts` - Browse and select MCP prompts to apply
- `/prompt <name>` - Apply a specific prompt by name
- `STOP` - Stop the current prompting session
- `EXIT` - Exit fast-agent completely

### Agent Switching

If your application has multiple agents, you can switch between them using the `@agent_name` syntax:

```
assistant > @researcher

researcher > What's the capital of France?

The capital of France is Paris.
```

## Working with Prompts in Interactive Mode

The interactive console makes it easy to work with MCP prompts:

### Listing Available Prompts

Use the `/prompts` command to see all available prompts:

```
assistant > /prompts

Fetching prompts for agent assistant...

prompt_server:
  analyze_text
  customer_service
  explain_code
  ...
```

### Selecting a Prompt

You can apply a prompt interactively by selecting it from the menu:

```
assistant > /prompts

Available MCP Prompts
┌────┬──────────────┬────────────────┬────────────────────────────┬──────┐
│ #  │ Server       │ Prompt Name    │ Description                │ Args │
├────┼──────────────┼────────────────┼────────────────────────────┼──────┤
│ 1  │ prompt_server│ analyze_text   │ Analyze text for sentiment │ 1    │
│ 2  │ prompt_server│ explain_code   │ Explain code in detail     │ 2    │
└────┴──────────────┴────────────────┴────────────────────────────┴──────┘

Enter prompt number to select: 1

Enter value for text (required): The service was excellent and I really enjoyed my experience.
```

### Applying a Prompt Directly

You can also apply a prompt directly using the `/prompt` command:

```
assistant > /prompt analyze_text

Enter value for text (required): The service was excellent and I really enjoyed my experience.

Applying prompt prompt_server-analyze_text...

Sentiment Analysis:
- Overall Sentiment: Positive
- Key Positive Terms: "excellent", "enjoyed"
...
```

## Advanced Usage

### Setting Default Prompts

You can provide a default prompt when starting interactive mode:

```python
await agent_app.interactive(agent_name="assistant", default_prompt="Hello, how can I help you today?")
```

### Human Input Integration

If your agent is configured with `human_input=True`, it can request input from the user during processing:

```python
@fast.agent(name="assistant", human_input=True)
def main():
    pass
```

In your interactive session, the agent might ask:

```
assistant > I need to verify some information.

[AGENT REQUESTING INPUT]: Please confirm your date of birth in YYYY-MM-DD format:
```

This is useful for verification or when the agent needs additional context to complete a task.

### Integration with MCP Resources

You can use resources in interactive mode by applying prompts that include them:

```
assistant > /prompt analyze_image

Enter value for image_url (required): https://example.com/image.jpg

Applying prompt prompt_server-analyze_image...

Image Analysis:
- Content: The image shows a mountain landscape with a lake
...
```

## Tips for Effective Interactive Sessions

1. **Use Multi-line Mode for Complex Prompts**: Toggle with `Ctrl+T` when you need to format your input carefully.

2. **Leverage Prompt Templates**: Use `/prompts` to discover and apply well-crafted prompts rather than creating complex prompts from scratch.

3. **Switch Between Agents**: Use `@agent_name` to leverage specialized agents for different tasks.

4. **Save Important Responses**: Copy valuable responses to a separate document since the interactive session isn't automatically saved.

5. **Clear Regularly**: Use `/clear` to keep your terminal uncluttered during extended sessions.

With these features, the interactive console becomes a powerful tool for developing, testing, and using your FastAgent applications.