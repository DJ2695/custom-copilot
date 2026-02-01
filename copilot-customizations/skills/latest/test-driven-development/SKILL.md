---
name: test-driven-development
description: 'Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle with failing tests first.'
---

# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

Always:
- New features
- Bug fixes
- Refactoring
- Behavior changes

Exceptions (ask your human partner):
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

No exceptions:
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## RED-GREEN-REFACTOR Cycle

### RED - Write Failing Test

Write one minimal test showing what should happen.

**Python (pytest):**
```python
def test_retries_failed_operations_3_times():
    """Should retry failed operations exactly 3 times before succeeding."""
    attempts = []
    
    def operation():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("fail")
        return "success"
    
    result = retry_operation(operation)
    
    assert result == "success"
    assert len(attempts) == 3
```

**Flutter (test package):**
```dart
test('retries failed operations 3 times', () async {
  int attempts = 0;
  
  Future<String> operation() async {
    attempts++;
    if (attempts < 3) throw Exception('fail');
    return 'success';
  }
  
  final result = await retryOperation(operation);
  
  expect(result, equals('success'));
  expect(attempts, equals(3));
});
```

Requirements:
- One behavior per test
- Clear descriptive name
- Real code (no mocks unless unavoidable)
- Tests behavior, not implementation

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

**Python:**
```bash
pytest path/to/test_module.py::test_retries_failed_operations_3_times -v
```

**Flutter:**
```bash
flutter test test/retry_test.dart
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

Test passes? You're testing existing behavior. Fix test.

Test errors? Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**Python:**
```python
def retry_operation(fn, max_retries=3):
    """Retry operation up to max_retries times."""
    for i in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if i == max_retries - 1:
                raise
    raise RuntimeError("unreachable")
```

**Flutter:**
```dart
Future<T> retryOperation<T>(Future<T> Function() fn, {int maxRetries = 3}) async {
  for (int i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i == maxRetries - 1) rethrow;
    }
  }
  throw StateError('unreachable');
}
```

Just enough to pass. Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN - Watch It Pass

**MANDATORY.**

**Python:**
```bash
pytest path/to/test_module.py -v
```

**Flutter:**
```bash
flutter test
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

Test fails? Fix code, not test.

Other tests fail? Fix now.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## Good Tests

| Criterion | Good | Bad |
|-----------|------|-----|
| Minimal | One thing. "and" in name? Split it. | `test_validates_email_and_domain_and_whitespace()` |
| Clear | Name describes behavior | `test_1()` |
| Shows intent | Demonstrates desired API | Obscures what code should do |

## Python-Specific Guidance

**Test structure:**
```python
# Arrange
user = User(email="test@example.com")

# Act
result = user.validate()

# Assert
assert result.is_valid is True
assert result.errors == []
```

**Fixtures for setup:**
```python
@pytest.fixture
def sample_user():
    return User(email="test@example.com", age=25)

def test_adult_user(sample_user):
    assert sample_user.is_adult() is True
```

**Parametrize for multiple cases:**
```python
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected
```

## Flutter-Specific Guidance

**Widget tests:**
```dart
testWidgets('LoginButton shows loading spinner when pressed', (tester) async {
  await tester.pumpWidget(MaterialApp(home: LoginButton()));
  
  // Initially shows text
  expect(find.text('Login'), findsOneWidget);
  expect(find.byType(CircularProgressIndicator), findsNothing);
  
  // Tap button
  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();
  
  // Now shows spinner
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

**Golden tests for UI:**
```dart
testWidgets('ProfileCard matches golden', (tester) async {
  await tester.pumpWidget(MaterialApp(
    home: ProfileCard(user: testUser),
  ));
  
  await expectLater(
    find.byType(ProfileCard),
    matchesGoldenFile('profile_card.png'),
  );
});
```

**Mock dependencies with mockito:**
```dart
@GenerateMocks([ApiClient])
void main() {
  test('fetches user data from API', () async {
    final mockClient = MockApiClient();
    when(mockClient.getUser(any))
        .thenAnswer((_) async => User(id: '1', name: 'Alice'));
    
    final service = UserService(mockClient);
    final user = await service.fetchUser('1');
    
    expect(user.name, equals('Alice'));
    verify(mockClient.getUser('1')).called(1);
  });
}
```

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (X more hours, high confidence)
- Keep it and add tests after (30 min, low confidence, likely bugs)

The "waste" is keeping code you can't trust. Working code without real tests is technical debt.

**"Tests after achieve the same goals - it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.

Tests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

Bug: Empty email accepted

**RED**
```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result.error == "Email required"
```

**Verify RED**
```bash
$ pytest test_form.py::test_rejects_empty_email -v
FAILED: AssertionError: assert None == 'Email required'
```

**GREEN**
```python
def submit_form(data):
    if not data.get("email", "").strip():
        return FormResult(error="Email required")
    # ...
```

**Verify GREEN**
```bash
$ pytest test_form.py -v
PASSED
```

**REFACTOR**

Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers/fixtures. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

**Never fix bugs without a test.**

## Testing Anti-Patterns

See [testing-anti-patterns.md](references/testing-anti-patterns.md) to avoid:
- Testing mock behavior instead of real behavior
- Adding test-only methods to production classes
- Mocking without understanding dependencies
- Incomplete mocks that hide structural issues

## Platform-Specific Test Commands

**Python:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user.py

# Run specific test
pytest tests/test_user.py::test_validates_email

# Run with coverage
pytest --cov=src tests/

# Run in watch mode (with pytest-watch)
ptw
```

**Flutter:**
```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/user_test.dart

# Run with coverage
flutter test --coverage

# Run in watch mode
flutter test --watch
```

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
