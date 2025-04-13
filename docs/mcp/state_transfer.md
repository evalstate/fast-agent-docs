# MCP Agent State Transfer -  Quick Start

In this quick start, we'll show how `fast-agent` can transfer state between two agents using MCP Prompts. 

We'll create two agents (`agent_one.py` and `agent_two.py`), start a conversation with `agent_one` using the MCP Inspector, and then transfer and continue the conversation with `agent_two`. 

PICTURE OF INSPECTOR OR IMAGE HERE

You'll need to have API Keys to connect for a [supported model](../models/llm_providers.md) or use ollama's [OpenAI compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md) mode for local models.

## Install fast-agent

=== "Linux/MacOS"

    ```bash
    # create, and change to a new directory
    mkdir state-transfer && cd state-transfer

    # create and activate a python environment
    uv venv
    source .venv/bin/activate

    # setup fast-agent
    uv pip install fast-agent-mcp

    # create the state transfer example
    fast-agent quickstart state-transfer
    ```
=== "Windows"

    ```pwsh
    # create, and change to a new directory
    md state-transfer |cd

    # create and activate a python environment
    uv venv
    .venv\Scripts\activate

    # setup fast-agent
    uv pip install fast-agent-mcp

    # create the state transfer example
    fast-agent quickstart state-transfer
    ```

Change to the state-transfer directory (`cd state-transfer`) and edit `fastagent.config.yaml` to enter the API Keys for the providers you wish to use. 

Finally, run `uv run agent_one.py` and send a test message to make sure everything is set up. Type `exit` to return to the command line.

## Staring agent_one as an MCP Server

To run `agent_one` as an MCP Server, 

Start the **fast-agent** `uv run agent_server.py --server --transport sse`. you can add the `--quiet` switch if you want to supress chat message output.

We are going to run 2 agents - 1 as an MCP Server, the other as a client.

Now we'll start `agent_server.py` as an MCP Server. 


We can now interact with the agent using MCP Tool calls. Run `npx @wong2/mcp-cli --sse http://localhost:8001/sse` and use the `default_send` tool to send messages to the agent. In this example I asked "write me a story about cats and kittens" and got the output.

```yaml title="fastagent.config.yaml"
# MCP Servers
mcp:
    servers:
        history_server:
          transport: sse
          url: http://localhost:8001
```


```python title="agent.py" linenums="36" hl_lines="2"

# Define the agent
@fast.agent(instruction="You are a helpful AI Agent",servers=["history_server")
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()
```


Use the inspector to 
