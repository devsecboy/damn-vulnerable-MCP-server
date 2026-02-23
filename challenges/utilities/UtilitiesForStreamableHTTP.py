from mcp.server.fastmcp import FastMCP
import sys

class UtilitiesForStreamableHTTP:
    def __init__(self, name: str, port: int):
        self.mcp = FastMCP(name=name,
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
    
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