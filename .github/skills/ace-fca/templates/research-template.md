# Research: [Topic Name]

**Date**: YYYY-MM-DD  
**Researcher**: [Your name or "AI Agent"]  
**Context**: [What prompted this research]

---

## Problem Understanding

[2-3 sentences describing the core issue or question being researched]

---

## Relevant Code Locations

List key files with specific responsibilities:

- **[path/to/file.ext]** (lines X-Y)
  - Responsibility: [What this file/section does]
  - Dependencies: [Key dependencies]
  - Notes: [Anything important to know]

- **[path/to/another.ext]** (lines A-B)
  - Responsibility: [What this file/section does]
  - Dependencies: [Key dependencies]
  - Notes: [Anything important to know]

---

## Key Dependencies

List only dependencies that matter for this task:

### External Dependencies
- **[package-name]** (version): [Why it's used, what it provides]
- **[another-package]** (version): [Why it's used, what it provides]

### Internal Dependencies
- **[module/service]**: [How it's used in this context]
- **[another-module]**: [How it's used in this context]

---

## Current Implementation Patterns

Document existing patterns that should be followed:

### Pattern 1: [Pattern Name]
**Used in**: [Where this pattern is used]  
**Purpose**: [Why this pattern exists]  
**Example**:
```[language]
[Code example showing the pattern]
```

### Pattern 2: [Pattern Name]
**Used in**: [Where this pattern is used]  
**Purpose**: [Why this pattern exists]  
**Example**:
```[language]
[Code example showing the pattern]
```

---

## Constraints & Considerations

### Technical Constraints
- [Constraint 1: e.g., "Must maintain backward compatibility with API v1"]
- [Constraint 2: e.g., "Database has row-level security enabled"]
- [Constraint 3: e.g., "Must work with Python 3.8+"]

### Business/Domain Constraints
- [Constraint 1: e.g., "Email must be unique across all tenants"]
- [Constraint 2: e.g., "Processing must complete within 5 seconds"]

### Testing Requirements
- [Requirement 1: e.g., "100% test coverage required"]
- [Requirement 2: e.g., "Integration tests must run in CI/CD"]

---

## Existing Solutions & Related Work

Document relevant existing implementations:

### Similar Features
- **[Feature name]** in [location]: [How it works, what we can learn]
- **[Another feature]** in [location]: [How it works, what we can learn]

### Utilities & Helpers
- **[Utility name]** in [location]: [What it does, how to use it]
- **[Helper name]** in [location]: [What it does, how to use it]

---

## Recommended Approach

Based on the research, recommend a high-level direction:

### Proposed Solution
[2-4 sentences describing the recommended approach]

### Why This Approach
- **Pro**: [Advantage 1]
- **Pro**: [Advantage 2]
- **Con**: [Trade-off 1]
- **Con**: [Trade-off 2]

### Alternatives Considered
1. **[Alternative 1]**: [Brief description]
   - Why not chosen: [Reason]

2. **[Alternative 2]**: [Brief description]
   - Why not chosen: [Reason]

---

## Open Questions

List anything that needs clarification before planning:

1. [Question 1: e.g., "Should validation be synchronous or asynchronous?"]
   - Impact: [Why this matters]
   - Recommendation: [If you have one]

2. [Question 2: e.g., "How should we handle legacy data that doesn't meet new validation rules?"]
   - Impact: [Why this matters]
   - Recommendation: [If you have one]

---

## Risk Assessment

### High Priority Risks
- **[Risk 1]**: [Description]
  - Mitigation: [How to address]

### Medium Priority Risks
- **[Risk 2]**: [Description]
  - Mitigation: [How to address]

### Low Priority Risks
- **[Risk 3]**: [Description]
  - Mitigation: [How to address]

---

## Next Steps

1. [Step 1: e.g., "Create implementation plan based on this research"]
2. [Step 2: e.g., "Get architectural decision approved"]
3. [Step 3: e.g., "Set up test environment"]

---

## References

- [Link to relevant documentation]
- [Link to related ADRs]
- [Link to similar implementations]
- [External resources consulted]

---

## Appendix: Research Notes

[Optional section for raw notes, commands run, files examined, etc.]

### Files Examined
- [List of all files read during research]

### Commands Run
```bash
[Commands used to gather information]
```

### Searches Performed
- Query: "[search term]" - Found: [brief summary]
- Query: "[another term]" - Found: [brief summary]
