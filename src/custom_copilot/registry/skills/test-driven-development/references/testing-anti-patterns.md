# Testing Anti-Patterns

Load this reference when: writing or changing tests, adding mocks, or tempted to add test-only methods to production code.

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

Following strict TDD prevents these anti-patterns.

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**

**Python:**
```python
# ❌ BAD: Testing that the mock exists
def test_renders_sidebar(mocker):
    mock_sidebar = mocker.patch('app.Sidebar')
    page = Page()
    
    # Testing the mock, not the behavior!
    mock_sidebar.assert_called_once()
```

**Flutter:**
```dart
// ❌ BAD: Testing mock was called
test('renders sidebar', () {
  final mockSidebar = MockSidebar();
  final page = Page(sidebar: mockSidebar);
  
  // Testing mock behavior, not Page behavior!
  verify(mockSidebar.render()).called(1);
});
```

**Why this is wrong:**
- You're verifying the mock works, not that the component works
- Test passes when mock is present, fails when it's not
- Tells you nothing about real behavior

**The fix:**

**Python:**
```python
# ✅ GOOD: Test real component or don't mock it
def test_renders_sidebar():
    page = Page()  # Don't mock sidebar
    assert page.has_navigation()
    
# OR if sidebar must be mocked for isolation:
# Don't assert on the mock - test Page's behavior with sidebar present
```

**Flutter:**
```dart
// ✅ GOOD: Test real widget
testWidgets('renders sidebar', (tester) async {
  await tester.pumpWidget(MaterialApp(home: Page()));
  expect(find.byType(Sidebar), findsOneWidget);
});
```

### Gate Function

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

## Anti-Pattern 2: Test-Only Methods in Production

**The violation:**

**Python:**
```python
# ❌ BAD: destroy() only used in tests
class Session:
    def destroy(self):  # Looks like production API!
        if self._workspace_manager:
            self._workspace_manager.destroy_workspace(self.id)
        # ... cleanup

# In tests
@pytest.fixture
def session():
    s = Session()
    yield s
    s.destroy()  # Test-only usage
```

**Flutter:**
```dart
// ❌ BAD: resetForTesting() only in tests
class UserService {
  static UserService? _instance;
  
  // Test-only method in production class!
  void resetForTesting() {
    _instance = null;
  }
}

// In tests
tearDown(() {
  UserService().resetForTesting();
});
```

**Why this is wrong:**
- Production class polluted with test-only code
- Dangerous if accidentally called in production
- Violates YAGNI and separation of concerns

**The fix:**

**Python:**
```python
# ✅ GOOD: Test utilities handle test cleanup
# Session has no destroy() - it's stateless in production

# In tests/conftest.py
@pytest.fixture
def session():
    s = Session()
    yield s
    # Cleanup handled by test infrastructure
    workspace_manager.destroy_workspace(s.workspace_id)
```

**Flutter:**
```dart
// ✅ GOOD: Test setup handles cleanup
class UserServiceTestHelper {
  static void reset() {
    UserService.instance = null;
  }
}

// In tests
tearDown(() {
  UserServiceTestHelper.reset();
});
```

### Gate Function

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**

**Python:**
```python
# ❌ BAD: Mock breaks test logic
def test_detects_duplicate_server(mocker):
    # Mock prevents config write that test depends on!
    mocker.patch('catalog.discover_and_cache_tools', return_value=None)
    
    add_server(config)
    add_server(config)  # Should throw - but won't!
```

**Flutter:**
```dart
// ❌ BAD: Over-mocking breaks behavior
test('detects duplicate user', () async {
  // Mock prevents state change test depends on
  when(mockUserRepo.addUser(any))
      .thenAnswer((_) async => null);
  
  await userService.addUser(user);
  await userService.addUser(user);  // Should throw!
});
```

**Why this is wrong:**
- Mocked method had side effect test depended on
- Over-mocking to "be safe" breaks actual behavior
- Test passes for wrong reason or fails mysteriously

**The fix:**

**Python:**
```python
# ✅ GOOD: Mock at correct level
def test_detects_duplicate_server(mocker):
    # Mock the slow part, preserve behavior test needs
    mocker.patch('server_manager.start_server')
    
    add_server(config)  # Config written
    with pytest.raises(DuplicateServerError):
        add_server(config)  # Duplicate detected ✓
```

**Flutter:**
```dart
// ✅ GOOD: Mock only external dependencies
test('detects duplicate user', () async {
  final repo = InMemoryUserRepo();  // Use real test repo
  final service = UserService(repo);
  
  await service.addUser(user);
  expect(
    () => service.addUser(user),
    throwsA(isA<DuplicateUserError>()),
  );
});
```

### Gate Function

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## Anti-Pattern 4: Incomplete Mocks

**The violation:**

**Python:**
```python
# ❌ BAD: Partial mock - only fields you think you need
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"}
    # Missing: metadata that downstream code uses
}

# Later: breaks when code accesses response["metadata"]["request_id"]
```

**Flutter:**
```dart
// ❌ BAD: Incomplete mock
final mockUser = User(
  id: '1',
  name: 'Alice',
  // Missing: email, createdAt that widgets display
);
```

**Why this is wrong:**
- Partial mocks hide structural assumptions
- Downstream code may depend on fields you didn't include
- Tests pass but integration fails
- False confidence

**The Iron Rule:** Mock the COMPLETE data structure as it exists in reality, not just fields your immediate test uses.

**The fix:**

**Python:**
```python
# ✅ GOOD: Mirror real API completeness
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"},
    "metadata": {"request_id": "req-789", "timestamp": 1234567890}
    # All fields real API returns
}
```

**Flutter:**
```dart
// ✅ GOOD: Complete test data
final mockUser = User(
  id: '1',
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: DateTime(2024, 1, 1),
  role: UserRole.member,
  // All fields real User has
);
```

### Gate Function

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## Anti-Pattern 5: Integration Tests as Afterthought

**The violation:**

```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**Why this is wrong:**
- Testing is part of implementation, not optional follow-up
- TDD would have caught this
- Can't claim complete without tests

**The fix:**

```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## When Mocks Become Too Complex

**Warning signs:**
- Mock setup longer than test logic
- Mocking everything to make test pass
- Mocks missing methods real components have
- Test breaks when mock changes

**Consider:** Integration tests with real components often simpler than complex mocks

**Python:**
```python
# ❌ Complex mocking
def test_user_workflow(mocker):
    mock_db = mocker.MagicMock()
    mock_cache = mocker.MagicMock()
    mock_email = mocker.MagicMock()
    # ... 20 lines of mock setup
    
# ✅ Use test database
def test_user_workflow(test_db):
    # Much simpler with real test database
    user = User.create(email="test@example.com")
    assert user.is_verified()
```

**Flutter:**
```dart
// ❌ Over-mocked widget test
testWidgets('complex workflow', (tester) async {
  final mockA = MockServiceA();
  final mockB = MockServiceB();
  final mockC = MockServiceC();
  // ... complex mock setup
  
// ✅ Integration test with real providers
testWidgets('complex workflow', (tester) async {
  await tester.pumpWidget(
    MaterialApp(home: WorkflowScreen()),
  );
  // Test actual behavior
});
```

## TDD Prevents These Anti-Patterns

**Why TDD helps:**

1. **Write test first** → Forces you to think about what you're actually testing
2. **Watch it fail** → Confirms test tests real behavior, not mocks
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies** → You see what the test actually needs before mocking

If you're testing mock behavior, you violated TDD - you added mocks without watching test fail against real code first.

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on mock elements | Test real component or unmock it |
| Test-only methods in production | Move to test utilities |
| Mock without understanding | Understand dependencies first, mock minimally |
| Incomplete mocks | Mirror real API completely |
| Tests as afterthought | TDD - tests first |
| Over-complex mocks | Consider integration tests |

## Red Flags

- Assertion checks for mock behavior
- Methods only called in test files
- Mock setup is >50% of test
- Test fails when you remove mock
- Can't explain why mock is needed
- Mocking "just to be safe"

## The Bottom Line

Mocks are tools to isolate, not things to test.

If TDD reveals you're testing mock behavior, you've gone wrong.

Fix: Test real behavior or question why you're mocking at all.
