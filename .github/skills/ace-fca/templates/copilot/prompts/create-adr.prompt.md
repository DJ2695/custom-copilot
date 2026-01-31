---
agent: 'agent'
model: Claude Sonnet 4.5
tools: ['search', 'createFile', 'edit']
description: Create Architectural Decision Record (ADR) - find next number, document decision with context/options/consequences
---

# Create ADR

I'll create an Architectural Decision Record following ACE-FCA methodology.

## Process

1. Scan `docs/adr/` to find next ADR number
2. Gather decision information from user:
   - **Context**: What problem we're solving
   - **Decision**: What we decided
   - **Options**: Alternatives considered (with pros/cons)
   - **Rationale**: Why this option
   - **Consequences**: Positive/negative outcomes and risks
3. Create ADR using standard format
4. Update README ADR index

## ADR Template Structure

```markdown
# {{NNNN}}. {{Decision Title}}

**Date**: {{DATE}}
**Status**: Proposed
**Deciders**: {{names}}

## Context

{{problem_description}}

## Decision

{{decision_statement}}

## Options Considered

### Option 1: {{name}}
**Pros**: {{benefits}}
**Cons**: {{drawbacks}}

### Option 2: {{name}} ⭐ SELECTED
**Pros**: {{benefits}}
**Cons**: {{drawbacks}}

## Consequences

**Positive**: {{benefits}}
**Negative**: {{trade_offs}}
**Risks**: {{risks_and_mitigations}}

## References

- {{research_doc}}
- {{related_ADRs}}
```

---

## ADR Complete

✅ **ADR created!**

**File**: `docs/adr/{{NNNN}}-{{title}}.md`
**Status**: Proposed (update to "Accepted" when approved)

---

## Next Steps

After ADR creation:
- `@Implementer` - Continue/resume implementation
- `@agent` with "Review ADR" - Get team feedback
- `#create-adr` - Document another decision
3. Document using standard ADR format
4. Update README ADR index

---

## Decision Documentation

Let me gather information about this decision:

### 1. Context
**What problem are we solving?**
- What forces are at play (technical, business, regulatory)?
- What constraints exist (time, budget, resources, existing systems)?
- Why does this decision matter?

{{USER_CONTEXT}}

### 2. Decision
**What did we decide?**
State the decision clearly in 2-4 sentences.

{{USER_DECISION}}

### 3. Options Considered
**What alternatives did we evaluate?**

For each option:
- Description
- Pros (benefits)
- Cons (drawbacks)
- Cost/effort estimate

Need at least 2-3 alternatives to show we considered options.

{{USER_OPTIONS}}

### 4. Why This One?
**Why was this option selected over alternatives?**

{{USER_RATIONALE}}

### 5. Consequences
**What are the outcomes of this decision?**

**Positive**:
- {{benefit_1}}
- {{benefit_2}}

**Negative**:
- {{trade_off_1}}
- {{trade_off_2}}

**Risks**:
- {{risk_1}} ({{likelihood}}, {{impact}}, mitigation: {{strategy}})

{{USER_CONSEQUENCES}}

---

## ADR Creation

[After gathering all information]

Creating ADR using template...

**File**: `docs/adr/{{next_number}}-{{kebab-case-title}}.md`

```markdown
# {{next_number}}. {{Decision Title}}

**Date**: {{DATE}}
**Status**: Proposed
**Deciders**: {{names}}
**Tags**: {{tags}}

## Context

{{context_from_user}}

**Key factors**:
- {{factor_1}}
- {{factor_2}}

## Decision

{{decision_statement}}

**Rationale**: {{why_this_choice}}

## Options Considered

### Option 1: {{name}}

**Description**: {{description}}

**Pros**:
- ✅ {{pro_1}}
- ✅ {{pro_2}}

**Cons**:
- ❌ {{con_1}}
- ❌ {{con_2}}

**Cost/Effort**: {{level}}

### Option 2: {{name}} ⭐ SELECTED

[Same structure, marked as selected]

### Option 3: {{name}}

[Same structure]

## Consequences

### Positive
- ✅ {{positive_1}}
- ✅ {{positive_2}}

### Negative
- ❌ {{negative_1}}
- ❌ {{negative_2}}

### Risks
- **{{risk}}**: {{description}}
  - Likelihood: {{H/M/L}}
  - Impact: {{H/M/L}}
  - Mitigation: {{strategy}}

## Implementation Notes

### Required Changes
1. {{change_1}}
2. {{change_2}}

### Dependencies
- {{dependency_1}}
- {{dependency_2}}

## Validation & Success Criteria

**Success Metrics**:
- {{metric_1}}: {{target}}
- {{metric_2}}: {{target}}

**Timeline**: {{when_to_evaluate}}

## Related Decisions

- {{related_ADR}}: {{relationship}}

## References

- {{research_doc_link}}
- {{external_docs}}
```

---

## Related ADRs

**Checking for related ADRs**:

[Scan existing ADRs for related topics]

**Related decisions**:
{{list_of_related_ADRs}}

**Relationship**:
- {{ADR_XXX}}: {{how_it_relates}}

Added cross-references to:
- This ADR → references related ADRs
- Related ADRs → updated to reference this one

---

## ADR Complete

✅ **ADR created!**

**File**: `docs/adr/{{next_number}}-{{title}}.md`
**Status**: Proposed (change to "Accepted" when approved)
**Size**: {{line_count}} lines

**Summary**:
- **Decision**: {{one_line_summary}}
- **Chosen**: {{selected_option}}
- **Why**: {{brief_rationale}}
- **Trade-offs**: {{key_trade_offs}}

---

## Handoff Proposal

**Next Steps** (choose one):

1. **[If from Planning] Continue with Implementation**
   - Say: `implement plan` or `#implementation-phase`
   - ADR documented, now execute the plan

2. **[If from Implementation] Continue with Remaining Tasks**
   - Say: `continue implementation`
   - Resume where we left off

3. **Review ADR with Team**
   - Say: `review ADR`
   - Get team feedback before marking as Accepted

4. **Create Another ADR** (if multiple decisions need documentation)
   - Say: `#create-adr {{next_decision}}`

5. **Update README** (link to ADR directory)
   - Say: `update README with ADRs`
   - Add ADR index to project documentation

What would you like to do?

---

## ADR Best Practices

**Remember**:
- ✅ Be specific (not "use database" but "use PostgreSQL 14+ for user data")
- ✅ Document alternatives (show we considered options)
- ✅ Explain trade-offs (acknowledge cons of chosen solution)
- ✅ Keep concise (1-3 pages target)
- ✅ Update status when decision finalized (Proposed → Accepted)
- ✅ Reference in code comments where decision impacts implementation

**When to Update**:
- Status changes (Proposed → Accepted)
- New information emerges
- Decision is superseded (create new ADR, link from old one)

**Don't**:
- ❌ Edit accepted ADRs (create new superseding ADR instead)
- ❌ Delete ADRs (historical record is valuable)
- ❌ Make ADRs for trivial choices
