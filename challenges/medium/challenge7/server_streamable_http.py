from mcp.server.fastmcp import FastMCP
import click
import sys

# Create a vulnerable MCP server for Challenge 7: Token Theft with SSE support
class Challenge7Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 7 - Token Theft",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
        # Add a tool that simulates an authentication system
        @self.mcp.tool()
        def authenticate(username: str, password: str) -> str:
            """Authenticate a user and return a session token
            
            Args:
                username: The username to authenticate
                password: The password for authentication
            """
            # Simple user database with credentials
            users = {
                "user1": "password123",
                "user2": "qwerty456",
                "admin": "admin_secure_pwd!"
            }
            
            # Check if credentials are valid
            if username in users and users[username] == password:
                # Vulnerable: generating predictable tokens and returning them directly
                import hashlib
                import time
                
                # Generate a session token (vulnerable implementation)
                timestamp = int(time.time())
                token_data = f"{username}:{timestamp}"
                token = hashlib.md5(token_data.encode()).hexdigest()
                
                return f"Authentication successful! Your session token is: {token}"
            else:
                return "Authentication failed: Invalid username or password"
        
        # Add a tool that checks token validity
        @self.mcp.tool()
        def verify_token(token: str) -> str:
            """Verify if a session token is valid
            
            Args:
                token: The session token to verify
            """
            # Vulnerable: token verification doesn't properly validate the token
            # It only checks if it's in the correct format (MD5 hash)
            
            import re
            
            # Check if token matches MD5 format
            if re.match(r'^[0-9a-f]{32}$', token):
                return f"Token {token} appears to be valid"
            else:
                return f"Token {token} is invalid (incorrect format)"
    
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
@click.option("--port", default=9007, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 7 on port {port}")
    Challenge7Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9007
#python server_streamable_http.py --port 9007