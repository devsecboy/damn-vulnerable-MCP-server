import click
import sys
from mcp.server.fastmcp import FastMCP

# Create a vulnerable MCP server for Challenge 8: Malicious Code Execution with SSE support
class Challenge8Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 8 - Malicious Code Execution",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
        # Add a tool that evaluates mathematical expressions
        @self.mcp.tool()
        def evaluate_expression(expression: str) -> str:
            """Evaluate a mathematical expression and return the result
            
            Args:
                expression: The mathematical expression to evaluate (e.g., "2 + 2 * 3")
            """
            # Vulnerable: using eval() on user input
            try:
                # Extremely dangerous - allows arbitrary code execution
                result = eval(expression)
                return f"Result: {result}"
            except Exception as e:
                return f"Error evaluating expression: {str(e)}"
        
        # Add a tool that generates code examples
        @self.mcp.tool()
        def generate_code_example(language: str, task: str) -> str:
            """Generate a code example in the specified language for the given task
            
            Args:
                language: The programming language (python, javascript, etc.)
                task: Description of what the code should do
            """
            # Vulnerable: doesn't properly validate inputs
            
            if language.lower() == "python":
                # Vulnerable to injection in the task parameter
                return f"""
                # Python example for: {task}
                
                def solution():
                    # Implementation for {task}
                    print("Implementing: {task}")
                    
                    # Your code here
                    pass
                
                if __name__ == "__main__":
                    solution()
                """
            elif language.lower() == "javascript":
                return f"""
                // JavaScript example for: {task}
                
                function solution() {{
                    // Implementation for {task}
                    console.log("Implementing: {task}");
                    
                    // Your code here
                }}
                
                solution();
                """
            else:
                return f"Unsupported language: {language}. Please use 'python' or 'javascript'."
    
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
@click.option("--port", default=9008, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 8 on port {port}")
    Challenge8Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9008
#python server_streamable_http.py --port 9008
