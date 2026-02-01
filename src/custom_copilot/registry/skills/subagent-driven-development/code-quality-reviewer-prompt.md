# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch AFTER spec compliance review passes.**

```
Task: runSubagent
Description: "Review code quality for Task N: [task name]"
Prompt: |
  You are reviewing the code quality of an implementation.

  ## Implementation Details

  **What was implemented:** [from implementer's report]
  
  **Task requirements:** Task N from [plan file name]
  
  **Commits to review:**
  - Base SHA: [commit before task started]
  - Head SHA: [commit after task completed]
  
  **Task summary:** [brief description of what this task accomplished]

  ## Your Job

  Review the code changes between the base and head commits for quality.

  **Focus on:**
  - Code cleanliness and readability
  - Test coverage and quality
  - Maintainability
  - Following project conventions
  - Proper error handling
  - Performance considerations (if relevant)

  **Do NOT focus on:**
  - Spec compliance (that was already verified)
  - Whether requirements were met (that's done)
  - Functionality (assume that's correct)

  ## Review Categories

  ### Strengths
  
  What is done well in this implementation?
  - Clear naming
  - Good test coverage
  - Clean structure
  - Follows patterns
  - Good error handling

  ### Issues

  Categorize issues by severity:

  **Critical (must fix):**
  - Security vulnerabilities
  - Data loss risks
  - Breaking changes
  - Test failures
  - Major bugs

  **Important (should fix):**
  - Poor naming
  - Missing error handling
  - Magic numbers/strings
  - Test gaps
  - Significant code duplication
  - Performance issues

  **Minor (nice to have):**
  - Minor style inconsistencies
  - Could be slightly cleaner
  - Marginal improvements

  For each issue, provide:
  - File and line reference
  - Clear description of the problem
  - Suggested fix (if not obvious)

  ## Report Format

  ```
  Strengths:
  - [List what's done well]

  Issues:

  Critical:
  - [Issue with file:line] - [description] - [suggested fix]

  Important:
  - [Issue with file:line] - [description] - [suggested fix]

  Minor:
  - [Issue with file:line] - [description] - [suggested fix]

  Assessment: [Approved | Needs fixes]
  ```

  ## Example: Approved

  ```
  Strengths:
  - Excellent test coverage (8/8 tests, all edge cases covered)
  - Clear, descriptive naming (validateToken, extractUserFromToken)
  - Good error handling with specific error messages
  - Follows existing middleware pattern in codebase
  - Comprehensive JSDoc comments

  Issues:

  Critical: None

  Important: None

  Minor:
  - src/middleware/auth.ts:25 - Could extract token expiration constant
    Currently: if (exp < Date.now() / 1000)
    Suggest: Extract MILLISECONDS_TO_SECONDS constant

  Assessment: Approved (minor issue acceptable)
  ```

  ## Example: Needs Fixes

  ```
  Strengths:
  - Good test coverage for happy path
  - Follows existing patterns

  Issues:

  Critical:
  - src/middleware/auth.ts:30 - Unhandled promise rejection
    Missing .catch() on async JWT verification
    Suggest: Add try/catch or .catch() handler

  Important:
  - src/middleware/auth.ts:15 - Magic number
    Token expiration hardcoded as 3600
    Suggest: Extract to AUTH_TOKEN_EXPIRY constant in config
  - src/middleware/auth.test.ts - Missing edge case tests
    No tests for malformed tokens or missing user ID
    Suggest: Add tests for error paths

  Minor:
  - src/middleware/auth.ts:40 - Variable name could be clearer
    'data' is vague, suggest 'decodedToken'

  Assessment: Needs fixes (Critical and Important issues must be addressed)
  ```

  ## Guidelines

  **Be specific:**
  - Always include file:line references
  - Explain why something is a problem
  - Suggest concrete fixes

  **Be fair:**
  - Acknowledge what's done well
  - Don't nitpick minor style preferences
  - Focus on meaningful improvements

  **Be consistent:**
  - Use project's conventions as the standard
  - Don't enforce personal preferences
  - Reference existing patterns in codebase

  **Be practical:**
  - Consider the scope of the task
  - Don't expect gold-plating
  - Balance thoroughness with pragmatism

  ## What to Approve

  Approve if:
  - No Critical or Important issues
  - Minor issues are acceptable trade-offs
  - Code is maintainable and follows patterns
  - Tests adequately cover the implementation

  Request fixes if:
  - Any Critical issues exist
  - Important issues that affect maintainability
  - Missing error handling
  - Inadequate test coverage

  ## After Reviewing

  If issues found:
  - Implementer (same subagent) will fix them
  - You will review again after fixes
  - Repeat until approved

  If approved:
  - Task is complete
  - Move to next task or final review
```

## Usage Notes

**When to dispatch:**
- Only AFTER spec compliance reviewer has approved (✅)
- Never before spec compliance passes

**What to provide:**
- What was implemented (from implementer report)
- Task requirements reference (plan file and task number)
- Git SHAs (base and head) for the diff
- Brief task summary

**What code quality reviewer checks:**
- Code cleanliness
- Test quality and coverage
- Maintainability
- Error handling
- Project conventions

**What code quality reviewer does NOT check:**
- Spec compliance (already verified)
- Functionality correctness (assumed correct after spec review)

**After dispatch:**
- If approved: Mark task complete, move to next task
- If needs fixes: Implementer fixes issues, then code quality reviewer reviews again
- Repeat until code quality passes

**Integration with existing skills:**
- Can reference systematic-debugging skill for issues found
- Can reference test-driven-development skill for test quality
- Should align with project's existing code review standards

**Common issues found:**
- Magic numbers/strings
- Poor naming
- Missing error handling
- Inadequate test coverage
- Code duplication
- Not following project patterns
