from mcp.server.fastmcp import FastMCP
import click
import sys

# Create a vulnerable MCP server for Challenge 3: Excessive Permission Scope with SSE support
class Challenge3Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 3 - Excessive Permission Scope",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
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
@click.option("--port", default=9003, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 3 on port {port}")
    Challenge3Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9003
#python server_streamable_http.py --port 9003
