---
name: flutter-testing
description: 'Comprehensive Flutter testing guide for BLoC/Cubit, repositories, widgets, and integration tests with Clean Architecture patterns. Use when: (1) Writing tests for Flutter apps, (2) Testing BLoC/Cubit state management, (3) Testing repositories and data sources, (4) Writing widget tests, (5) Creating integration tests, (6) Setting up test coverage, (7) Working with mocktail/bloc_test. Keywords: flutter test, bloc test, cubit test, widget test, integration test, mocktail, bloc_test, repository test, clean architecture testing, TDD.'
---

# Flutter Testing

Testing patterns for Flutter apps with BLoC/Cubit, Clean Architecture, bloc_test, and mocktail.

## When to Use

- Writing BLoC/Cubit, widget, or integration tests
- Mocking dependencies with mocktail
- Testing Clean Architecture layers
- Setting up test coverage or TDD workflow

## Test Types

| Type | Purpose | Coverage |
|------|---------|----------|
| **Unit** | BLoC/Cubit, repositories | 80%+ |
| **Widget** | UI components | Key flows |
| **Integration** | E2E flows | Critical paths |

## Dependencies

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
  integration_test:
    sdk: flutter
```

## BLoC/Cubit Testing

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';

class MockRepository extends Mock implements FeatureRepository {}

blocTest<FeatureCubit, FeatureState>(
  'emits [loading, loaded] on success',
  build: () {
    when(() => mockRepo.getData(any()))
        .thenAnswer((_) => TaskEither.right(mockData));
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadData('id'),
  expect: () => [
    const FeatureState(status: Status.loading),
    FeatureState(status: Status.loaded, data: mockData),
  ],
  verify: (_) => verify(() => mockRepo.getData('id')).called(1),
);
```

**Details:** [BLOC_CUBIT_TESTING.md](references/BLOC_CUBIT_TESTING.md)

## Widget Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockFeatureCubit extends Mock implements FeatureCubit {}

testWidgets('displays data when loaded', (tester) async {
  final mockCubit = MockFeatureCubit();
  when(() => mockCubit.state).thenReturn(
    FeatureState(status: Status.loaded, data: mockData),
  );

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider(create: (_) => mockCubit, child: FeaturePage()),
    ),
  );

  expect(find.text('Expected Data'), findsOneWidget);
});

testWidgets('handles tap', (tester) async {
  await tester.tap(find.byKey(Key('button')));
  await tester.pumpAndSettle();
  verify(() => mockCubit.loadData()).called(1);
});
```

**Details:** [WIDGET_TESTING.md](references/WIDGET_TESTING.md)

## Integration Testing

```dart
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('complete user journey', (tester) async {
    await tester.pumpWidget(MyApp());
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(Key('nav_button')));
    await tester.pumpAndSettle();

    expect(find.text('Success'), findsOneWidget);
  });
}
```

## Best Practices

✅ Test behavior not implementation • Mock dependencies only • Cover success AND failure • Use descriptive names • Test state transitions • Use `verify()` for interactions • Add keys to widgets • Use `pumpAndSettle()` after async

❌ Don't test private methods • Don't mock the thing being tested • Don't skip error tests • Don't use hard-coded delays

## Commands

```bash
flutter test                    # All tests
flutter test --coverage         # With coverage
flutter test test/path/         # Specific path
flutter test integration_test/  # Integration tests
```

## Mocking Essentials

```dart
// Setup
class MockRepo extends Mock implements FeatureRepo {}
when(() => mock.method(any())).thenAnswer((_) => TaskEither.right(data));

// Verify
verify(() => mock.method('arg')).called(1);
verifyNever(() => mock.method(any()));

// Fallback for custom types
setUpAll(() => registerFallbackValue(FakeFeature()));
```

## References

- **[BLoC/Cubit Testing](references/BLOC_CUBIT_TESTING.md)** - State management patterns
- **[Widget Testing](references/WIDGET_TESTING.md)** - UI testing and finders
- **[Mocking Patterns](references/MOCKING_PATTERNS.md)** - Mocktail techniques
- **[Repository Testing](references/REPOSITORY_TESTING.md)** - Testing repositories and datasources
- **[Integration Testing](references/INTEGRATION_TESTING.md)** - E2E flows and user journeys
- **[Clean Architecture](references/CLEAN_ARCHITECTURE.md)** - Layer-by-layer testing strategy
- **[Advanced Patterns](references/ADVANCED_PATTERNS.md)** - Golden tests, performance, custom matchers

## Quick Tips

- Use keys for reliable widget finding
- `pumpAndSettle()` after async operations
- Mock dependencies, not the thing being tested
- Test both success and failure paths
- Use `isA<T>().having()` for complex assertions
