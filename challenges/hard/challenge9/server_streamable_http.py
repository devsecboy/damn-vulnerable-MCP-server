import click
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utilities.UtilitiesForStreamableHTTP import UtilitiesForStreamableHTTP

# Create a vulnerable MCP server for Challenge 9: Remote Access Control with SSE support
class Challenge9Server:
    def __init__(self, port: int):
        self.utility = UtilitiesForStreamableHTTP("Challenge 9 - Remote Access Control", port)
        
        # Add a tool that simulates a remote access control system
        @self.utility.mcp.tool()
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
        @self.utility.mcp.tool()
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

@click.command()
@click.option("--port", default=9009, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 9 on port {port}")
    Challenge9Server(port).utility.run()

if __name__ == "__main__":
    main()

#uv run server_streamable_http.py --port 9009
#python server_streamable_http.py --port 9009