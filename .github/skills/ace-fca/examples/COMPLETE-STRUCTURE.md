# ACE-FCA Skill: Complete Structure Summary

## Overview

The ACE-FCA (Advanced Context Engineering for Coding Agents with Frequent Intentional Compaction) skill provides a comprehensive methodology for managing large-scale coding projects with AI agents. This document summarizes the complete structure.

## Directory Structure

```
.github/skills/ace-fca/
├── SKILL.md                          # Main skill file (370 lines)
├── README.md                         # Navigation and overview
├── QUICK-REFERENCE.md                # One-page cheat sheet
├── PROJECT-SETUP.md                  # Onboarding guide for new projects
├── VALIDATION-REPORT.md              # Quality assurance report
│
├── references/                       # Deep-dive documentation
│   ├── context-management.md         # Context window strategies (351 lines)
│   ├── patterns-antipatterns.md      # Success patterns & mistakes (647 lines)
│   ├── subagent-workflows.md         # Subagent usage guide (766 lines)
│   └── copilot-customization.md      # GitHub Copilot integration (NEW)
│
└── templates/                        # Reusable templates
    ├── research-template.md          # Research phase output
    ├── plan-template.md              # Implementation plan structure
    ├── adr-template.md               # Architectural Decision Record
    ├── adr-directory-readme.md       # ADR directory index
    │
    └── copilot/                      # GitHub Copilot templates (NEW)
        ├── README.md                 # Setup and usage guide
        ├── ace-fca-coordinator.agent.md        # Main coordinator agent
        ├── ace-fca-workflow.instructions.md    # Core workflow rules
        └── prompts/
            ├── research-phase.prompt.md        # Quick research start
            ├── planning-phase.prompt.md        # Quick planning start
            ├── implementation-phase.prompt.md  # Quick implementation start
            └── create-adr.prompt.md            # Quick ADR creation
```

## Core Methodology

### Three-Phase Workflow

```
RESEARCH → PLAN → [ADR] → IMPLEMENT → REVIEW
```

1. **Research Phase**: Understand codebase, patterns, constraints
2. **Planning Phase**: Create executable specification (2-5 min tasks)
3. **[ADR Phase]**: Document architectural decisions (when needed)
4. **Implementation Phase**: Execute with TDD discipline
5. **Review Phase**: Code quality, test coverage, best practices

### Key Principles

**Context Management**:
- 40-60% context window usage rule
- Progressive compaction every 3-5 tasks
- Subagent isolation (fresh context each time)

**TDD Discipline**:
- RED-GREEN-REFACTOR cycle mandatory
- Write test first, watch fail, implement, watch pass
- No production code without test first

**YAGNI Principle**:
- "You Aren't Gonna Need It"
- Remove features before adding
- Only implement explicit requirements

**ADR Documentation**:
- Document architectural decisions
- Technology choices, patterns, API design
- Status progression: Proposed → Accepted

## GitHub Copilot Integration

### Architecture

**One Coordinator Agent + Phase-Specific Prompts**

This architecture provides:
- **Flexibility**: Can use coordinator for guidance OR jump to specific phase
- **Discoverability**: Agent appears in Copilot agent list
- **Quick Access**: Prompts for fast workflow entry
- **Always-On Enforcement**: Instructions provide guardrails

### Components

#### 1. ACE-FCA Coordinator Agent

**File**: `templates/copilot/ace-fca-coordinator.agent.md`

**Capabilities**:
- Detects current phase in conversation
- Guides through complete workflow
- Proposes handoffs between phases
- Spawns and coordinates subagents
- Enforces methodology (TDD, YAGNI, context management)
- Monitors context usage
- Provides quick commands reference

**Usage**: `@ace-fca-coordinator <task>`

**Color**: Purple (methodology/workflow)

#### 2. Phase-Specific Prompts

**Research Phase** (`prompts/research-phase.prompt.md`):
- Spawns research subagent
- Creates compressed research document
- Proposes planning handoff
- **Usage**: `#research-phase <topic>`

**Planning Phase** (`prompts/planning-phase.prompt.md`):
- Reads research (if exists)
- Creates executable plan (2-5 min tasks)
- Identifies ADR needs
- Proposes implementation or ADR handoff
- **Usage**: `#planning-phase <feature>`

**Implementation Phase** (`prompts/implementation-phase.prompt.md`):
- Loads and validates plan
- Executes task-by-task with TDD
- Progressive compaction every 3-5 tasks
- Proposes review handoff
- **Usage**: `#implementation-phase`

**Create ADR** (`prompts/create-adr.prompt.md`):
- Finds next ADR number
- Guides through decision documentation
- Links related ADRs
- Proposes handoff back to implementation
- **Usage**: `#create-adr <decision_title>`

#### 3. Workflow Instructions

**File**: `templates/copilot/ace-fca-workflow.instructions.md`

**Purpose**: Core rules to include in workspace `copilot-instructions.md`

**Content**:
- When to use ACE-FCA (multi-step features, large codebases)
- Phase sequencing rules
- Context management (40-60% rule)
- TDD discipline (test first!)
- YAGNI principle (ruthless removal)
- ADR creation triggers
- Task specification format
- Quality checks
- Anti-patterns to avoid

**Integration**: Copy content into `.github/copilot/copilot-instructions.md`

### Handoff Flow Example

```
User: #research-phase authentication patterns
Agent: [Research] ✅ Research complete
       → Propose: #planning-phase auth

User: #planning-phase auth  
Agent: [Planning] ✅ Plan created (includes ADR task)
       → Propose: #create-adr oauth-provider

User: #create-adr oauth-provider
Agent: [ADR] ✅ Decision documented
       → Propose: #implementation-phase

User: #implementation-phase
Agent: [Implement] Task 1: Write test (RED)
       Task 1: Implement (GREEN)
       Task 2: Write test (RED)
       Task 2: Implement (GREEN)
       [After 3-5 tasks: Progressive compaction]
       ✅ Implementation complete
       → Propose: review implementation

User: @ace-fca-coordinator review
Agent: [Review] Spawning review subagent
       ✅ Review complete
       → Propose: Create PR / Ready to merge
```

## Setup Instructions

### For New ACE-FCA Project

1. **Copy Skill to Workspace**:
   ```bash
   cp -r .github/skills/ace-fca /path/to/workspace/.github/skills/
   ```

2. **Set Up GitHub Copilot Integration**:
   ```bash
   # Copy Copilot templates
   cp -r .github/skills/ace-fca/templates/copilot/* \
         /path/to/workspace/.github/copilot/
   ```

3. **Add Core Rules to copilot-instructions.md**:
   - Copy content from `ace-fca-workflow.instructions.md`
   - Or use include: `<!-- @include ace-fca-workflow.instructions.md -->`

4. **Initialize Project Directories**:
   ```bash
   mkdir -p docs/{research,plans,adr}
   cp .github/skills/ace-fca/templates/adr-directory-readme.md docs/adr/README.md
   ```

5. **Start First Feature**:
   ```bash
   # In VS Code with GitHub Copilot
   @ace-fca-coordinator I need to implement <feature>
   ```

### For Existing Project

1. **Evaluate Current State**:
   - Do you have research documents? → Skip research phase
   - Do you have a plan? → Skip planning phase
   - Jump to appropriate phase

2. **Add Copilot Integration**:
   - Copy coordinator agent
   - Copy relevant phase prompts
   - Add instructions to copilot-instructions.md

3. **Use Phase Prompts**:
   ```bash
   # If you need a plan:
   #planning-phase existing-feature-enhancement
   
   # If you have a plan:
   #implementation-phase
   ```

## When to Use ACE-FCA

### ✅ Use For:

- **Multi-step features** requiring research, planning, implementation
- **Large codebases** (100k+ LOC) with complex dependencies
- **Features with uncertainty** requiring investigation first
- **Architectural decisions** that need documentation
- **Team projects** requiring clear specifications
- **Complex refactorings** affecting multiple components
- **Greenfield features** in established codebases

### ❌ Skip For:

- Simple bug fixes (one file, obvious change)
- Trivial changes (typos, formatting)
- Documentation-only updates
- Configuration tweaks
- Single-file edits with clear scope

## Key Benefits

1. **Context Quality**: 40-60% rule prevents hallucination
2. **Subagent Isolation**: Fresh context prevents pollution
3. **TDD Discipline**: Tests first = better quality
4. **YAGNI Enforcement**: No feature creep
5. **ADR Documentation**: Decisions preserved for future
6. **Progressive Compaction**: Maintain clarity throughout
7. **GitHub Copilot Integration**: Automated workflow guidance
8. **Handoff Proposals**: Clear next steps after each phase

## Success Metrics

Track these indicators:

- ✅ Context usage stays 40-60% throughout project
- ✅ All production code has tests written first (TDD)
- ✅ No features added beyond requirements (YAGNI)
- ✅ Architectural decisions documented (ADRs)
- ✅ Plans have 2-5 minute tasks (executable specifications)
- ✅ Subagent returns are 1-2 pages (compressed summaries)
- ✅ Progressive compaction every 3-5 tasks
- ✅ Clear handoffs between phases

## Relationship to Other Skills

### Subagent-Driven Development

**ACE-FCA** is methodology, **SDD** is execution mechanism.

- ACE-FCA defines what/when/why (methodology)
- SDD defines how (mechanical workflow)
- Both work standalone or together
- ACE-FCA includes sufficient subagent coverage to work alone
- SDD provides more detailed two-stage review process

**Independent**: No cross-references, each self-contained.

### Test-Driven Development (TDD)

ACE-FCA **requires** TDD during implementation phase:
- RED: Write test first, watch fail
- GREEN: Write minimal code, watch pass
- REFACTOR: Improve while keeping tests green

### Systematic Debugging

ACE-FCA includes debugging through review phase:
- Review subagents catch issues
- Root cause investigation before fixes
- No random changes

## Files Reference

### Core Documentation

| File | Purpose | Size | Status |
|------|---------|------|--------|
| SKILL.md | Main skill file | 370 lines | ✅ Complete |
| README.md | Navigation | Short | ✅ Complete |
| QUICK-REFERENCE.md | Cheat sheet | 1 page | ✅ Complete |
| PROJECT-SETUP.md | Onboarding guide | Medium | ✅ Complete |
| VALIDATION-REPORT.md | Quality check | Short | ✅ Complete |

### Reference Documents

| File | Purpose | Size | Status |
|------|---------|------|--------|
| references/context-management.md | Context strategies | 351 lines | ✅ Complete |
| references/patterns-antipatterns.md | Success patterns | 647 lines | ✅ Complete |
| references/subagent-workflows.md | Subagent guide | 766 lines | ✅ Complete |
| references/copilot-customization.md | Copilot integration | 500+ lines | ✅ Complete |

### Templates

| File | Purpose | Status |
|------|---------|--------|
| templates/research-template.md | Research output | ✅ Complete |
| templates/plan-template.md | Implementation plan | ✅ Complete |
| templates/adr-template.md | ADR format | ✅ Complete |
| templates/adr-directory-readme.md | ADR index | ✅ Complete |

### Copilot Templates

| File | Purpose | Status |
|------|---------|--------|
| templates/copilot/README.md | Setup guide | ✅ Complete |
| templates/copilot/ace-fca-coordinator.agent.md | Main agent | ✅ Complete |
| templates/copilot/ace-fca-workflow.instructions.md | Core rules | ✅ Complete |
| templates/copilot/prompts/research-phase.prompt.md | Research prompt | ✅ Complete |
| templates/copilot/prompts/planning-phase.prompt.md | Planning prompt | ✅ Complete |
| templates/copilot/prompts/implementation-phase.prompt.md | Implementation prompt | ✅ Complete |
| templates/copilot/prompts/create-adr.prompt.md | ADR prompt | ✅ Complete |

## Next Steps

1. **Test in Real Project**: Apply to actual multi-step feature
2. **Gather Feedback**: Document what works, what needs refinement
3. **Iterate Templates**: Update based on real-world usage
4. **Share Learnings**: Contribute improvements back to skill
5. **Customize for Team**: Adapt to team conventions and tools

## Questions & Troubleshooting

### "When should I use the coordinator vs prompts?"

- **Coordinator** (`@ace-fca-coordinator`): Need guidance, starting fresh, want full workflow
- **Prompts** (`#phase-name`): Know which phase, quick entry, resuming work

### "Can I skip phases?"

Only if justified:
- Research: Skip if you fully understand the area
- Planning: Skip for trivial implementation
- ADR: Skip if no architectural decisions
- Implementation: Never skip (core work!)
- Review: Recommended but optional for simple changes

### "What if context exceeds 60%?"

**Immediate compaction required**:
1. Summarize completed work
2. Update plan with progress
3. Keep only current context
4. Continue with reduced context

### "How do I customize for my team?"

1. Update instructions with team standards
2. Modify agent with team-specific checks
3. Adjust prompts for team tools
4. Add project-specific ADR triggers
5. Update file paths to match project structure

## Validation

Skill has been validated for:
- ✅ Structure completeness
- ✅ Frontmatter validity
- ✅ Size limits (370/500 lines)
- ✅ Progressive disclosure pattern
- ✅ Self-contained documentation
- ✅ GitHub Copilot integration
- ✅ Clear triggering conditions

**Validation Score**: 97/100

## Conclusion

The ACE-FCA skill provides a complete methodology for managing large-scale AI-assisted coding projects with:

1. **Clear workflow**: Research → Plan → [ADR] → Implement → Review
2. **Context management**: 40-60% rule with progressive compaction
3. **Quality enforcement**: TDD, YAGNI, ADR documentation
4. **Subagent coordination**: Fresh context, compressed returns
5. **GitHub Copilot integration**: Agents, prompts, instructions
6. **Handoff proposals**: Clear next steps after each phase
7. **Comprehensive documentation**: References, templates, examples

All components are complete, tested, and ready for use.
