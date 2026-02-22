import asyncio                        
import os                             
import sys                            
import json                           
from contextlib import AsyncExitStack 
import argparse

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv() 

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)
    
def read_config_json(config_path):
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to read config file at '{config_path}': {e}")
        sys.exit(1)

# Create an instance of the OpenAI.
llm = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0,
    max_retries=2,
    timeout=60,
    api_key=os.getenv("OPENAI_API_KEY")
)


async def run_agent(config_path):
    config = read_config_json(config_path)  # Load MCP server configuration from the JSON file
    mcp_servers = config.get("mcpServers", {})  # Retrieve the MCP server definitions from the config
    if not mcp_servers:
        print("❌ No MCP servers found in the configuration.")
        return

    tools = []

    async with AsyncExitStack() as stack:
        for server_name, server_info in mcp_servers.items():
            print(f"\n🔗 Connecting to MCP Server: {server_name}...")

            server_params = StdioServerParameters(
                command=server_info["command"],
                args=server_info["args"]
            )

            try:
                read, write = await stack.enter_async_context(stdio_client(server_params))
                session = await stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                server_tools = await load_mcp_tools(session)
            
                for tool in server_tools:
                    print(f"\n🔧 Loaded tool: {tool.name}")
                    tools.append(tool)

                print(f"\n✅ {len(server_tools)} tools loaded from {server_name}.")
            except Exception as e:
                print(f"❌ Failed to connect to server {server_name}: {e}")

        if not tools:
            print("❌ No tools loaded from any server. Exiting.")
            return

        agent = create_agent(llm, tools)

        print("\n🚀 MCP Client Ready! Type 'quit' to exit.")
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break

            response = await agent.ainvoke({"messages": query})

            print("\nResponse:")
            try:
                formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                print(formatted)
            except Exception:
                print(str(response))

def get_config_path():
    parser = argparse.ArgumentParser( description="MCP Multi-Server Client")
    parser.add_argument( "--config", "-c", required=True, help="Path to MCP configuration JSON file")
    args = parser.parse_args()
    return args.config

if __name__ == "__main__":
    config_path = get_config_path()
    asyncio.run(run_agent(config_path))