---
agent: 'agent'
model: Claude Sonnet 4
tools: ['githubRepo', 'search/codebase']
description: '[Brief task description - shown in prompt picker UI]'
---

# [Task Name]

[Detailed explanation of what this prompt accomplishes]

## Initial Questions

<!-- Ask clarifying questions if required information is missing -->
If not provided, ask the user for:
- [Required input 1]
- [Required input 2]

## Context

<!-- Reference external resources -->
Reference templates: #tool:githubRepo [org/repo-templates]
Reference local files: [relevant-doc.md](../docs/relevant-doc.md)

## Requirements

### [Category 1]
- [Requirement 1.1]
- [Requirement 1.2]

### [Category 2]
- [Requirement 2.1]
- [Requirement 2.2]

## Output Format

- [Expected structure]
- [File naming conventions]
- [Quality criteria]

## Examples

<!-- Optional: Include examples of expected output -->

### Input
```
[Example input]
```

### Expected Output
```
[Example output structure]
```
