# ACE-FCA: Advanced Context Engineering for Coding Agents

A comprehensive skill for GitHub Copilot that implements proven patterns for managing large codebases and complex implementations through disciplined context management.

## What is ACE-FCA?

ACE-FCA (Advanced Context Engineering for Coding Agents) is a methodology that enables AI coding agents to work effectively with:
- Large codebases (100k+ LOC)
- Complex, multi-step implementations
- Context window limitations
- High code quality requirements

**Core insight**: Context quality is the ONLY lever affecting output quality. ACE-FCA provides structured patterns for managing context throughout development.

## The Three-Phase Workflow

```
Research → Plan → Implement
   ↓         ↓         ↓
Compress  Specify  Execute+Test
```

1. **Research Phase**: Investigate codebase using subagents, return compressed summaries
2. **Planning Phase**: Create executable specifications with exact code and tests
3. **Implementation Phase**: Execute with TDD discipline, update progress continuously

## Quick Start

**New users**: See [QUICK-START.md](QUICK-START.md) for 5-minute setup guide.

### For Skill Users

**Trigger the skill** by mentioning:
- "Use ACE-FCA methodology"
- "Set up ACE-FCA for this project"
- "Create implementation plan with research phase"
- "Document this as an ADR"

The agent will automatically load and follow the ACE-FCA workflow.

### With GitHub Copilot Integration

```bash
# Quick setup (1 minute)
@ace-fca-coordinator setup this project

# Start first feature
@ace-fca-coordinator implement <feature>

# Quick phase entry
#research-phase <topic>
#planning-phase <feature>
#implementation-phase
#create-adr <decision>
```

See [templates/copilot/README.md](templates/copilot/README.md) for full setup.

### Manual Project Setup

```bash
# 1. Create directory structure
mkdir -p docs/{research,plans,adr}

# 2. Copy templates
cp .github/skills/ace-fca/templates/*.md docs/

# 3. Create first ADR (adopting ACE-FCA)
cp docs/adr-template.md docs/adr/0001-adopt-ace-fca-methodology.md

# 4. See PROJECT-SETUP.md for complete guide
```

## Skill Structure

```
ace-fca/
├── SKILL.md                      # Main skill (370 lines)
├── README.md                     # This file
├── PROJECT-SETUP.md              # Complete onboarding guide
├── QUICK-REFERENCE.md            # One-page cheat sheet
│
├── references/                   # Deep-dive documentation
│   ├── context-management.md     # Context window optimization
│   ├── patterns-antipatterns.md  # Proven approaches & pitfalls
│   ├── subagent-workflows.md     # Advanced coordination patterns
│   └── copilot-customization.md  # GitHub Copilot integration guide
│
├── templates/                    # Reusable artifacts
│   ├── research-template.md      # Research phase output
│   ├── plan-template.md          # Implementation plan
│   ├── adr-template.md           # Architectural Decision Record
│   ├── adr-directory-readme.md   # ADR setup guide
│   └── copilot/                  # GitHub Copilot integration
│       ├── README.md             # Setup guide
│       ├── researcher.agent.md   # Investigation specialist (~86 lines)
│       ├── planner.agent.md      # Architecture specialist (~86 lines)
│       ├── implementer.agent.md  # Build specialist (~107 lines)
│       ├── ace-fca-workflow.instructions.md  # Core rules
│       └── prompts/              # Phase-specific prompts
│           ├── research-phase.prompt.md
│           ├── planning-phase.prompt.md
│           ├── implementation-phase.prompt.md
│           └── create-adr.prompt.md
│
└── examples/                     # Usage examples & guides
    ├── QUICK-START.md            # 5-minute setup guide
    ├── COMPLETE-STRUCTURE.md     # Full structure summary
    └── VALIDATION-REPORT.md      # Quality assurance
```

## Key Features

### 1. Frequent Intentional Compaction (FIC)
- Select only relevant information
- Compress into compact artifacts
- Isolate from distracting noise
- Target 40-60% context window usage

### 2. Subagent-Driven Development
- Fresh context per task
- Parallel investigation
- Summary returns (not full files)
- Two-stage review (spec + quality)

### 3. Test-Driven Development (TDD)
- Write test first
- Watch it FAIL (RED) - critical!
- Write minimal code
- Watch it PASS (GREEN)
- Refactor if needed

### 4. ADR Integration
- Document significant decisions
- Integrated into planning phase
- Create before implementation
- Reference in related tasks

### 5. Progressive Compaction
- Update plan every 3-5 tasks
- Maintain context quality
- Track progress clearly
- Prevent context drift

## When to Use This Skill

**Use ACE-FCA when**:
- ✅ Working with large codebases (100k+ LOC)
- ✅ Complex, multi-step feature implementation
- ✅ Context window causing issues (hallucinations, irrelevant suggestions)
- ✅ Need to document architectural decisions
- ✅ Want disciplined, verifiable TDD workflow
- ✅ Setting up development workflow for new project

**Skip ACE-FCA when**:
- ❌ Simple, single-file changes
- ❌ Greenfield micro-projects
- ❌ Quick bug fixes with obvious solutions

## Real-World Results

From ACE-FCA case study (300k LOC Rust codebase):
- ✅ Week's worth of work completed in 1 day
- ✅ Code quality passed expert review
- ✅ Developer was amateur in Rust, never touched codebase before
- ✅ Success attributed to context engineering, not model intelligence

## Documentation Map

### Getting Started
1. **Read**: [SKILL.md](SKILL.md) - Core methodology (15 min read)
2. **Setup**: [PROJECT-SETUP.md](PROJECT-SETUP.md) - Onboard your project (5 min)
3. **Reference**: [QUICK-REFERENCE.md](QUICK-REFERENCE.md) - One-page cheat sheet

### Deep Dives
- [Context Management](references/context-management.md) - Optimize context window usage
- [Patterns & Anti-Patterns](references/patterns-antipatterns.md) - What works, what doesn't
- [Subagent Workflows](references/subagent-workflows.md) - Advanced coordination

### Templates
- [Research Template](templates/research-template.md) - Structure research findings
- [Plan Template](templates/plan-template.md) - Create executable specifications
- [ADR Template](templates/adr-template.md) - Document architectural decisions
- [ADR Setup](templates/adr-directory-readme.md) - Configure ADR directory

## Core Principles

### 1. Context Quality Over Quantity
More context ≠ better results. Target 40-60% usage with highly relevant, compressed information.

### 2. Subagents for Isolation
One subagent = one concern. Parent receives summaries, not full data. Prevents context pollution.

### 3. Spec Before Code
Research → Plan → Implement. Most bugs are spec bugs. Catch them before writing code.

### 4. True RED-GREEN TDD
Must watch test fail before implementing. Confirms test actually tests something.

### 5. YAGNI Ruthlessly
Remove features before adding them. "Might need later" = delete it. Simpler is better.

### 6. Document Decisions
Significant architectural choices become ADRs. Future maintainers understand "why."

## Example Workflow

### Scenario: Add Email Validation

**Phase 1: Research** (10 minutes)
```markdown
Agent: Launch research subagent to understand validation patterns

Subagent investigates, returns:
- Existing validators in `src/validators/`
- Pattern: Using Pydantic for validation
- Test coverage requirement: 100%
- Recommendation: Create new EmailValidator class

Output: docs/research/2026-01-31-email-validation-research.md
```

**Phase 2: Planning** (15 minutes)
```markdown
Agent: Create implementation plan based on research

Plan includes:
- Task 1: Create EmailValidator class (5 min)
- Task 2: Document validation approach (ADR) (3 min)
- Task 3: Add validation to User model (5 min)
- Task 4: Write comprehensive tests (7 min)

Each task has:
- Exact file paths
- Complete code snippets
- Test expectations
- Verification commands

Output: docs/plans/2026-01-31-email-validation-plan.md
```

**Phase 3: Implementation** (20 minutes)
```markdown
Agent: Execute plan task-by-task with TDD

For each task:
1. Write test → Watch FAIL (RED)
2. Write code → Watch PASS (GREEN)
3. Refactor if needed
4. Commit with clear message
5. Update plan progress

After Task 2: Progress update in plan
✅ Task 1: EmailValidator class - COMPLETE
✅ Task 2: ADR created - COMPLETE
⏳ Task 3: Integration - IN PROGRESS
❌ Task 4: Tests - TODO

Output: Working code + passing tests + documented decision
```

## Validation Checklist

Ensure your skill implementation follows ACE-FCA:

- [ ] SKILL.md under 500 lines? (✅ 369 lines)
- [ ] Name matches directory name? (✅ ace-fca)
- [ ] Description includes triggers and keywords? (✅ Yes)
- [ ] References split from main skill? (✅ 3 reference files)
- [ ] Templates provided? (✅ 4 templates)
- [ ] Setup guide included? (✅ PROJECT-SETUP.md)
- [ ] Quick reference available? (✅ QUICK-REFERENCE.md)

## Integration with Other Skills

ACE-FCA works well with:
- **TDD skills**: Natural fit, ACE-FCA enforces TDD discipline
- **Debugging skills**: Research phase helps understand bugs
- **Architecture skills**: ADR integration documents decisions
- **Code review skills**: Two-stage review in subagent workflow

## Customization

### For Your Project

ACE-FCA is designed to be adapted:

**Lightweight (small projects)**:
- Skip research phase for simple features
- Lighter ADR requirements
- Combine small tasks

**Comprehensive (large projects)**:
- Mandatory research phase
- Detailed planning required
- Comprehensive ADRs for all decisions

See [PROJECT-SETUP.md](PROJECT-SETUP.md) for customization guidance.

### For Your Team

**Solo developers**:
- ADRs capture decisions for future you
- Research docs prevent forgetting context
- Plans ensure task completion

**Large teams**:
- ADRs prevent re-litigating decisions
- Research docs share knowledge
- Plans enable parallel work

## Troubleshooting

### Skill Not Triggering?

**Check**:
- Is agent loading `.github/skills/` directory?
- Does user mention keywords from description?
- Try explicit: "Use the ace-fca skill"

### Context Still Overwhelming?

**Solutions**:
- Use subagents more aggressively
- Compress research summaries further
- Review [Context Management](references/context-management.md)

### Tasks Taking Too Long?

**Fixes**:
- Break into smaller tasks (target 2-5 minutes)
- Remove unnecessary complexity (YAGNI)
- Check if task needs research phase first

## Contributing

To improve this skill:

1. **Test it**: Use on real projects
2. **Document learnings**: What worked? What didn't?
3. **Propose improvements**: Update templates, add patterns
4. **Share results**: Document case studies

## License

[Specify your license or note if this follows project license]

## References

### Research Sources
- ACE-FCA methodology (original research 2026-01-31)
- Superpowers framework patterns
- Coding agent community best practices

### Related Concepts
- Frequent Intentional Compaction (FIC)
- Subagent-driven development
- Test-driven development (TDD)
- You Aren't Gonna Need It (YAGNI)
- Architectural Decision Records (ADR)

## Support

For questions or issues:
1. Review [SKILL.md](SKILL.md) for methodology
2. Check [QUICK-REFERENCE.md](QUICK-REFERENCE.md) for patterns
3. Read relevant [references/](references/) for deep dives
4. Ask your AI agent to reference this skill

## Version History

- **v1.0** (2026-01-31): Initial release
  - Three-phase workflow (Research → Plan → Implement)
  - Context management framework (40-60% rule)
  - Subagent coordination patterns
  - ADR integration
  - TDD discipline
  - YAGNI principles
  - Complete templates and setup guide

---

**Remember**: Context quality is the only lever. Better compression, not bigger context windows. 🎯
