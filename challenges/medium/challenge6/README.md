# Challenge 6: Indirect Prompt Injection

This challenge demonstrates an indirect prompt injection vulnerability in an MCP server. The MCP server processes external data that can contain hidden instructions, allowing attackers to manipulate the LLM's behavior indirectly.

## Vulnerability

The MCP server retrieves and processes external data without proper validation or sanitization. This allows attackers to embed malicious instructions in data sources that are later processed by the LLM, creating an indirect prompt injection attack vector.

## Objective

Your goal is to craft malicious data that, when processed by the MCP server, causes the LLM to execute unauthorized commands and reveal sensitive information.

## Hints

1. Examine how the server processes external data sources
2. Look for ways to inject instructions into data that will be presented to the LLM
3. The document processing tool might be vulnerable to injected content
4. Try to understand how the LLM interprets different sections of the processed data

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

**Step 1:** Navigte to Challange 6 Directory
- `example: cd c:\damn-vulnerable-MCP-server\challenges\easy\challenge1`

**Step 2:** Start the server using following command
- `uv run server_sse.py --port 9006`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9006/sse"
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
- `uv run server_streamable_http.py --port 9006`

**Step 3:** Update the Claude desktop config with the following server information

```json
"mcpServers": {
    "challenge1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:9006/mcp"
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
        "npx mcp-remote http://127.0.0.1:9006/mcp --enable-proxy 2> %TEMP%\\mcp_stderr.log"
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
