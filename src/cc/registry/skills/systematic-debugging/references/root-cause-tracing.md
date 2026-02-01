# Root Cause Tracing

Bugs often manifest deep in the call stack (function called with wrong parameters, file created in wrong location, database opened with wrong path). Your instinct is to fix where the error appears, but that's treating a symptom.

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

## When to Use

Use when:
- Error happens deep in execution (not at entry point)
- Stack trace shows long call chain
- Unclear where invalid data originated
- Need to find which test/code triggers the problem

## The Tracing Process

### 1. Observe the Symptom

**Python:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/tmp//config.json'
#                                                            ^^
#                                                        Double slash!
```

**Flutter:**
```
Exception: Bad state: Cannot add events to a closed stream
#0      StreamController.add (dart:async/stream_controller.dart:867)
#1      UserBloc._onAddUser (package:app/blocs/user_bloc.dart:45)
```

### 2. Find Immediate Cause

What code directly causes this?

**Python:**
```python
with open(f"{base_dir}/{filename}", 'r') as f:  # Line causing error
    config = json.load(f)
```

**Flutter:**
```dart
void _onAddUser(AddUserEvent event, Emitter<UserState> emit) {
  _streamController.add(event.user);  // Line causing error
}
```

### 3. Ask: What Called This?

**Python:**
```python
load_config(base_dir, filename)
  ← called by setup_environment()
  ← called by initialize_app()
  ← called by main()
  ← called by test_app_initialization()
```

**Flutter:**
```dart
UserBloc._onAddUser()
  ← called by Bloc.add()
  ← called by widget.onPressed()
  ← called by user tap
  ← in test: await tester.tap()
```

### 4. Keep Tracing Up

What value was passed?

**Python:**
```python
# base_dir = '' (empty string!)
# f"{base_dir}/{filename}" = '/config.json'
# Should be: '/tmp/config.json'

# Where did empty string come from?
setup_environment(config_dir='')  # Empty string passed!
```

**Flutter:**
```dart
// _streamController already closed!
// When was it closed?
// Who called close() before this event?

// Trace shows:
// - Widget disposed
// - BLoC.close() called  
// - Then event still added
```

### 5. Find Original Trigger

Where did the bad value originate?

**Python:**
```python
# In test setup
@pytest.fixture
def app_config():
    return {"config_dir": ""}  # Empty string set here!
    
# Should be:
@pytest.fixture
def app_config(tmp_path):
    return {"config_dir": str(tmp_path)}
```

**Flutter:**
```dart
// In widget test
tearDown(() {
  bloc.close();  // Closed too early!
});

testWidgets('adds user', (tester) async {
  // Test continues after tearDown already scheduled
  await tester.pump();
  bloc.add(AddUserEvent(user));  // Tries to add after close
});
```

## Adding Stack Traces

When you can't trace manually, add instrumentation:

**Python:**
```python
import traceback

def load_config(base_dir: str, filename: str):
    """Load configuration file."""
    # Add diagnostic logging
    print(f"DEBUG load_config called:")
    print(f"  base_dir: {base_dir!r}")
    print(f"  filename: {filename!r}")
    print(f"  cwd: {os.getcwd()}")
    print(f"  Stack trace:")
    traceback.print_stack()
    
    with open(f"{base_dir}/{filename}", 'r') as f:
        return json.load(f)
```

**Flutter:**
```dart
void _onAddUser(AddUserEvent event, Emitter<UserState> emit) {
  // Add diagnostic logging
  debugPrint('DEBUG _onAddUser called:');
  debugPrint('  event: $event');
  debugPrint('  isClosed: ${isClosed}');
  debugPrint('  state: $state');
  debugPrint('  Stack trace:');
  debugPrint(StackTrace.current.toString());
  
  _streamController.add(event.user);
}
```

**Critical:** Use direct output in tests:
- Python: `print()` not logger (logger may be suppressed)
- Flutter: `debugPrint()` appears in test output

**Run and capture:**

**Python:**
```bash
pytest tests/test_app.py -s 2>&1 | grep 'DEBUG load_config'
```

**Flutter:**
```bash
flutter test test/user_bloc_test.dart 2>&1 | grep 'DEBUG _onAddUser'
```

**Analyze stack traces:**
- Look for test file names
- Find the line number triggering the call
- Identify the pattern (same test? same parameter?)

## Finding Which Test Causes Pollution

If something appears during tests but you don't know which test:

**Python:**
```python
# Run tests one at a time
pytest tests/ --collect-only | grep "test_" | while read test; do
    echo "Testing: $test"
    pytest "$test"
    if [ -f "/tmp/unexpected_file" ]; then
        echo "FOUND POLLUTER: $test"
        exit 0
    fi
done
```

**Flutter:**
```bash
# Run tests individually
flutter test --plain-name "" | grep "test.*dart" | while read file; do
    echo "Testing: $file"
    flutter test "$file"
    # Check for pollution
    if [ -d "build/test_pollution" ]; then
        echo "FOUND POLLUTER: $file"
        exit 0
    fi
done
```

## Real Example: Empty Base Directory

**Python:**

Symptom: Files created in `/` (root directory) instead of temp directory

Trace chain:
1. `open(f"{base_dir}/{filename}")` resolves to `/{filename}` ← empty base_dir
2. `setup_environment(config_dir)` called with empty string
3. `initialize_app(config)` passed `{"config_dir": ""}`
4. Test fixture returns `{"config_dir": ""}` initially
5. `tmp_path` fixture not used

Root cause: Test fixture not using pytest's `tmp_path`

Fix at source:
```python
@pytest.fixture
def app_config(tmp_path):
    # Now uses temporary directory
    return {"config_dir": str(tmp_path)}
```

Also add defense-in-depth:
- Layer 1: Validate base_dir not empty in `load_config()`
- Layer 2: Assert base_dir exists in `setup_environment()`
- Layer 3: Test validates temp directory used

**Flutter:**

Symptom: "Bad state: Cannot add events to closed stream"

Trace chain:
1. `_streamController.add()` called on closed controller
2. `_onAddUser()` triggered after bloc closed
3. Widget test calls `bloc.add()` after dispose
4. `tearDown()` closes bloc before test completes
5. `tester.pump()` triggers pending events

Root cause: Test lifecycle issue - bloc closed too early

Fix at source:
```dart
// Use addTearDown instead of tearDown
testWidgets('adds user', (tester) async {
  final bloc = UserBloc();
  addTearDown(bloc.close);  // Closes after test actually completes
  
  await tester.pumpWidget(MyApp(bloc: bloc));
  bloc.add(AddUserEvent(user));
  await tester.pump();
});
```

Also add defense-in-depth:
- Layer 1: Check `isClosed` before adding events
- Layer 2: Emit error state instead of crashing
- Layer 3: Widget checks bloc state before dispatching

## Key Principle

**NEVER fix just where the error appears. Trace back to find the original trigger.**

The symptom is rarely the cause:
- Empty string in path → Root cause: fixture not initialized
- Closed stream error → Root cause: lifecycle management
- Wrong directory → Root cause: variable scope issue

Always trace up to the source and fix there.

## Stack Trace Tips

**Python:**
- Use `traceback.print_stack()` before dangerous operation
- Include context: paths, cwd, environment variables
- Capture with `pytest -s` to see output
- Use `logging.debug()` for persistent traces

**Flutter:**
- Use `debugPrint(StackTrace.current.toString())` 
- Include context: widget state, stream status, bloc state
- Capture with `flutter test` (shows debugPrint by default)
- Use `debugPrintStack()` for current stack trace

## Real-World Impact

From debugging sessions:
- Found root cause through 5-level trace
- Fixed at source (parameter validation)
- Added 3-4 layers of defense
- All tests passed, zero pollution
