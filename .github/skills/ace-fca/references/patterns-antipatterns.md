# Patterns & Anti-Patterns

Proven approaches and pitfalls to avoid when working with ACE-FCA methodology.

## ✅ Effective Patterns

### Pattern: Spec-First Development

**Principle**: Write specification before code, validate spec before implementing.

**Process**:
1. Research phase → Understand problem
2. Write detailed specification
3. **Get human validation** on spec
4. Implement to spec
5. Review against spec

**Why it works**: Most bugs are spec bugs, not code bugs. Catching spec issues early is 10x cheaper than catching them in code review.

**Example**:
```markdown
## Spec: Email Validation

**Requirement**: Validate user email addresses

**Acceptance criteria**:
- [x] Accepts valid RFC 5322 emails
- [x] Rejects emails without @ symbol
- [x] Rejects emails without domain
- [x] Returns clear error messages

**Edge cases**:
- [ ] Plus addressing (user+tag@domain.com)
- [ ] International domains
- [ ] IP address domains

[Human reviews and approves before implementation starts]
```

### Pattern: True Red-Green TDD

**Critical**: Must actually watch test fail before writing implementation.

**Process**:
1. Write test for desired behavior
2. **Run test, watch it FAIL (RED)** ← Don't skip!
3. Write minimal code to make test pass
4. **Run test, watch it PASS (GREEN)**
5. Refactor if needed (test stays green)
6. Commit

**Why watching RED matters**:
```python
# Test that looks good but doesn't actually test anything:
def test_email_validation():
    validator = EmailValidator()
    result = validator.validate("test@example.com")
    # Oops, forgot to assert!
    # This test always passes, even if validate() is broken
```

If you skip RED phase, you won't catch that this test is useless.

**Correct version**:
```python
def test_email_validation():
    validator = EmailValidator()
    result = validator.validate("test@example.com")
    assert result.is_valid == True
    # Run this BEFORE implementing validate()
    # Watch it fail with "AttributeError: 'NoneType' object has no attribute 'is_valid'"
    # NOW implement validate()
    # Watch it pass
```

### Pattern: Context Isolation Through Subagents

**When**: Need to investigate multiple areas without polluting parent context.

**Approach**:
```
Parent Agent (Clean context)
    ↓
    Spawns Subagent A: "Research database schema"
    (Subagent A context: database files only)
    ↓
    Returns: 1-page summary
    ↓
    Spawns Subagent B: "Research API patterns"
    (Subagent B context: API files only)
    ↓
    Returns: 1-page summary
    ↓
Parent compiles summaries into research doc
(Parent context: 2 pages, not 50 files)
```

**Why it works**: Each subagent has focused, clean context. Parent receives compressed knowledge without noise.

### Pattern: Progressive Compaction on Long Tasks

**Problem**: Implementing 20-task plan, context grows stale by task 15.

**Solution**: Update plan with progress every 3-5 tasks.

**Example**:
```markdown
# Initial Plan (20 tasks)
[Full task descriptions for all 20 tasks]

# After Task 5 (Compaction 1)
✅ Completed (Tasks 1-5):
- User model created
- Database migration done
- Basic validation added

⏳ Current Focus (Task 6):
[Full details for task 6 only]

❌ Remaining (Tasks 7-20):
[High-level list, full details removed]

# After Task 10 (Compaction 2)
✅ Completed (Tasks 1-10):
- Phase 1 complete: Models and validation
- Phase 2 complete: API endpoints

⏳ Current Focus (Task 11):
[Full details for task 11 only]

❌ Remaining (Tasks 12-20):
[High-level list]
```

**Key**: Each compaction maintains context quality. Agent doesn't need to remember all 10 completed tasks in detail, just that they're done.

### Pattern: Incremental Validation with Humans

**Anti-pattern**: Build entire feature, then show to human (surprise!)

**Better pattern**: Show work in chunks, get feedback early.

**Example timeline**:
```
Day 1 Morning: Research phase
    → Show research doc to human
    → Human validates understanding

Day 1 Afternoon: Planning phase  
    → Show plan to human
    → Human approves approach

Day 2: Implement tasks 1-5
    → Show progress + working demo
    → Human validates direction

Day 3: Implement tasks 6-10
    → Show completed feature
    → Human reviews
```

**Why**: Course corrections are cheap early, expensive late.

### Pattern: YAGNI Ruthlessly Applied

**Principle**: You Aren't Gonna Need It - remove features before adding them.

**During design review**:
```markdown
## Initial Design (Feature bloat)
1. User registration
2. Email validation
3. Password strength checking
4. Two-factor authentication
5. Social login (Google, GitHub, Twitter)
6. Password recovery
7. Account lockout after failed attempts
8. Login history tracking
9. Session management across devices
10. Remember me functionality

## After YAGNI Review
1. User registration
2. Email validation
3. Password strength checking
4. Password recovery

Removed:
- 2FA (can add if users request)
- Social login (no user demand yet)
- Account lockout (premature optimization)
- Login history (nice-to-have)
- Multi-device session (adds complexity)
- Remember me (security concern for MVP)

Result: 4 tasks instead of 10, ships faster, less to maintain
```

**Rule**: If in doubt, leave it out. You can always add later if actually needed.

### Pattern: Subagent-Driven Development with Two-Stage Review

**When**: Implementation plan with 5+ independent tasks.

**Process**:
1. Parent dispatches subagent for Task 1
2. Subagent implements Task 1 (TDD)
3. **Review Stage 1**: Spec compliance
   - Does implementation match specification?
   - Are all acceptance criteria met?
   - If no → subagent fixes
4. **Review Stage 2**: Code quality
   - Is code clean and maintainable?
   - Are there better approaches?
   - If no → subagent refactors
5. Mark Task 1 complete
6. Repeat for Task 2, etc.

**Why two stages**: Separation of concerns. Spec compliance is objective. Code quality is subjective. Don't mix them.

### Pattern: Git Worktree for Isolation

**When**: Long implementation that might need abandoning or parallel urgent work.

**Setup**:
```bash
# Main branch stays clean
git branch feature/email-validation

# Create worktree for implementation
git worktree add ../email-validation-work feature/email-validation
cd ../email-validation-work

# Implement here, main branch unaffected
# Can switch back to main for urgent fixes

# When done:
cd /main/project
git worktree remove ../email-validation-work
git merge feature/email-validation
```

**Benefits**:
- Main branch stays stable for urgent work
- Easy to abandon failed experiments
- Clear separation of WIP from stable code

## ❌ Anti-Patterns to Avoid

### Anti-Pattern: Jumping Straight to Code

**Mistake**: Skip research and planning, start coding immediately.

**Consequences**:
- Wrong assumptions baked into code
- Have to rewrite when assumptions proven wrong
- Miss existing patterns and utilities
- Break existing conventions

**Example scenario**:
```
Task: "Add email validation"

Bad approach:
    → Immediately write new EmailValidator class
    → Later discover validators/ module already exists
    → Later discover codebase uses Pydantic validation
    → Rewrite everything to match patterns

Good approach:
    → Research phase finds validators/ module
    → Research phase finds Pydantic usage pattern
    → Plan uses existing patterns
    → Implementation fits seamlessly
```

**Fix**: Always research first, even if it feels like wasted time. 15 minutes research saves hours of rework.

### Anti-Pattern: Vague Plans

**Mistake**: Plans with unclear specifications.

**Examples of vague tasks**:
- "Add validation" (What kind? Where? How?)
- "Refactor for clarity" (What criteria? What's clear?)
- "Improve performance" (How much? What metrics?)
- "Fix the bug" (Which bug? How to verify?)

**Consequences**: Agent guesses, guesses wrong, implementation doesn't match expectations.

**Fix - Specific tasks**:
```markdown
❌ Vague: "Add validation"

✅ Specific:
**Task 3: Add email validation to User model**

**File**: `src/models/user.py`

**Add method**:
```python
def validate_email(self) -> ValidationResult:
    """Validate email against RFC 5322."""
    if not self.email or '@' not in self.email:
        return ValidationResult(valid=False, error="Invalid email format")
    # ... full implementation
```

**Update**: Call from `User.__init__()` before saving

**Test**: Add `test_user_email_validation()` in `tests/test_user.py`
- Valid email: test@example.com → passes
- No @: testexample.com → raises ValidationError
- Empty: "" → raises ValidationError

**Verification**: `pytest tests/test_user.py::test_user_email_validation`
```

### Anti-Pattern: Loading Full Codebase

**Mistake**: "Here's the entire repository" approach.

**Why it fails**:
```
100 files × 500 lines × ~3 tokens/word = 150k+ tokens
                                       ↓
                          Agent context overloaded
                                       ↓
                     Generic, irrelevant suggestions
                                       ↓
                              Hallucinations
```

**Example**:
```
Human: "Fix the login bug"
[Uploads entire 100-file codebase]

Agent: "Have you tried adding error handling?" (generic, unhelpful)
```

**Fix - Targeted context**:
```
Human: "Fix the login bug"

Step 1: Research phase (subagent)
- Subagent investigates authentication flow
- Returns: Login handled in auth/login_controller.py:45
- Bug likely in token validation logic

Step 2: Load targeted context
- auth/login_controller.py (relevant function only)
- auth/token_service.py (validation method)
- Related test file

Step 3: Agent provides specific fix
Agent: "Token validation on line 67 doesn't handle expired tokens..."
```

### Anti-Pattern: Long Tasks Without Checkpoints

**Mistake**: Task takes 30+ minutes with no intermediate verification.

**Consequences**:
- Context drift (agent loses track)
- No early warning of wrong direction
- Hard to debug where things went wrong
- Demotivating (no sense of progress)

**Example**:
```markdown
❌ Long task:
Task 1: Implement complete authentication system (2 hours)
- Build user model
- Add JWT generation
- Create login endpoint
- Add middleware
- Write all tests
- Add password recovery
[Agent loses track around step 4, produces broken code]
```

**Fix - Break into checkpoints**:
```markdown
✅ Broken down:
Task 1: Create User model (5 min)
Task 2: Add JWT token service (5 min)
Task 3: Create login endpoint (5 min)
Task 4: Add auth middleware (5 min)
Task 5: Write authentication tests (10 min)
Task 6: Add password recovery (10 min)

[Each task verified independently, clear progress]
```

### Anti-Pattern: Skipping the "Red" in TDD

**Mistake**: Write test and implementation at the same time, or implement first then test.

**Why it's dangerous**:
```python
# Test written after implementation:
def test_email_validation():
    result = validator.validate("test@example.com")
    assert result == True  # Passes!

# But implementation was:
def validate(self, email):
    return True  # Always returns True (bug!)

# Test passes even though implementation is wrong
# Test isn't actually testing validation logic
```

**Fix**: Always watch test fail first:
```python
# 1. Write test first
def test_email_validation():
    result = validator.validate("invalid-email")
    assert result == False  # What we expect

# 2. Run test - should FAIL (validate() doesn't exist yet)
# ✗ AttributeError: 'EmailValidator' object has no attribute 'validate'

# 3. Write minimal implementation
def validate(self, email):
    return '@' in email

# 4. Run test - should PASS
# ✓ test_email_validation PASSED

# Now you know test actually tests something!
```

### Anti-Pattern: Accepting First Draft

**Mistake**: Design or implementation without exploring alternatives.

**Example**:
```markdown
Design Review:

Approach: Store user sessions in database

[Implement immediately without considering alternatives]

Later discover:
- Database becomes bottleneck
- Session cleanup is complex
- Redis would have been better choice
```

**Fix - Explore alternatives**:
```markdown
Design Review:

Options considered:
1. Database sessions
   - Pro: Simple, no new infrastructure
   - Con: Database overhead, cleanup complexity
   
2. Redis sessions
   - Pro: Fast, built-in expiry
   - Con: New dependency
   
3. JWT (stateless)
   - Pro: No storage needed
   - Con: Can't revoke easily

Decision: JWT for MVP (simplest), can add Redis later if needed

Rationale: YAGNI - start simple, scale when actually needed
```

### Anti-Pattern: Context Pollution in Parent Agent

**Mistake**: Parent agent doing detailed work instead of delegating to subagents.

**Example**:
```
Parent agent needs to understand authentication:

❌ Bad approach:
1. Parent reads auth/login.py (200 lines)
2. Parent reads auth/token_service.py (150 lines)
3. Parent reads auth/middleware.py (180 lines)
4. Parent reads tests (300 lines)
→ Parent context now at 830 lines just for auth
→ Still needs to understand other systems
→ Context explodes

✅ Good approach:
1. Parent spawns auth research subagent
2. Subagent reads all auth files
3. Subagent returns summary:
   "Auth uses JWT tokens. Login at auth/login.py:45.
    Token validation in middleware. 85% test coverage."
→ Parent context: 4 lines summary
→ Parent has same understanding, 200x less context
```

### Anti-Pattern: No Architectural Decision Records

**Mistake**: Make significant decisions without documentation.

**Consequences**:
- Future maintainers don't understand "why"
- Decisions get re-litigated months later
- Same debates happen repeatedly
- Knowledge lost when team members leave

**Example scenario**:
```
Month 1: Team debates SQL vs NoSQL, chooses PostgreSQL
[No ADR written]

Month 6: New team member suggests MongoDB
[Can't remember why PostgreSQL was chosen]
[Debate starts over, wastes time]

Month 12: Another new member asks about database choice
[Original decision makers have left]
[Context is lost forever]
```

**Fix - Write ADR**:
```markdown
# ADR-003: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
Need database for user data and transactions. Evaluated SQL vs NoSQL options.

## Decision
Use PostgreSQL as primary database.

## Alternatives Considered
- MySQL: Less robust JSON support
- MongoDB: No ACID guarantees for transactions
- DynamoDB: Vendor lock-in concerns

## Consequences
- Strong ACID guarantees for transactions
- Excellent JSON support (JSONB)
- Mature ecosystem and tooling
- Team has PostgreSQL expertise
- Trade-off: More setup than managed NoSQL

## Date
2026-01-31
```

Now future team members understand the decision and won't re-litigate it.

### Anti-Pattern: Batch Commits

**Mistake**: Implement multiple tasks, then one big commit.

**Example**:
```bash
[Implement tasks 1-5 over 3 hours]
git add .
git commit -m "Added user features"
```

**Consequences**:
- Hard to review (too much changed)
- Hard to revert (all or nothing)
- Hard to understand history
- Lost granularity of what changed when

**Fix - Commit per task**:
```bash
# Task 1
git add src/models/user.py tests/test_user.py
git commit -m "Add User model with email field"

# Task 2  
git add src/validators/email.py tests/test_email.py
git commit -m "Add email validation with RFC 5322 support"

# Task 3
git add src/models/user.py tests/test_user.py
git commit -m "Integrate email validation into User model"

# Now history is clear, can revert task 3 without losing 1 & 2
```

## Pattern Selection Guide

| Situation | Recommended Pattern |
|-----------|---------------------|
| New feature with unclear requirements | Spec-First Development |
| Large codebase (100k+ LOC) | Subagent isolation + Research phase |
| Multi-step implementation (5+ tasks) | Progressive compaction |
| Need to explore options | YAGNI review with alternatives |
| Independent tasks in plan | Subagent-Driven Development |
| Long-running implementation | Git Worktree + Progressive compaction |
| Context feels overwhelming | Aggressive compaction + subagents |
| Quality concerns | True Red-Green TDD + Two-stage review |
| Significant architectural choice | ADR documentation |
| Human validation needed | Incremental validation in chunks |

## Red Flags Checklist

Watch for these warning signs:

- [ ] Plan has tasks longer than 10 minutes
- [ ] Context usage above 60%
- [ ] Agent suggesting generic solutions
- [ ] Tests written after implementation
- [ ] No consideration of alternatives
- [ ] No human validation checkpoints
- [ ] Architectural decisions undocumented
- [ ] Full codebase loaded into context
- [ ] Parent agent doing detailed investigation
- [ ] Implementation without research phase

If you check any box, apply corresponding pattern to fix.

## Key Takeaways

**Effective patterns**:
1. Research before implementation
2. Spec before code  
3. True RED-GREEN TDD
4. Subagents for isolation
5. Progressive compaction
6. YAGNI ruthlessly
7. Incremental validation
8. ADR for decisions
9. Commit per task

**Anti-patterns to avoid**:
1. Jumping to code
2. Vague plans
3. Context overload
4. Long tasks
5. Skipping RED phase
6. No alternatives
7. Context pollution
8. No ADRs
9. Batch commits

**Remember**: Patterns are tools, not rules. Adapt to your specific context. The goal is quality code shipped efficiently, not pattern adherence for its own sake.
