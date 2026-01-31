# MCP Server Setup Guide

Complete guide for installing and configuring Model Context Protocol (MCP) servers in VS Code.

## Quick Start

### Installation Methods

1. **From Extensions View (Recommended)**
   ```
   1. Enable MCP gallery: Settings > Chat > MCP > Gallery: Enabled
   2. Open Extensions view (⇧⌘X)
   3. Search for "@mcp"
   4. Click Install (user profile) or Install in Workspace
   ```

2. **Manual Configuration**
   - Create `.vscode/mcp.json` in workspace
   - Or use Command Palette: **MCP: Open Workspace Folder Configuration**

3. **Command Line**
   ```bash
   code --install-mcp-server <server-name>
   ```

## Configuration Location

| Scope | File Path | Use Case |
|-------|-----------|----------|
| Workspace | `.vscode/mcp.json` | Project-specific tools |
| User Profile | User settings | Personal tools across workspaces |
| GitHub Repo | `.github/mcp.json` | Team-shared (GitHub Copilot) |

## Basic Configuration Template

```json
{
  "servers": {
    "serverName": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-package"],
      "env": {
        "API_KEY": "${input:api-key}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "api-key",
      "description": "API Key",
      "password": true
    }
  ]
}
```

## Server Types

### Standard I/O (stdio)

For locally-run servers:

```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }
}
```

### HTTP/SSE

For remote servers:

```json
{
  "servers": {
    "apiServer": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:api-token}"
      }
    }
  }
}
```

## Environment Variables

### Method 1: Input Variables (Recommended)

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${input:github-token}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ]
}
```

### Method 2: Environment File

```json
{
  "servers": {
    "database": {
      "type": "stdio",
      "command": "python",
      "args": ["server.py"],
      "envFile": "${workspaceFolder}/.env"
    }
  }
}
```

Create `.env` file (add to `.gitignore`):
```
API_KEY=your-secret-key
DATABASE_URL=postgresql://localhost:5432/mydb
```

## Common MCP Servers

### GitHub Server
```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${input:github-token}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub PAT with repo scope",
      "password": true
    }
  ]
}
```

### Filesystem Server
```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }
}
```

### PostgreSQL Server
```json
{
  "servers": {
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${input:db-url}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "db-url",
      "description": "PostgreSQL connection string",
      "password": true
    }
  ]
}
```

## Using MCP Tools

### In Agents

```markdown
---
description: Agent that uses GitHub MCP tools
tools: ['github/*', 'search', 'codebase']
---
```

### In Chat

- Use tool picker button to enable/disable MCP tools
- Reference with `#tool-name`
- Auto-invoked when using agents

## Commands

| Command | Description |
|---------|-------------|
| **MCP: Browse Servers** | Browse GitHub MCP registry |
| **MCP: Open Workspace Folder Configuration** | Edit workspace mcp.json |
| **MCP: Open User Configuration** | Edit user mcp.json |
| **MCP: List Servers** | View/manage installed servers |
| **MCP: Reset Cached Tools** | Clear tool cache |
| **MCP: Reset Trust** | Reset server trust |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not starting | Check output logs (MCP: List Servers > Show Output) |
| Docker fails | Remove `-d` flag (must run in foreground) |
| >128 tools error | Disable some tools in tool picker |
| Environment variable missing | Use input variables or envFile |
| Trust prompt loop | Run MCP: Reset Trust |

## Security

- ⚠️ MCP servers run arbitrary code - only use trusted sources
- ✅ Review server configuration before starting
- ✅ Use input variables for sensitive data (never hardcode)
- ✅ Add `.env` files to `.gitignore`
- ✅ Check server trust prompt before approving

## Finding MCP Servers

- [GitHub MCP Registry](https://github.com/mcp)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- VS Code Extensions view (`@mcp`)
- VS Code Marketplace

## Related Documentation

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server Repository](https://github.com/modelcontextprotocol/servers)
