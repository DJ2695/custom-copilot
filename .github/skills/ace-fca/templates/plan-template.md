# Implementation Plan: [Feature Name]

**Date**: YYYY-MM-DD  
**Author**: [Your name or "AI Agent"]  
**Status**: 🔵 Planning | 🟢 In Progress | ✅ Complete  
**Related Research**: [Link to research doc if exists]

---

## Overview

[2-4 sentences describing what this plan accomplishes]

### Goals
- [Goal 1: Specific, measurable outcome]
- [Goal 2: Specific, measurable outcome]
- [Goal 3: Specific, measurable outcome]

### Non-Goals
- [What this plan explicitly does NOT include]
- [Use YAGNI to identify scope creep]

---

## Requirements

### Functional Requirements
1. [FR-1]: [Specific, testable requirement]
2. [FR-2]: [Specific, testable requirement]
3. [FR-3]: [Specific, testable requirement]

### Non-Functional Requirements
1. [NFR-1]: [Performance, security, scalability requirement]
2. [NFR-2]: [Performance, security, scalability requirement]

### Acceptance Criteria
- [ ] [Criterion 1: How to verify this is complete]
- [ ] [Criterion 2: How to verify this is complete]
- [ ] [Criterion 3: How to verify this is complete]

---

## Architecture & Design

### High-Level Design

[Brief description or ASCII diagram of the approach]

```
[Component A] ──> [Component B]
      │                │
      ↓                ↓
[Component C] ──> [Component D]
```

### Key Design Decisions

**Decision 1**: [Decision name]
- **Choice**: [What was decided]
- **Rationale**: [Why]
- **Alternatives**: [What else was considered]
- **ADR**: [Link to ADR if created]

**Decision 2**: [Decision name]
- **Choice**: [What was decided]
- **Rationale**: [Why]
- **Alternatives**: [What else was considered]
- **ADR**: [Link to ADR if created]

---

## Dependencies

### External Dependencies
- **[Dependency name]**: [Why needed, version requirements]
- **[Another dependency]**: [Why needed, version requirements]

### Internal Dependencies
- **[Module/service]**: [What functionality we depend on]
- **[Another module]**: [What functionality we depend on]

### Blocked By
- [ ] [Task or decision that must complete first]
- [ ] [Another blocking item]

---

## Implementation Tasks

### Phase 1: Foundation

#### Task 1: [Task Name] (Est: 5 min)

**File**: `path/to/file.ext`

**Changes**:
- [Specific change 1]
- [Specific change 2]

**Code**:
```[language]
[Complete code snippet showing exact implementation]
```

**Test Expectation**:
- Test file: `path/to/test_file.ext`
- Test name: `test_[specific_scenario]`
- Expected behavior: [What the test should verify]

**Verification**:
```bash
[Exact command to run to verify this task]
```

**Dependencies**: [None | Task X must complete first]

---

#### Task 2: [Create ADR for Key Decision] (Est: 3 min)

**Create**: `docs/adr/NNNN-[decision-title].md`

**Decision**: [What architectural decision needs documentation]

**Rationale**: [Why this decision is being made]

**Alternatives Considered**: [Brief list]

**Template**: Use `templates/adr-template.md`

**Verification**: ADR file created and reviewed

---

#### Task 3: [Another Task Name] (Est: 7 min)

**File**: `path/to/another_file.ext`

**Changes**:
- [Specific change 1]
- [Specific change 2]

**Code**:
```[language]
[Complete code snippet showing exact implementation]
```

**Test Expectation**:
- Test file: `path/to/test_file.ext`
- Test name: `test_[specific_scenario]`
- Expected behavior: [What the test should verify]

**Verification**:
```bash
[Exact command to run to verify this task]
```

**Dependencies**: Task 1 must complete first

---

### Phase 2: Core Implementation

[Continue with same task format for each phase]

---

### Phase 3: Integration & Testing

[Final phase tasks]

---

## Testing Strategy

### Unit Tests
- **Coverage target**: [Percentage or "100%"]
- **Location**: `tests/unit/[module]_test.ext`
- **Key scenarios**:
  - [Scenario 1: e.g., "Valid input returns success"]
  - [Scenario 2: e.g., "Invalid input raises ValidationError"]
  - [Scenario 3: e.g., "Edge case X handled correctly"]

### Integration Tests
- **Coverage target**: [What integration points to test]
- **Location**: `tests/integration/[feature]_test.ext`
- **Key scenarios**:
  - [Scenario 1: e.g., "End-to-end user registration flow"]
  - [Scenario 2: e.g., "Error handling in multi-step process"]

### Manual Testing
- [ ] [Manual test 1: e.g., "Test UI with screen reader"]
- [ ] [Manual test 2: e.g., "Verify email delivery in staging"]

---

## Rollout Plan

### Development Environment
1. [Step 1: e.g., "Run migrations in local DB"]
2. [Step 2: e.g., "Start development server"]
3. [Step 3: e.g., "Verify feature works locally"]

### Testing Environment
1. [Step 1: e.g., "Deploy to test environment"]
2. [Step 2: e.g., "Run full test suite"]
3. [Step 3: e.g., "Manual QA verification"]

### Production (if applicable)
1. [Step 1: e.g., "Deploy behind feature flag"]
2. [Step 2: e.g., "Enable for 10% of users"]
3. [Step 3: e.g., "Monitor metrics for 24 hours"]
4. [Step 4: e.g., "Full rollout if metrics healthy"]

---

## Risk Mitigation

### Technical Risks
- **[Risk 1]**: [Description]
  - **Likelihood**: High | Medium | Low
  - **Impact**: High | Medium | Low
  - **Mitigation**: [How to address]

### Operational Risks
- **[Risk 2]**: [Description]
  - **Likelihood**: High | Medium | Low
  - **Impact**: High | Medium | Low
  - **Mitigation**: [How to address]

---

## Success Metrics

### How to Measure Success
- **[Metric 1]**: [What to measure, expected value]
- **[Metric 2]**: [What to measure, expected value]
- **[Metric 3]**: [What to measure, expected value]

### Monitoring
- **Dashboards**: [Links to relevant dashboards]
- **Alerts**: [What alerts should be configured]
- **Logs**: [What to log for debugging]

---

## Timeline

| Phase | Tasks | Est. Duration | Status |
|-------|-------|--------------|--------|
| Phase 1: Foundation | Tasks 1-3 | 15 min | ❌ Not Started |
| Phase 2: Core Implementation | Tasks 4-8 | 30 min | ❌ Not Started |
| Phase 3: Integration | Tasks 9-10 | 20 min | ❌ Not Started |
| **Total** | **10 tasks** | **~65 min** | |

---

## Progress Tracking

### Completed ✅
_[Tasks move here as they complete]_

### In Progress ⏳
_[Current task being worked on]_

### Blocked ⚠️
_[Tasks that can't proceed due to dependencies]_

### Todo ❌
- [ ] Task 1: [Task name]
- [ ] Task 2: [Task name]
- [ ] Task 3: [Task name]
- [... all remaining tasks]

---

## Progress Updates

### Update 1: [Date/Time]
**Status**: [Brief status summary]

**Completed since last update**:
- ✅ Task X: [Brief note]
- ✅ Task Y: [Brief note]

**Current focus**: Task Z

**Blockers**: [None | Description of blocker]

**Next steps**: [What's coming next]

---

### Update 2: [Date/Time]
[Same format as Update 1]

---

## Post-Implementation

### Documentation Updates Needed
- [ ] [Doc 1: e.g., "Update API documentation"]
- [ ] [Doc 2: e.g., "Add feature to user guide"]

### Follow-Up Tasks (Future)
- [ ] [Task 1: e.g., "Add internationalization support"]
- [ ] [Task 2: e.g., "Performance optimization if metrics show need"]

### Retrospective Notes
_[After completion, document lessons learned]_

**What went well**:
- [Success 1]
- [Success 2]

**What could be improved**:
- [Improvement 1]
- [Improvement 2]

**Action items**:
- [Action 1: e.g., "Update planning template based on learning"]
- [Action 2: e.g., "Add new pattern to team guidelines"]

---

## References

- Research doc: [Link]
- Related ADRs: [Links]
- Related issues/tickets: [Links]
- External documentation: [Links]

---

## Notes

[Any additional context, open questions, or clarifications needed]
