# [NUMBER]. [Title in Present Tense]

**Date**: YYYY-MM-DD  
**Status**: Proposed | Accepted | Deprecated | Superseded  
**Deciders**: [List people involved in decision]  
**Tags**: [e.g., architecture, database, api, security, performance]

---

## Context

[Describe the context and problem statement]

What is the issue we're facing that requires a decision?
- What forces are at play (technical, business, regulatory)?
- What constraints do we have (time, budget, resources, existing systems)?
- Why does this decision matter?

**Key factors**:
- [Factor 1: e.g., "Need to handle 1M+ records efficiently"]
- [Factor 2: e.g., "Team has limited experience with distributed systems"]
- [Factor 3: e.g., "Must integrate with existing legacy database"]

---

## Decision

[Describe the decision in 2-4 sentences]

**We will**: [State the decision clearly and unambiguously]

**Rationale**: [Brief explanation of why this is the right choice]

---

## Options Considered

### Option 1: [Name of option]

**Description**: [Brief description of this approach]

**Pros**:
- ✅ [Pro 1]
- ✅ [Pro 2]
- ✅ [Pro 3]

**Cons**:
- ❌ [Con 1]
- ❌ [Con 2]
- ❌ [Con 3]

**Cost/Effort**: High | Medium | Low

---

### Option 2: [Name of option] ⭐ SELECTED

**Description**: [Brief description of this approach]

**Pros**:
- ✅ [Pro 1]
- ✅ [Pro 2]
- ✅ [Pro 3]

**Cons**:
- ❌ [Con 1]
- ❌ [Con 2]
- ❌ [Con 3]

**Cost/Effort**: High | Medium | Low

**Why Selected**: [Specific reasons why this was chosen over alternatives]

---

### Option 3: [Name of option]

**Description**: [Brief description of this approach]

**Pros**:
- ✅ [Pro 1]
- ✅ [Pro 2]

**Cons**:
- ❌ [Con 1]
- ❌ [Con 2]

**Cost/Effort**: High | Medium | Low

---

## Consequences

### Positive Consequences

- ✅ [Positive 1: e.g., "Better performance under high load"]
- ✅ [Positive 2: e.g., "Simplified maintenance"]
- ✅ [Positive 3: e.g., "Improved developer experience"]

### Negative Consequences

- ❌ [Negative 1: e.g., "Increased initial setup time"]
- ❌ [Negative 2: e.g., "New dependency to manage"]
- ❌ [Negative 3: e.g., "Learning curve for team"]

### Neutral Consequences

- ⚪ [Neutral 1: e.g., "Different but not worse/better than alternative"]

### Risks and Mitigations

- **[Risk 1]**: [Description]
  - **Likelihood**: High | Medium | Low
  - **Impact**: High | Medium | Low
  - **Mitigation**: [How we'll address this risk]

- **[Risk 2]**: [Description]
  - **Likelihood**: High | Medium | Low
  - **Impact**: High | Medium | Low
  - **Mitigation**: [How we'll address this risk]

---

## Implementation Notes

### Required Changes

1. [Change 1: e.g., "Update database schema"]
2. [Change 2: e.g., "Refactor authentication module"]
3. [Change 3: e.g., "Add new dependencies to package.json"]

### Migration Path

[If this decision requires migrating from an existing solution]

**Steps**:
1. [Step 1: e.g., "Deploy new system alongside old"]
2. [Step 2: e.g., "Migrate data in phases"]
3. [Step 3: e.g., "Switch over and deprecate old system"]

**Timeline**: [Expected timeline for implementation]

### Dependencies

**Technical Dependencies**:
- [Dependency 1: e.g., "Requires PostgreSQL 14+"]
- [Dependency 2: e.g., "Must complete ADR-002 first"]

**Team Dependencies**:
- [Dependency 1: e.g., "Requires training on new framework"]
- [Dependency 2: e.g., "Need infrastructure team to provision resources"]

---

## Validation & Success Criteria

### How to Validate Decision

[How will we know this decision was correct?]

**Success Metrics**:
- [Metric 1: e.g., "Response time < 100ms for 95th percentile"]
- [Metric 2: e.g., "Zero security vulnerabilities in first month"]
- [Metric 3: e.g., "Team productivity increases by 20%"]

**Timeline for Validation**: [When we'll evaluate these metrics]

### Exit Criteria

[Under what conditions would we reconsider this decision?]

- [Criterion 1: e.g., "If performance degrades beyond acceptable limits"]
- [Criterion 2: e.g., "If maintenance cost exceeds 20 hours/month"]
- [Criterion 3: e.g., "If critical security issues emerge"]

---

## Related Decisions

- [ADR-XXX]: [Related decision and how it relates]
- [ADR-YYY]: [Another related decision]

**Supersedes**: [ADR-ZZZ if this replaces a previous decision]

**Superseded by**: [Leave blank unless this decision is later replaced]

---

## References

- [Link to research document]
- [Link to RFC or proposal]
- [External documentation]
- [Proof of concept or prototype]
- [Related GitHub issues or tickets]
- [Technical documentation for chosen solution]

---

## Discussion Notes

[Optional: Key points from decision discussion]

**Concerns Raised**:
- [Concern 1 and how it was addressed]
- [Concern 2 and how it was addressed]

**Questions Answered**:
- Q: [Question 1]
  - A: [Answer]
- Q: [Question 2]
  - A: [Answer]

---

## Approval

**Decision Date**: YYYY-MM-DD  
**Approved by**: [Names/roles of approvers]  
**Review Date**: [When this decision should be reviewed, if applicable]

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial version | [Name] |
| YYYY-MM-DD | Updated status to Accepted | [Name] |
| YYYY-MM-DD | [Other changes] | [Name] |

---

## Template Usage Notes

**Remove this section before committing the ADR**

### ADR Numbering
- Use sequential numbers: 0001, 0002, 0003, etc.
- Check `docs/adr/` directory for the next available number
- Pad with leading zeros (e.g., 0001 not 1)

### Status Values
- **Proposed**: Under consideration
- **Accepted**: Approved and being/will be implemented
- **Deprecated**: No longer recommended but still in use
- **Superseded**: Replaced by a newer decision (reference the new ADR)

### Title Guidelines
- Use present tense ("Use PostgreSQL" not "Using PostgreSQL")
- Be specific ("Use PostgreSQL for user data" not "Choose database")
- Keep it short but descriptive (< 60 characters)

### File Naming
Format: `NNNN-title-in-kebab-case.md`

Examples:
- `0001-use-postgresql-for-user-data.md`
- `0002-adopt-microservices-architecture.md`
- `0003-implement-jwt-authentication.md`

### When to Create an ADR
Create an ADR for:
- Technology/framework choices
- Architectural patterns
- Database design decisions
- Security models
- API design approaches
- Major refactoring decisions

Don't create an ADR for:
- Minor implementation details
- Obvious or trivial choices
- Temporary workarounds
- Bug fixes (unless they reveal an architectural issue)

### How Much Detail?
- **Minimum viable ADR**: Context, Decision, Consequences
- **Recommended**: Add Options Considered for important decisions
- **Full ADR**: Include all sections for critical architectural decisions

Keep it concise but complete. Aim for 1-3 pages.
