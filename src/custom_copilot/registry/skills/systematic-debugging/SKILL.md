---
name: systematic-debugging
description: 'Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Enforces root cause investigation over random fixes.'
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

Use this ESPECIALLY when:
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

Don't skip when:
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

BEFORE attempting ANY fix:

**1. Read Error Messages Carefully**

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Python:**
```python
# Read the full traceback
Traceback (most recent call last):
  File "/app/users.py", line 45, in create_user
    db.execute(query, params)
  File "/app/database.py", line 23, in execute
    cursor.execute(sql, params)
sqlite3.IntegrityError: UNIQUE constraint failed: users.email
#                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                        This tells you EXACTLY what's wrong
```

**Flutter:**
```dart
// Read the full exception
Exception: Bad state: Cannot add new events after calling close
#0      _BroadcastStreamController.add (dart:async/broadcast_stream_controller.dart:248)
#1      UserBloc.addUser (package:app/blocs/user_bloc.dart:45)
#                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                        Line 45 in user_bloc.dart is the issue
```

**2. Reproduce Consistently**

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Python:**
```bash
# Make it reproducible
pytest tests/test_user.py::test_create_user -v
# Does it fail every time? Or just sometimes?

# If flaky, run multiple times
for i in {1..10}; do pytest tests/test_user.py::test_create_user; done
```

**Flutter:**
```bash
# Make it reproducible
flutter test test/user_bloc_test.dart --name "creates user"

# If flaky, run multiple times
for i in {1..10}; do flutter test test/user_bloc_test.dart; done
```

**3. Check Recent Changes**

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes
- Environmental differences

```bash
# What changed recently?
git log --oneline -10
git diff HEAD~5

# What dependencies changed?
git diff HEAD~5 requirements.txt  # Python
git diff HEAD~5 pubspec.yaml      # Flutter
```

**4. Gather Evidence in Multi-Component Systems**

WHEN system has multiple components (API → service → database, UI → BLoC → repository):

BEFORE proposing fixes, add diagnostic instrumentation:

```
For EACH component boundary:
  - Log what data enters component
  - Log what data exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Python example (multi-layer system):**
```python
# Layer 1: API endpoint
@app.post("/users")
def create_user(user_data: dict):
    print(f"=== API received: {user_data}")
    result = user_service.create(user_data)
    print(f"=== API returning: {result}")
    return result

# Layer 2: Service
class UserService:
    def create(self, data: dict):
        print(f"=== Service received: {data}")
        user = User(**data)
        print(f"=== Service created user: {user}")
        saved = self.repository.save(user)
        print(f"=== Service saved: {saved}")
        return saved

# Layer 3: Repository
class UserRepository:
    def save(self, user: User):
        print(f"=== Repository saving: {user.dict()}")
        print(f"=== DB state: {self.db.is_connected}")
        result = self.db.insert("users", user.dict())
        print(f"=== Repository result: {result}")
        return result
```

**Flutter example (BLoC pattern):**
```dart
// Layer 1: Widget
ElevatedButton(
  onPressed: () {
    debugPrint('=== Widget: Adding user event');
    context.read<UserBloc>().add(AddUserEvent(user));
  },
)

// Layer 2: BLoC
class UserBloc extends Bloc<UserEvent, UserState> {
  Future<void> _onAddUser(AddUserEvent event, Emitter<UserState> emit) async {
    debugPrint('=== BLoC received: ${event.user}');
    debugPrint('=== BLoC state before: $state');
    
    final result = await repository.createUser(event.user);
    
    debugPrint('=== BLoC result: $result');
    emit(UserCreated(result));
  }
}

// Layer 3: Repository
class UserRepository {
  Future<User> createUser(User user) async {
    debugPrint('=== Repository creating: ${user.toJson()}');
    final response = await httpClient.post('/users', body: user.toJson());
    debugPrint('=== Repository response: ${response.statusCode}');
    return User.fromJson(response.body);
  }
}
```

**5. Trace Data Flow**

WHEN error is deep in call stack:

See [root-cause-tracing.md](references/root-cause-tracing.md) for the complete backward tracing technique.

Quick version:
- Where does bad value originate?
- What called this with bad value?
- Keep tracing up until you find the source
- Fix at source, not at symptom

### Phase 2: Pattern Analysis

Find the pattern before fixing:

**1. Find Working Examples**

- Locate similar working code in same codebase
- What works that's similar to what's broken?

**Python:**
```python
# Find similar working test
# Working: test_create_user_with_email()
# Broken:  test_create_user_without_email()
# What's different?
```

**Flutter:**
```dart
// Find similar working widget test
// Working: testWidgets('creates user with valid data')
// Broken:  testWidgets('creates user with empty email')
// What's different?
```

**2. Compare Against References**

- If implementing pattern, read reference implementation COMPLETELY
- Don't skim - read every line
- Understand the pattern fully before applying

**3. Identify Differences**

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

**4. Understand Dependencies**

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

### Phase 3: Hypothesis and Testing

Scientific method:

**1. Form Single Hypothesis**

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

**Example:**
```
Hypothesis: User creation fails because email validation runs before
the email field is set, causing it to reject empty string.

Evidence: Logs show validator called with email='' before
user.email is assigned.
```

**2. Test Minimally**

- Make the SMALLEST possible change to test hypothesis
- One variable at a time
- Don't fix multiple things at once

**Python:**
```python
# Test hypothesis: validation order issue
# Change ONLY the order, nothing else
def create_user(data: dict):
    user = User(**data)  # Create first
    user.validate()      # Then validate (was: validate first)
    return user
```

**Flutter:**
```dart
// Test hypothesis: state emission order
// Change ONLY the order
void _onAddUser(AddUserEvent event, Emitter<UserState> emit) async {
  emit(UserLoading());     // Was after repository call
  final result = await repository.createUser(event.user);
  emit(UserCreated(result));
}
```

**3. Verify Before Continuing**

- Did it work? Yes → Phase 4
- Didn't work? Form NEW hypothesis
- DON'T add more fixes on top

**4. When You Don't Know**

- Say "I don't understand X"
- Don't pretend to know
- Ask for help
- Research more

### Phase 4: Implementation

Fix the root cause, not the symptom:

**1. Create Failing Test Case**

- Simplest possible reproduction
- Automated test if possible
- One-off test script if no framework
- MUST have before fixing
- Use the test-driven-development skill for writing proper failing tests

**Python:**
```python
def test_creates_user_with_empty_email():
    """Regression test for issue #123."""
    user_data = {"name": "Alice", "email": ""}
    
    with pytest.raises(ValidationError, match="Email required"):
        create_user(user_data)
```

**Flutter:**
```dart
test('creates user with empty email', () {
  final user = User(name: 'Alice', email: '');
  
  expect(
    () => userBloc.add(AddUserEvent(user)),
    throwsA(isA<ValidationError>()),
  );
});
```

**2. Implement Single Fix**

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

**3. Verify Fix**

- Test passes now?
- No other tests broken?
- Issue actually resolved?

**Python:**
```bash
# Run the specific test
pytest tests/test_user.py::test_creates_user_with_empty_email -v

# Run all tests to check for regressions
pytest tests/ -v
```

**Flutter:**
```bash
# Run the specific test
flutter test test/user_bloc_test.dart --name "creates user with empty email"

# Run all tests
flutter test
```

**4. If Fix Doesn't Work**

- STOP
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- If ≥ 3: STOP and question the architecture (step 5 below)
- DON'T attempt Fix #4 without architectural discussion

**5. If 3+ Fixes Failed: Question Architecture**

Pattern indicating architectural problem:
- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

STOP and question fundamentals:
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

Discuss with your human partner before attempting more fixes.

This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)
- Each fix reveals new problem in different place

**ALL of these mean: STOP. Return to Phase 1.**

If 3+ fixes failed: Question the architecture (see Phase 4.5)

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Actions | Outcome |
|-------|---------|---------|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

## Python-Specific Debugging Tools

**Using pdb (Python debugger):**
```python
import pdb; pdb.set_trace()  # Python < 3.7
breakpoint()                  # Python >= 3.7

# Common pdb commands:
# l(ist)    - Show current code
# n(ext)    - Next line
# s(tep)    - Step into function
# c(ontinue) - Continue execution
# p variable - Print variable
# pp variable - Pretty-print variable
```

**Logging for diagnosis:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug(f"Variable state: {var}")
logger.debug(f"Function called with: {args}, {kwargs}")
```

**pytest debugging:**
```bash
# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Verbose output
pytest -vv
```

## Flutter-Specific Debugging Tools

**Using debugger:**
```dart
// Add breakpoint in IDE or use debugger;
void someFunction() {
  debugger();  // Execution pauses here when running in debug mode
  // ...
}
```

**Logging for diagnosis:**
```dart
import 'package:flutter/foundation.dart';

debugPrint('Variable state: $var');
debugPrint('Function called with: ${widget.toString()}');

// Conditional logging
if (kDebugMode) {
  print('Debug only: $sensitiveData');
}
```

**Flutter DevTools:**
```bash
# Launch DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Then run app in debug mode
flutter run
```

**Widget inspection:**
```dart
// Dump widget tree to console
debugDumpApp();

// Dump render tree
debugDumpRenderTree();

// Dump layer tree
debugDumpLayerTree();
```

## Supporting Techniques

See references/ directory for detailed techniques:

- [root-cause-tracing.md](references/root-cause-tracing.md) - Trace bugs backward through call stack to find original trigger
- [condition-based-waiting.md](references/condition-based-waiting.md) - Replace arbitrary timeouts with condition polling for async operations

Related skills:
- test-driven-development - For creating failing test case (Phase 4, Step 1)

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

But: 95% of "no root cause" cases are incomplete investigation.

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
