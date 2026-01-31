---
description: [One-line description - shown in chat input placeholder]
name: [AgentName]
argument-hint: [Optional: Hint text for users]
tools: ['codebase', 'search', 'usages']
model: Claude Sonnet 4.5
handoffs:
  - label: 🚀 [Next Step]
    agent: [target-agent]
    prompt: [Optional handoff prompt]
    send: false
---

# [Agent Name]

[2-3 sentence purpose statement]

## Process

1. **[Step Name]**: [What to do]
2. **[Step Name]**: [What to do]
3. **[Step Name]**: [What to do]

## Output

[Expected output format and requirements]

## Constraints

- ❌ [What NOT to do]
- ✅ [What to do instead]

---

<!-- 
CUSTOMIZATION GUIDE:
- Set tools from: references/chat-tools.md
- Models: Sonnet 4.5 (analysis), Opus 4.5 (generation), Haiku 4.5 (fast)
- Handoff emojis: 🚀 ✅ 🔍 📝 🐛 ✏️ 📖 🧪
- Agent names: Use 'name' field or filename-without-.agent.md
- See references/agent-examples.md for patterns
-->
