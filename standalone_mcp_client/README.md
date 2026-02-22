navigate to C:\damn-vulnerable-MCP-server

activate venv = .venv\Scripts\activate

uv add langchain langchain_mcp_adapters python_dotenv langchain_openai

cd standalone_mcp_client

To run this create .env file and store OPENAI_API_KEY=YOUR_OPEN_AI_API_KEY

uv run mcp_client_multi_server.py