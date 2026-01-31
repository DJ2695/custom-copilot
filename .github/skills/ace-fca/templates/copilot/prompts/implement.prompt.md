---
agent: 'agent'
model: Claude Opus 4.5
tools: ['search', 'usages', 'edit', 'createFile']
description: Execute ACE-FCA implementation plan - strict TDD (test first!), progressive compaction every 3-5 tasks
---

# ACE-FCA Implementation

I'll execute the implementation plan task-by-task with strict TDD discipline.

## Process

1. Load implementation plan from `docs/plans/*.md`
2. Pre-flight checklist (tests passing, clean git state)
3. Execute each task following TDD cycle
4. Progressive compaction every 3-5 tasks

## TDD Cycle (Per Task)

1. **Write test FIRST** (before any implementation code)
2. **Run test** → Must see FAIL ❌ (RED)
3. **Write minimal implementation** to make test pass
4. **Run test** → Must see PASS ✅ (GREEN)
5. **Refactor** if needed (tests stay green)
6. **Run full test suite** to verify no regressions
7. **Commit** with clear message
8. **Update plan** with progress

## Progressive Compaction

Every 3-5 tasks:
- Summarize completed work
- Update plan with progress
- Keep only current context
- Prevents context overload (stay under 60%)

## Quality Gates

- Block if ADR needed but missing
- Flag tests that pass before implementation (bad test)
- Ensure all tests in scope pass 100%
- Apply YAGNI ruthlessly (no extra features)

## Next Steps

After implementation, use handoff buttons or invoke:
- `@agent` with "Review Code" - Code quality review
- `#create-adr` - Document decision made during implementation
