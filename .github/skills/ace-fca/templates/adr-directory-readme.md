# ADR Directory Template

This directory should be copied to your project as `docs/adr/` to start documenting architectural decisions.

## Quick Start

1. **Copy to your project**:
   ```bash
   mkdir -p docs/adr
   cp .github/skills/ace-fca/templates/adr-template.md docs/adr/
   cp .github/skills/ace-fca/templates/adr-directory-readme.md docs/adr/README.md
   ```

2. **Create your first ADR** (adopting ACE-FCA methodology):
   ```bash
   cp docs/adr/adr-template.md docs/adr/0001-adopt-ace-fca-methodology.md
   # Edit the file to document the decision
   ```

3. **Update this README** with your ADR list as you create them.

## What is an ADR?

An **Architectural Decision Record** (ADR) captures important architectural decisions along with their context and consequences. ADRs help:
- Future maintainers understand "why" decisions were made
- Prevent re-litigating settled decisions
- Create institutional knowledge
- Track architectural evolution

## When to Create an ADR

**Create ADRs for**:
- Technology/framework choices (databases, frontend frameworks, etc.)
- Architectural patterns (microservices, event-driven, etc.)
- Database schema design decisions
- Security models and authentication approaches
- API design patterns
- Major refactoring decisions
- Significant performance optimization strategies

**Don't create ADRs for**:
- Minor implementation details
- Obvious or trivial choices
- Temporary workarounds or hacks
- Individual bug fixes (unless they reveal architectural issues)

## ADR Workflow with ACE-FCA

ADRs integrate naturally into the ACE-FCA workflow:

### During Planning Phase
When creating an implementation plan:
1. Identify decisions that need documentation
2. Add "Create ADR" as a task in the plan
3. Create ADR before implementing the decision
4. Reference ADR in related implementation tasks

### Example from Plan
```markdown
### Task 2: Document database choice (ADR)
**Create**: `docs/adr/0003-use-postgresql-for-user-data.md`
**Reason**: Multi-tenancy requires JSONB support
**Template**: Use `templates/adr-template.md`

### Task 3: Implement database connection
**Reference**: See ADR-0003 for context
...
```

## ADR List

Replace this section with your actual ADRs:

### Active Decisions

| # | Title | Status | Date | Tags |
|---|-------|--------|------|------|
| [0001](0001-example-decision.md) | Example Decision Title | Accepted | 2026-01-31 | architecture |

### Superseded Decisions

| # | Title | Status | Date | Superseded By |
|---|-------|--------|------|---------------|
| [0000](0000-old-decision.md) | Old Decision | Superseded | 2025-12-01 | ADR-0001 |

### Deprecated Decisions

| # | Title | Status | Date | Reason |
|---|-------|--------|------|--------|
| - | - | - | - | - |

## ADR Statuses

- **Proposed**: Under consideration, not yet approved
- **Accepted**: Approved and being/will be implemented
- **Deprecated**: No longer recommended but still in use somewhere
- **Superseded**: Replaced by a newer decision (link to the new ADR)

## Numbering Convention

Use sequential 4-digit numbers with leading zeros:
- `0001-first-decision.md`
- `0002-second-decision.md`
- `0010-tenth-decision.md`
- etc.

To find the next number:
```bash
ls -1 docs/adr/*.md | grep -E '^[0-9]{4}' | tail -1
```

## File Naming Convention

Format: `NNNN-title-in-kebab-case.md`

**Good examples**:
- `0001-use-postgresql-for-user-data.md`
- `0002-adopt-microservices-architecture.md`
- `0003-implement-jwt-authentication.md`

**Bad examples**:
- `1-database.md` (no leading zeros)
- `0001-Database_Choice.md` (not kebab-case)
- `decision-about-databases.md` (no number)

## Template Location

The ADR template is available at:
- In this skill: `.github/skills/ace-fca/templates/adr-template.md`
- Copy it to start a new ADR, then fill in the sections

## Review Process

1. Create ADR in **Proposed** status
2. Share with team/stakeholders for review
3. Address feedback and concerns
4. Update status to **Accepted** when approved
5. Implement the decision
6. Reference the ADR in code comments or documentation

## Tips for Good ADRs

### Be Specific
❌ "Use a database"  
✅ "Use PostgreSQL 14+ for user and transaction data"

### Document Alternatives
Always include 2-3 alternatives considered and why they weren't chosen.

### Keep It Concise
Aim for 1-3 pages. If longer, consider splitting into multiple ADRs.

### Write for Future Readers
Assume the reader has no context about the decision or why it was made.

### Update When Superseded
If a decision is replaced, update the old ADR's status and link to the new one.

## Resources

- [ADR GitHub Organization](https://adr.github.io/) - Community resources
- [Michael Nygard's ADR article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Original ADR proposal
- ACE-FCA Skill: `.github/skills/ace-fca/SKILL.md` - Full methodology

## Integration with Version Control

- **Commit ADRs with related code**: Include ADR in the same commit/PR as the implementation when possible
- **Review ADRs in code review**: ADRs should be reviewed before merging
- **Keep ADRs in main branch**: Don't squash or delete ADRs; they're historical record
- **Update via new ADRs**: Don't edit accepted ADRs; create new ones that supersede them
