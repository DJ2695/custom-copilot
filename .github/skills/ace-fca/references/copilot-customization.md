# GitHub Copilot Customization for ACE-FCA

Complete guide for integrating ACE-FCA methodology with GitHub Copilot through specialized agents, prompts, and instructions.

## Architecture Overview

### Design Decision: Three Specialized Agents

**Structure**:
- **Three Agents**: Each with distinct personality and expertise
  - `researcher.agent.md` - Investigation specialist (blue)
  - `planner.agent.md` - Architecture specialist (green)
  - `implementer.agent.md` - Build specialist (orange)
- **Four Phase Prompts**: Stateless, task-focused entry points
- **One Instructions File**: Core workflow rules

**Why Three Agents?**

✅ **Specialized Expertise**: Each agent has distinct behavior and personality:
- **Researcher**: Curious investigator, returns compressed summaries
- **Planner**: Meticulous architect, **automatically detects ADRs**
- **Implementer**: TDD purist, strict RED-GREEN-REFACTOR

✅ **Personality Customization**: Agents can embody different personas
- Researcher asks questions, explores alternatives
- Planner is structured, detail-oriented
- Implementer is honest about test quality, blocks on ADRs

✅ **Automatic ADR Detection**: Planner scans for architectural decisions and inserts ADR tasks
- Users often forget to create ADRs
- Automatic detection ensures decisions are documented
- ADR tasks inserted BEFORE dependent implementation

✅ **Clear Handoffs**: Each agent proposes next agent in sequence

✅ **Flexibility**: Can use agents for guided workflow OR prompts for quick entry

## Components

### 1. Specialized Agents

#### Researcher Agent (`researcher.agent.md`)

**Role**: Investigation specialist for research phase

**Personality**:
- 🔍 Curious: Digs deep to find truth
- 📊 Analytical: Identifies patterns
- 🎯 Focused: Answers specific questions
- 📝 Concise: Compresses findings
- ❓ Never assumes: Always investigates

**Capabilities**:
- Spawns research subagents for parallel investigation
- Returns compressed summaries (1-2 pages max, NOT full files)
- Semantic search and targeted grep
- Progressive disclosure investigation
- Clarifies research questions before starting

**Color**: Blue (investigation)

**Triggers**: `@ace-fca-researcher`

**Handoff**: Proposes `@ace-fca-planner` after research complete

**Example**:
```
@ace-fca-researcher investigate authentication patterns in user module

Agent clarifies:
- Goal: Understanding existing implementation? Evaluating new auth?
- Scope: User module only or related modules?
- Depth: High-level overview or detailed code patterns?

[After clarification]

Agent investigates, returns compressed summary:
- JWT tokens (jsonwebtoken@9.0.0)
- Auth middleware pattern
- Test approach with mocks
- ⚠️ No rate limiting

→ Propose: @ace-fca-planner create plan for [feature]
```

#### Planner Agent (`planner.agent.md`)

**Role**: Architecture specialist for planning phase

**Personality**:
- 📐 Architect: Designs clear specifications
- 🎯 Precise: Every task has exact files, code, tests
- ⏱️ Time-conscious: Tasks are 2-5 minutes
- 🔍 Detail-oriented: Nothing vague
- 🏛️ Decision-aware: **Automatically detects ADR needs**
- 📋 Methodical: Complete, ordered, testable plans

**Capabilities**:
- Creates executable specifications (2-5 min tasks)
- Includes exact code snippets (not pseudocode)
- Specifies complete test expectations
- **Automatically detects architectural decisions**
- **Inserts ADR tasks BEFORE dependent implementation**
- Orders tasks by dependencies
- Identifies when ADRs needed vs following existing patterns

**Color**: Green (architecture/design)

**Triggers**: `@ace-fca-planner`

**Handoff**: 
- If ADR needed: Proposes `#create-adr` (or notes implementer will remind)
- If no ADR: Proposes `@ace-fca-implementer`

**ADR Auto-Detection**:

Planner automatically scans every task for these triggers:
- Technology/library selection
- Architecture patterns
- API design decisions
- Data model changes
- Security approaches
- Performance strategies
- Integration patterns

When detected, planner:
1. **Inserts ADR task** with full context
2. **Documents alternatives** to consider
3. **Marks as mandatory** (implementation depends on it)
4. **Orders correctly** (ADR before implementation)

**Example**:
```
@ace-fca-planner create plan for social authentication

Agent loads research (if exists) and gathers requirements.

Agent creates plan with 12 tasks:
1. Setup test structure
2. Research OAuth providers (quick comparison)
3. 🏛️ **CREATE ADR**: OAuth provider selection ← AUTO-DETECTED
   - Alternatives: Auth0, Firebase, AWS Cognito, Supabase
   - Decision context provided
   - Must complete before Tasks 4-10
4. Implement OAuthService (depends on Task 3)
5-12. [Remaining implementation tasks]

→ Options:
1. Create ADR now: `#create-adr oauth-provider`
2. Continue: `@ace-fca-implementer execute plan`
   (Implementer will pause at Task 3)
```

#### Implementer Agent (`implementer.agent.md`)

**Role**: Build specialist for implementation phase

**Personality**:
- 🔨 Builder: Turns specs into working code
- 🧪 TDD Purist: Test first, ALWAYS
- 📊 Methodical: One task at a time
- ✅ Quality-focused: All tests pass
- 📦 Compactor: Maintains context quality
- ⚠️ Honest: Flags bad tests, blocks on missing ADRs

**Capabilities**:
- Strict RED-GREEN-REFACTOR cycle enforcement
- Detects "bad tests" that pass before implementation
- Progressive compaction every 3-5 tasks
- **Pauses at ADR tasks and blocks implementation**
- Commits after each task
- Runs full test suite after each change

**Color**: Orange (building/execution)

**Triggers**: `@ace-fca-implementer`

**Handoff**: Proposes `@ace-fca-implementer review` after complete

**ADR Enforcement**:

When implementer reaches an ADR task:
```
⚠️ ADR REQUIRED BEFORE CONTINUING

Task 3 (OAuth provider selection) is an ADR creation task.
Tasks 4-10 depend on this decision being documented.

I cannot proceed with implementation until the ADR is created.

→ Create ADR now:
Say: `#create-adr oauth-provider-selection`

I'll wait for ADR creation.
```

**TDD Enforcement**:

Implementer enforces RED phase:
```
Task 4: Implement OAuthService

Step 1: Write test FIRST
[Creates test]

Running test (must see RED):
$ npm test -- oauth.test.ts
❌ FAILED: Cannot find module '@/auth/oauth'

🔴 RED phase confirmed!

Step 2: Write implementation
[Creates implementation]

Running test again (must see GREEN):
$ npm test -- oauth.test.ts
✅ PASS: 2/2 tests

🟢 GREEN phase confirmed!

✅ Task 4 complete!
```

### 2. Phase-Specific Prompts

Prompts are **stateless and unpersonalized** - focused solely on tasks they solve.

**Research Phase** (`research-phase.prompt.md`):
- Gathers research questions
- Spawns subagent with context
- Creates research document
- Proposes planning handoff
- **Usage**: `#research-phase <topic>`

**Planning Phase** (`planning-phase.prompt.md`):
- Checks for research document
- Gathers requirements
- Creates executable plan
- Identifies ADR needs
- Proposes ADR or implementation handoff
- **Usage**: `#planning-phase <feature>`

**Implementation Phase** (`implementation-phase.prompt.md`):
- Loads plan, validates it exists
- Pre-flight checks (tests passing, clean git)
- Executes task-by-task with TDD
- Progressive compaction every 3-5 tasks
- Proposes review handoff
- **Usage**: `#implementation-phase`

**Create ADR** (`create-adr.prompt.md`):
- **Manually triggerable** for explicit ADR creation
- Finds next ADR number
- Guides through decision documentation
- Links related ADRs
- Proposes handoff back to implementation
- **Usage**: `#create-adr <decision_title>`
- **Note**: Planner auto-detects and includes ADR tasks in plans

### 3. Workflow Instructions

**File**: `ace-fca-workflow.instructions.md`

**Purpose**: Core rules to include in workspace `copilot-instructions.md`

**Content**:
- When to use ACE-FCA (multi-step features, large codebases)
- Phase sequencing (Research → Plan → [ADR] → Implement → Review)
- Context management (40-60% rule, progressive compaction)
- TDD discipline (test FIRST, RED-GREEN-REFACTOR)
- YAGNI principle (ruthless feature removal)
- **ADR creation triggers** (auto-detected by planner)
- Task specification format
- Quality checks before completion
- Anti-patterns to avoid

**Integration**: Copy into `.github/copilot/copilot-instructions.md`

## ADR Workflow

### Automatic Detection (Planner Agent)

The **Planner agent automatically detects** architectural decisions:

**Triggers**:
- Technology selection (database, framework, library)
- Architecture pattern (MVC, microservices, layered)
- API design (public interface, breaking changes)
- Data model (schema, major changes)
- Security approach (auth, encryption)
- Performance strategy (caching, optimization)
- Integration pattern (third-party services)

**When detected**:
1. Planner inserts ADR task BEFORE dependent implementation
2. Provides full decision context in task description
3. Lists alternatives to consider
4. Marks dependencies (which tasks need this ADR)

**Example ADR Task**:
```markdown
### Task 3: 🏛️ Create ADR for OAuth Provider Selection (Est: 5 min)

**Decision**: Select OAuth provider for user authentication

**Why This is Architectural**:
- Technology choice affecting long-term maintenance
- Impacts user experience, security, cost
- Difficult to change later (vendor lock-in)

**Context for ADR**:
- Alternatives: Auth0, Firebase Auth, AWS Cognito, Supabase Auth
- Factors: Cost, features, integration, team familiarity
- Impact: User flow, scaling, maintenance

**Create**: docs/adr/NNNN-oauth-provider-selection.md
**Template**: templates/adr-template.md
**Dependencies**: Tasks 4-10 depend on this decision
```

### Manual Triggering (Create ADR Prompt)

Users can manually create ADRs anytime:

```
#create-adr <decision_title>
```

**Use cases**:
- Quick ADR creation without full planning
- Mid-implementation decision emerges
- Documenting past decisions retroactively

### Implementation Phase ADR Blocking

Implementer agent **pauses and blocks** at ADR tasks:

```
@ace-fca-implementer execute plan

Tasks 1-2: [executed with TDD]

Task 3: 🏛️ Create ADR

⚠️ ADR REQUIRED BEFORE CONTINUING

Task 3 (OAuth provider selection) is an ADR creation task.
I cannot proceed with Tasks 4-10 until this decision is documented.

→ Create ADR: `#create-adr oauth-provider-selection`

[WAITS]
```

After ADR created:
```
User: continue

@ace-fca-implementer:
✅ ADR Created: docs/adr/0015-oauth-provider-selection.md
Decision: Supabase Auth

Resuming implementation with Task 4...
```

### Why Automatic ADR Detection?

**Problem**: Users forget to create ADRs

**Solution**: Planner automatically detects and mandates them

**Benefits**:
- ✅ No forgotten architectural decisions
- ✅ Decisions documented before implementation
- ✅ Clear decision context preserved
- ✅ Future developers understand WHY
- ✅ Prevents decision re-litigation

## Handoff Patterns

### Full Workflow Example

```
1. Research Phase
User: @ace-fca-researcher investigate authentication patterns
Agent: ✅ Research complete
       Findings: JWT, middleware, test patterns
       → Propose: @ace-fca-planner create plan

2. Planning Phase
User: @ace-fca-planner create plan for social auth
Agent: ✅ Plan created (12 tasks)
       🏛️ ADR Auto-Detected: Task 3 (OAuth provider)
       → Options:
          A) Create ADR now: #create-adr oauth-provider
          B) Continue: @ace-fca-implementer (will be reminded)

3. Implementation Phase (with ADR pause)
User: @ace-fca-implementer execute plan
Agent: Tasks 1-2 complete
       ⚠️ Task 3: ADR Required - PAUSING
       → Must create: #create-adr oauth-provider

4. ADR Creation
User: #create-adr oauth-provider-selection
Agent: [Guides through decision documentation]
       ✅ ADR created: docs/adr/0015-oauth-provider.md
       → Resume: say "continue"

5. Implementation Resume
User: continue
Agent: ✅ ADR confirmed (Supabase Auth selected)
       Resuming implementation...
       Task 4: [TDD cycle - RED, GREEN, commit]
       Task 5: [TDD cycle - RED, GREEN, commit]
       [After 3 tasks: Progressive compaction]
       Task 6-12: [continues with TDD]
       ✅ Implementation complete!
       → Propose: @ace-fca-implementer review

6. Review Phase
User: @ace-fca-implementer review
Agent: Spawning review subagent...
       ✅ Review complete (quality: excellent)
       → Ready to merge
```

### Agent-to-Agent Handoffs

**Researcher → Planner**:
```
✅ Research complete
→ @ace-fca-planner create plan for [feature]
```

**Planner → ADR Creation** (if architectural decision):
```
✅ Plan created
🏛️ ADR detected in Task 3
→ Options:
  1. #create-adr [decision] (create now)
  2. @ace-fca-implementer (will be reminded)
```

**Planner → Implementer** (no ADR):
```
✅ Plan created
No ADRs needed
→ @ace-fca-implementer execute plan
```

**Implementer Pause** (at ADR task):
```
⚠️ ADR Required (Task 3)
→ #create-adr [decision]
```

**ADR → Implementation Resume**:
```
✅ ADR created
→ say "continue" to resume implementation
```

**Implementer → Review**:
```
✅ Implementation complete
→ @ace-fca-implementer review
```

### Prompt Handoffs

Prompts can also propose handoffs, but are more stateless:

```
#research-phase auth
→ Propose: #planning-phase auth

#planning-phase auth
→ Propose: #create-adr oauth-provider (if ADR detected)
→ Or: #implementation-phase (if no ADR)

#create-adr oauth-provider
→ Propose: #implementation-phase (resume)

#implementation-phase
→ Propose: review implementation
```

## Setup Instructions

### 1. Copy Agent Templates

```bash
# Copy all three agents to workspace
cp .github/skills/ace-fca/templates/copilot/researcher.agent.md \
   .github/copilot/agents/

cp .github/skills/ace-fca/templates/copilot/planner.agent.md \
   .github/copilot/agents/

cp .github/skills/ace-fca/templates/copilot/implementer.agent.md \
   .github/copilot/agents/
```

Or if not using agents subdirectory:
```bash
cp .github/skills/ace-fca/templates/copilot/*.agent.md \
   .github/copilot/
```

### 2. Copy Prompts

```bash
# Copy all prompts
cp -r .github/skills/ace-fca/templates/copilot/prompts \
      .github/copilot/
```

### 3. Add Instructions to copilot-instructions.md

```bash
# Append core rules to instructions
cat .github/copilot/ace-fca-workflow.instructions.md >> \
    .github/copilot/copilot-instructions.md
```

Or use include syntax:
```markdown
# .github/copilot/copilot-instructions.md

<!-- Include ACE-FCA workflow rules -->
<!-- @include ace-fca-workflow.instructions.md -->
```

### 4. Initialize Project Directories

```bash
# Create required directories
mkdir -p docs/{research,plans,adr}

# Copy ADR directory README
cp .github/skills/ace-fca/templates/adr-directory-readme.md \
   docs/adr/README.md
```

### 5. Test the Workflow

```
# Start with researcher
@ace-fca-researcher investigate [topic]

# Or jump to planner if you have context
@ace-fca-planner create plan for [feature]

# Or use prompts for quick entry
#research-phase [topic]
#planning-phase [feature]
```

## Customization Guide

### Agent Personalities

**Researcher** (`researcher.agent.md`):
- Adjust questions asked before research
- Modify investigation depth
- Customize compression strategy
- Add project-specific search patterns

**Planner** (`planner.agent.md`):
- Customize ADR detection rules
- Adjust task size estimates (2-5 min default)
- Add project-specific quality checks
- Modify test expectation formats

**Implementer** (`implementer.agent.md`):
- Adjust TDD enforcement strictness
- Customize commit message format
- Modify compaction frequency (3-5 tasks default)
- Add project-specific verification steps

### Prompts (Keep Stateless)

Prompts should remain task-focused and unpersonalized:
- ✅ Clear inputs and outputs
- ✅ Focused on specific phase
- ✅ Minimal context assumptions
- ❌ Don't add personality (use agents for that)
- ❌ Don't make stateful (agents handle state)

### Instructions

Add project-specific rules:
- File naming conventions
- Test framework specifics
- Commit message format
- Code review checklist
- ADR triggers specific to your domain

## Usage Patterns

### When to Use Agents vs Prompts

**Use Specialized Agents**:
- ✅ Want guided workflow with personality
- ✅ Need automatic ADR detection
- ✅ Prefer conversational interaction
- ✅ Starting complex multi-step feature

**Use Prompts**:
- ✅ Know exact phase needed
- ✅ Want quick, stateless execution
- ✅ Resuming work mid-phase
- ✅ Simple, focused task

### Agent Selection

**@ace-fca-researcher**:
- Starting new feature (understand codebase first)
- Need to find patterns to follow
- Investigating feasibility
- Understanding constraints

**@ace-fca-planner**:
- Have requirements or research
- Need executable specification
- Want ADRs auto-detected
- Breaking down complex feature

**@ace-fca-implementer**:
- Have detailed plan
- Ready to build with TDD
- Want automatic ADR enforcement
- Need progressive compaction

### Quick Commands Summary

```bash
# Agents (with personalities)
@ace-fca-researcher investigate <topic>
@ace-fca-planner create plan for <feature>
@ace-fca-implementer execute plan
@ace-fca-implementer review

# Prompts (stateless, task-focused)
#research-phase <topic>
#planning-phase <feature>
#implementation-phase
#create-adr <decision>
```

## Best Practices

### ADR Automation

✅ **Trust the planner**: Let it detect architectural decisions
✅ **Don't skip ADRs**: If planner detected it, it's important
✅ **Document before implementation**: ADR tasks come first
✅ **Review ADR tasks**: Planner may suggest alternatives to consider

### Agent Workflow

✅ **Follow handoffs**: Each agent proposes next step
✅ **One phase at a time**: Don't skip research or planning
✅ **Let implementer block**: If ADR needed, create it
✅ **Progressive compaction**: Let implementer manage context

### TDD Discipline

✅ **RED phase is mandatory**: Must see test fail first
✅ **Bad test detection**: If test passes before implementation, rewrite it
✅ **Trust the implementer**: It will enforce TDD strictly
✅ **Commit per task**: Clear, focused commits

## Troubleshooting

### Agent Not Responding

- Check agent file location (`.github/copilot/agents/` or `.github/copilot/`)
- Verify frontmatter (name, description, color)
- Try `@` syntax: `@ace-fca-researcher`
- Reload VS Code window

### ADR Not Auto-Detected

- Check if decision is truly architectural (not implementation detail)
- Verify planner agent includes ADR detection logic
- Manually trigger if needed: `#create-adr <decision>`

### Implementer Doesn't Block on ADR

- Verify plan includes ADR task with 🏛️ marker
- Check implementer agent has ADR blocking logic
- Manually create ADR if missed

### Context Overload

- Let agents manage context (progressive compaction)
- If manual intervention needed: compact early
- Agents target 40-60% context usage

## See Also

- [Main Skill Document](../SKILL.md) - Core ACE-FCA methodology
- [Context Management](context-management.md) - Context strategies
- [Subagent Workflows](subagent-workflows.md) - Subagent patterns
- [Copilot Templates README](../templates/copilot/README.md) - Template usage

---

**Ready to integrate?**

1. Copy agents, prompts, instructions
2. Initialize project directories
3. Start with: `@ace-fca-researcher investigate <topic>`
