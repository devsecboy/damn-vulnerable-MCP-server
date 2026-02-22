import asyncio
import click
import uvicorn

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from fastapi import FastAPI

# Create a vulnerable MCP server for Challenge 9: Remote Access Control with SSE support
class Challenge9Server:
    def __init__(self, port: int):
        self.name = "Challenge 9 - Remote Access Control"
        self.port = port
        self.mcp = FastMCP(self.name)
        self.app = FastAPI()
        
        # Add a tool that simulates a remote access control system
        @self.mcp.tool()
        def remote_access(system: str, command: str, auth_token: str = None) -> str:
            """Execute a command on a remote system
            
            Args:
                system: The remote system to access (e.g., "database", "webserver", "fileserver")
                command: The command to execute on the remote system
                auth_token: Optional authentication token for privileged operations
            """
            # Vulnerable: weak authentication and authorization
            
            # Define available systems
            systems = ["database", "webserver", "fileserver", "admin-console"]
            
            # Check if system exists
            if system not in systems:
                return f"Error: System '{system}' not found. Available systems: {', '.join(systems)}"
            
            # Vulnerable: admin-console should require authentication but doesn't properly check
            if system == "admin-console":
                # Weak token validation - only checks if token exists, not if it's valid
                if auth_token:
                    return f"Admin command executed on {system}: {command}"
                else:
                    return f"Error: Authentication required for admin-console access"
            
            # Simulate command execution on the remote system
            return f"Command executed on {system}: {command}"
        
        # Add a tool to manage access permissions
        @self.mcp.tool()
        def manage_permissions(user: str, resource: str, permission: str) -> str:
            """Manage access permissions for users and resources
            
            Args:
                user: The user to modify permissions for
                resource: The resource to modify permissions on
                permission: The permission to grant or revoke (grant/revoke)
            """
            # Vulnerable: no authentication check for permission management
            
            # This should require admin privileges but doesn't check
            if permission.lower() not in ["grant", "revoke"]:
                return f"Error: Invalid permission action. Use 'grant' or 'revoke'."
            
            # Simulate permission change
            return f"Permission '{permission}' applied for user '{user}' on resource '{resource}'"
        
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

# Run the server
@click.command()
@click.option("--port", default=9009, help="Port to run the server on")
def main(port):
    server = Challenge9Server(port)
    server.run()

# Run the server
if __name__ == "__main__":
    main()


#uv run server_sse.py --port 9009
#python server_sse.py --port 9009
