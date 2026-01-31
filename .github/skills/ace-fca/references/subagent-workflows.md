# Subagent Workflows

Advanced patterns for coordinating subagents in complex development tasks.

## Core Concepts

### What is a Subagent?

A **subagent** is a fresh agent instance with:
- **Clean context** - Only receives what you explicitly pass
- **Single purpose** - Completes one task then terminates
- **Summary return** - Returns compressed results to parent

**Key principle**: Subagents prevent context pollution in the parent agent.

### When to Use Subagents

**Use subagents when**:
- Investigating multiple independent areas
- Need to read many files but only need summaries
- Implementing independent tasks from a plan
- Context in parent agent approaching 60%
- Want fresh perspective on implementation

**Don't use subagents when**:
- Simple, single-file tasks
- Parent agent has all needed context
- Overhead outweighs benefit (very simple tasks)

## Pattern 1: Research Subagent

**Purpose**: Investigate codebase without polluting parent context.

### Basic Research Subagent

**Parent agent prompt**:
```
Launch a subagent to research the authentication system.

Task: Understand how authentication works in this codebase.

Specific questions:
1. What authentication method is used? (JWT, sessions, OAuth?)
2. Where is authentication logic implemented?
3. What tests exist for authentication?
4. Are there any known issues or TODOs?

Return: A 1-2 page summary with:
- Authentication method and location
- Key files and their responsibilities  
- Test coverage summary
- Any concerns or recommendations
```

**Subagent receives**:
- Access to full codebase
- The specific research questions
- Instruction to return summary only

**Subagent process**:
1. Search for auth-related files (`grep`, `file_search`)
2. Read authentication implementation
3. Examine test files
4. Check for TODOs and comments
5. Compile findings into summary

**Subagent returns**:
```markdown
# Authentication Research Summary

## Method
JSON Web Tokens (JWT) with HTTP-only cookies

## Implementation
- **Token generation**: `src/auth/token_service.py:23-45`
  - Algorithm: HS256
  - Secret from environment variable
  - 24-hour expiry
  
- **Token validation**: `src/auth/middleware.py:12-34`
  - Validates signature and expiry
  - Attaches user object to request
  - Returns 401 on invalid token

- **Login endpoint**: `src/api/auth_routes.py:56-78`
  - POST /api/login
  - Returns token in HTTP-only cookie
  
## Test Coverage
- Token generation: 100% coverage (`tests/test_token_service.py`)
- Middleware validation: 87% coverage (`tests/test_middleware.py`)
- Missing: Edge case for expired tokens during request

## Recommendations
1. Add test for token expiry during request processing
2. Consider token refresh mechanism
3. Add rate limiting to login endpoint

## Files
- `src/auth/token_service.py` (145 lines)
- `src/auth/middleware.py` (89 lines)
- `src/api/auth_routes.py` (234 lines)
- `tests/test_token_service.py` (178 lines)
- `tests/test_middleware.py` (134 lines)
```

**Parent agent receives**: 1-page summary instead of 780 lines of code.

### Multi-Area Research with Parallel Subagents

**When**: Need to research multiple independent areas.

**Parent agent prompt**:
```
Launch three subagents in parallel:

Subagent A - Database Research:
- What database is used?
- Where are models defined?
- What migrations system exists?
- Return summary

Subagent B - API Research:
- What API framework is used?
- What's the routing structure?
- What's the error handling pattern?
- Return summary

Subagent C - Testing Research:
- What test framework is used?
- What's the current test coverage?
- What testing patterns are used?
- Return summary
```

**Each subagent**:
- Investigates their area independently
- Returns focused summary
- Dies after completing task

**Parent compiles**:
```markdown
# Codebase Research Summary

## Database (from Subagent A)
[Summary]

## API (from Subagent B)
[Summary]

## Testing (from Subagent C)
[Summary]

## Overall Architecture Pattern
[Parent's synthesis of all three summaries]
```

**Benefit**: Three parallel investigations, parent receives 3 pages total instead of reading 100+ files.

## Pattern 2: Implementation Subagent

**Purpose**: Implement single task from plan with clean context.

### Single Task Implementation

**Parent has plan**:
```markdown
# Email Validation Feature Plan

## Task 1: Create EmailValidator class
[Detailed specs]

## Task 2: Add validation to User model
[Detailed specs]

## Task 3: Add validation tests
[Detailed specs]
```

**Parent launches subagent for Task 1**:
```
Launch subagent to implement Task 1 from the plan.

Context:
- Task specification: [paste Task 1 specs]
- Relevant code: src/validators/ directory structure
- Pattern to follow: [existing validator example]

Instructions:
1. Follow TDD: write test first
2. Implement EmailValidator class
3. Ensure test passes
4. Return: confirmation of completion + test results

Do NOT show parent the full implementation - parent trusts you.
Just return success/failure and test output.
```

**Subagent**:
1. Writes test for EmailValidator
2. Watches test fail (RED)
3. Implements EmailValidator
4. Watches test pass (GREEN)
5. Runs full test suite
6. Returns result

**Subagent returns**:
```markdown
# Task 1 Complete

## Status
✅ Implemented successfully

## Test Results
```
test_email_validator.py::test_valid_email PASSED
test_email_validator.py::test_invalid_email PASSED
test_email_validator.py::test_empty_email PASSED
All tests passing (3/3)
```

## Files Created
- src/validators/email_validator.py (34 lines)
- tests/test_email_validator.py (67 lines)

## Ready for Task 2
```

**Parent agent**:
- Marks Task 1 complete
- Moves to Task 2
- Context remains clean

### Subagent-Driven Development

**When**: Plan with 5+ mostly independent tasks.

**Full workflow**:

```markdown
# Implementation Plan (10 tasks)

Phase 1: Parent Agent
- Read plan
- Understand overall structure
- Identify task dependencies

Phase 2: Task-by-Task Implementation

For each task:
  1. Parent: Launch subagent with task specs
  2. Subagent: Implement task (TDD)
  3. Subagent: Return results
  4. Parent: Review Stage 1 - Spec compliance
     ├─ Pass → Continue to Stage 2
     └─ Fail → Subagent fixes issues
  5. Parent: Review Stage 2 - Code quality
     ├─ Pass → Mark complete
     └─ Fail → Subagent refactors
  6. Parent: Update plan progress
  7. Next task

Phase 3: Integration
- Parent: Run full test suite
- Parent: Integration testing
- Parent: Final review
```

**Benefits**:
- Fresh context per task (high quality)
- Fast iteration (parallel potential)
- Clear progress tracking
- Separation of implementation and review

## Pattern 3: Specialist Subagents

**Purpose**: Leverage specialized knowledge for specific tasks.

### Code Review Subagent

**Parent implements feature, then**:
```
Launch a code review subagent.

Context:
- Changed files: [list]
- Feature purpose: [description]

Review for:
1. Code quality and maintainability
2. Test coverage adequacy
3. Performance concerns
4. Security issues
5. Best practice adherence

Return: Review summary with specific recommendations.
```

**Review subagent**:
- Fresh eyes on implementation
- No bias from implementation process
- Can cite best practices objectively

**Returns**:
```markdown
# Code Review: Email Validation Feature

## ✅ Strengths
- Good test coverage (95%)
- Clean separation of concerns
- Proper error handling

## ⚠️ Recommendations

1. **Performance** (medium priority)
   - Line 45: Regex compilation happens on every call
   - Fix: Compile regex once at class level
   
2. **Security** (low priority)
   - Consider email enumeration attack vector
   - Recommendation: Generic error messages

3. **Maintainability** (low priority)
   - Docstrings missing for public methods
   
## 📊 Metrics
- Test coverage: 95%
- Cyclomatic complexity: 3 (good)
- No security vulnerabilities detected

## Verdict
✅ Approved with minor recommendations
```

### Testing Specialist Subagent

**Parent asks**:
```
Launch a testing specialist subagent.

Task: Review test coverage for email validation feature.

Analyze:
1. Are all code paths tested?
2. Are edge cases covered?
3. Are error conditions tested?
4. Is there any redundant testing?

Return: Test coverage analysis with specific gaps to fill.
```

**Testing subagent returns**:
```markdown
# Test Coverage Analysis

## Coverage Summary
- Line coverage: 95%
- Branch coverage: 87%

## Missing Coverage

### EmailValidator.validate()
- ✅ Valid emails tested
- ✅ Invalid format tested
- ❌ Missing: null/None input test
- ❌ Missing: extremely long email test (>254 chars)
- ❌ Missing: special characters in local part

### Integration
- ✅ User model integration tested
- ❌ Missing: Database constraint violation handling

## Recommended Additional Tests
1. `test_validate_null_email()`
2. `test_validate_oversized_email()`
3. `test_validate_special_characters()`
4. `test_db_unique_constraint_on_duplicate_email()`

## Redundant Tests
- `test_empty_string_email()` and `test_null_email()` overlap
- Recommendation: Keep null test, remove empty string test
```

### Security Review Subagent

**For security-critical features**:
```
Launch a security review subagent.

Context: New authentication implementation

Review for:
1. Injection vulnerabilities
2. Authentication bypasses
3. Token security
4. Session management
5. Error message information leakage

Return: Security assessment with vulnerability severity ratings.
```

## Pattern 4: Iterative Refinement with Subagents

**Purpose**: Improve implementation through multiple rounds.

### Round 1: Implementation Subagent
```
Task: Implement feature X
Returns: Working implementation
```

### Round 2: Review Subagent
```
Task: Review implementation of feature X
Returns: List of improvements needed
```

### Round 3: Refactoring Subagent
```
Task: Apply improvements from review
Context: Original implementation + review feedback
Returns: Refined implementation
```

### Round 4: Final Validation Subagent
```
Task: Validate all improvements applied correctly
Returns: Final approval or additional concerns
```

**Why multiple rounds**: Each subagent has fresh, focused context for their specific role.

## Pattern 5: Hierarchical Subagents

**Purpose**: Break down very complex tasks into sub-tasks.

```
Parent Agent (Master Coordinator)
    │
    ├─ Subagent A: Implement Backend
    │   │
    │   ├─ Sub-subagent A1: Models
    │   ├─ Sub-subagent A2: API routes
    │   └─ Sub-subagent A3: Tests
    │
    └─ Subagent B: Implement Frontend  
        │
        ├─ Sub-subagent B1: Components
        ├─ Sub-subagent B2: State management
        └─ Sub-subagent B3: Integration
```

**Communication flow**:
- Parent → Subagent A: "Implement backend"
- Subagent A → Sub-subagent A1: "Create models"
- Sub-subagent A1 → Subagent A: Returns summary
- Subagent A → Parent: Returns complete backend summary

**Warning**: Don't go more than 2-3 levels deep. Diminishing returns and communication overhead.

## Advanced Coordination Patterns

### Pattern: Shared Artifact Coordination

**Problem**: Multiple subagents need to coordinate through shared state.

**Solution**: Use artifacts (files) as coordination mechanism.

**Example**:
```markdown
# Implementation Progress (shared artifact)

## Completed
- [x] Task 1 by Subagent A
- [x] Task 2 by Subagent B

## In Progress
- [ ] Task 3 by Subagent C (started 14:23)

## Blocked
- [ ] Task 4 (waiting for Task 3)

## Notes
- Subagent A: Changed User model schema, updated tests
- Subagent B: Added validation, may affect Task 4
```

Each subagent:
1. Reads progress file
2. Executes their task
3. Updates progress file
4. Returns to parent

### Pattern: Dependency Chain Subagents

**When**: Tasks have dependencies (Task B needs Task A complete).

**Approach**:
```
Parent determines order:
1. Launch Subagent A for Task 1 (no dependencies)
2. Wait for completion
3. Launch Subagent B for Task 2 (depends on Task 1)
4. Wait for completion
5. Launch Subagents C, D, E in parallel (all depend on Task 2)
6. Wait for all to complete
7. Continue...
```

**Dependency graph**:
```
Task 1
  ↓
Task 2
  ↓
  ├─ Task 3
  ├─ Task 4
  └─ Task 5
      ↓
    Task 6
```

**Execution order**:
- Sequential: 1 → 2
- Parallel: 3, 4, 5
- Sequential: 6

### Pattern: Validation Subagent After Each Task

**Quality assurance pattern**:
```
For each implementation task:
  1. Implementation Subagent: Write code
  2. Validation Subagent: Verify correctness
     - Run tests
     - Check spec compliance
     - Verify no regressions
  3. If validation fails:
     - Implementation Subagent: Fix issues
     - Validation Subagent: Re-verify
  4. Else:
     - Mark complete, move to next task
```

**Benefit**: Catch issues immediately, not at end when 10 tasks are done.

## Subagent Communication Patterns

### Push Pattern (Parent → Subagent)

**Parent sends**:
- Task specification
- Relevant context (minimal)
- Success criteria
- Return format

**Subagent does not**:
- Ask parent for more info (should be self-contained)
- Report progress (just completes and returns)

### Pull Pattern (Subagent → Parent)

**Less common**, but sometimes needed:

**Subagent encounters**:
- Ambiguity in specification
- Unexpected blocking issue
- Need for architectural decision

**Subagent returns early**:
```markdown
# Task 1 - Blocked

## Issue
Spec says "add validation to User model" but User model 
has both UserProfile and UserAccount classes.

## Question
Which class should receive validation?
- UserProfile (demographics)
- UserAccount (auth credentials)
- Both

## Waiting for clarification
```

**Parent clarifies, relaunches subagent**.

## Best Practices

### 1. Minimal Context Transfer

**❌ Bad**: Give subagent everything
```
Subagent context:
- Entire codebase (50,000 lines)
- Full conversation history
- All research documents
```

**✅ Good**: Give subagent only what's needed
```
Subagent context:
- Task specification (50 lines)
- Relevant code file (200 lines)
- Pattern example (30 lines)
```

### 2. Clear Success Criteria

**❌ Bad**:
```
Task: Make the code better
```

**✅ Good**:
```
Task: Refactor validate_email() method

Success criteria:
1. Extract regex to class constant
2. Add docstring with examples
3. All existing tests still pass
4. No new dependencies introduced
```

### 3. Structured Return Format

**❌ Bad**: Let subagent return whatever
```
[Returns 500 lines of implementation details]
```

**✅ Good**: Specify return format
```
Return format:
## Status
[✅ Complete / ❌ Failed / ⏸️ Blocked]

## Summary
[2-3 sentences]

## Tests
[Test results]

## Files Changed
[List with line counts]

## Notes
[Anything parent should know]
```

### 4. Trust But Verify

**Parent should**:
- Trust subagent completed task correctly
- Verify with automated tests (don't manually review every line)
- Only deep-dive if tests fail or issues arise

**Don't micromanage**: If you're reading every line subagent wrote, you're not getting benefit of subagent isolation.

### 5. Failure Handling

**When subagent fails**:
1. Analyze failure reason
2. Improve task specification
3. Relaunch subagent with better specs
4. If fails again, might need parent to handle

**Don't**: Blame subagent. Failure = specification problem or task too complex.

## Measuring Subagent Effectiveness

### Success Metrics

**Good signs**:
- Tasks complete correctly first try (>80%)
- Parent context stays under 60%
- Fast iteration (tasks complete in minutes)
- High code quality from subagents

**Warning signs**:
- Subagents need multiple attempts (>50%)
- Parent has to micromanage subagent work
- Subagents return questions instead of results
- Code quality below expectations

### When Subagents Aren't Working

**If subagents struggle**:
1. **Specs too vague** → Make specifications more detailed
2. **Context insufficient** → Give subagent more relevant code
3. **Tasks too complex** → Break into smaller subtasks
4. **Pattern unclear** → Provide better examples

**Remember**: Subagent effectiveness reflects parent's ability to specify work clearly.

## Anti-Patterns

### ❌ Micro-Management
```
Parent: Implement Task 1
Subagent: [working...]
Parent: How's it going?
Parent: Did you consider X?
Parent: Try approach Y instead
```
→ Defeats purpose of subagent. Let them work.

### ❌ Context Dumping
```
Parent: Here's 10,000 lines of code, implement feature X
```
→ Subagent overwhelmed, same problem as parent had.

### ❌ Scope Creep
```
Subagent implementing Task 1
Subagent notices Task 2 could be improved
Subagent implements Task 2 too
Subagent starts refactoring unrelated code
```
→ Subagent should stick to assigned task only.

### ❌ Infinite Delegation
```
Parent → Subagent A → Sub-subagent B → Sub-sub-subagent C → ...
```
→ Communication overhead overwhelms benefit.

## Subagent Decision Tree

```
Need to complete task?
    │
    ├─ Simple, single file, <5 min?
    │   └─ Do it yourself (parent)
    │
    ├─ Need to read many files?
    │   └─ Launch research subagent
    │
    ├─ Complex multi-step with dependencies?
    │   └─ Launch subagents sequentially
    │
    ├─ Multiple independent tasks?
    │   └─ Launch subagents in parallel
    │
    └─ Need fresh perspective for review?
        └─ Launch review subagent
```

## Key Takeaways

1. **Subagents prevent context pollution** - Primary benefit
2. **Minimal context transfer** - Give only what's needed
3. **Clear specifications** - Success criteria + return format
4. **Trust but verify** - Use tests, not manual review
5. **Parallel when possible** - Independent tasks simultaneously
6. **Sequential for dependencies** - Respect task ordering
7. **Specialized subagents** - Review, testing, security
8. **Don't micro-manage** - Let subagents work autonomously
9. **Failure = spec problem** - Improve specification, retry
10. **2-3 levels max** - Don't over-layer subagents

**Remember**: Subagents are about context isolation and fresh perspective, not just parallelization. Even sequential subagent work provides value through clean context per task.
