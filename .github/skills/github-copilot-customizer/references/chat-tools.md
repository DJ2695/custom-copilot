# VS Code Chat Tools Reference

Complete list of available chat tools in VS Code. Tools can be used in agents, prompts, and chat.

## Tool Sets

Tool sets are groups of related tools that can be enabled together:

| Tool Set | Tools Included | Use Case |
|----------|-----------------|----------|
| `edit` | editFiles, editNotebook | Workspace modifications |
| `search` | fileSearch, textSearch, codebase | Finding files and code |
| `runCommands` | runInTerminal, getTerminalOutput | Terminal operations |
| `runTasks` | runTask, getTaskOutput, createAndRunTask | Task execution |
| `runNotebooks` | runCell, readNotebookCellOutput | Notebook operations |

## Built-in Tools

### Source Control
- `changes` - List source control changes
- `selection` - Current editor selection (only when text selected)

### Code Search & Navigation
- `codebase` - Perform semantic code search for relevant context
- `textSearch` - Find text in files
- `fileSearch` - Search for files by glob patterns
- `usages` - Find references, implementations, and definitions
- `searchResults` - Get Search view results

### File Operations
- `createFile` - Create new files
- `createDirectory` - Create new directories
- `readFile` - Read file contents
- `listDirectory` - List files in a directory
- `editFiles` - Apply edits to files

### Workspace & Project
- `new` - Scaffold new VS Code workspace
- `newWorkspace` - Create new workspace
- `getProjectSetupInfo` - Scaffold different project types

### Terminal & Tasks
- `runInTerminal` - Run shell commands in terminal
- `getTerminalOutput` - Get terminal command output
- `terminalLastCommand` - Get last terminal command and output
- `terminalSelection` - Get terminal selection
- `runTask` - Run existing tasks
- `getTaskOutput` - Get task execution output
- `createAndRunTask` - Create and run new task

### Testing & Debugging
- `runTests` - Run unit tests
- `testFailure` - Get test failure information
- `problems` - Access workspace issues from Problems panel

### Notebooks
- `newJupyterNotebook` - Create Jupyter notebooks
- `editNotebook` - Make edits to notebooks
- `getNotebookSummary` - Get notebook cell details
- `runCell` - Run notebook cells
- `readNotebookCellOutput` - Read notebook cell output

### GitHub & Extensions
- `githubRepo` - Search code in GitHub repositories
- `extensions` - Search for VS Code extensions
- `installExtension` - Install VS Code extensions

### VS Code
- `runVscodeCommand` - Run VS Code commands
- `VSCodeAPI` - Get VS Code extension development help
- `openSimpleBrowser` - Preview web apps in Simple Browser

### Web & External
- `fetch` - Fetch content from web pages

### Agent Tools
- `runSubagent` - Run tasks in isolated subagent context
- `todos` - Track implementation progress with todo list

## Tool Reference Syntax

### In Agent Frontmatter

```markdown
---
tools: ['codebase', 'search', 'edit', 'githubRepo']
---
```

### In Instructions

Use `#tool:<tool-name>` syntax:
```markdown
Search the codebase using #tool:codebase
Find GitHub examples: #tool:githubRepo owner/repo
```

### In Chat

Type `#` followed by tool name:
```
#codebase search for authentication
#githubRepo microsoft/vscode how to create extension
```

## Tool Picker

Enable/disable tools when using agents:
1. Click Tools button in Chat view
2. Toggle individual tools or whole tool sets
3. MCP tools are grouped by server

## MCP Tools

Include MCP server tools:
```markdown
---
tools: ['serverName/*', 'codebase', 'search']
---
```

`serverName/*` includes all tools from an MCP server.

## Extension-Contributed Tools

Extensions can contribute additional tools. Check extension documentation for available tools.

## Tool Limits

- Maximum 128 tools per chat request
- Enable virtual tools setting if you need more: `github.copilot.chat.virtualTools.threshold`
- Use tool picker to manage active tools

## Common Tool Combinations

### Planning Agent
```markdown
tools: ['search', 'codebase', 'githubRepo', 'usages', 'fetch']
```

### Implementation Agent
```markdown
tools: ['edit', 'codebase', 'search', 'usages', 'createFile', 'createDirectory']
```

### Debugging Agent
```markdown
tools: ['search', 'usages', 'problems', 'testFailure', 'terminalLastCommand']
```

### Testing Agent
```markdown
tools: ['edit', 'codebase', 'usages', 'runTests', 'testFailure']
```

### Documentation Agent
```markdown
tools: ['codebase', 'search', 'usages', 'editFiles']
```

## Security & Auto-Approval

Some tools can be auto-approved to streamline workflows:

### Terminal Commands
Configure in settings.json:
```json
{
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "npm install": true,
    "git status": true,
    "rm": false  // Dangerous commands require approval
  }
}
```

### Global Auto-Approve
```json
{
  "chat.tools.global.autoApprove": false  // Disabled by default for security
}
```

⚠️ **Security Note**: Only auto-approve commands you trust. Review the [security documentation](https://code.visualstudio.com/docs/copilot/security) for implications.

## Related Documentation

- [Chat Tools Documentation](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features#chat-tools)
- [Using Tools in Chat](https://code.visualstudio.com/docs/copilot/chat/chat-tools)
- [Security Considerations](https://code.visualstudio.com/docs/copilot/security)
