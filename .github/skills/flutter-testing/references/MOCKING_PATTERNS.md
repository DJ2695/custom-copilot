# Mocking Patterns with Mocktail

Comprehensive guide to mocking dependencies in Flutter tests using mocktail.

## Table of Contents

- [Setup](#setup)
- [Basic Mocking](#basic-mocking)
- [When and ThenAnswer](#when-and-thenanswer)
- [Verify](#verify)
- [Argument Matchers](#argument-matchers)
- [Mocking TaskEither](#mocking-taskeither)
- [Mocking Streams](#mocking-streams)
- [Fallback Values](#fallback-values)
- [Advanced Patterns](#advanced-patterns)
- [Common Pitfalls](#common-pitfalls)

## Setup

### Dependencies

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
```

### Why Mocktail?

Mocktail is preferred over Mockito because:
- No code generation required
- Simpler syntax
- Better null safety support
- More intuitive API

## Basic Mocking

### Creating a Mock

```dart
import 'package:mocktail/mocktail.dart';

class MockRepository extends Mock implements FeatureRepository {}

void main() {
  late MockRepository mockRepository;

  setUp(() {
    mockRepository = MockRepository();
  });

  test('example test', () {
    // Use mockRepository
  });
}
```

### Mock Classes, Interfaces, and Abstract Classes

```dart
// Interface
abstract class UserRepository {
  Future<User> getUser(String id);
}

class MockUserRepository extends Mock implements UserRepository {}

// Abstract class
abstract class BaseService {
  Future<void> process();
}

class MockBaseService extends Mock implements BaseService {}

// Concrete class
class ApiClient {
  Future<Response> get(String url);
}

class MockApiClient extends Mock implements ApiClient {}
```

## When and ThenAnswer

### Basic When/ThenAnswer

```dart
test('mocks method return value', () {
  final mockRepo = MockRepository();

  // When method is called, return this value
  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData);

  // Call method
  final result = await mockRepo.getData('id');

  expect(result, testData);
});
```

### Synchronous Returns with thenReturn

```dart
test('uses thenReturn for synchronous values', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getCount()).thenReturn(5);

  expect(mockRepo.getCount(), 5);
});
```

### Async Returns with thenAnswer

```dart
test('uses thenAnswer for async values', () async {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData);

  final result = await mockRepo.getData('id');
  expect(result, testData);
});
```

### Delayed Responses

```dart
test('simulates network delay', () async {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id')).thenAnswer((_) async {
    await Future.delayed(const Duration(milliseconds: 100));
    return testData;
  });

  final result = await mockRepo.getData('id');
  expect(result, testData);
});
```

### Throwing Exceptions

```dart
test('throws exception', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenThrow(Exception('Network error'));

  expect(
    () => mockRepo.getData('id'),
    throwsA(isA<Exception>()),
  );
});
```

### Multiple Calls with Different Returns

```dart
test('returns different values on sequential calls', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getCount())
      .thenReturn(1)
      .thenReturn(2)
      .thenReturn(3);

  expect(mockRepo.getCount(), 1);
  expect(mockRepo.getCount(), 2);
  expect(mockRepo.getCount(), 3);
});
```

## Verify

### Basic Verification

```dart
test('verifies method was called', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData);

  mockRepo.getData('id');

  verify(() => mockRepo.getData('id')).called(1);
});
```

### Verify Call Count

```dart
test('verifies method called specific times', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData(any()))
      .thenAnswer((_) async => testData);

  mockRepo.getData('id1');
  mockRepo.getData('id2');
  mockRepo.getData('id3');

  verify(() => mockRepo.getData(any())).called(3);
});
```

### Verify Never Called

```dart
test('verifies method was never called', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData(any()))
      .thenAnswer((_) async => testData);

  // Don't call the method

  verifyNever(() => mockRepo.getData(any()));
});
```

### Verify Call Order

```dart
test('verifies call order', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData(any()))
      .thenAnswer((_) async => testData);

  mockRepo.getData('first');
  mockRepo.getData('second');

  verifyInOrder([
    () => mockRepo.getData('first'),
    () => mockRepo.getData('second'),
  ]);
});
```

### Verify No More Interactions

```dart
test('verifies no other interactions', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData);

  mockRepo.getData('id');

  verify(() => mockRepo.getData('id')).called(1);
  verifyNoMoreInteractions(mockRepo);
});
```

## Argument Matchers

### Any Matcher

```dart
test('matches any argument', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData(any()))
      .thenAnswer((_) async => testData);

  await mockRepo.getData('any-id');

  verify(() => mockRepo.getData(any())).called(1);
});
```

### Any Named Arguments

```dart
test('matches any named argument', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData(
        id: any(named: 'id'),
        includeDeleted: any(named: 'includeDeleted'),
      )).thenAnswer((_) async => testData);

  await mockRepo.getData(id: 'test', includeDeleted: false);

  verify(() => mockRepo.getData(
        id: any(named: 'id'),
        includeDeleted: any(named: 'includeDeleted'),
      )).called(1);
});
```

### Capturing Arguments

```dart
test('captures arguments', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.saveData(any()))
      .thenAnswer((_) async => unit);

  mockRepo.saveData(testData);

  final captured = verify(() => mockRepo.saveData(captureAny()))
      .captured;

  expect(captured.single, testData);
});
```

### Capturing Multiple Calls

```dart
test('captures multiple arguments', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.saveData(any()))
      .thenAnswer((_) async => unit);

  mockRepo.saveData(data1);
  mockRepo.saveData(data2);

  final captured = verify(() => mockRepo.saveData(captureAny()))
      .captured;

  expect(captured, [data1, data2]);
});
```

### Custom Matchers

```dart
test('uses custom matcher', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.searchUsers(
        query: any(
          named: 'query',
          that: startsWith('test'),
        ),
      )).thenAnswer((_) async => testUsers);

  await mockRepo.searchUsers(query: 'test-query');

  verify(() => mockRepo.searchUsers(
        query: any(
          named: 'query',
          that: startsWith('test'),
        ),
      )).called(1);
});
```

## Mocking TaskEither

### Success Case (Right)

```dart
test('mocks TaskEither success', () async {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) => TaskEither.right(testData));

  final result = await mockRepo.getData('id').run();

  expect(result.isRight(), isTrue);
  result.fold(
    (l) => fail('Should be right'),
    (r) => expect(r, testData),
  );
});
```

### Failure Case (Left)

```dart
test('mocks TaskEither failure', () async {
  final mockRepo = MockRepository();
  final testFailure = const FeatureFailure.serverError('Error');

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) => TaskEither.left(testFailure));

  final result = await mockRepo.getData('id').run();

  expect(result.isLeft(), isTrue);
  result.fold(
    (l) => expect(l, testFailure),
    (r) => fail('Should be left'),
  );
});
```

### Complex TaskEither Chain

```dart
test('mocks TaskEither chain', () async {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) => TaskEither.right(rawData));

  when(() => mockRepo.transform(any()))
      .thenAnswer((_) => TaskEither.right(transformedData));

  final result = await mockRepo
      .getData('id')
      .flatMap((data) => mockRepo.transform(data))
      .run();

  expect(result.isRight(), isTrue);
});
```

## Mocking Streams

### Simple Stream

```dart
test('mocks stream', () async {
  final mockCubit = MockFeatureCubit();
  final controller = StreamController<FeatureState>();

  when(() => mockCubit.stream).thenAnswer((_) => controller.stream);

  controller.add(const FeatureState(status: Status.loading));

  final state = await mockCubit.stream.first;
  expect(state.status, Status.loading);

  controller.close();
});
```

### Empty Stream

```dart
test('mocks empty stream', () {
  final mockCubit = MockFeatureCubit();

  when(() => mockCubit.stream).thenAnswer((_) => const Stream.empty());

  expect(mockCubit.stream, emits(isEmpty));
});
```

### Stream with Multiple Values

```dart
test('mocks stream with multiple values', () async {
  final mockCubit = MockFeatureCubit();

  when(() => mockCubit.stream).thenAnswer((_) => Stream.fromIterable([
        const FeatureState(status: Status.initial),
        const FeatureState(status: Status.loading),
        const FeatureState(status: Status.loaded),
      ]));

  final states = await mockCubit.stream.toList();

  expect(states.length, 3);
  expect(states[0].status, Status.initial);
  expect(states[1].status, Status.loading);
  expect(states[2].status, Status.loaded);
});
```

### Stream with Delays

```dart
test('mocks stream with delays', () async {
  final mockCubit = MockFeatureCubit();

  when(() => mockCubit.stream).thenAnswer((_) => Stream.periodic(
        const Duration(milliseconds: 100),
        (i) => FeatureState(count: i),
      ).take(3));

  await expectLater(
    mockCubit.stream,
    emitsInOrder([
      isA<FeatureState>().having((s) => s.count, 'count', 0),
      isA<FeatureState>().having((s) => s.count, 'count', 1),
      isA<FeatureState>().having((s) => s.count, 'count', 2),
    ]),
  );
});
```

## Fallback Values

### Register Fallback Value

When using `any()` with custom types, you must register a fallback:

```dart
class FakeFeature extends Fake implements Feature {}

void main() {
  setUpAll(() {
    registerFallbackValue(FakeFeature());
  });

  test('uses fallback value', () {
    final mockRepo = MockRepository();

    when(() => mockRepo.saveFeature(any()))
        .thenAnswer((_) async => unit);

    mockRepo.saveFeature(Feature(id: '1', name: 'Test'));

    verify(() => mockRepo.saveFeature(any())).called(1);
  });
}
```

### Multiple Fallback Values

```dart
class FakeFeature extends Fake implements Feature {}
class FakeUser extends Fake implements User {}

void main() {
  setUpAll(() {
    registerFallbackValue(FakeFeature());
    registerFallbackValue(FakeUser());
  });

  test('uses multiple fallback values', () {
    final mockRepo = MockRepository();

    when(() => mockRepo.linkFeatureToUser(any(), any()))
        .thenAnswer((_) async => unit);

    mockRepo.linkFeatureToUser(testFeature, testUser);

    verify(() => mockRepo.linkFeatureToUser(any(), any())).called(1);
  });
}
```

## Advanced Patterns

### Conditional Mocking

```dart
test('returns different values based on input', () async {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('valid'))
      .thenAnswer((_) => TaskEither.right(testData));

  when(() => mockRepo.getData('invalid'))
      .thenAnswer((_) => TaskEither.left(
        const FeatureFailure.notFound(),
      ));

  final validResult = await mockRepo.getData('valid').run();
  expect(validResult.isRight(), isTrue);

  final invalidResult = await mockRepo.getData('invalid').run();
  expect(invalidResult.isLeft(), isTrue);
});
```

### Mocking Getters

```dart
test('mocks getter', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.isConnected).thenReturn(true);

  expect(mockRepo.isConnected, isTrue);
});
```

### Mocking Setters

```dart
test('mocks setter', () {
  final mockRepo = MockRepository();

  mockRepo.setting = 'value';

  verify(() => mockRepo.setting = 'value').called(1);
});
```

### Reset Mocks

```dart
test('resets mock between tests', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getCount()).thenReturn(5);
  expect(mockRepo.getCount(), 5);

  reset(mockRepo);

  // Mock is now reset, no behavior defined
  expect(() => mockRepo.getCount(), throwsNoSuchMethodError);
});
```

### Stub Nothing

```dart
test('stubs method to do nothing', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.logEvent(any())).thenReturn(null);

  // This won't throw
  mockRepo.logEvent('test-event');

  verify(() => mockRepo.logEvent('test-event')).called(1);
});
```

## Common Pitfalls

### 1. Not Registering Fallback Values

**Problem:**
```dart
test('fails without fallback', () {
  final mockRepo = MockRepository();

  // This will throw: Bad state: No fallback value
  when(() => mockRepo.saveFeature(any()))
      .thenAnswer((_) async => unit);
});
```

**Solution:**
```dart
setUpAll(() {
  registerFallbackValue(FakeFeature());
});
```

### 2. Using When After Act

**Problem:**
```dart
test('wrong order', () {
  final mockRepo = MockRepository();

  mockRepo.getData('id'); // Called before when()

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData); // Too late!
});
```

**Solution:**
```dart
test('correct order', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData);

  mockRepo.getData('id'); // Now it works
});
```

### 3. Forgetting to Use ThenAnswer for Futures

**Problem:**
```dart
test('wrong return type', () {
  final mockRepo = MockRepository();

  // getData returns Future<Data>, not Data
  when(() => mockRepo.getData('id')).thenReturn(testData); // Wrong!
});
```

**Solution:**
```dart
test('correct return type', () {
  final mockRepo = MockRepository();

  when(() => mockRepo.getData('id'))
      .thenAnswer((_) async => testData); // Correct
});
```

### 4. Not Closing Streams

**Problem:**
```dart
test('leaks stream', () {
  final controller = StreamController<State>();

  when(() => mockCubit.stream).thenAnswer((_) => controller.stream);

  // Test code...

  // Forgot to close!
});
```

**Solution:**
```dart
test('closes stream', () {
  final controller = StreamController<State>();

  when(() => mockCubit.stream).thenAnswer((_) => controller.stream);

  // Test code...

  controller.close(); // Don't forget!
});
```

### 5. Verifying Before Method Call

**Problem:**
```dart
test('verifies too early', () {
  final mockRepo = MockRepository();

  verify(() => mockRepo.getData('id')).called(1); // Nothing called yet!

  mockRepo.getData('id');
});
```

**Solution:**
```dart
test('verifies after call', () {
  final mockRepo = MockRepository();

  mockRepo.getData('id');

  verify(() => mockRepo.getData('id')).called(1); // Correct order
});
```

## Best Practices

1. **Use `setUpAll` for fallback values**
   - Register once for all tests in a group

2. **Use `setUp` for mock creation**
   - Creates fresh mocks for each test

3. **Always use `thenAnswer` for async returns**
   - Use `(_) async =>` for Futures

4. **Verify important interactions**
   - Ensure methods were called with correct arguments

5. **Don't over-verify**
   - Only verify what's important to the test

6. **Use `any()` wisely**
   - Be specific when argument values matter

7. **Clean up resources**
   - Close streams, controllers, etc.

8. **Reset mocks when needed**
   - Use `reset()` for fresh state

9. **Use descriptive mock names**
   - `mockUserRepository` not `mock1`

10. **Group related tests**
    - Share setup code in `setUp` blocks
