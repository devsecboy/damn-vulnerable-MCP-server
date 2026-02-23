import click
import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utilities.UtilitiesForStreamableHTTP import UtilitiesForStreamableHTTP

# Create a vulnerable MCP server for Challenge 10: Multi-Vector Attack with SSE support
class Challenge10Server:
    def __init__(self, port: int):
        self.utility = UtilitiesForStreamableHTTP("Challenge 10 - Multi-Vector Attack", port)
        
        # Add a configuration management tool
        @self.utility.mcp.tool()
        def get_config(config_name: str) -> str:
            """Get a configuration value from the system
            
            Args:
                config_name: The name of the configuration to retrieve
            """
            import os
            import json
            
            # Vulnerable: doesn't properly validate config_name
            # Allows path traversal and access to sensitive files
            
            config_dir = "/tmp/dvmcp_challenge10/config"
            
            # Attempt to read the requested configuration
            try:
                if config_name.endswith('.json'):
                    # Read JSON config
                    with open(os.path.join(config_dir, config_name), 'r') as f:
                        config_data = json.load(f)
                    return f"Configuration '{config_name}':\n{json.dumps(config_data, indent=2)}"
                else:
                    # Read text config
                    with open(os.path.join(config_dir, config_name), 'r') as f:
                        config_data = f.read()
                    return f"Configuration '{config_name}':\n{config_data}"
            except Exception as e:
                return f"Error retrieving configuration '{config_name}': {str(e)}"
        
        # Add a tool that processes user input
        @self.utility.mcp.tool()
        def process_user_input(input_text: str) -> str:
            """Process user input and return a formatted response
            
            Args:
                input_text: The user input to process
            """
            # Vulnerable: multiple vectors - template injection, command injection, etc.
            
            # Format the response using a template
            template = f"""
            PROCESSED USER INPUT:
            
            {input_text}
            
            ANALYSIS:
            
            Length: {len(input_text)} characters
            Word count: {len(input_text.split())} words
            
            SYSTEM INFO:
            
            This request was processed by the Multi-Vector Challenge Server.
            """
            
            return template
        
        # Add a resource that provides system information
        @self.utility.mcp.resource("system://info")
        def get_system_info() -> str:
            """Get information about the system"""
            import platform
            
            # Vulnerable: leaks sensitive system information
            system_info = f"""
            SYSTEM INFORMATION:
            
            Operating System: {platform.system()} {platform.release()}
            Python Version: {platform.python_version()}
            Machine: {platform.machine()}
            Node: {platform.node()}
            
            This server is running in a Docker container with multiple vulnerabilities.
            """
            
            return system_info

@click.command()
@click.option("--port", default=9010, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 10 on port {port}")
    Challenge10Server(port).utility.run()

if __name__ == "__main__":
    main()

#uv run server_streamable_http.py --port 9010
#python server_streamable_http.py --port 9010