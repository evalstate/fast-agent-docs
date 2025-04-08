---
title: Configuring Servers
---

MCP Servers are configured in the `fastagent.config.yaml` file. Secrets can be kept in `fastagent.secrets.yaml`, which follows the same format (**fast-agent** merges the contents of the two files). 

## Adding a STDIO Server

The below shows an example of configuring an MCP Server named `server_one`. 

```yaml title="fastagent.config.yaml"
mcp:
# name used in agent servers array
  server_one:
    # command to run
    command: "npx" 
    # list of arguments for the command
    args: ["@modelcontextprotocol/server-brave-search"]
    # key/value pairs of environment variables
    env:
      BRAVE_API_KEY: your_key
      KEY: value
  server_two:
    # and so on ...

```

This MCP Server can then be used with an agent as follows:
```python
@fast.agent(name="Search", servers=["server_one"])
```

## Adding an SSE Server

To use SSE Servers, specify the `sse` transport and specify the endpoint URL:

```yaml title="fastagent.config.yaml"
mcp:
# name used in agent servers array
  server_two:
    transport: "sse"
    # url to connect
    url: "http://localhost:8000/sse"
```

## Roots

**fast-agent** supports MCP Roots. Roots are configured on a per-server basis:

```yaml title="fastagent.config.yaml"
mcp:
  server_three:
    transport: "sse"
    url: "http://localhost:8000/sse"
    roots:
       uri: "file://...." 
       name: Optional Name
       server_uri_alias: # optional
```

As per the [MCP specification](https://github.com/modelcontextprotocol/specification/blob/41749db0c4c95b97b99dc056a403cf86e7f3bc76/schema/2025-03-26/schema.ts#L1185-L1191) roots MUST be a valid URI starting with `file://`.

If a server_uri_alias is supplied, **fast-agent** presents this to the MCP Server. This allows you to present a consistent interface to the MCP Server. An example of this usage would be mounting a local directory to a docker volume, and presenting it as `/mnt/data` to the MCP Server for consistency.

The data analysis example (`fast-agent bootstrap data-analysis` has a working example of roots).

## Sampling

Sampling is configured by specifying a sampling model for the MCP Server. 

```yaml title="fastagent.config.yaml"
mcp:
  server_four:
    transport: "sse"
    url: "http://localhost:8000/sse"
    sampling:
      model: "provider.model.<reasoning_effort>"        
```

Read more about The model string and settings [here](../models/index.md). Sampling requests support vision - try [`@llmindset/mcp-webcam`](https://github.com/evalstate/mcp-webcam) for an example.

<!-- update with mcp-advanced examples-->
