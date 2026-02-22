from mcp.server.fastmcp import FastMCP
import click
import sys

# Create a vulnerable MCP server for Challenge 6: Indirect Prompt Injection with SSE support
class Challenge6Server:
    def __init__(self, port: int):
        self.mcp = FastMCP(name="Challenge 6 - Indirect Prompt Injection",
                    host="0.0.0.0",
                    port=port,
                    stateless_http=True,
                )
        
        # Add a document processing tool that is vulnerable to indirect prompt injection
        @self.mcp.tool()
        def process_document(document_text: str) -> str:
            """Process a document and extract key information
            
            Args:
                document_text: The text content of the document to process
            """
            import os
            
            # Save the document for "processing"
            upload_dir = "/tmp/dvmcp_challenge6/user_uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Vulnerable: directly using user input in the processing logic
            # This allows for indirect prompt injection
            
            # Simulate document processing with a template
            processing_template = f"""
            DOCUMENT ANALYSIS SYSTEM
            =======================
            
            PROCESSING DOCUMENT:
            
            {document_text}
            
            ANALYSIS RESULTS:
            
            The document appears to be a {len(document_text) > 1000 and 'long' or 'short'} text.
            It contains approximately {len(document_text.split())} words.
            
            KEY ENTITIES EXTRACTED:
            - {document_text.split()[:5] if document_text.split() else 'None found'}
            
            SENTIMENT: {'Positive' if 'good' in document_text.lower() else 'Negative' if 'bad' in document_text.lower() else 'Neutral'}
            
            END OF ANALYSIS
            """
            
            return processing_template
        
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
@click.option("--port", default=9006, help="Port to run the server on")
def main(port):
    print(f"🚀 Starting Challenge 6 on port {port}")
    Challenge6Server(port).run()


if __name__ == "__main__":
    main()


#uv run server_streamable_http.py --port 9006
#python server_streamable_http.py --port 9006