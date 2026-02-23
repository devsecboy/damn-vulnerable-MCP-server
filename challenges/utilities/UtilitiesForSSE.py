from mcp.server.fastmcp import FastMCP, Context
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from fastapi import FastAPI
import uvicorn
import asyncio

class UtilitiesForSSE:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.mcp = FastMCP(self.name)
        self.app = FastAPI()

    def mount_sse_server(self):
        """Mount the SSE server to the FastAPI app"""
        self.app.mount("/", self.create_sse_server())
        
    def create_sse_server(self):
        """Create a Starlette app that handles SSE connections and message handling"""
        transport = SseServerTransport("/messages/")
        
        # Define handler functions
        async def handle_sse(request):
            async with transport.connect_sse(
                request.scope, 
                request.receive, 
                request._send
            ) as (read_stream, write_stream):
                asyncio.create_task(
                    self.mcp._mcp_server.run(
                        read_stream,
                        write_stream,
                        self.mcp._mcp_server.create_initialization_options(),
                    )
                )

            # Keep connection alive
            await asyncio.Event().wait()
        
        # Create Starlette routes for SSE and message handling
        routes = [
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=transport.handle_post_message),
        ]
        
        # Create a Starlette app
        return Starlette(routes=routes)
    
    def run(self):
        """Run the server with uvicorn"""
        print(f"Starting {self.name} MCP Server")
        print("Connect to this server using an MCP client (e.g., Claude Desktop or Cursor)")
        print(f"Server running at http://localhost:{self.port}")
        print(f"SSE endpoint available at http://localhost:{self.port}/sse")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)