# Advanced Testing Patterns

Advanced Flutter testing techniques including golden tests, performance testing, custom matchers, and test utilities.

## Table of Contents

- [Golden Tests](#golden-tests)
- [Performance Testing](#performance-testing)
- [Custom Matchers](#custom-matchers)
- [Test Helpers](#test-helpers)
- [Parameterized Tests](#parameterized-tests)
- [Test Coverage](#test-coverage)
- [CI/CD Integration](#cicd-integration)

## Golden Tests

Golden tests (screenshot tests) verify UI renders correctly by comparing against baseline images.

### Basic Golden Test

```dart
testWidgets('golden test for button', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ElevatedButton(
          onPressed: () {},
          child: const Text('Click Me'),
        ),
      ),
    ),
  );

  await expectLater(
    find.byType(ElevatedButton),
    matchesGoldenFile('goldens/button.png'),
  );
});
```

### Golden Test with Different States

```dart
group('Card golden tests', () {
  testWidgets('default state', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ProductCard(
            title: 'Product',
            price: 99.99,
          ),
        ),
      ),
    );

    await expectLater(
      find.byType(ProductCard),
      matchesGoldenFile('goldens/product_card_default.png'),
    );
  });

  testWidgets('loading state', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ProductCard(
            title: 'Product',
            price: 99.99,
            isLoading: true,
          ),
        ),
      ),
    );

    await expectLater(
      find.byType(ProductCard),
      matchesGoldenFile('goldens/product_card_loading.png'),
    );
  });

  testWidgets('error state', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ProductCard(
            title: 'Product',
            price: 99.99,
            error: 'Failed to load',
          ),
        ),
      ),
    );

    await expectLater(
      find.byType(ProductCard),
      matchesGoldenFile('goldens/product_card_error.png'),
    );
  });
});
```

### Golden Test for Full Screen

```dart
testWidgets('home page golden test', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  await expectLater(
    find.byType(HomePage),
    matchesGoldenFile('goldens/home_page.png'),
  );
});
```

### Golden Test with Theme Variants

```dart
void main() {
  testWidgets('card with light theme', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData.light(),
        home: const Scaffold(body: MyCard()),
      ),
    );

    await expectLater(
      find.byType(MyCard),
      matchesGoldenFile('goldens/card_light.png'),
    );
  });

  testWidgets('card with dark theme', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData.dark(),
        home: const Scaffold(body: MyCard()),
      ),
    );

    await expectLater(
      find.byType(MyCard),
      matchesGoldenFile('goldens/card_dark.png'),
    );
  });
}
```

### Updating Golden Files

```bash
# Generate/update golden files
flutter test --update-goldens

# Test with specific path
flutter test --update-goldens test/goldens/
```

### Platform-Specific Goldens

```dart
testWidgets('button golden test', (tester) async {
  await tester.pumpWidget(const MyButton());

  final platform = debugDefaultTargetPlatformOverride?.name ?? 'default';
  
  await expectLater(
    find.byType(MyButton),
    matchesGoldenFile('goldens/button_$platform.png'),
  );
});
```

## Performance Testing

### Frame Timing

```dart
testWidgets('animation performance', (tester) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  await tester.pumpWidget(const MyApp());

  final timeline = await binding.watchPerformance(() async {
    await tester.tap(find.text('Animate'));
    await tester.pumpAndSettle();
  });

  final summary = TimelineSummary.summarize(timeline);
  
  // Check 90th percentile frame build time is under 16ms (60fps)
  expect(summary.computePercentileFrameBuildTimeMillis(90), lessThan(16.0));
});
```

### Scroll Performance

```dart
testWidgets('list scrolling performance', (tester) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  await tester.pumpWidget(const MyApp());

  await binding.traceAction(
    () async {
      await tester.fling(
        find.byType(ListView),
        const Offset(0, -300),
        1000,
      );
      await tester.pumpAndSettle();
    },
    reportKey: 'scrolling_performance',
  );
});
```

### Memory Profiling

```dart
import 'package:flutter_driver/flutter_driver.dart';
import 'package:test/test.dart';

void main() {
  late FlutterDriver driver;

  setUpAll(() async {
    driver = await FlutterDriver.connect();
  });

  tearDownAll(() async {
    await driver.close();
  });

  test('memory usage stays reasonable', () async {
    // Navigate through app
    await driver.tap(find.byValueKey('list_button'));
    await driver.waitFor(find.byType('ListView'));

    // Get memory info
    final memoryInfo = await driver.getMemoryStats();
    
    // Check memory usage
    expect(memoryInfo['current'], lessThan(200 * 1024 * 1024)); // 200MB
  });
}
```

### CPU Profiling

```dart
testWidgets('CPU usage during complex operation', (tester) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  await tester.pumpWidget(const MyApp());

  final timeline = await binding.traceAction(
    () async {
      await tester.tap(find.text('Process Data'));
      await tester.pumpAndSettle();
    },
    reportKey: 'cpu_usage',
  );

  final summary = TimelineSummary.summarize(timeline);
  
  // Verify no frame drops
  expect(summary.countFrames(), greaterThan(0));
});
```

## Custom Matchers

### Custom Widget Matcher

```dart
Matcher hasTextStyle(TextStyle style) {
  return isA<Text>().having(
    (text) => text.style,
    'text style',
    style,
  );
}

// Usage
test('text has correct style', () {
  final widget = Text('Hello', style: TextStyle(fontSize: 20));
  expect(widget, hasTextStyle(TextStyle(fontSize: 20)));
});
```

### Custom State Matcher

```dart
Matcher hasStatus(Status status) {
  return isA<FeatureState>().having(
    (state) => state.status,
    'status',
    status,
  );
}

Matcher hasData<T>(T data) {
  return isA<FeatureState>().having(
    (state) => state.data,
    'data',
    data,
  );
}

// Usage
blocTest<FeatureCubit, FeatureState>(
  'loads data',
  build: () => cubit,
  act: (cubit) => cubit.load(),
  expect: () => [
    hasStatus(Status.loading),
    hasStatus(Status.loaded),
  ],
);
```

### Custom List Matcher

```dart
Matcher containsInOrder<T>(List<T> expected) {
  return predicate<List<T>>((actual) {
    if (actual.length < expected.length) return false;
    
    int expectedIndex = 0;
    for (final item in actual) {
      if (item == expected[expectedIndex]) {
        expectedIndex++;
        if (expectedIndex == expected.length) return true;
      }
    }
    return false;
  }, 'contains items in order: $expected');
}

// Usage
test('list contains items in order', () {
  final list = [1, 2, 3, 4, 5];
  expect(list, containsInOrder([2, 4]));
});
```

### Custom Async Matcher

```dart
Matcher completesWithin(Duration duration) {
  return completion(predicate(
    (_) => true,
    'completes within $duration',
  )).timeout(duration);
}

// Usage
test('future completes quickly', () async {
  final future = fetchData();
  await expectLater(
    future,
    completesWithin(const Duration(seconds: 2)),
  );
});
```

## Test Helpers

### Widget Test Helper

```dart
class WidgetTestHelper {
  const WidgetTestHelper(this.tester);
  
  final WidgetTester tester;

  Future<void> pumpApp(Widget widget) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(body: widget),
      ),
    );
    await tester.pumpAndSettle();
  }

  Future<void> enterTextAndSubmit(String key, String text) async {
    await tester.enterText(find.byKey(Key(key)), text);
    await tester.testTextInput.receiveAction(TextInputAction.done);
    await tester.pumpAndSettle();
  }

  Future<void> tapAndSettle(Finder finder) async {
    await tester.tap(finder);
    await tester.pumpAndSettle();
  }

  Future<void> scrollToBottom(Finder scrollable) async {
    await tester.drag(scrollable, const Offset(0, -500));
    await tester.pumpAndSettle();
  }
}

// Usage
testWidgets('using helper', (tester) async {
  final helper = WidgetTestHelper(tester);
  
  await helper.pumpApp(const MyWidget());
  await helper.enterTextAndSubmit('email', 'test@example.com');
  await helper.tapAndSettle(find.text('Submit'));
});
```

### BLoC Test Helper

```dart
class BlocTestHelper {
  static Future<void> testSuccessFlow<B extends BlocBase<S>, S>({
    required B Function() build,
    required void Function(B) act,
    required List<S> expectedStates,
  }) async {
    await blocTest<B, S>(
      'success flow',
      build: build,
      act: act,
      expect: () => expectedStates,
    );
  }

  static Future<void> testErrorFlow<B extends BlocBase<S>, S>({
    required B Function() build,
    required void Function(B) act,
    required Matcher errorMatcher,
  }) async {
    await blocTest<B, S>(
      'error flow',
      build: build,
      act: act,
      expect: () => [errorMatcher],
    );
  }
}
```

### Mock Data Builder

```dart
class TestDataBuilder {
  static User buildUser({
    String? id,
    String? email,
    String? name,
  }) {
    return User(
      id: id ?? 'test-id',
      email: email ?? 'test@example.com',
      name: name ?? 'Test User',
    );
  }

  static List<User> buildUserList(int count) {
    return List.generate(
      count,
      (i) => buildUser(
        id: 'id-$i',
        email: 'user$i@example.com',
        name: 'User $i',
      ),
    );
  }

  static Feature buildFeature({
    String? id,
    String? name,
    bool isActive = true,
  }) {
    return Feature(
      id: id ?? 'feature-id',
      name: name ?? 'Test Feature',
      isActive: isActive,
    );
  }
}

// Usage
test('repository returns users', () async {
  final testUsers = TestDataBuilder.buildUserList(5);
  
  when(() => mockRepo.getUsers())
      .thenAnswer((_) => TaskEither.right(testUsers));
});
```

### Setup Helper

```dart
class TestSetup {
  late MockRepository mockRepo;
  late MockDataSource mockDataSource;
  late FeatureCubit cubit;

  void setup() {
    mockRepo = MockRepository();
    mockDataSource = MockDataSource();
    cubit = FeatureCubit(mockRepo);
  }

  void teardown() {
    cubit.close();
  }

  void whenGetDataSucceeds([Feature? data]) {
    when(() => mockRepo.getData(any()))
        .thenAnswer((_) => TaskEither.right(data ?? TestDataBuilder.buildFeature()));
  }

  void whenGetDataFails([Failure? failure]) {
    when(() => mockRepo.getData(any()))
        .thenAnswer((_) => TaskEither.left(failure ?? const Failure.network()));
  }
}

// Usage
void main() {
  final setup = TestSetup();

  setUp(setup.setup);
  tearDown(setup.teardown);

  blocTest<FeatureCubit, FeatureState>(
    'loads data successfully',
    build: () {
      setup.whenGetDataSucceeds();
      return setup.cubit;
    },
    act: (cubit) => cubit.load(),
    expect: () => [
      const FeatureState(status: Status.loading),
      isA<FeatureState>().having((s) => s.status, 'status', Status.loaded),
    ],
  );
}
```

## Parameterized Tests

### Simple Parameterized Test

```dart
void main() {
  final testCases = [
    (input: 0, expected: 'Zero'),
    (input: 1, expected: 'One'),
    (input: 5, expected: 'Five'),
    (input: 10, expected: 'Ten'),
  ];

  for (final testCase in testCases) {
    test('converts ${testCase.input} to ${testCase.expected}', () {
      final result = numberToWord(testCase.input);
      expect(result, testCase.expected);
    });
  }
}
```

### Parameterized Widget Test

```dart
void main() {
  final themes = [
    ('light', ThemeData.light()),
    ('dark', ThemeData.dark()),
  ];

  for (final (name, theme) in themes) {
    testWidgets('widget renders with $name theme', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: theme,
          home: const MyWidget(),
        ),
      );

      expect(find.byType(MyWidget), findsOneWidget);
    });
  }
}
```

### Parameterized BLoC Test

```dart
void main() {
  final errorScenarios = [
    (error: NetworkException(), expected: Failure.network()),
    (error: NotFoundException(), expected: Failure.notFound()),
    (error: ServerException(), expected: Failure.server()),
  ];

  for (final scenario in errorScenarios) {
    blocTest<FeatureCubit, FeatureState>(
      'handles ${scenario.error.runtimeType}',
      build: () {
        when(() => mockRepo.getData(any())).thenThrow(scenario.error);
        return FeatureCubit(mockRepo);
      },
      act: (cubit) => cubit.load(),
      expect: () => [
        const FeatureState(status: Status.loading),
        isA<FeatureState>().having(
          (s) => s.failure,
          'failure',
          scenario.expected,
        ),
      ],
    );
  }
}
```

## Test Coverage

### Generating Coverage Report

```bash
# Run tests with coverage
flutter test --coverage

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html

# Open report
open coverage/html/index.html  # macOS
xdg-open coverage/html/index.html  # Linux
start coverage/html/index.html  # Windows
```

### Coverage Configuration

```yaml
# flutter_test.yaml
coverage:
  exclude:
    - '**/*.g.dart'
    - '**/*.freezed.dart'
    - '**/main.dart'
    - 'lib/generated/**'
```

### Checking Coverage Threshold

```bash
# Check if coverage meets threshold (e.g., 80%)
flutter test --coverage
lcov --summary coverage/lcov.info | grep "lines......"
```

### Coverage in CI

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test --coverage
      - name: Check coverage
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines......" | awk '{print $2}' | sed 's/%//')
          echo "Coverage: $COVERAGE%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage is below 80%"
            exit 1
          fi
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Flutter Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Analyze
        run: flutter analyze
      
      - name: Run tests
        run: flutter test --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: coverage/lcov.info
```

### Running Integration Tests in CI

```yaml
# .github/workflows/integration_test.yml
name: Integration Tests

on:
  push:
    branches: [main]

jobs:
  android:
    runs-on: macos-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: subosito/flutter-action@v2
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Run integration tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 29
          script: flutter test integration_test/
```

### Test Sharding

```yaml
# Split tests across multiple jobs
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: |
          flutter test \
            --total-shards=4 \
            --shard-index=${{ matrix.shard }}
```

## Best Practices

### 1. Organize Tests

```
test/
├── unit/
│   ├── models/
│   ├── repositories/
│   └── services/
├── widget/
│   ├── components/
│   └── pages/
├── integration/
│   └── flows/
├── helpers/
│   ├── test_helpers.dart
│   ├── mock_data.dart
│   └── custom_matchers.dart
└── goldens/
    ├── button.png
    └── card.png
```

### 2. Reusable Test Utilities

```dart
// test/helpers/pump_app.dart
extension PumpApp on WidgetTester {
  Future<void> pumpAppWithProviders(
    Widget widget, {
    List<RepositoryProvider>? providers,
  }) async {
    await pumpWidget(
      MultiRepositoryProvider(
        providers: providers ?? [],
        child: MaterialApp(home: widget),
      ),
    );
    await pumpAndSettle();
  }
}
```

### 3. Test Tagging

```dart
@Tags(['unit'])
test('unit test', () {});

@Tags(['integration'])
testWidgets('integration test', (tester) async {});

@Tags(['slow'])
test('slow test', () {});
```

Run specific tags:
```bash
flutter test --tags unit
flutter test --exclude-tags slow
```

### 4. Shared Test Setup

```dart
// test/helpers/shared_setup.dart
void sharedSetUp() {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  // Set up fake platform
  debugDefaultTargetPlatformOverride = TargetPlatform.android;
  
  // Initialize fakes
  registerFallbackValues();
}

void sharedTearDown() {
  debugDefaultTargetPlatformOverride = null;
}
```

### 5. Avoid Test Flakiness

```dart
// ❌ Bad: Hard-coded delays
test('bad test', () async {
  await Future.delayed(Duration(seconds: 1));
  expect(result, expected);
});

// ✅ Good: Wait for conditions
test('good test', () async {
  await tester.pumpAndSettle();
  expect(find.text('Loaded'), findsOneWidget);
});
```

### 6. Test Isolation

```dart
// Ensure tests don't affect each other
setUp(() {
  // Fresh state for each test
  mockRepo = MockRepository();
  cubit = FeatureCubit(mockRepo);
});

tearDown(() {
  // Clean up
  cubit.close();
});
```

### 7. Meaningful Test Names

```dart
// ❌ Bad
test('test1', () {});

// ✅ Good
test('returns user when repository call succeeds', () {});
```

### 8. Test One Thing

```dart
// ❌ Bad: Testing multiple things
test('user operations', () {
  // Creates user
  // Updates user
  // Deletes user
});

// ✅ Good: Separate tests
test('creates user successfully', () {});
test('updates user successfully', () {});
test('deletes user successfully', () {});
```

### 9. Use Test Groups

```dart
group('UserRepository', () {
  group('getUser', () {
    test('returns user on success', () {});
    test('returns failure on error', () {});
  });
  
  group('saveUser', () {
    test('saves user successfully', () {});
    test('handles save error', () {});
  });
});
```

### 10. Document Complex Tests

```dart
test('complex business logic', () {
  // Arrange: Set up test data with specific conditions
  final user = User(id: '1', credits: 100);
  
  // Act: Perform the operation
  final result = calculateDiscount(user, purchaseAmount: 50);
  
  // Assert: Verify expected outcome
  expect(result.discount, 10);
  expect(result.finalAmount, 40);
});
```

## Performance Tips

1. **Use `setUp` and `setUpAll` wisely**
   - `setUpAll` for expensive one-time setup
   - `setUp` for per-test initialization

2. **Minimize widget rebuilds in tests**
   - Use `const` constructors where possible

3. **Parallel test execution**
   ```bash
   flutter test --concurrency=4
   ```

4. **Skip slow tests in development**
   ```dart
   test('slow test', () {}, skip: true);
   ```

5. **Use test sharding for large test suites**
   ```bash
   flutter test --total-shards=4 --shard-index=1
   ```
