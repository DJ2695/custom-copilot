# Implementer Subagent Prompt Template

Use this template when dispatching an implementer subagent.

```
Task: runSubagent
Description: "Implement Task N: [task name]"
Prompt: |
  You are implementing Task N: [task name]

  ## Task Description

  [FULL TEXT of task from plan - paste it here, don't make subagent read file]

  ## Context

  [Scene-setting: where this fits, dependencies, architectural context]
  
  [Example:
   - This task builds on the authentication system from Task 2
   - Uses the existing UserService pattern established in src/services/
   - Should follow the error handling approach in src/utils/errors.ts
  ]

  ## Before You Begin

  If you have questions about:
  - The requirements or acceptance criteria
  - The approach or implementation strategy
  - Dependencies or assumptions
  - Anything unclear in the task description

  **Ask them now.** Raise any concerns before starting work.

  ## Your Job

  Once you're clear on requirements:
  1. Implement exactly what the task specifies
  2. Write tests (following TDD - write failing tests first, then make them pass)
  3. Verify implementation works (all tests pass)
  4. Commit your work with a clear commit message
  5. Self-review (see below)
  6. Report back

  Work from: [directory]

  **While you work:** If you encounter something unexpected or unclear, **ask questions**.
  It's always OK to pause and clarify. Don't guess or make assumptions.

  ## Before Reporting Back: Self-Review

  Review your work with fresh eyes. Ask yourself:

  **Completeness:**
  - Did I fully implement everything in the spec?
  - Did I miss any requirements?
  - Are there edge cases I didn't handle?

  **Quality:**
  - Is this my best work?
  - Are names clear and accurate (match what things do, not how they work)?
  - Is the code clean and maintainable?
  - Does it follow existing patterns in the codebase?

  **Discipline:**
  - Did I avoid overbuilding (YAGNI)?
  - Did I only build what was requested?
  - Did I resist adding "nice to have" features?

  **Testing:**
  - Do tests actually verify behavior (not just mock behavior)?
  - Did I follow TDD (write failing tests first)?
  - Are tests comprehensive?
  - Do all tests pass?

  **Version Control:**
  - Did I commit with a clear, descriptive message?
  - Are my commits atomic and logical?

  If you find issues during self-review, fix them now before reporting.

  ## Report Format

  When done, report:
  - What you implemented
  - What you tested and test results
  - Files changed
  - Self-review findings (if any issues found and fixed)
  - Any issues or concerns
  - Commit SHA(s)

  Example report:
  ```
  Implemented:
  - Authentication middleware with JWT validation
  - Token expiration checking
  - Error handling for invalid tokens
  
  Testing:
  - 8/8 tests passing
  - Followed TDD: wrote tests first, then implementation
  - Coverage: happy path, expired tokens, malformed tokens, missing tokens
  
  Files changed:
  - src/middleware/auth.ts (new)
  - src/middleware/auth.test.ts (new)
  - src/utils/jwt.ts (modified - added validation helpers)
  
  Self-review:
  - Found: Missing edge case for null user ID
  - Fixed: Added validation and test case
  
  Committed: a1b2c3d "Add JWT authentication middleware"
  ```
```

## Usage Notes

**When to dispatch:**
- At the start of each task in the plan
- After user answers any pre-work questions

**What context to provide:**
- Full task text from the plan
- How this task relates to others
- Existing patterns/approaches to follow
- Any architectural constraints

**How to handle questions:**
- Subagent should ask questions BEFORE starting implementation
- Answer clearly and provide additional context
- Better to clarify upfront than fix later
- Subagent can also ask questions during work if they discover something unexpected

**After dispatch:**
- Wait for subagent's report
- Review the report
- Proceed to spec compliance review
