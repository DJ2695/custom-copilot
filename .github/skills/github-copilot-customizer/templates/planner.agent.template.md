---
description: [Brief description of what this agent does - shown in UI when selecting agents]
name: [Display Name]
tools: ['search', 'fetch', 'githubRepo', 'usages']
model: Claude Sonnet 4.5
handoffs:
  - label: [Button Label for Handoff]
    agent: [target-agent-name]
    prompt: [Optional prompt to send with handoff]
    send: false
---

# [Agent Name] Instructions

[Explain the agent's core purpose and behavior in 2-3 sentences]

## When to Use This Agent

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Task Guidelines

### Process
1. [First step the agent should take]
2. [Second step]
3. [Third step]
4. [Final step]

### Output Requirements
- [Format requirement]
- [Quality criteria]
- [Structure expectations]

## Project Context

Reference project patterns: #tool:githubRepo [org/repo-templates]
Reference documentation: #tool:search/codebase

## Constraints

- [What the agent should NOT do]
- [Limitations to respect]
- [Boundaries to maintain]
