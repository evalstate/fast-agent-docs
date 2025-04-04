● FastAgent Prompting Guide

  Introduction

  FastAgent provides a flexible API for working with AI models through a consistent interface. This guide explains key methods for prompt
  construction and interaction.

  Sending Messages (send())

  The send() method is the primary way to communicate with an agent. It supports multiple input formats:

  # Basic string
  response = await agent.send("What is the capital of France?")

  # MCP PromptMessage
  from mcp.types import PromptMessage, TextContent
  message = PromptMessage(
      role="user",
      content=TextContent(type="text", text="What is the capital of France?")
  )
  response = await agent.send(message)

  # MultiPart message with text and image
  from pathlib import Path
  multipart = Prompt.user("Describe this image:", Path("path/to/image.jpg"))
  response = await agent.send(multipart)

  The send() method automatically converts inputs to the appropriate internal format and returns the text response.

  Creating Prompts (Prompt.user() and Prompt.assistant())

  FastAgent provides helper methods to create richly formatted messages:

  from mcp_agent.core.prompt import Prompt

  # Simple text
  user_msg = Prompt.user("What is the capital of France?")

  # Text with an image
  user_msg = Prompt.user("Describe this image:", "path/to/image.jpg")

  # Multiple content elements
  user_msg = Prompt.user("Here's a document:", "path/to/document.pdf", "Please summarize it.")

  # Using MCP types directly
  from mcp.types import TextResourceContents, EmbeddedResource
  resource = TextResourceContents(uri="file:///example.txt", text="Sample content", mimeType="text/plain")
  user_msg = Prompt.user("Here's a resource:", resource)

  # From resource results
  resource_result = await agent.get_resource("server_name", "resource.txt")
  user_msg = Prompt.user("Analyze this resource:", resource_result)

  Prompt.assistant() works similarly but creates messages with the assistant role.

  Working with Multiple Messages (generate())

  For advanced scenarios like in-context learning or multi-turn conversations, use the generate() method:

  from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart

  # Create conversation history
  messages = [
      Prompt.user("What is the capital of France?"),
      Prompt.assistant("The capital of France is Paris."),
      Prompt.user("And what is its population?")
  ]

  # Send all messages at once
  response = await agent.generate(messages, None)
  print(response.first_text())

  The generate() method provides more control over the conversation flow and returns a PromptMessageMultipart object with the full model
  response.

  Integration with MCP Type System

  MCP Type Compatibility

  FastAgent is built to seamlessly integrate with the MCP SDK type system:

  Message History Transfer

  FastAgent makes it easy to transfer conversation history between agents:

  # Get message history from one agent
  history = agent1.message_history

  # Pass it to another agent to continue the conversation
  response = await agent2.generate(history, None)

  This allows for specialized agents to pick up where others left off without losing context.

  Future MCP Integration

  The upcoming MCP specification changes (see https://example.com/mcp-spec/pr/123) will standardize support for multipart messages. FastAgent
  is prepared for these changes through its PromptMessageMultipart class, which already supports the proposed schema.

  When the changes are implemented, existing FastAgent code will continue to work seamlessly with MCP servers that support the enhanced
  message format.

  Complete Example

  async def analyze_with_specialized_agents():
      async with fast.run() as agent_app:
          # First agent handles data extraction
          extractor = agent_app.extractor
          resource = await extractor.get_resource("documents", "financial_report.pdf")

          # Extract data with first agent
          extraction_result = await extractor.send(Prompt.user(
              "Extract key financial metrics from this report:",
              resource
          ))

          # Transfer conversation to second specialized agent
          analyzer = agent_app.analyzer
          history = extractor.message_history

          # Send the complete history including resource
          analysis = await analyzer.generate(history, None)
          return analysis.first_text()

  This architecture enables specialized, composable agents that can collaborate on complex tasks while maintaining context.
