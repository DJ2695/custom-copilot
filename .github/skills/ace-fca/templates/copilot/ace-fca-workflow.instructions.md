# ACE-FCA Workflow Section

<!-- Copy content below into .github/copilot-instructions.md -->

---

## ACE-FCA Workflow

**Use for**: Multi-step features, large codebases (100k+ LOC), architectural decisions
**Skip for**: Simple bugs, single-file edits, documentation-only

### Phase Sequencing

```
RESEARCH → PLAN → [ADR] → IMPLEMENT → REVIEW
```

1. **Research**: Understand patterns, constraints, dependencies
2. **Plan**: Break into 2-5 min tasks with exact specs
3. **[ADR]**: Document architectural decisions
4. **Implement**: Execute with TDD
5. **Review**: Quality, coverage, practices

### Context Management (40-60% Rule)

- **Below 40%**: Missing context
- **Above 60%**: Must compact NOW
- **Progressive compaction**: Every 3-5 tasks
- **Subagent isolation**: Fresh context, 1-2 page summaries only

### TDD Discipline

```
1. Write test FIRST → Must FAIL (RED)
2. Minimal code → Must PASS (GREEN)  
3. Refactor → Tests stay green
4. Full suite → No regressions
```

**No exceptions**: Test first, always.

### YAGNI Principle

Before adding ANY feature:
1. In requirements? (No → Delete)
2. Needed now? (No → Delete)
3. Simpler solution? (Yes → Use it)

### ADR Triggers

Create ADR when:
- Technology/library choice
- Architecture pattern
- API design changes
- Data model changes
- Security approach
- Performance strategy
- Third-party integration

**Format**: `docs/adr/NNNN-title.md` (numbered, Proposed → Accepted)

### Task Specifications

Each task must have:
1. **File**: Exact path
2. **Changes**: Specific modifications
3. **Code**: Complete snippet (not pseudocode)
4. **Test**: What to verify
5. **Verification**: Exact command

### Quality Gates

- [ ] All tests passing (100%)
- [ ] Context < 60%
- [ ] TDD followed (test first)
- [ ] YAGNI applied (no extras)
- [ ] ADRs created
- [ ] Plan updated
- [ ] Clear commits

### Agents & Prompts

- `@Researcher` → `#research` - Investigate codebase
- `@Planner` → `#planning` - Create executable plan
- `@Implementer` → `#implementation` - Execute with TDD
- `#create-adr` - Document decisions

### Anti-Patterns

❌ Skip research → ✅ Investigate first
❌ Vague tasks → ✅ Exact specifications
❌ Code before test → ✅ Test FIRST
❌ Scope creep → ✅ YAGNI ruthlessly
❌ Missing ADRs → ✅ Document decisions
❌ Context overload → ✅ Compact at 60%
