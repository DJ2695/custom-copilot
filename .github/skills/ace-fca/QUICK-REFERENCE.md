# ACE-FCA Quick Reference Card

**Advanced Context Engineering for Coding Agents - Essential Patterns at a Glance**

---

## The Three-Phase Workflow

```
┌─────────────┐      ┌──────────┐      ┌────────────────┐
│  RESEARCH   │  →   │   PLAN   │  →   │  IMPLEMENT     │
│  Understand │      │ Specify  │      │  Execute w/TDD │
└─────────────┘      └──────────┘      └────────────────┘
     │                    │                     │
     ↓                    ↓                     ↓
  Research Doc       Executable Plan       Working Code
 (Compressed)         (Detailed)            (Tested)
```

---

## Phase 1: Research (Context Isolation)

**Goal**: Understand without polluting context

**Process**:
1. Launch subagent(s) for investigation
2. Subagent returns summary only
3. Compile into research doc

**Output**: `docs/research/YYYY-MM-DD-topic-research.md`

**Key Sections**:
- Problem understanding (2-3 sentences)
- Relevant code locations (files + roles)
- Key dependencies (only what matters)
- Recommended approach

---

## Phase 2: Planning (Executable Specification)

**Goal**: Complete spec before coding

**Process**:
1. Break into 2-5 minute tasks
2. Specify files, changes, tests
3. Include complete code snippets
4. Add ADR tasks for decisions

**Output**: `docs/plans/YYYY-MM-DD-feature-plan.md`

**Each Task Must Have**:
- Exact file path
- Specific changes
- Complete code
- Test expectations
- Verification command

---

## Phase 3: Implementation (TDD + Compaction)

**Goal**: Execute with discipline

**Process** (per task):
1. Write test
2. Watch FAIL (RED) ← Don't skip!
3. Write code
4. Watch PASS (GREEN)
5. Refactor
6. Commit
7. Every 3-5 tasks: Update plan

**Progressive Compaction Example**:
```
✅ Tasks 1-3: Complete
⏳ Task 4: In progress
❌ Tasks 5-8: Todo
```

---

## Context Quality Rules

### Target: 40-60% Context Window Usage

**Too Little (<40%)**:
- Missing dependencies
- Reinventing solutions
- Breaking patterns

**Too Much (>60%)**:
- Can't identify relevant info
- Hallucinations increase
- Slower responses

**Fix**: Use subagents + compress more

---

## Subagent Patterns

### When to Use Subagents:
- ✅ Research multiple areas
- ✅ Read many files (need summaries only)
- ✅ Independent task implementation
- ✅ Fresh perspective needed

### How to Use:
```
Parent Agent (Clean context)
    ↓
Launch Subagent (Focused task)
    ↓
Subagent returns summary
    ↓
Parent receives compressed result
```

---

## TDD Non-Negotiables

```
1. Write test                    # Defines expected behavior
2. Run test → MUST FAIL (RED)   # Confirms test works
3. Write minimal code            # Just enough to pass
4. Run test → MUST PASS (GREEN) # Confirms solution
5. Refactor if needed            # Clean up
6. Commit                        # Save progress
```

**Why RED matters**: Confirms test actually tests something!

---

## YAGNI (You Aren't Gonna Need It)

**Before implementing any feature, ask**:
- Do we need this NOW?
- Can we add it later if needed?
- What's the simplest version?

**Remove features aggressively**:
- "Might need later" = Delete it
- "Nice to have" = Delete it
- "Just in case" = Delete it

---

## ADR Integration

**Create ADR when**:
- Technology/framework choice
- Database design decision
- Security model
- API design pattern
- Architectural pattern

**Workflow**:
1. During planning, identify decision
2. Add ADR task to plan (before implementation)
3. Create using template
4. Reference in implementation tasks

**File**: `docs/adr/NNNN-title-with-hyphens.md`

---

## Critical Anti-Patterns to Avoid

| ❌ Anti-Pattern | ✅ Solution |
|----------------|------------|
| Jump straight to code | Research → Plan → Implement |
| Vague plan tasks | Specify files, code, tests exactly |
| Load full codebase | Use subagents + summaries |
| Skip RED in TDD | Always watch test fail first |
| Long tasks (30+ min) | Break into 2-5 min tasks |
| No ADRs | Document significant decisions |

---

## Context Compaction Checklist

- [ ] Using subagents for research?
- [ ] Returning summaries, not full files?
- [ ] Context at 40-60%?
- [ ] Plans executable (not vague)?
- [ ] Updating plan after 3-5 tasks?
- [ ] Each task under 10 minutes?

---

## Success Metrics

**You'll know it's working when**:
- Features planned before implementation
- Context issues rare
- High code quality consistently
- Less rework
- Team can work in parallel

**From case study (300k LOC codebase)**:
- Week's work → completed in 1 day
- Code passed expert review
- Developer was amateur in that language
- Success = context engineering, not smarter model

---

## Quick Commands

### Create New Documents:
```bash
# Research doc
cp docs/research-template.md docs/research/$(date +%Y-%m-%d)-topic.md

# Plan doc  
cp docs/plan-template.md docs/plans/$(date +%Y-%m-%d)-feature.md

# ADR (find next number first)
cp docs/adr/adr-template.md docs/adr/NNNN-decision.md
```

### Check Context:
```bash
# Count words in research doc (keep < 1000)
wc -w docs/research/current.md

# Count lines in plan (keep < 500)
wc -l docs/plans/current.md
```

---

## The Golden Rules

1. **Quality over quantity**: 40-60% context beats 90%
2. **Compress at every stage**: Research → summary, Code → plan, Progress → status
3. **Isolate with subagents**: One concern = one subagent
4. **Test before code**: RED-GREEN-REFACTOR, always
5. **Document decisions**: ADRs for significant choices
6. **YAGNI ruthlessly**: Remove features, don't add them

---

## When Stuck

**Context feels overwhelming?**
→ Use more subagents, compress more aggressively

**Tasks taking too long?**
→ Break into smaller tasks (2-5 minutes each)

**Agent suggestions generic?**
→ Context too broad, narrow with research phase

**Tests passing but code wrong?**
→ Skipped RED phase, rewrite test first

**Decision unclear?**
→ Create ADR, document alternatives

---

## Remember

> "The more you use the context window, the worse the outcomes you'll get."

**The answer is always**: Better compression, not bigger context.

---

## Full Documentation

- **Main Skill**: `.github/skills/ace-fca/SKILL.md`
- **Context Deep Dive**: `references/context-management.md`
- **Patterns**: `references/patterns-antipatterns.md`
- **Subagents**: `references/subagent-workflows.md`
- **Setup**: `PROJECT-SETUP.md`

---

**Print this card** and keep it visible while working with AI agents! 📋
