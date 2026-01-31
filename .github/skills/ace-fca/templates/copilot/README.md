# GitHub Copilot Integration Templates

This directory contains templates for integrating ACE-FCA methodology with GitHub Copilot workspaces.

## Architecture

**Three Specialized Agents** + **Four Prompts** + **Instructions Section**

Following [github-copilot-customizer](../../github-copilot-customizer/SKILL.md) guidelines:

- **Agents** (86-118 lines): Personality + behavior, assume methodology in instructions
  - `researcher.agent.md` - Curious investigator
  - `planner.agent.md` - Meticulous architect with automatic ADR detection
  - `implementer.agent.md` - TDD purist with ADR enforcement
- **Prompts**: Task-focused entry points with proper frontmatter (agent/model/tools)
  - `research.prompt.md`, `planning.prompt.md`, `implementation.prompt.md`, `create-adr.prompt.md`
- **Instructions Section**: Add to your `.github/copilot-instructions.md`
  - `ace-fca-section.md` - Core ACE-FCA workflow rules (NOT a standalone .instructions.md file)

## Files Overview

### Agents

**`researcher.agent.md`**
- Investigation specialist for research phase
- Personality: Curious, thorough, analytical
- Tools: search, usages, fetch
- Returns compressed summaries (1-2 pages max)
- Handoff: "Create Plan" → planner
- **Usage**: `@researcher investigate <topic>`

**`planner.agent.md`**
- Architecture specialist for planning phase
- Personality: Meticulous, structured, detail-oriented
- Tools: search, usages
- Creates executable specifications (2-5 min tasks)
- **Automatically detects ADR needs** and inserts ADR tasks in plan
- Handoffs: "Execute Plan" → implementer, "Create ADR" → agent
- **Usage**: `@planner create plan for <feature>`

**`implementer.agent.md`**
- Build specialist for implementation phase
- Personality: TDD purist, methodical, honest
- Tools: search, usages
- Strict RED-GREEN-REFACTOR discipline
- Progressive compaction every 3-5 tasks
- **Blocks implementation if ADRs missing**
- Handoffs: "Create ADR" → agent, "Review Code" → agent
- **Usage**: `@implementer execute plan`

**`prompts/research.prompt.md`**
- Agent: 'agent', Model: Claude Sonnet 4.5
- Tools: search, usages, fetch
- Investigates codebase, returns compressed summary
- Creates research document in `docs/research/`
- **Usage**: `#research` (then provide topic)

**`prompts/planning.prompt.md`**
- Agent: 'agent', Model: Claude Sonnet 4.5
- Tools: search, usages
- Creates executable implementation plan
- Identifies ADR needs automatically
- **Usage**: `#planning` (then provide feature details)

**`prompts/implementation.prompt.md`**
- Agent: 'agent', Model: Claude Opus 4.5
- Tools: search, usages, edit, createFile
- Executes plan task-by-task with strict TDD
- Progressive compaction every 3-5 tasks
- **Usage**: `#implementation` (loads plan from `docs/plans/`)

**`prompts/create-adr.prompt.md`**
- Agent: 'agent', Model: Claude Sonnet 4.5
- Tools: search, createFile, edit
- Finds next ADR number, documents decision
- Manual ADR creation (planner auto-detects ADR needs)
- **Usage**: `#create-adr` (then provide decision detailsasks in plans

**Usage**: `#create-adr <decision_title>` (manual creation when needed)

### Instructions

**`ace-fca-workflow.instructions.md`**
- Core workflow rules for `copilot-instructions.md`
- Context management (40-60% rule)
- TDCopilot Instructions Section

**`ace-fca-section.md`**
- **NOT a standalone .instructions.md file!**
- Section template to add to your `.github/copilot-instructions.md`
- Contains core ACE-FCA workflow rules:
  - Context management (40-60% rule)
  - TDD discipline (test first!)
  - YAGNI principle
  - ADR creation triggers
  - Phase sequencing
  - Quality checks

**Usage**: Copy the content (starting from "## ACE-FCA Workflow") into your workspace's `.github/copilot-instructions.md` file
### 1. Copy Templates to Your Workspace

```bash
# Copy agent templates
cp templates/copilot/*.agent.md /path/to/your/workspace/.github/agents/

# Copy prompt templates
cp templates/copilot/prompts/*.prompt.md /path/to/your/workspace/.github/prompts/
```

### 2. Add ACE-FCA Section to copilot-instructions.md

Open `ace-fca-section.md` and copy the content (starting from "## ACE-FCA Workflow") into your workspace's `.github/copilot-instructions.md`:

```markdown
# .github/copilot-instructions.md

# Project Instructions

## Project Overview
- [Your project details]

## Coding Standards
- [Your standards]

## ACE-FCA Workflow

### When to Use ACE-FCA

Apply Advanced Context Engineering for Coding Agents (ACE-FCA) for:

✅ **Multi-step features** requiring research, planning, and implementation
[...rest of ACE-FCA section...]
```

**Important**: This is a SECTION to add to your copilot-instructions.md, not a standalone .instructions.md file.

### 3. Customize Agents (Optional)

Edit agent files to add:
- Project-specific patterns
- Team conventions
- Custom quality checks

### 4. Customize Prompts (Optional)

Edit prompt files to:
- Add project-specific questions
- Adjust output formats
- Include team standards

## Usage Patterns

### Using Agents

Invoke agents directly in chat:

```
@researcher investigate authentication patterns
@planner create plan for user login feature
@implementer execute the plan
```

### Using Prompts

Use # prefix for prompts:

```
#research
  (agent asks: what topic?)
  
#planning
  (agent asks: what feature?)
  
#implementation
  (agent loads plan from docs/plans/)
  
#create-adr
  (agent asks: what decision?)
```

### Handoff Flow Example

```
1. @researcher investigate auth
   → Research complete
   → Use "Create Plan" handoff → @planner

2. @planner create auth plan
   → Plan created (includes ADR task if needed)
   → Use "Execute Plan" handoff → @implementer
   → Or "Create ADR" handoff if decision needed first

3. @implementer execute plan
   → Executes with TDD
   → Use "Review Code" handoff when complete
```

## Customization Guide

### For Your Team

1. **Add Team Standards**:
   - Update instructions with team conventions
   - Add links to internal docs
   - Reference team tools

2. **Project-Specific Checks**:
   - Add pre-flight checks in implementation prompt
   - Custom validation steps
   - Project-specific ADR triggers

3. **Tool Integration**:
   - Add commands for your CI/CD
   - Reference your testing framework
   - Include deployment steps

### For Your Project

1. **File Paths**:
   - Update default directories (docs/, tests/, etc.)
   - Adjust to match project structure

2. **Testing Framework**:
   - Update test commands in prompts
   - Adjust TDD examples

3. **ADR Numbering**:
   - If using different numbering scheme
   - If ADRs in different location

## ADR Automation

### Automatic Detection by Planner

The **Planner agent automatically detects** architectural decisions and inserts ADR creation tasks in plans:

**ADR Triggers** (auto-detected):
- Technology/library selection
- Architecture patterns
- API design decisions
- Data model changes
- Security approaches
- Performance strategies
- Integration patterns

**Workflow**:
1. `@planner` scans requirements/tasks for architectural decisions
2. Inserts ADR task BEFORE dependent implementation tasks
3. `@implementer` blocks at ADR task if ADR not created
4. User creates ADR (via `#create-adr` or manually)
5. `@implementer` continues after ADR is documented

**Why Automatic?** Users often forget to create ADRs. Automatic detection ensures architectural decisions are always documented.

## Best Practices

### When to Use What

**Use Agents** (`@agent-name`):
- `@researcher`: Investigate codebase area, understand patterns
- `@planner`: Create executable specification with ADR detection
- `@implementer`: Execute plan with strict TDD discipline

**Use Prompts** (`#prompt-name`):
- Quick entry to specific phase
- Stateless, task-focused execution
- Alternative to agent invocation

**Both work** - choose based on preference:
- Agents: Conversational, maintain some context
- Prompts: Quick, clean slate each time

### Handoff Buttons

Agents provide handoff buttons after completing work:
- Click to continue to next phase
- Pre-filled prompt for smooth transition
- E.g., "Create Plan", "Execute Plan", "Review Code"

### Context Management

ACE-FCA enforces context discipline:
- Keep usage between 40-60% of context window
- Below 40%: Probably missing necessary context
- Above 60%: Risk hallucination, must compact NOW
- Progressive compaction every 3-5 implementation tasks

## Troubleshooting

### Agent Not Found

- Verify file is in `.github/agents/` (relative to workspace root)
- Check filename: `researcher.agent.md`, `planner.agent.md`, `implementer.agent.md`
- Ensure YAML frontmatter is valid
- Try: `@researcher`, `@planner`, `@implementer`

### Prompt Not Working

- Verify file is in `.github/prompts/`
- Check filename: `research.prompt.md`, etc.
- Ensure YAML frontmatter is valid (agent, model, tools)
- Try: `#research`, `#planning`, `#implementation`, `#create-adr`

### Instructions Not Applied

- Check file is at `.github/copilot-instructions.md` (exact path)
- Ensure ACE-FCA section is properly copied (starting with "## ACE-FCA Workflow")
- Restart VS Code if needed

### Handoffs Not Showing

- Verify handoffs in agent frontmatter (label, agent, prompt, send)
- Ensure target agent name matches exactly
- Handoff buttons appear after agent completes task

## File Organization

After setup, your workspace should look like:

```
.github/
├── copilot-instructions.md         # With ACE-FCA section added
├── agents/
│   ├── researcher.agent.md
│   ├── planner.agent.md
│   └── implementer.agent.md
└── prompts/
    ├── research.prompt.md
    ├── planning.prompt.md
    ├── implementation.prompt.md
    └── create-adr.prompt.md
```

## See Also

- [ACE-FCA Main Skill](../../SKILL.md) - Complete methodology reference
- [GitHub Copilot Customizer](../../../github-copilot-customizer/SKILL.md) - Copilot customization guide
4. Update examples with learnings
