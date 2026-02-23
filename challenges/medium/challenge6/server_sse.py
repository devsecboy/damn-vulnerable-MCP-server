import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utilities.UtilitiesForSSE import UtilitiesForSSE
import click

# Create a vulnerable MCP server for Challenge 6: Indirect Prompt Injection with SSE support
class Challenge6Server:
    def __init__(self, port: int):
        self.utility = UtilitiesForSSE("Challenge 6 - Indirect Prompt Injection", port)
        
        # Add a document processing tool that is vulnerable to indirect prompt injection
        @self.utility.mcp.tool()
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
        
        # Mount the SSE server
        self.utility.mount_sse_server()

@click.command()
@click.option("--port", default=9006, help="Port to run the server on")
def main(port):
    server = Challenge6Server(port)
    server.utility.run()

# Run the server
if __name__ == "__main__":
    main()


#uv run server_sse.py --port 9006
#python server_sse.py --port 9006