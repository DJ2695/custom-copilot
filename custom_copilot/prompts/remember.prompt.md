---
description: 'Review conversation and capture valuable knowledge in appropriate customization files'
tools: ['search']
---

Review our conversation and capture valuable knowledge in GitHub Copilot customization files. Focus especially on **best practices** we discussed or discovered—these are the most important things to preserve.

## Step 1: Identify Best Practices and Key Learnings

Scan the conversation for:

### Best Practices (highest priority)
- **Patterns that worked well** - approaches, techniques, or solutions we found effective
- **Anti-patterns to avoid** - mistakes, gotchas, or approaches that caused problems
- **Quality standards** - criteria we established for good code, documentation, or processes
- **Decision rationale** - why we chose one approach over another

### Other Valuable Knowledge
- Coding conventions and style preferences
- Project architecture decisions
- Workflows and processes we developed
- Tools, libraries, or techniques worth remembering
- Feedback I gave about your behavior or outputs

## Step 2: Decide Where to Store Each Learning

For each best practice or learning, choose the right destination in GitHub Copilot's customization structure:

### → Instructions (.instructions.md) for coding guidelines and preferences
Use instruction files when the knowledge is:
- A coding standard, convention, or style preference
- A guideline that should apply to specific files (use `applyTo` glob patterns)
- A simple rule or pattern
- Something to always keep in mind during code generation

**Workspace** (`.github/copilot-instructions.md`): General instructions for all chat requests
**Targeted** (`instructions/<name>.instructions.md`): Specific guidelines with `applyTo` patterns

Example locations:
- `instructions/general-coding.instructions.md` (applies to all files with `applyTo: "**"`)
- `instructions/python-standards.instructions.md` (applies to `**/*.py`)
- `instructions/react-guidelines.instructions.md` (applies to `**/*.tsx,**/*.jsx`)

### → Prompts (.prompt.md) for reusable task workflows
**Create a prompt file when** we developed:
- A specific task workflow (e.g., "generate API endpoint", "security review")
- A multi-step process for a particular type of work
- A methodology with clear inputs and outputs
- A template for a repeatable task

**Location:** `prompts/<task-name>.prompt.md`

### → Skills (SKILL.md) for comprehensive, reusable capabilities
**Create a skill when** we developed:
- A comprehensive methodology requiring multiple steps
- A workflow with best practices baked in
- A specialized capability that combines knowledge and process
- A procedure that should be followed consistently across contexts

**Location:** `skills/<skill-name>/SKILL.md`

Skills are the most powerful option because they can encode both **what** to remember and **how** to do something well.

### → Agents (agent.md) for specialized modes with handoffs
**Create an agent when** we developed:
- A specialized working mode (e.g., planner, reviewer, implementer)
- A workflow that hands off to other agents
- A configuration requiring specific tools or model settings

**Location:** `agents/<agent-name>/agent.md`

## Step 3: Create Files for Significant Best Practices

### For Instruction Files (.instructions.md)

**Location:** `instructions/<name>.instructions.md`

**Structure:**
```markdown
---
applyTo: "<glob-pattern>"
---
# <Category> Guidelines

## <Subcategory>
- Guideline 1: explanation
- Guideline 2: explanation

## Best Practices
- Best practice 1: why it matters
- Anti-pattern to avoid: why it's problematic

## <Another Subcategory>
- Guideline 3: explanation
```

**Key Principles:**
- Use specific glob patterns in `applyTo` to target relevant files
- Keep guidelines concise and actionable
- Include both do's and don'ts
- Explain the "why" for non-obvious rules

### For Prompt Files (.prompt.md)

**Location:** `prompts/<task-name>.prompt.md`

**Structure:**
```markdown
---
agent: 'agent' | 'ask'
model: Claude Sonnet 4 | GPT-4o
description: 'Brief description of what this prompt does'
tools: ['search', 'codebase', 'githubRepo']
---

Brief overview of the task this prompt handles.

## Requirements
- Requirement 1
- Requirement 2

## Process
1. First, do X
2. Then, do Y
3. Finally, do Z

## Best Practices
- Best practice 1: explanation
- Anti-pattern to avoid: why

## Output Format
Describe the expected output format (e.g., Markdown, code, structured response)
```

**Key Principles:**
- Clear description in frontmatter (used for prompt discovery)
- Specify required tools
- Include best practices learned from experience
- Define clear output expectations

### For Skills (SKILL.md)

**Location:** `skills/<skill-name>/SKILL.md`

**Structure:**
```markdown
---
name: skill-name
description: "What this skill does AND when to use it. Include triggers like 'when the user asks to X' or 'when working with Y'. This description determines when the skill activates."
---

# Skill Name

## Overview
Brief explanation of what this skill accomplishes and when to use it.

## Best Practices
Capture the key best practices upfront:
- Best practice 1: explanation and why it matters
- Best practice 2: explanation and context
- Anti-pattern to avoid: why it causes problems

## Prerequisites
- Required tools, knowledge, or setup

## Process
Step-by-step instructions (imperative form):
1. First, do X because Y
2. Then, check Z to ensure A
3. Finally, verify B

## Common Pitfalls
- Pitfall to avoid and why
- Another anti-pattern we discovered and its consequences

## Examples
Brief examples of the skill in action (optional but helpful)

## References
Links to related documentation or resources (optional)
```

**Skill Folder Structure:**
```
skill-name/
├── SKILL.md          (required - main instructions with best practices)
├── scripts/          (optional - executable code)
├── references/       (optional - detailed documentation)
└── assets/           (optional - templates, examples)
```

**Key Principles:**
1. **Encode best practices prominently** - Put them near the top so they guide the entire workflow
2. **Concise is key** - Only include non-obvious knowledge. Every paragraph should justify its token cost
3. **Clear triggers** - The description determines when the skill activates. Be specific
4. **Imperative form** - Write as commands: "Create a file" not "You should create a file"
5. **Include anti-patterns** - What NOT to do is often as valuable as what to do
6. **Explain the why** - Context helps understand when to deviate from the pattern

### For Agents (agent.md)

**Location:** `agents/<agent-name>/agent.md`

**Structure:**
```markdown
---
description: What this agent does
name: Agent Name
tools: ['search', 'codebase', 'githubRepo']
model: Claude Sonnet 4
handoffs:
  - label: Next Step
    agent: other-agent
    prompt: Prompt to send when handing off
    send: false
---

# Agent instructions

You are in <mode> mode. Your task is to <primary responsibility>.

## Responsibilities
- Responsibility 1
- Responsibility 2

## Best Practices
- Best practice from our conversation
- Anti-pattern to avoid

## Output
Expected output format and structure

## Handoff Criteria
When to hand off to the next agent:
- Condition 1
- Condition 2
```

## Step 4: Create or Update Files

Use the appropriate tool based on what you're creating:

### For new files:
```bash
# Instruction file
create <path>/instructions/<name>.instructions.md

# Prompt file  
create <path>/prompts/<task-name>.prompt.md

# Skill
create <path>/skills/<skill-name>/SKILL.md

# Agent
create <path>/agents/<agent-name>/agent.md
```

### For updates:
```bash
# Use edit to modify existing files
edit <path>/<file>
```

## Step 5: Reference Related Files

When creating customization files, reference related files when appropriate:

**In instruction files:**
```markdown
Apply the [general coding guidelines](./general-coding.instructions.md) to all code.
```

**In prompt files:**
```markdown
Use form design system components: [design-system/Form.md](../docs/design-system/Form.md)
```

**In skill files:**
```markdown
See [reference documentation](./references/detailed-guide.md) for more details.
```

## Step 6: Summarize Changes

After creating or updating files, provide a clear summary:

### Files Created
- **instructions/python-best-practices.instructions.md**
  - Captured best practices for Python development
  - Key learnings: error handling patterns, type hints usage
  - Applies to: `**/*.py`

- **skills/api-review/SKILL.md**
  - Comprehensive API security review workflow
  - Encoded best practices for: authentication checks, input validation
  - Anti-patterns documented: missing rate limiting, inadequate logging

### Files Updated
- **instructions/general-coding.instructions.md**
  - Added naming convention best practices discovered in conversation
  - Added error handling pattern that solved our issue

### Best Practices Captured
List the key best practices preserved:
1. **Pattern X** - Why it works well and when to use it
2. **Avoiding Y** - Why this causes problems and what to do instead
3. **Standard Z** - The rationale behind this decision

## Guidelines for Effective Capture

### What Makes Good Customization Content
- **Actionable:** Clear, specific instructions rather than vague advice
- **Contextual:** Explains why a practice matters, not just what to do
- **Scoped:** Applies appropriate `applyTo` patterns or clear trigger descriptions
- **Concise:** Every sentence adds value; remove obvious or redundant information
- **Discoverable:** Good descriptions and names make content easy to find and reuse

### What to Avoid
- Generic advice that applies to all programming (unless project-specific context added)
- Duplicating information across multiple files
- Creating files for one-off solutions that won't be reused
- Overly verbose instructions that dilute key points
- Vague descriptions that make content hard to discover

### Quality Check
Before finalizing, ask:
- [ ] Does this capture knowledge we actually developed in the conversation?
- [ ] Is this specific enough to be actionable?
- [ ] Will this be valuable the next time we encounter this situation?
- [ ] Is this in the right type of file for its purpose?
- [ ] Have I included the "why" for non-obvious practices?
- [ ] Are the triggers/patterns clear for when this should be used?