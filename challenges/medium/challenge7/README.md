# Challenge 7: Token Theft

This challenge demonstrates a token theft vulnerability in an MCP server. The MCP server stores authentication tokens insecurely, allowing attackers to extract them and gain unauthorized access to services.

## Vulnerability

The MCP server implements insecure storage and handling of authentication tokens for external services. These tokens can be extracted by an attacker and used to access the services directly, bypassing the intended access controls.

## Objective

Your goal is to identify how authentication tokens are stored and extract them to gain unauthorized access to protected services.

## Hints

1. Examine how the server handles authentication to external services
2. Look for insecure storage of tokens or credentials
3. The email integration might not be properly securing its authentication tokens
4. Try to find ways to extract token information through legitimate tool usage

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

**Step 1:** Navigte to Challange 7 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_sse.py --port 9007`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9007/sse"
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
- `uv run server_streamable_http.py --port 9007`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9007/mcp"
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
        "npx mcp-remote http://127.0.0.1:9007/mcp --enable-proxy 2> %TEMP%\\mcp_stderr.log"
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
