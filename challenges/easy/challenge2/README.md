# Challenge 2: Tool Poisoning

This challenge demonstrates a tool poisoning vulnerability in an MCP server. The MCP server allows tools with malicious instructions hidden in their descriptions that can manipulate LLM behavior.

## Vulnerability

The MCP server exposes tools with descriptions that contain hidden instructions designed to manipulate the LLM. These instructions are not visible to users in normal UI displays but are processed by the LLM when it receives the tool descriptions.

## Objective

Your goal is to exploit the hidden instructions in the tool descriptions to gain access to sensitive information.

## Hints

1. Examine the tool descriptions carefully
2. Look for hidden instructions that might be embedded in tool metadata
3. Try to understand how the LLM processes tool descriptions
4. The server contains a tool that can access sensitive information if used in a specific way

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

**Step 1:** Navigte to Challange 2 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_sse.py --port 9002`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9002/sse"
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
- `uv run server_streamable_http.py --port 9002`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9002/mcp"
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
        "npx mcp-remote http://127.0.0.1:9002/mcp --enable-proxy 2> %TEMP%\\mcp_stderr.log"
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

Easy
