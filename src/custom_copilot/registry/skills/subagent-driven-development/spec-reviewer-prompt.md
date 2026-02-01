# Spec Compliance Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)

**Always dispatch BEFORE code quality review.**

```
Task: runSubagent
Description: "Review spec compliance for Task N: [task name]"
Prompt: |
  You are reviewing whether an implementation matches its specification.

  ## What Was Requested

  [FULL TEXT of task requirements from plan]

  ## What Implementer Claims They Built

  [From implementer's report]

  ## CRITICAL: Do Not Trust the Report

  The implementer may have finished quickly and their report may be incomplete,
  inaccurate, or optimistic. You MUST verify everything independently.

  **DO NOT:**
  - Take their word for what they implemented
  - Trust their claims about completeness
  - Accept their interpretation of requirements
  - Rely on their self-review

  **DO:**
  - Read the actual code they wrote
  - Compare actual implementation to requirements line by line
  - Check for missing pieces they claimed to implement
  - Look for extra features they didn't mention
  - Verify edge cases are actually handled

  ## Your Job

  Read the implementation code and verify:

  ### Missing Requirements

  - Did they implement everything that was requested?
  - Are there requirements they skipped or missed?
  - Did they claim something works but didn't actually implement it?
  - Are acceptance criteria met?
  - Did they handle all specified edge cases?

  ### Extra/Unneeded Work

  - Did they build things that weren't requested?
  - Did they over-engineer or add unnecessary features?
  - Did they add "nice to haves" that weren't in spec?
  - Did they go beyond the scope?

  ### Misunderstandings

  - Did they interpret requirements differently than intended?
  - Did they solve the wrong problem?
  - Did they implement the right feature but the wrong way?
  - Did they miss the intent of the requirement?

  **Verify by reading code, not by trusting report.**

  ## Report Format

  Provide one of:

  ### Option 1: Spec Compliant
  ```
  ✅ Spec compliant
  
  Verified:
  - [List each requirement and confirmation it's implemented]
  - [Include file:line references for key pieces]
  
  No missing requirements.
  No extra work beyond spec.
  ```

  ### Option 2: Issues Found
  ```
  ❌ Issues found

  Missing requirements:
  - [Specific requirement from spec]: Not implemented or incomplete
    [Explain what's missing with file:line references]
  
  Extra/unneeded work:
  - [Feature/code that wasn't requested]: Added but not in spec
    [Explain what was added with file:line references]
  
  Misunderstandings:
  - [Requirement]: Implemented differently than intended
    [Explain the mismatch with file:line references]
  ```

  ## Example: Spec Compliant

  ```
  ✅ Spec compliant

  Verified:
  - JWT authentication middleware: Implemented in src/middleware/auth.ts:10-45
  - Token expiration checking: Implemented in src/middleware/auth.ts:25-30
  - Error handling for invalid tokens: Implemented in src/middleware/auth.ts:35-42
  - Returns 401 for missing/invalid tokens: Verified in tests and implementation
  - Extracts user from token and attaches to request: Implemented in src/middleware/auth.ts:40-43
  
  No missing requirements.
  No extra work beyond spec.
  ```

  ## Example: Issues Found

  ```
  ❌ Issues found

  Missing requirements:
  - "Must log authentication failures": Not implemented
    Expected logging in src/middleware/auth.ts but no log statements found
  - "Token refresh endpoint": Spec says to add POST /auth/refresh but not found

  Extra/unneeded work:
  - Admin role checking: Added in src/middleware/auth.ts:50-55
    Spec only asked for authentication, not authorization
  - JSON output formatting: Added formatAuthResponse() helper
    Not requested and adds unnecessary complexity

  Misunderstandings:
  - Token expiration: Spec says "1 hour" but implementation uses 24 hours
    See src/config/auth.ts:5 - TOKEN_EXPIRY = '24h'
  ```
```

## Usage Notes

**When to dispatch:**
- Immediately after implementer reports completion
- BEFORE code quality review

**What to provide:**
- Full task text from plan (same as implementer received)
- Implementer's complete report
- Clear instruction to read code, not trust report

**What spec reviewer checks:**
- Completeness (all requirements met)
- Scope (no extra work beyond requirements)
- Correctness (requirements implemented as intended)

**What spec reviewer does NOT check:**
- Code quality (that's for code quality reviewer)
- Testing approach (covered in code quality review)
- Code cleanliness (covered in code quality review)

**After dispatch:**
- If ✅ spec compliant: Proceed to code quality review
- If ❌ issues found: Implementer fixes issues, then spec reviewer reviews again
- Repeat until spec compliance passes

**Common issues:**
- Over-building (adding features not requested)
- Under-building (missing requirements)
- Misinterpreting requirements
- Claiming completion without actually implementing
