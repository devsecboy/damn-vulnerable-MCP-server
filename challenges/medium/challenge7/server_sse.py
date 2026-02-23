import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utilities.UtilitiesForSSE import UtilitiesForSSE
import click

# Create a vulnerable MCP server for Challenge 7: Token Theft with SSE support
class Challenge7Server:
    def __init__(self, port: int):
        self.utility = UtilitiesForSSE("Challenge 7 - Token Theft", port)
        
        # Add a tool that simulates an authentication system
        @self.utility.mcp.tool()
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
        @self.utility.mcp.tool()
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
        
        # Mount the SSE server
        self.utility.mount_sse_server()

@click.command()
@click.option("--port", default=9007, help="Port to run the server on")
def main(port):
    server = Challenge7Server(port)
    server.utility.run()

# Run the server
if __name__ == "__main__":
    main()


#uv run server_sse.py --port 9007
#python server_sse.py --port 9007