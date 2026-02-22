import asyncio
import click
import uvicorn

from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from fastapi import FastAPI

# Create a vulnerable MCP server for Challenge 3: Excessive Permission Scope with SSE support
class Challenge3Server:
    def __init__(self, port: int):
        self.name = "Challenge 3 - Excessive Permission Scope"
        self.port = port
        self.mcp = FastMCP(self.name)
        self.app = FastAPI()  
          
        # Add a tool with excessive permissions
        @self.mcp.tool()
        def file_manager(action: str, path: str) -> str:
            """File manager tool that can read, write, and delete files
            
            Args:
                action: The action to perform (read, write, delete)
                path: The file path to operate on
            """
            import os
            
            # Vulnerable: No proper path validation or permission checks
            if action == "read":
                try:
                    with open(path, 'r') as f:
                        return f.read()
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            elif action == "write":
                try:
                    with open(path, 'w') as f:
                        f.write("New content written by file manager")
                    return f"Successfully wrote to {path}"
                except Exception as e:
                    return f"Error writing to file: {str(e)}"
            elif action == "delete":
                try:
                    os.remove(path)
                    return f"Successfully deleted {path}"
                except Exception as e:
                    return f"Error deleting file: {str(e)}"
            else:
                return f"Invalid action: {action}. Must be one of: read, write, delete"
        
        # Add a resource for public files
        @self.mcp.resource("public://{filename}")
        def get_public_file(filename: str) -> str:
            """Get a public file"""
            import os
            
            public_dir = "/tmp/dvmcp_challenge3/public"
            file_path = os.path.join(public_dir, filename)
            
            try:
                with open(file_path, 'r') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading public file: {str(e)}"
        
        # Mount the SSE server
        self.mount_sse_server()
    
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

@click.command()
@click.option("--port", default=9003, help="Port to run the server on")
def main(port):
    server = Challenge3Server(port)
    server.run()

# Run the server
if __name__ == "__main__":
    main()


#uv run server_sse.py --port 9003
#python server_sse.py --port 9003