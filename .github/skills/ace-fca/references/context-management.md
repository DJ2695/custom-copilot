# Context Management Deep Dive

## The Context Window as Scarce Resource

**Fundamental truth**: Your context window is the most valuable resource in agent interactions. Every token competes for the agent's attention.

### The 40-60% Rule

**Optimal utilization**: 40-60% of available context window

**Below 40% (Under-contextualized)**:
- Missing critical dependencies and patterns
- Agent reinvents existing solutions
- Breaks established conventions
- Asks for information repeatedly

**Above 60% (Over-contextualized)**:
- Agent struggles to identify relevant information
- Increased hallucinations and fabrications
- Slower processing and response times
- More errors in output
- "Lost in the noise" syndrome

**The 90%+ trap**: Worst possible state. Agent sees everything but understands nothing. Results in generic, irrelevant suggestions.

## Progressive Context Building

Build context in layers, not all at once:

### Layer 1: Problem Statement (Always include)
```markdown
## Objective
Add email validation to user registration

## Context
User model exists in `src/models/user.py`
Current validation is minimal (only checks non-empty)
Need RFC 5322 compliance
```

### Layer 2: Relevant Code Only (Research phase output)
```markdown
## Key Files
- `src/models/user.py` - User model definition
- `src/validators/` - Existing validation utilities
- `tests/test_user_model.py` - Existing user tests

## Patterns in Use
- Using `pydantic` for model validation
- Validators in separate `validators/` module
- 100% test coverage requirement
```

### Layer 3: Specific Implementation Details (Planning phase)
```markdown
## Implementation Approach
1. Create `validators/email_validator.py`
2. Add method to User model
3. Update tests

[Specific code snippets and test cases]
```

**Notice**: Each layer adds specificity without dumping entire files. Agent receives exactly what's needed at each stage.

## Compaction Techniques

### Technique 1: Summarize, Don't Include

**❌ Bad** (5000 tokens):
```markdown
Here's the full UserService class:
[paste entire 200-line file]
```

**✅ Good** (200 tokens):
```markdown
UserService responsibilities:
- CRUD operations for users (create/read/update/delete)
- Email validation: Currently uses simple regex
- Password hashing: bcrypt with salt
- Session management: JWT tokens
Located: `src/services/user_service.py:45-250`
```

### Technique 2: Reference, Don't Duplicate

**❌ Bad**:
```markdown
Research phase found:
[full file contents]

Planning phase needs:
[same full file contents again]
```

**✅ Good**:
```markdown
Research phase found:
[summary in research doc]

Planning phase:
See research doc for details. Focus: lines 45-67 of user_service.py
```

### Technique 3: Progressive Detail

**Stage 1 - High level**:
```markdown
Authentication system uses JWT tokens
```

**Stage 2 - When needed**:
```markdown
JWT tokens:
- Generated in `auth/token_service.py`
- Validated in middleware
- 24-hour expiry
```

**Stage 3 - Only if implementation requires**:
```markdown
TokenService.generate():
- Algorithm: HS256
- Secret from ENV['JWT_SECRET']
- Payload: {user_id, email, exp}
- Returns: token string
```

## Subagent Isolation Patterns

### Pattern 1: Research Subagent

**Parent agent task**:
```
Launch subagent to research authentication patterns in codebase.
Report back: What auth method is used, where it's implemented, what tests exist.
```

**Subagent investigates** (in its own context):
- Searches for auth-related files
- Reads authentication code
- Examines test coverage
- Analyzes patterns

**Subagent returns** (to parent's context):
```markdown
## Authentication Research Summary

**Method**: JWT tokens (JSON Web Tokens)
**Implementation**: `src/auth/token_service.py` (145 lines)
**Key functions**: 
- `generate_token(user_id)` - Creates JWT
- `verify_token(token)` - Validates and decodes
**Tests**: 87% coverage in `tests/test_token_service.py`
**Dependencies**: PyJWT library
**Pattern**: Tokens stored in HTTP-only cookies
```

**Key**: Parent never saw the 145 lines. Only received compressed summary.

### Pattern 2: Multi-Subagent Parallel Research

**When**: Multiple independent areas to research

**Parent launches**:
- Subagent A: Research database schema
- Subagent B: Research API patterns  
- Subagent C: Research testing setup

**Each returns summary → Parent compiles into single research doc**

**Benefit**: Parallelization + each subagent has clean context

### Pattern 3: Implementation Subagent

**Parent**: "Implement task 3 from plan"

**Implementation subagent receives**:
- Task 3 specification (from plan)
- Relevant code context (minimal)
- Test requirements

**Implementation subagent does NOT receive**:
- Full codebase
- All previous tasks
- Entire plan

**Benefit**: Fresh perspective, focused context, faster execution

## Context Collapse Prevention

**Context collapse**: When agent loses track of important information due to context overload.

### Warning Signs
- Agent asks for information you already provided
- Agent suggests solutions that contradict earlier decisions
- Agent forgets constraints or requirements
- Agent's responses become generic and unfocused

### Prevention Strategies

#### 1. Create Persistent Artifacts
Don't rely on conversation history. Create documents:
- `docs/research/current-research.md`
- `docs/plans/current-plan.md`
- `docs/context/key-decisions.md`

#### 2. Reference Artifacts, Don't Repeat
**❌ Bad**:
```
[Repeat all requirements in every message]
```

**✅ Good**:
```
See current-plan.md for full requirements. 
Focus on task 4: email validation.
```

#### 3. Progressive Compaction During Long Tasks
After every 3-5 tasks in implementation:

```markdown
## Progress Update
✅ Tasks 1-3: User model complete
⏳ Task 4: Working on validation
❌ Tasks 5-8: Not started

## Key Context for Remaining Work
- User model in `src/models/user.py`
- Validation pattern: use `validators/` module
- Tests must cover edge cases
```

This becomes new context, replaces all previous messages.

## Measuring Context Quality

### Method 1: Token Counting
Most models display token usage. Monitor:
- Total tokens in context
- Percentage of max context window
- Aim for 40-60%

### Method 2: Agent Behavior
Quality indicators:
- ✅ Agent cites specific files/functions
- ✅ Agent asks clarifying questions
- ✅ Agent suggests relevant solutions
- ✅ Agent remembers constraints

Poor quality indicators:
- ❌ Agent makes broad generalizations
- ❌ Agent suggests off-topic solutions
- ❌ Agent asks for info already provided
- ❌ Agent contradicts earlier decisions

### Method 3: Output Relevance
For each agent response, evaluate:
- How much is directly relevant to task? (Target: >80%)
- How much is boilerplate/generic? (Target: <20%)
- How much contradicts existing code? (Target: 0%)

## Context Handoff Between Phases

### Research → Planning Handoff

**Research phase outputs**:
```markdown
docs/research/2026-01-31-email-validation-research.md
```

**Planning phase receives**:
- Link to research doc
- 2-3 sentence summary
- NOT full research details

**Planning phase reads research doc when needed**, doesn't load it all upfront.

### Planning → Implementation Handoff

**Planning phase outputs**:
```markdown
docs/plans/2026-01-31-email-validation-plan.md
```

**Implementation receives**:
- Link to plan
- Current task only (e.g., "Task 3: Add validator")
- Relevant code context for that task
- NOT entire plan in context

**Implementation references plan** for next tasks, doesn't load all tasks upfront.

## Advanced: Context Budgeting

For very complex work, allocate context budget:

| Category | Token Budget | Purpose |
|----------|-------------|---------|
| System prompts | 5,000 | Agent instructions, skills |
| Problem statement | 2,000 | Current objective |
| Relevant code | 10,000 | Files being modified |
| Tests | 3,000 | Test expectations |
| Plan/research | 5,000 | Current phase artifact |
| Conversation | 5,000 | Recent exchanges |
| **Total** | **30,000** | ~40% of 200k window |

**Budget enforcement**:
- If code exceeds 10k tokens → summarize more
- If conversation exceeds 5k tokens → create progress artifact, start fresh
- If approaching 60% total → aggressive compaction needed

## The Compaction Flywheel

```
Large context
    ↓
Subagent researches
    ↓
Returns summary (compressed)
    ↓
Parent uses summary to plan
    ↓
Plan is compressed specification
    ↓
Implementation uses plan (not original context)
    ↓
Result: 10x context reduction with maintained quality
```

**Example**:
- Original: 100 files, 50k LOC, would be 500k tokens
- After research: 5-page research doc, 3k tokens
- After planning: 10-page plan, 6k tokens  
- Implementation: Single task + relevant code, 5k tokens

**Compression ratio**: 500k → 5k = 100:1 compression while preserving all necessary information.

## Key Takeaways

1. **Quality over quantity**: 40-60% utilization beats 90%+
2. **Compress at every stage**: Research → summary, Codebase → plan, Progress → status
3. **Isolate with subagents**: Clean context per concern
4. **Artifacts over conversation**: Persistent documents beat message history
5. **Measure and adjust**: Monitor context usage, adjust compression
6. **Prevent collapse**: Progressive compaction on long tasks
7. **Budget context**: Allocate tokens like scarce resource they are

**Remember**: The goal is not to maximize context usage. The goal is to optimize context relevance.
