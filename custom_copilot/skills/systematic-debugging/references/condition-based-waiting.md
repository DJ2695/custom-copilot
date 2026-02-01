# Condition-Based Waiting

Flaky tests often guess at timing with arbitrary delays. This creates race conditions where tests pass on fast machines but fail under load or in CI.

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

## When to Use

Use when:
- Tests have arbitrary delays (`time.sleep()`, `await Future.delayed()`)
- Tests are flaky (pass sometimes, fail under load)
- Tests timeout when run in parallel
- Waiting for async operations to complete

Don't use when:
- Testing actual timing behavior (debounce, throttle intervals)
- Always document WHY if using arbitrary timeout

## Core Pattern

**Python (pytest):**
```python
# ❌ BEFORE: Guessing at timing
import time
time.sleep(0.5)
result = get_result()
assert result is not None

# ✅ AFTER: Waiting for condition
from utils import wait_for

result = wait_for(lambda: get_result())
assert result is not None
```

**Flutter (test package):**
```dart
// ❌ BEFORE: Guessing at timing  
await Future.delayed(Duration(milliseconds: 500));
final result = getResult();
expect(result, isNotNull);

// ✅ AFTER: Waiting for condition
await waitFor(() => getResult() != null);
final result = getResult();
expect(result, isNotNull);
```

## Quick Patterns

| Scenario | Python | Flutter |
|----------|--------|---------|
| Wait for value | `wait_for(lambda: get_value())` | `await waitFor(() => getValue())` |
| Wait for state | `wait_for(lambda: obj.state == 'ready')` | `await waitFor(() => obj.state == State.ready)` |
| Wait for count | `wait_for(lambda: len(items) >= 5)` | `await waitFor(() => items.length >= 5)` |
| Wait for file | `wait_for(lambda: path.exists())` | `await waitFor(() => file.existsSync())` |
| Complex condition | `wait_for(lambda: obj.ready and obj.value > 10)` | `await waitFor(() => obj.ready && obj.value > 10)` |

## Implementation

**Python:**
```python
import time
from typing import Callable, TypeVar, Optional

T = TypeVar('T')

def wait_for(
    condition: Callable[[], Optional[T]],
    description: str = "condition",
    timeout_ms: int = 5000,
    poll_interval_ms: int = 10
) -> T:
    """
    Poll condition until it returns truthy value or timeout.
    
    Args:
        condition: Function that returns truthy value when ready
        description: Human-readable description for error messages
        timeout_ms: Maximum time to wait in milliseconds
        poll_interval_ms: Time between checks in milliseconds
        
    Returns:
        The truthy value returned by condition
        
    Raises:
        TimeoutError: If condition doesn't become truthy within timeout
    """
    start_time = time.time() * 1000
    
    while True:
        result = condition()
        if result:
            return result
            
        elapsed = (time.time() * 1000) - start_time
        if elapsed > timeout_ms:
            raise TimeoutError(
                f"Timeout waiting for {description} after {timeout_ms}ms"
            )
        
        time.sleep(poll_interval_ms / 1000)


# Domain-specific helpers
def wait_for_file(path, timeout_ms=5000):
    """Wait for file to exist."""
    from pathlib import Path
    return wait_for(
        lambda: path if Path(path).exists() else None,
        f"file {path} to exist",
        timeout_ms
    )


def wait_for_state(obj, expected_state, timeout_ms=5000):
    """Wait for object to reach expected state."""
    return wait_for(
        lambda: obj.state if obj.state == expected_state else None,
        f"state to be {expected_state}",
        timeout_ms
    )
```

**Flutter:**
```dart
import 'package:flutter_test/flutter_test.dart';

/// Poll condition until it returns non-null value or timeout.
///
/// Returns the non-null value returned by condition.
/// Throws [TimeoutException] if condition doesn't return non-null within timeout.
Future<T> waitFor<T>(
  T? Function() condition, {
  String description = 'condition',
  Duration timeout = const Duration(seconds: 5),
  Duration pollInterval = const Duration(milliseconds: 10),
}) async {
  final stopwatch = Stopwatch()..start();
  
  while (true) {
    final result = condition();
    if (result != null) {
      return result;
    }
    
    if (stopwatch.elapsed > timeout) {
      throw TimeoutException(
        'Timeout waiting for $description after ${timeout.inMilliseconds}ms',
      );
    }
    
    await Future.delayed(pollInterval);
  }
}

// Domain-specific helpers
Future<void> waitForState<T>(
  ValueNotifier<T> notifier,
  T expectedState, {
  Duration timeout = const Duration(seconds: 5),
}) async {
  await waitFor(
    () => notifier.value == expectedState ? notifier.value : null,
    description: 'state to be $expectedState',
    timeout: timeout,
  );
}

Future<Widget> waitForWidget(
  WidgetTester tester,
  Finder finder, {
  Duration timeout = const Duration(seconds: 5),
}) async {
  return waitFor(
    () {
      tester.binding.scheduleFrame();
      tester.pump(Duration.zero);
      return finder.evaluate().isNotEmpty ? finder.evaluate().first.widget : null;
    },
    description: 'widget ${finder}',
    timeout: timeout,
  );
}
```

## Usage Examples

**Python (pytest):**
```python
def test_async_operation_completes():
    """Test that async operation eventually completes."""
    manager = AsyncManager()
    manager.start_operation()
    
    # Wait for operation to complete
    result = wait_for(
        lambda: manager.get_result() if manager.is_complete else None,
        description="operation to complete",
        timeout_ms=3000
    )
    
    assert result.status == "success"


def test_multiple_items_processed():
    """Test that multiple items are processed."""
    processor = ItemProcessor()
    processor.add_items([1, 2, 3, 4, 5])
    
    # Wait for all items to be processed
    wait_for(
        lambda: len(processor.processed_items) >= 5,
        description="all 5 items to be processed",
        timeout_ms=2000
    )
    
    assert len(processor.processed_items) == 5
```

**Flutter (widget tests):**
```dart
testWidgets('async operation completes', (tester) async {
  await tester.pumpWidget(MyApp());
  
  // Trigger async operation
  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();
  
  // Wait for loading to finish
  await waitFor(
    () => find.byType(CircularProgressIndicator).evaluate().isEmpty 
        ? true 
        : null,
    description: 'loading to finish',
  );
  
  expect(find.text('Success'), findsOneWidget);
});

testWidgets('BLoC state changes', (tester) async {
  final bloc = MyBloc();
  addTearDown(bloc.close);
  
  await tester.pumpWidget(MyApp(bloc: bloc));
  
  bloc.add(LoadDataEvent());
  
  // Wait for BLoC to emit loaded state
  await waitFor(
    () => bloc.state is DataLoaded ? bloc.state : null,
    description: 'BLoC to emit DataLoaded state',
  );
  
  expect(bloc.state, isA<DataLoaded>());
});
```

## Common Mistakes

❌ **Polling too fast:** `poll_interval=1ms` - wastes CPU  
✅ **Fix:** Poll every 10ms (fast enough, not wasteful)

❌ **No timeout:** Loop forever if condition never met  
✅ **Fix:** Always include timeout with clear error

❌ **Stale data:** Cache value before loop  
✅ **Fix:** Call getter inside loop for fresh data

**Python example:**
```python
# ❌ BAD: Cached value
result = manager.get_result()  # Called once
wait_for(lambda: result is not None)  # Always checks same value!

# ✅ GOOD: Fresh value each time
wait_for(lambda: manager.get_result())  # Calls getter each iteration
```

**Flutter example:**
```dart
// ❌ BAD: Cached finder
final widget = find.byType(MyWidget);  // Evaluated once
await waitFor(() => widget.evaluate().isNotEmpty);  // Stale!

// ✅ GOOD: Fresh finder each time
await waitFor(() => find.byType(MyWidget).evaluate().isNotEmpty);
```

## When Arbitrary Timeout IS Correct

Sometimes you DO need to wait for time-based behavior:

**Python:**
```python
# Tool ticks every 100ms - need 2 ticks to verify partial output
wait_for(lambda: manager.started, description="tool started")  # First: condition
time.sleep(0.2)  # Then: wait for timed behavior
# 200ms = 2 ticks at 100ms intervals - documented and justified
```

**Flutter:**
```dart
// Animation duration is 300ms - need to verify mid-animation state
await waitFor(() => controller.isAnimating);  // First: condition
await Future.delayed(Duration(milliseconds: 150));  // Then: wait for timing
// 150ms = halfway through 300ms animation - documented
```

Requirements:
1. First wait for triggering condition
2. Based on known timing (not guessing)
3. Comment explaining WHY

## pytest-specific: Using pytest-timeout

For entire test timeouts:

```python
# In pyproject.toml or pytest.ini
[tool.pytest.ini_options]
timeout = 10  # Fail any test that runs longer than 10 seconds

# Per-test override
@pytest.mark.timeout(30)
def test_slow_operation():
    wait_for(lambda: slow_operation_complete(), timeout_ms=25000)
```

## Flutter-specific: Using pumpAndSettle

For simple widget tests, Flutter provides `pumpAndSettle`:

```dart
// Pumps until no more frames scheduled
await tester.pumpAndSettle();

// Equivalent to:
await waitFor(() {
  tester.pump(Duration.zero);
  return tester.binding.hasScheduledFrame ? null : true;
});

// But pumpAndSettle has built-in timeout and better errors
```

Use `pumpAndSettle()` when:
- Waiting for animations to complete
- No complex conditions to check
- Default behavior is acceptable

Use `waitFor()` when:
- Need to check specific condition
- Need custom timeout
- Need custom error messages

## Real-World Impact

From debugging sessions:
- Fixed 15 flaky tests across 3 files
- Pass rate: 60% → 100%
- Execution time: 40% faster (no conservative delays)
- No more race conditions
