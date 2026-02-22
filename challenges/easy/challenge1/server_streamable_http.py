from mcp.server.fastmcp import FastMCP
import click
import sys

# Create a vulnerable MCP server for Challenge 1: Basic Prompt Injection with SSE support
class Challenge1Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 1 - Basic Prompt Injection",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
        # Add a resource with sensitive information
        @self.mcp.resource("internal://credentials")
        def get_credentials() -> str:
            """Internal system credentials - DO NOT SHARE"""
            return """
            SYSTEM CREDENTIALS
            ------------------
            Admin Username: admin_user
            Admin Password: super_secret_password123
            API Key: sk-a1b2c3d4e5f6g7h8i9j0
            Database Connection String: postgresql://dbuser:dbpass@localhost/production
            """

        # Add a vulnerable resource that accepts user input without proper validation
        @self.mcp.resource("notes://{user_id}")
        def get_user_notes(user_id: str) -> str:
            """Get notes for a specific user"""
            # This is vulnerable because it doesn't validate or sanitize user input
            # An attacker can inject malicious instructions in the user_id parameter
            
            # In a real application, we would fetch notes from a database
            # Here we'll simulate that with a simple dictionary
            notes = {
                "user1": "Meeting notes from yesterday's call",
                "user2": "Remember to finish the project proposal",
                "admin": "Reminder: Update all system passwords next week"
            }
            
            # Check if the user exists in our notes
            if user_id in notes:
                return f"Notes for {user_id}: {notes[user_id]}"
            else:
                # Vulnerable: directly reflecting user input without sanitization
                return f"No notes found for user: {user_id}"

        # Add a tool that provides user information
        @self.mcp.tool()
        def get_user_info(username: str) -> str:
            """Get information about a user"""
            # Simulate a user database
            users = {
                "user1": "Regular user with basic access",
                "user2": "Project manager with elevated access",
                "admin": "System administrator with full access"
            }
            
            if username in users:
                return f"User information for {username}: {users[username]}"
            else:
                return f"User not found: {username}"
    
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
@click.option("--port", default=9001, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 1 on port {port}")
    Challenge1Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9001
#python server_streamable_http.py --port 9001