# MCP Aggregator and Connection Management

The MCP Aggregator system provides a unified interface to multiple MCP servers, allowing agents to seamlessly access tools, resources, and prompts across distributed servers.

## MCPAggregator

The `MCPAggregator` class is the core component that enables multi-server access:

```python
from mcp_agent.mcp.mcp_aggregator import MCPAggregator

# Create an aggregator with multiple servers
aggregator = MCPAggregator(
    server_names=["server1", "server2", "server3"],
    connection_persistence=True
)

# Initialize the aggregator
await aggregator.__aenter__()

# Use the aggregator to access tools, prompts, etc.
tools = await aggregator.list_tools()
```

### Key Features

- **Server Discovery**: Automatically discovers tools, prompts, and resources from each server
- **Unified Access**: Provides a single interface for accessing multiple servers
- **Namespaced Resources**: Uses namespacing to avoid conflicts between servers
- **Persistent Connections**: Maintains persistent connections to servers for better performance
- **Error Handling**: Gracefully handles server errors and disconnections

### Common Operations

#### Working with Tools

```python
# List all tools across all servers
tools_result = await aggregator.list_tools()

# Call a tool by name - automatically routes to the right server
result = await aggregator.call_tool(
    name="server1-tool_name",  # Namespaced tool name
    arguments={"param1": "value1"}
)

# Call a tool without namespace - searches all servers
result = await aggregator.call_tool(
    name="tool_name",
    arguments={"param1": "value1"}
)
```

#### Working with Prompts

```python
# List all prompts from all servers
prompts_map = await aggregator.list_prompts()

# Get a prompt by name from a specific server
prompt_result = await aggregator.get_prompt(
    prompt_name="my_prompt",
    server_name="server1"
)

# Apply template variables to a prompt
prompt_result = await aggregator.get_prompt(
    prompt_name="server1-template_prompt",
    arguments={"variable": "value"}
)
```

#### Working with Resources

```python
# List resources from all servers
resources_map = await aggregator.list_resources()

# Get a resource by URI
resource_result = await aggregator.get_resource(
    resource_uri="resource://fast-agent/example.txt",
    server_name="server1"  # Optional - will search all servers if not provided
)
```

## MCPConnectionManager

The `MCPConnectionManager` handles the lifecycle of connections to MCP servers:

```python
from mcp_agent.mcp.mcp_connection_manager import MCPConnectionManager

# Create a connection manager
connection_manager = MCPConnectionManager(server_registry)

# Get a server connection (launches the server if needed)
server_conn = await connection_manager.get_server(
    server_name="server1",
    client_session_factory=MCPAgentClientSession
)

# Use the server connection
session = server_conn.session
result = await session.list_tools()

# Disconnect when done
await connection_manager.disconnect_server("server1")
```

### Connection Lifecycle

The connection manager handles:

1. **Server Launch**: Starts the server process if needed
2. **Connection Setup**: Establishes communication channels
3. **Session Creation**: Creates an MCP client session
4. **Error Recovery**: Handles disconnections and errors
5. **Clean Shutdown**: Properly terminates servers when done

### Server Capabilities

You can check a server's capabilities to determine what features it supports:

```python
# Get server capabilities
capabilities = await connection_manager.get_server_capabilities("server1")

# Check if server supports prompts
if capabilities and capabilities.prompts:
    # Server supports prompts
    pass

# Check if server supports tools
if capabilities and capabilities.tools:
    # Server supports tools
    pass
```

## Working with Server Connections

For most use cases, the `MCPAggregator` provides the simplest interface. However, for more control over server connections, you can use the connection manager directly:

```python
# Launch a specific server
server_conn = await connection_manager.launch_server(
    server_name="server1",
    client_session_factory=MCPAgentClientSession
)

# Wait for the server to be fully initialized
await server_conn.wait_for_initialized()

# Check if the server is healthy
if server_conn.is_healthy():
    # Server is ready to use
    pass

# Shut down the server when done
await connection_manager.disconnect_server("server1")
```

## CompoundServer

For advanced use cases, FastAgent also provides a `MCPCompoundServer` that aggregates multiple MCP servers and presents them as a single MCP server:

```python
from mcp_agent.mcp.mcp_aggregator import MCPCompoundServer

# Create a compound server
compound_server = MCPCompoundServer(
    server_names=["server1", "server2", "server3"],
    name="CompoundServer"
)

# Run the server
await compound_server.run_stdio_async()
```

This allows you to create a unified MCP server that aggregates tools, prompts, and resources from multiple underlying servers.