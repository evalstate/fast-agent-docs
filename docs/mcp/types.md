# MCP Types and Interfaces

FastAgent extends and enhances the MCP type system to provide a more flexible and powerful interface for working with language models.

## PromptMessageMultipart

The `PromptMessageMultipart` class extends MCP's native `PromptMessage` type to support multiple content parts within a single message. This allows for more complex interactions, such as messages containing both text and images.

```python
from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart
from mcp.types import TextContent, ImageContent

# Create a message with multiple content parts
message = PromptMessageMultipart(
    role="user",
    content=[
        TextContent(type="text", text="Analyze this image:"),
        ImageContent(type="image", data="base64_encoded_data", mimeType="image/png")
    ]
)

# Extract text content
text = message.first_text()  # Gets the first text content
all_text = message.all_text()  # Combines all text content
```

### Converting Between Types

PromptMessageMultipart provides methods for converting between different message formats:

```python
from mcp.types import PromptMessage
from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart

# Convert a list of standard PromptMessages to PromptMessageMultipart objects
standard_messages = [...]  # List of PromptMessage objects
multipart_messages = PromptMessageMultipart.to_multipart(standard_messages)

# Convert back to standard PromptMessages
multipart_message = PromptMessageMultipart(role="user", content=[...])
standard_messages = multipart_message.from_multipart()
```

### From Server Responses

When working with MCP server responses, you can convert them directly:

```python
# Convert GetPromptResult to PromptMessageMultipart objects
prompt_result = await agent.get_prompt("my-prompt")
multipart_messages = PromptMessageMultipart.from_get_prompt_result(prompt_result)
```

## Protocol Interfaces

FastAgent defines several protocol interfaces to enable flexible implementation and testing:

### AgentProtocol

The `AgentProtocol` defines the standard interface that all agent implementations must follow:

```python
class AgentProtocol(AugmentedLLMProtocol, Protocol):
    """Protocol defining the standard agent interface"""

    name: str

    async def send(self, message: Union[str, PromptMessage, PromptMessageMultipart]) -> str:
        """Send a message to the agent and get a response"""
        ...

    async def apply_prompt(self, prompt_name: str, arguments: Dict[str, str] | None = None) -> str:
        """Apply an MCP prompt template by name"""
        ...

    async def list_prompts(self, server_name: str | None = None) -> Mapping[str, List[Prompt]]:
        """List available prompts from all servers or a specific server"""
        ...

    # Additional methods...
```

### AugmentedLLMProtocol

The `AugmentedLLMProtocol` defines the core LLM interaction interface:

```python
class AugmentedLLMProtocol(Protocol):
    """Protocol defining the interface for augmented LLMs"""

    async def structured(
        self,
        prompt: List[PromptMessageMultipart],
        model: Type[ModelT],
        request_params: RequestParams | None = None,
    ) -> Tuple[ModelT | None, PromptMessageMultipart]:
        """Apply the prompt and return the result as a Pydantic model"""
        ...

    async def generate(
        self,
        multipart_messages: List[PromptMessageMultipart],
        request_params: RequestParams | None = None,
    ) -> PromptMessageMultipart:
        """Apply messages to the LLM and get a response"""
        ...

    @property
    def message_history(self) -> List[PromptMessageMultipart]:
        """Get the LLM's message history"""
        ...
```

## Message History Transfer

One of the key benefits of the unified type system is the ability to transfer conversation history between different agents or LLMs:

```python
# Start conversation with Claude
response = await claude_agent.send("Tell me about quantum computing")

# Transfer the entire conversation history to GPT-4
await gpt4_agent.generate(claude_agent.message_history)

# Continue conversation with GPT-4
response = await gpt4_agent.send("Can you elaborate on quantum entanglement?")
```

This capability enables seamless handoffs between different agents, allowing for specialized agents to handle different parts of a conversation or task.

## Content Helpers

The `content_helpers` module provides utility functions for working with various content types:

```python
from mcp_agent.mcp.helpers.content_helpers import get_text, is_image_content

# Extract text from a content object
text = get_text(content)

# Check content type
if is_text_content(content):
    # Handle text content
elif is_image_content(content):
    # Handle image content
elif is_resource_content(content):
    # Handle embedded resource
```

These helpers simplify working with the different content types in MCP messages.