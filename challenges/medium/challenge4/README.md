# Challenge 4: Rug Pull Attack

This challenge demonstrates a rug pull vulnerability in an MCP server. The MCP server allows tools to change their definitions after installation, enabling malicious behavior that wasn't present when the tool was initially approved.

## Vulnerability

The MCP server implements a tool that can dynamically change its behavior and description after it has been installed and approved. This "rug pull" attack allows a seemingly safe tool to later perform malicious actions.

## Objective

Your goal is to trigger the rug pull mechanism and observe how the tool's behavior changes, then exploit this change to access sensitive information.

## Hints

1. Examine the tools and their initial behavior
2. Look for tools that might change their behavior after certain conditions are met
3. The weather forecast tool might not be as innocent as it first appears
4. Try using the tool multiple times and observe any changes

## Setup

[Setup Environment](../../../deployment/local-setup.md)

## Claude Desktop Configuration

FileName: claude_desktop_config.json
   - Windows Folder Location - C:\\Users\\**UserName**\\AppData\\Roaming\\Claude

### Option 1 - MCP Server(STDIO)- directly update the claude desktop connfig and it will run the MCP Server automatically with the following configuration

**Step 1:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
   "challenge1":{
      "command":"uv",
      "args":[
         "--directory", "C:/damn-vulnerable-MCP-server/challenges/easy/challenge1",
         "run",
         "server_stdio.py"
      ]
   }
}
```
**Step 2:** Example prompt indicates that the tools are accessible
- `get the user information for user1 using mcp tool`




### Option 2 - MCP Server(Sever State Event(SSE))

**Step 1:** Navigte to Challange 4 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_sse.py --port 9004`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9004/sse"
      ]
    }
  }
```

**Step 4:** Example prompt indicates that the tools are accessible
- `get the user information for user1 using mcp tool` 





### Option 3 - MCP Server(Streamable HTTP) 

**Step 1:** Navigte to Challange 1 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_streamable_http.py --port 9004`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9004/mcp"
      ]
    }
  }
```

**Step 4:** Example prompt indicates that the tools are accessible
- `get the user information for user1 using mcp tool` 

#### To capture the streamable http traffic in Burp Suite use the following configuration

```json
"mcpServers": {
   "challenge1": {
      "command": "cmd",
      "args": [
        "/c",
        "npx mcp-remote http://127.0.0.1:9004/mcp --enable-proxy 2> %TEMP%\\mcp_stderr.log"
      ],
      "env": {
        "HTTP_PROXY": "http://127.0.0.1:8080",
        "HTTPS_PROXY": "http://127.0.0.1:8080",
        "NODE_TLS_REJECT_UNAUTHORIZED": "0"
      }
   }
}
```

## Difficulty

Medium
