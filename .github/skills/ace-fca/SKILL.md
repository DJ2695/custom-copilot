---
name: ace-fca
description: 'Advanced Context Engineering for Coding Agents (ACE-FCA) - Structured workflow for large codebases using Research → Plan → Implement phases with Frequent Intentional Compaction (FIC). Use when: setting up ACE-FCA for new projects, onboarding to complex codebases (100k+ LOC), implementing multi-step features with context management, documenting architectural decisions (ADRs), or needing disciplined TDD workflow with subagent isolation. Keywords: context engineering, large codebase, subagent workflow, ADR, implementation plan, research phase, TDD, YAGNI, progressive compaction.'
---

# Advanced Context Engineering for Coding Agents (ACE-FCA)

A proven methodology for managing complex codebases and multi-step implementations through disciplined context management, subagent isolation, and progressive compaction.

## Core Principle: Frequent Intentional Compaction (FIC)

**The Problem**: Context quality is the ONLY lever affecting output quality. Each agent interaction is stateless: context in → decision out. Poor context leads to hallucinations, incorrect assumptions, and task failure.

**The Solution**: Deliberately structure how context flows through development:
1. **Selection** - Choose only relevant code/info
2. **Compression** - Condense into compact artifacts
3. **Isolation** - Shield from distracting noise

**Key Insight**: Use 40-60% of context window optimally, not 90-100%. More context ≠ better results.

## When to Use This Skill

**Use when:**
- Setting up ACE-FCA workflow for a new or existing project
- Working with large codebases (100k+ LOC)
- Implementing complex, multi-step features
- Context window struggles (hallucinations, irrelevant suggestions)
- Need to document architectural decisions during implementation
- Want disciplined TDD with verification at each step
- Breaking down large tasks into manageable pieces

**Skip when:**
- Simple, single-file changes
- Greenfield projects with minimal context
- Quick bug fixes that don't require research

## The Three-Phase Workflow

### Phase 1: Research (Context Isolation)

**Purpose**: Understand codebase/problem without polluting context.

**Process**:
1. Launch subagent(s) for file searches and code analysis
2. Subagent investigates, returns **summary only** (not full files)
3. Subagent dies after task (clean context)
4. Compile findings into compacted research document

**Output**: `docs/research/YYYY-MM-DD-topic-research.md`

**Template structure**:
```markdown
## Problem Understanding
[2-3 sentences on core issue]

## Relevant Code Locations
- `path/to/file.ts`: [specific responsibility]
- `path/to/other.py`: [specific responsibility]

## Key Dependencies
[Only what matters for this task]

## Constraints & Considerations
[Technical/business constraints]

## Recommended Approach
[High-level direction based on findings]
```

**Why it works**: Parent agent receives compressed insights, not overwhelming raw data.

### Phase 2: Planning (Executable Specification)

**Purpose**: Create complete specification before touching code.

**Process**:
1. Consume research document (not entire codebase)
2. Break work into 2-5 minute tasks
3. Specify exact files, exact changes, exact test expectations
4. Include complete code snippets (not "add validation")
5. **Document key architectural decisions as ADRs**

**Output**: `docs/plans/YYYY-MM-DD-feature-plan.md`

**Task specification format**:
```markdown
### Task 3: Add validation to UserService

**File**: `src/services/user_service.py`

**Changes**:
- Add `validate_email()` method
- Call from `create_user()` before DB insert

**Code**:
```python
def validate_email(self, email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

**Test expectation**: `test_create_user_invalid_email()` should raise `ValidationError`

**Verification**: `pytest tests/test_user_service.py -k email`
```

**ADR Integration**: For significant architectural choices made during planning, create ADR before implementation:
```markdown
### Task 2: Document database choice (ADR)

**Create**: `docs/adr/0003-use-postgresql-for-user-data.md`

**Reason**: Multi-tenancy requires JSONB support and row-level security

**Alternatives considered**: MySQL, MongoDB

**Decision**: PostgreSQL for ACID + JSONB

**Template**: Use `templates/adr-template.md`
```

**Why it works**: Plan becomes compacted context for implementation. Tasks are unambiguous. ADRs capture "why" for future maintainers.

### Phase 3: Implementation (TDD + Progressive Compaction)

**Purpose**: Execute plan step-by-step with verification.

**Process**:
1. Select one task from plan
2. Write test first (if not present)
3. Watch test **fail** (RED) - don't skip!
4. Write minimal code to pass (GREEN)
5. Refactor if needed
6. Run full test suite
7. Commit with clear message
8. **After every 3-5 tasks**: Update plan with progress to prevent context drift

**Progressive compaction example**:
```markdown
✅ Task 1: Add User model - COMPLETE
✅ Task 2: Document DB choice (ADR) - COMPLETE
✅ Task 3: Add validation - COMPLETE
⏳ Task 4: Email uniqueness check - IN PROGRESS
   - Test written and failing
   - Working on implementation
❌ Task 5: Add API endpoint - TODO
❌ Task 6: Integration test - TODO
```

**Why it works**: Plan stays current without re-reading completed work. Context remains in 40-60% optimal range.

## Architectural Decision Records (ADRs)

**Integration with ACE-FCA**: Document significant decisions during Planning phase or Implementation phase when they emerge.

**When to create ADR**:
- Technology/framework choices
- Database schema decisions
- API design patterns
- Security model choices
- Performance trade-offs
- Architectural patterns

**ADR Workflow**:
1. During planning, identify decision points
2. Add ADR task to plan before implementation task
3. Create ADR using template (see `templates/adr-template.md`)
4. Reference ADR in related implementation tasks
5. Commit ADR before implementing decision

**File naming**: `docs/adr/NNNN-title-with-hyphens.md` (e.g., `0001-use-react-for-frontend.md`)

**Benefits**:
- Future maintainers understand "why"
- Prevents re-litigating decisions
- Documents alternatives considered
- Creates knowledge base

## Subagent-Driven Development

**When to use**: Implementation plan with mostly independent tasks.

**Process**:
1. Dispatch **fresh subagent** for each task
2. Subagent implements following TDD
3. **Two-stage review**:
   - Stage 1: Spec compliance check
   - Stage 2: Code quality review
4. If review fails, subagent fixes
5. Mark complete, move to next

**Why it works**: Fresh context per task prevents pollution. Separation of implementation and review maintains objectivity.

## Context Quality Framework

**Target**: 40-60% of context window usage

**Too Little (<40%)**:
- Missing critical dependencies
- Reinventing existing solutions
- Breaking existing patterns
→ **Fix**: Include more relevant files in research

**Too Much (>60%)**:
- Model struggles to identify relevant info
- Increased hallucinations
- Slower responses
→ **Fix**: Use subagents for isolation, create more compressed artifacts

**Measurement**: Monitor which files/docs agent references. If citing everything, context too broad. If missing obvious connections, too narrow.

## Critical Principles

### YAGNI (You Aren't Gonna Need It)
- Remove features from designs
- Implement only what's needed now
- Resist "might need later"
- Simpler designs complete faster

### TDD Non-Negotiable
- Tests first, always
- **Watch test fail (RED)** - confirms test works
- Minimal code to pass (GREEN)
- Refactor for quality
- Tests are safety net for refactoring

### Incremental Validation
- Present work in chunks
- Get feedback early and often
- Don't surprise with huge deliverables
- Course-correct early

### Spec-First Development
- Write spec before code
- Get human validation on spec
- Implement to spec
- Review against spec
→ Most bugs are spec bugs, not code bugs

## Project Setup for ACE-FCA

When onboarding a new project:

1. **Create directory structure**:
```bash
mkdir -p docs/{research,plans,adr}
```

2. **Initialize ADR log**:
```bash
# Create docs/adr/README.md with:
# - ADR naming convention
# - List of all ADRs with links
# - Status of each ADR (accepted, superseded, deprecated)
```

3. **Document current state** (if existing codebase):
   - Launch research subagent
   - Map key files and responsibilities
   - Identify testing patterns
   - Note architectural constraints
   - Create `docs/research/YYYY-MM-DD-codebase-overview.md`

4. **Set up TDD environment**:
   - Verify test runner works
   - Confirm test watching (if applicable)
   - Document test commands in README

5. **First ADR**: Document decision to use ACE-FCA
   - `docs/adr/0001-adopt-ace-fca-methodology.md`
   - Explains why, alternatives considered, consequences

## Common Patterns

### Pattern: Breaking Down Large Feature
```
1. Research phase → Understand existing architecture
2. Create high-level plan → Break into 5-10 major chunks
3. For each chunk:
   a. Detailed task breakdown (2-5 min tasks)
   b. Identify ADR needs
   c. Implement with TDD
   d. Update progress in plan
4. Final integration testing
```

### Pattern: Debugging with ACE-FCA
```
1. Research phase → Reproduce bug, understand context
2. Planning phase → Identify root cause, design fix
3. Implementation:
   a. Write test that fails with bug
   b. Fix bug (test goes green)
   c. Add regression test if needed
   d. Document in commit message or ADR if architectural
```

### Pattern: Refactoring Safely
```
1. Research → Map dependencies and usage
2. Plan → Define transformation steps with test strategy
3. Implement:
   a. Ensure 100% test coverage of code to refactor
   b. Make smallest possible change
   c. Run tests (should stay green)
   d. Commit
   e. Repeat for next small change
```

## Anti-Patterns to Avoid

❌ **Jumping straight to code** - No research or planning phase  
→ Results in rework, bugs, frustration

❌ **Vague plans** - "Add validation" without specifics  
→ Agent guesses, guesses wrong

❌ **Loading full codebase** - "Here's the entire repo"  
→ Agent overwhelmed, generic suggestions

❌ **Long tasks without checkpoints** - 30+ minute tasks  
→ Context drift, agent loses thread

❌ **Skipping RED in TDD** - Writing test and code together  
→ Test might not be testing anything

❌ **No ADRs** - Decisions made without documentation  
→ Future confusion, re-litigation of settled decisions

## References

For detailed information, see:
- [Context Management Deep Dive](references/context-management.md) - Context window optimization techniques
- [Patterns & Anti-Patterns](references/patterns-antipatterns.md) - Proven approaches and what to avoid
- [Subagent Workflows](references/subagent-workflows.md) - Advanced subagent patterns and coordination
- [GitHub Copilot Customization](references/copilot-customization.md) - Integration with agents, prompts, and instructions

## Templates

Available in `templates/` directory:

**Core Workflow**:
- `research-template.md` - Research phase output structure
- `plan-template.md` - Implementation plan structure
- `adr-template.md` - Architectural Decision Record format

**GitHub Copilot Integration** (`templates/copilot/`):
- `ace-fca-coordinator.agent.md` - Main coordinator agent
- `prompts/research-phase.prompt.md` - Quick research start
- `prompts/planning-phase.prompt.md` - Quick planning start
- `prompts/implementation-phase.prompt.md` - Quick implementation start
- `prompts/create-adr.prompt.md` - Quick ADR creation
- `ace-fca-workflow.instructions.md` - Core workflow rules for copilot-instructions.md

## Success Metrics

From ACE-FCA case study (300k LOC Rust codebase):
- Week's worth of work completed in a day
- Code quality passed expert review
- Developer was amateur in that language
- Success: context engineering, not model intelligence

**Key enablers**:
- Research phase isolated complexity
- Plan provided clear roadmap
- TDD discipline caught regressions
- Progressive compaction maintained context quality
- ADRs documented decisions for future

## Quick Reference Card

| Phase | Input | Output | Key Tool |
|-------|-------|--------|----------|
| **Research** | Problem statement | Compacted research doc | Subagents |
| **Planning** | Research doc | Executable plan + ADRs | Task breakdown |
| **Implementation** | Plan | Working code + tests | TDD + commits |

**Context flow**: Problem (large) → Research Doc (compact) → Plan (executable) → Code (tested)

**Golden rule**: If context feels overwhelming, **compact more aggressively**. The answer is always better compression, not bigger context windows.
