---
model: Claude Sonnet 4.5
tools: ['search', 'edit', 'codebase', 'readFile', 'listDirectory']
description: 'Sync and maintain GitHub Copilot customizations with best practices and current project guidelines'
---

# Sync GitHub Copilot Customizations

Systematically audit, update, and synchronize all GitHub Copilot customization files to ensure they follow best practices, reflect current project guidelines, and maintain a clear dependency hierarchy without redundancies or ambiguities.

## Context

Leverages **#skill:github-copilot-customizer** for:
- Six customization methods (workspace instructions, agents, prompts, instructions, skills, MCP)
- Best practices and templates
- Detailed guides in `references/` (agent properties, tools, settings, MCP setup)
- Working examples in `references/agent-examples.md` and `references/instruction-examples.md`

## Process Overview

This is a multi-phase audit and synchronization process:

1. **Discovery Phase**: Analyze current state
2. **Onboarding Phase**: Initialize missing customizations (if needed)
3. **Audit Phase**: Identify issues and gaps
4. **Clarification Phase**: Resolve ambiguities with user
5. **Synchronization Phase**: Update all files
6. **Validation Phase**: Verify dependency graph and coherence

---

## Phase 1: Discovery

**Check existing customizations**: copilot-instructions.md, agents/, prompts/, instructions/, skills/, settings.json

**Analyze project**:
- Tech stack (package.json, requirements.txt, go.mod, etc.)
- Structure, tooling, docs, coding standards

**Discover ADRs** (if `docs/adr/` exists):
- Read recent ADRs (last 10-15 or 6 months)
- Extract relevant decisions: coding standards, tech choices, architecture, testing, docs, tooling
- Create ADR summary mapping decisions to customization files
- Note: ADRs are authoritative source

**Determine path**: 
- No customizations → Phase 2 (Onboarding)
- Existing customizations → Phase 3 (Audit)

---

## Phase 2: Onboarding (If Needed)

Use **#skill:github-copilot-customizer** templates and examples.

1. Enable instruction files in settings
2. Create copilot-instructions.md (project overview, principles, references)
3. Create instruction files (general + language-specific)
4. Ask about workflows → create 1-3 starter agents
5. Optional: Create starter prompts

Then proceed to Phase 3.

---

## Phase 3: Audit

**Check each file for**:
- Content: Follows best practices, clear/actionable, proper formatting/frontmatter
- Alignment: Current tech stack, project structure, tooling, ADRs (if applicable)
- Redundancy: No duplicates, conflicts, or unclear scope
- Dependencies: Clear hierarchy, proper references, no circular refs

**Document findings**: Missing, outdated, redundant, ambiguous, misaligned, dependency issues, ADR conflicts

---

## Phase 4: Clarification

**Ask user about**:
- Technology choices (conflicts, scope)
- Standards/conventions (conflicts, currency)
- Debatable topics (tabs vs spaces, import order, testing strategy, etc.)
- Missing guidelines
- ADR interpretation (if applicable)
- Workflow priorities

**Document decisions** with context and impact.

---

## Phase 5: Synchronization

**Update order**: copilot-instructions.md → instruction files → skills → agents → prompts

**Principles**:
- ADRs are authoritative (extract guidelines, reference ADRs, remove superseded)
- Workspace instructions: High-level overview, principles, ADR decisions, references (<200 lines)
- Instruction files: Detailed rules, clear glob patterns, incorporate ADRs (e.g., "Use X pattern per ADR-0015")
- Agents: Workflow-focused, reference skills/prompts/instructions
- Prompts: Task templates, clear I/O, reference docs/skills
- Skills: Domain knowledge, self-contained, no project-specific details

**Avoid redundancy**: Single source of truth + cross-references
**Ensure consistency**: Terminology, formatting, references, examples

---

## Phase 6: Validation

**Create dependency graph** (visual hierarchy)

**Verify**:
- No circular deps, clear hierarchy, no ambiguities/redundancies
- Complete coverage, current alignment, proper cross-refs
- ADR compliance (if applicable): decisions reflected, no contradictions, accurate refs, no superseded guidance

**Test agents** (if updated): Sample tasks, skill/instruction loading, no conflicts

---

## Success Criteria

✅ Clear foundation, detailed guidance, efficient workflows  
✅ No conflicts, ambiguities, or outdated content  
✅ Maintainable dependency graph, documented decisions

## Output

**Summary**: Changes made, dependency graph, key decisions, ADR integration (if applicable), recommendations, next steps

## Notes

- Incremental approach (high-impact first)
- Ask questions early/often
- Commit in logical groups
- Update README if needed
- Schedule regular syncs (quarterly or on major changes)
