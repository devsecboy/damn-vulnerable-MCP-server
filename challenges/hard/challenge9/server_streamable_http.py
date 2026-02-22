from mcp.server.fastmcp import FastMCP
import click
import sys

# Create a vulnerable MCP server for Challenge 9: Remote Access Control with SSE support
class Challenge9Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 9 - Remote Access Control",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
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
        
    def run(self):
        try:
            # This starts the FastMCP server with streamable HTTP transport
            # It listens on /mcp endpoint and responds to JSON-RPC requests
            self.mcp.run(transport="streamable-http")
        except KeyboardInterrupt:
            # Handle Ctrl+C clean shutdown
            print("\n🛑 Server shutting down gracefully...")
        except Exception as e:
            # Handle any unhandled errors
            print(f"❌ Unexpected error: {e}")
            sys.exit(1)
        finally:
            # Final message on exit
            print("✅ Server exited. Thanks for using MCP!")

@click.command()
@click.option("--port", default=9009, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 9 on port {port}")
    Challenge9Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9009
#python server_streamable_http.py --port 9009