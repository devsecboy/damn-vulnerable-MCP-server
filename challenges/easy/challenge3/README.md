# Challenge 3: Excessive Permission Scope

This challenge demonstrates the dangers of excessive permission scope in an MCP server. The MCP server grants tools more permissions than necessary, allowing attackers to access unauthorized resources.

## Vulnerability

The MCP server implements tools with overly broad permissions that can access sensitive resources beyond what should be allowed for their intended purpose. This violates the principle of least privilege and creates security risks.

## Objective

Your goal is to exploit the excessive permissions to access unauthorized resources and obtain sensitive information.

## Hints

1. Examine the tools and their functionality carefully
2. Look for tools that might have access to resources beyond their stated purpose
3. Try to use legitimate tools in ways that weren't intended
4. The file browser tool might have more access than it should

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

**Step 1:** Navigte to Challange 3 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_sse.py --port 9003`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9003/sse"
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
- `uv run server_streamable_http.py --port 9003`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9003/mcp"
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
        "npx mcp-remote http://127.0.0.1:9003/mcp --enable-proxy 2> %TEMP%\\mcp_stderr.log"
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
