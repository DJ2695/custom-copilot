---
name: subagent-driven-development
description: 'Execute implementation plans by dispatching fresh subagents for each independent task, with two-stage review after each (spec compliance first, then code quality). Use when: (1) you have an implementation plan with independent tasks, (2) tasks can be done in sequence within current session, (3) user asks to "use subagent-driven development" or "execute plan with subagents". Triggers on: "subagent driven", "dispatch subagents", "subagent for each task", "fresh subagent per task".'
---

# Subagent-Driven Development

Execute implementation plans by dispatching a fresh subagent for each task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use This Skill

Use this skill when ALL of these conditions are met:

1. **You have an implementation plan** - A detailed plan with numbered tasks
2. **Tasks are mostly independent** - Can be done sequentially without tight coupling
3. **Staying in this session** - Not spawning parallel sessions

**Decision tree:**
- No plan yet? → Create plan first or brainstorm
- Tasks tightly coupled? → Manual execution or refactor plan
- Want parallel execution? → Use alternative workflow for parallel sessions

## Prerequisites

- **Plan file** - Contains numbered tasks with clear specifications
- **Git worktree** - Isolated workspace for this work (REQUIRED before starting)
- **Test-driven development skill** - Subagents will follow TDD
- **Code review skill** - For reviewer subagents

## The Process

### Step 1: Initialize

1. Read plan file once to understand full scope
2. Extract all tasks with their complete text and context
3. Create todo list with all tasks marked as not-started

### Step 2: Per Task Loop

For each task in sequence:

#### A. Dispatch Implementer Subagent

Use `./implementer-prompt.md` template:
- Provide FULL task text (don't make subagent read the file)
- Include scene-setting context (where this fits, dependencies, architecture)
- Subagent may ask questions before starting - answer them completely
- Subagent implements, tests, commits, and self-reviews

#### B. Dispatch Spec Compliance Reviewer

Use `./spec-reviewer-prompt.md` template:
- Reviewer verifies implementation matches spec exactly
- Checks for missing requirements
- Checks for extra/unneeded work
- **If issues found:** Implementer fixes, then spec reviewer reviews again
- Repeat until spec compliance passes ✅

#### C. Dispatch Code Quality Reviewer

**Only after spec compliance passes.**

Use `./code-quality-reviewer-prompt.md` template:
- Get git SHAs (base and current commit)
- Reviewer checks code quality (clean, tested, maintainable)
- **If issues found:** Implementer fixes, then code quality reviewer reviews again
- Repeat until quality review passes ✅

#### D. Mark Task Complete

Once both reviews pass, mark task as completed in todo list.

### Step 3: Final Review

After all tasks completed:
1. Dispatch final code reviewer for entire implementation
2. Use finishing workflow to complete the development branch

## Prompt Templates

- [`./implementer-prompt.md`](./implementer-prompt.md) - Dispatch implementer subagent
- [`./spec-reviewer-prompt.md`](./spec-reviewer-prompt.md) - Dispatch spec compliance reviewer
- [`./code-quality-reviewer-prompt.md`](./code-quality-reviewer-prompt.md) - Dispatch code quality reviewer

## Example Workflow

```
You: I'm using Subagent-Driven Development to execute this plan.

[Read plan file once: docs/plans/feature-plan.md]
[Extract all 5 tasks with full text and context]
[Create todo list with all tasks]

Task 1: Add authentication middleware

[Get Task 1 text and context (already extracted)]
[Dispatch implementation subagent with full task text + context]

Implementer: "Before I begin - should I use JWT or session-based auth?"

You: "JWT with 1-hour expiration"

Implementer: "Got it. Implementing now..."
[Later]
Implementer:
  - Implemented auth middleware
  - Added tests, 8/8 passing
  - Self-review: Found edge case handling missing, added it
  - Committed

[Dispatch spec compliance reviewer]
Spec reviewer: ✅ Spec compliant - all requirements met

[Get git SHAs, dispatch code quality reviewer]
Code reviewer: Strengths: Good coverage. Issues: Magic number for expiration. Approved after fix.

[Implementer fixes]
Implementer: Extracted AUTH_TOKEN_EXPIRY constant

[Code reviewer reviews again]
Code reviewer: ✅ Approved

[Mark Task 1 complete]

Task 2: Add rate limiting
...
[Continue for remaining tasks]

[After all tasks]
[Dispatch final code reviewer]
Final reviewer: All requirements met, tests pass, ready to merge

Done!
```

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion from previous work)
- Parallel-safe (subagents don't interfere with each other)
- Subagent can ask questions before AND during work

**vs. Parallel session execution:**
- Same session (no context handoff overhead)
- Continuous progress (no waiting for parallel sessions)
- Review checkpoints automatic and immediate

**Efficiency gains:**
- No file reading overhead (controller provides full text upfront)
- Controller curates exactly what context is needed
- Subagent gets complete information from the start
- Questions surfaced before work begins (not discovered after)

**Quality gates:**
- Self-review catches issues before handoff to reviewers
- Two-stage review: spec compliance prevents under/over-building, then code quality ensures good implementation
- Review loops ensure fixes actually work
- Spec compliance first prevents wasted effort on poorly built features
- Code quality ensures maintainability

**Cost considerations:**
- More subagent invocations (implementer + 2 reviewers per task)
- Controller does more prep work (extracting all tasks upfront)
- Review loops add iterations
- BUT catches issues early (cheaper than debugging later)

## Red Flags

### Never Do These

- ❌ Start implementation on main/master branch without explicit user consent
- ❌ Skip reviews (spec compliance OR code quality)
- ❌ Proceed with unfixed review issues
- ❌ Dispatch multiple implementation subagents in parallel (causes conflicts)
- ❌ Make subagent read plan file (provide full text instead)
- ❌ Skip scene-setting context (subagent needs to understand where task fits)
- ❌ Ignore subagent questions (answer before letting them proceed)
- ❌ Accept "close enough" on spec compliance (spec reviewer found issues = not done)
- ❌ Skip review loops (reviewer found issues = implementer fixes = review again)
- ❌ Let implementer self-review replace actual review (both are needed)
- ❌ **Start code quality review before spec compliance passes** (wrong order)
- ❌ Move to next task while either review has open issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation
- Better to clarify upfront than fix later

### If Reviewer Finds Issues

- Implementer (same subagent) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails Task

- Dispatch fix subagent with specific instructions
- Don't try to fix manually (causes context pollution)

## Integration

**Required workflow skills:**
- **test-driven-development** - Subagents follow TDD for each task
- **systematic-debugging** - If issues arise during implementation

**Recommended workflow skills:**
- Create implementation plan first (with clear, independent tasks)
- Use git worktrees for isolated workspace
- Have code review workflow available for reviewers

**When to use alternatives:**
- Need parallel execution? → Use parallel session workflow instead
- Tasks tightly coupled? → Consider manual execution or refactor plan
- No plan yet? → Create plan first

## Troubleshooting

**Subagent asks too many questions:**
- Provide more context upfront in task description
- Include architectural context and constraints
- Reference similar existing code

**Spec reviewer keeps finding issues:**
- Requirements may be unclear or incomplete
- Refine spec before re-dispatching implementer
- Ensure implementer has full understanding

**Code quality reviewer keeps finding issues:**
- Implementer may need better examples of good code
- Point to existing patterns to follow
- Clarify quality standards upfront

**Tasks taking too long:**
- Tasks may be too large - consider breaking down
- Subagent may be overbuilding - emphasize YAGNI
- Review cycle may be too strict - balance thoroughness with progress
