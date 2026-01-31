# Recommended VS Code Settings for Copilot

Essential settings to enable and configure for optimal GitHub Copilot experience.

## Minimal Required Settings

Start with these essential settings in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.agent.enabled": true
}
```

## Recommended Settings by Category

### 📋 Essential Settings

```json
{
  // REQUIRED: Enable instruction files
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  
  // Enable agent mode (required for custom agents)
  "chat.agent.enabled": true,
  
  // Show Chat menu in title bar
  "chat.commandCenter.enabled": true,
  
  // Enable AI search in Settings editor
  "workbench.settings.showAISearchToggle": true
}
```

### 🤖 Agent Settings

```json
{
  // Maximum requests agents can make
  "chat.agent.maxRequests": 25,
  
  // Auto-fix issues in generated code
  "github.copilot.chat.agent.autoFix": true,
  
  // Enable MCP server access
  "chat.mcp.access": true,
  
  // Enable MCP gallery in Extensions view
  "chat.mcp.gallery.enabled": true,
  
  // Auto-start MCP servers when config changes
  "chat.mcp.autoStart": "newAndOutdated"
}
```

### 💬 Chat Settings

```json
{
  // Enable chat participant detection
  "chat.detectParticipant.enabled": true,
  
  // Enable checkpoints in chat
  "chat.checkpoints.enabled": true,
  
  // Show file changes summary after each request
  "chat.checkpoints.showFileChanges": true,
  
  // Enable math rendering with KaTeX
  "chat.math.enabled": true,
  
  // Show chat session title in header
  "chat.viewTitle.enabled": true,
  
  // Use AGENTS.md files as context
  "chat.useAgentsMdFile": true
}
```

### ✍️ Code Editing Settings

```json
{
  // Show Copilot commands as Code Actions
  "github.copilot.editor.enableCodeActions": true,
  
  // Auto-generate symbol renaming suggestions
  "github.copilot.renameSuggestions.triggerAutomatically": true,
  
  // Enable next edit suggestions (NES)
  "github.copilot.nextEditSuggestions.enabled": true,
  
  // Allow code shifting for NES
  "editor.inlineSuggest.edits.allowCodeShifting": "always",
  
  // Enable NES based on diagnostics
  "github.copilot.nextEditSuggestions.fixes": true,
  
  // Show syntax highlighting for inline suggestions
  "editor.inlineSuggest.syntaxHighlightingEnabled": true
}
```

### 🔧 Terminal & Tools

```json
{
  // Enable auto-approval of terminal commands
  "chat.tools.terminal.enableAutoApprove": true,
  
  // Configure which commands to auto-approve
  "chat.tools.terminal.autoApprove": {
    "npm install": true,
    "npm test": true,
    "git status": true,
    "git diff": true,
    "ls": true,
    "cat": true,
    // Require approval for dangerous commands
    "rm": false,
    "rmdir": false,
    "del": false,
    "kill": false
  },
  
  // Require approval for file writes outside workspace
  "chat.tools.terminal.blockDetectedFileWrites": "outsideWorkspace"
}
```

### 📝 Custom Instructions & Prompts

```json
{
  // Locations to search for instruction files
  "chat.instructionsFilesLocations": {
    ".github/instructions": true
  },
  
  // Locations to search for prompt files
  "chat.promptFilesLocations": {
    ".github/prompts": true
  },
  
  // Custom commit message instructions
  "github.copilot.chat.commitMessageGeneration.instructions": [
    { "text": "Use conventional commits format (feat:, fix:, docs:, etc.)" },
    { "text": "Keep subject line under 50 characters" },
    { "text": "Reference issue numbers when applicable" }
  ],
  
  // Custom PR description instructions
  "github.copilot.chat.pullRequestDescriptionGeneration.instructions": [
    { "text": "Include summary of changes" },
    { "text": "List breaking changes if any" },
    { "text": "Add testing instructions" }
  ]
}
```

### 🧪 Testing & Debugging

```json
{
  // Enable /startDebugging command
  "github.copilot.chat.startDebugging.enabled": true,
  
  // Enable copilot-debug terminal command
  "github.copilot.chat.copilotDebugCommand.enabled": true,
  
  // Enable /setupTests command
  "github.copilot.chat.setupTests.enabled": true
}
```

### 🔎 Search Settings

```json
{
  // Semantic search in Search view
  "search.searchView.semanticSearchBehavior": "auto",
  
  // Show keyword suggestions
  "search.searchView.keywordSuggestions": true
}
```

### 🎨 Inline Chat Settings

```json
{
  // Hold shortcut key to enable speech
  "inlineChat.holdToSpeech": true,
  
  // Trigger inline chat on natural language
  "inlineChat.lineNaturalLanguageHint": true
}
```

## Experimental Features

Enable cutting-edge features (may change):

```json
{
  // Enable Agent Skills support
  "chat.useAgentSkills": true,
  
  // Show recent chat history in empty state
  "chat.emptyState.history.enabled": true,
  
  // Use custom agents with subagents
  "chat.customAgentInSubagent.enabled": true,
  
  // Enable thinking tool when using agents
  "github.copilot.chat.agent.thinkingTool": true,
  
  // Auto-discover MCP servers from other apps
  "chat.mcp.discovery.enabled": false,
  
  // Show Generate tests code lens
  "github.copilot.chat.generateTests.codeLens": true
}
```

## Complete Recommended Configuration

Copy this comprehensive configuration to `.vscode/settings.json`:

```json
{
  // ===== ESSENTIAL =====
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.agent.enabled": true,
  "chat.commandCenter.enabled": true,
  
  // ===== AGENTS =====
  "chat.agent.maxRequests": 25,
  "github.copilot.chat.agent.autoFix": true,
  "chat.mcp.access": true,
  "chat.mcp.gallery.enabled": true,
  "chat.mcp.autoStart": "newAndOutdated",
  
  // ===== CHAT =====
  "chat.detectParticipant.enabled": true,
  "chat.checkpoints.enabled": true,
  "chat.math.enabled": true,
  "chat.useAgentsMdFile": true,
  
  // ===== CODE EDITING =====
  "github.copilot.editor.enableCodeActions": true,
  "github.copilot.renameSuggestions.triggerAutomatically": true,
  "github.copilot.nextEditSuggestions.enabled": true,
  "editor.inlineSuggest.syntaxHighlightingEnabled": true,
  
  // ===== TERMINAL & TOOLS =====
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "npm install": true,
    "npm test": true,
    "git status": true,
    "rm": false,
    "del": false
  },
  
  // ===== CUSTOM INSTRUCTIONS =====
  "chat.instructionsFilesLocations": {
    ".github/instructions": true
  },
  "chat.promptFilesLocations": {
    ".github/prompts": true
  },
  
  // ===== TESTING =====
  "github.copilot.chat.startDebugging.enabled": true,
  "github.copilot.chat.setupTests.enabled": true,
  
  // ===== SEARCH =====
  "search.searchView.semanticSearchBehavior": "auto"
}
```

## Setting Priority Order

When settings conflict, this is the resolution order:
1. **Workspace** settings (`.vscode/settings.json`)
2. **Workspace folder** settings
3. **User** settings
4. **Default** values

## Settings by Use Case

### For Team Projects
```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.agent.enabled": true,
  "chat.instructionsFilesLocations": {
    ".github/instructions": true
  },
  "chat.promptFilesLocations": {
    ".github/prompts": true
  }
}
```

### For Individual Development
```json
{
  "chat.agent.enabled": true,
  "chat.agent.maxRequests": 50,
  "github.copilot.chat.agent.autoFix": true,
  "chat.tools.terminal.enableAutoApprove": true
}
```

### For Security-Conscious Teams
```json
{
  "chat.tools.terminal.enableAutoApprove": false,
  "chat.tools.global.autoApprove": false,
  "chat.tools.terminal.blockDetectedFileWrites": "outsideWorkspace",
  "chat.mcp.access": false
}
```

## Troubleshooting

| Issue | Setting to Check |
|-------|------------------|
| Instructions not applied | `github.copilot.chat.codeGeneration.useInstructionFiles` |
| Custom agents not showing | `chat.agent.enabled` |
| MCP servers not available | `chat.mcp.access`, `chat.mcp.gallery.enabled` |
| Terminal commands need approval | `chat.tools.terminal.enableAutoApprove` |
| Too many agent requests | Increase `chat.agent.maxRequests` |

## Related Documentation

- [Copilot Settings Reference](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
- [VS Code User and Workspace Settings](https://code.visualstudio.com/docs/configure/settings)
- [Security Considerations](https://code.visualstudio.com/docs/copilot/security)
