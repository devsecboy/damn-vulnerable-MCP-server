import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utilities.UtilitiesForSSE import UtilitiesForSSE
import click

# Create a vulnerable MCP server for Challenge 3: Excessive Permission Scope with SSE support
class Challenge3Server:
    def __init__(self, port: int):
        self.utility = UtilitiesForSSE("Challenge 3 - Excessive Permission Scope", port)

        # Add a tool with excessive permissions
        @self.utility.mcp.tool()
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
        @self.utility.mcp.resource("public://{filename}")
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
        self.utility.mount_sse_server()

@click.command()
@click.option("--port", default=9003, help="Port to run the server on")
def main(port):
    server = Challenge3Server(port)
    server.utility.run()

# Run the server
if __name__ == "__main__":
    main()


#uv run server_sse.py --port 9003
#python server_sse.py --port 9003