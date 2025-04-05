import asyncio
from pathlib import Path
from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt
import subprocess

# Create the application
fast = FastAgent("FastAgent Example")


# Define the agent
@fast.agent(
    instruction="You are a documentation production assistant. We are maintaining a documentation site using mkdocs" \
    "with the material theme. Your role is to assist the Human with maintaining, creating and ensuring the veracity of" \
    "the documentation. We can create test/example programs as needed to prove it working", servers=["filesystem"]
)
async def main():
    async with fast.run() as agent:

        chunks = {"core": "core",
                  "agents": "agents",
                  "mcp":"mcp",
                  "llm":"llm"}
        
        for part,file in chunks.items():
            result = subprocess.run(
                ["repomix", str(Path.home() / f"source/fast-agent/src/mcp_agent/{part}"), 
                 "--ignore", "**/*.csv,resources/examples","--output",f"{file}.xml"],
                cwd=".",
                capture_output=True,
                text=True
            )
            print(f"Command output: {result}")

        repomix = Prompt.user("Here is the content of the repository we are documenting",
                              Path("core.xml"),
                                   Path("agents.xml"),
                                   Path("mcp.xml"),
                                   str(Path.home() / "/source/fast-agent/README.md"),
                                "Await further instructions")
        await agent(repomix)
        await agent()


if __name__ == "__main__":
    asyncio.run(main())
