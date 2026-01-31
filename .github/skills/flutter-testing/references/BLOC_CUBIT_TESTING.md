# BLoC/Cubit Testing Patterns

Comprehensive guide to testing BLoC and Cubit state management with bloc_test, mocktail, and fpdart.

## Table of Contents

- [Setup](#setup)
- [Basic Cubit Testing](#basic-cubit-testing)
- [Advanced Cubit Patterns](#advanced-cubit-patterns)
- [BLoC Testing with Events](#bloc-testing-with-events)
- [Testing with fpdart TaskEither](#testing-with-fpdart-taskeither)
- [Async Operations](#async-operations)
- [Error Handling](#error-handling)
- [State Transitions](#state-transitions)
- [Complete Examples](#complete-examples)

## Setup

### Dependencies

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
```

### Basic Test Structure

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockRepository extends Mock implements FeatureRepository {}

void main() {
  late MockRepository mockRepository;
  late FeatureCubit cubit;

  setUp(() {
    mockRepository = MockRepository();
    cubit = FeatureCubit(mockRepository);
  });

  tearDown(() => cubit.close());

  group('FeatureCubit', () {
    // Tests go here
  });
}
```

## Basic Cubit Testing

### Test Initial State

```dart
test('initial state is correct', () {
  expect(cubit.state, const FeatureState());
  expect(cubit.state.status, Status.initial);
});
```

### Test Single State Emission

```dart
blocTest<CounterCubit, int>(
  'emits [1] when increment is called',
  build: () => CounterCubit(),
  act: (cubit) => cubit.increment(),
  expect: () => [1],
);
```

### Test Multiple State Emissions

```dart
blocTest<CounterCubit, int>(
  'emits [1, 2, 3] when increment is called multiple times',
  build: () => CounterCubit(),
  act: (cubit) => cubit
    ..increment()
    ..increment()
    ..increment(),
  expect: () => [1, 2, 3],
);
```

### Using Seed State

```dart
blocTest<CounterCubit, int>(
  'emits [11] when increment is called with seed 10',
  build: () => CounterCubit(),
  seed: () => 10,
  act: (cubit) => cubit.increment(),
  expect: () => [11],
);
```

## Advanced Cubit Patterns

### Testing with Freezed States

```dart
@freezed
class FeatureState with _$FeatureState {
  const factory FeatureState({
    @Default(Status.initial) Status status,
    @Default([]) List<Item> items,
    Failure? failure,
  }) = _FeatureState;
}

blocTest<FeatureCubit, FeatureState>(
  'loads items successfully',
  build: () {
    when(() => mockRepo.getItems())
        .thenAnswer((_) => TaskEither.right(mockItems));
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadItems(),
  expect: () => [
    const FeatureState(status: Status.loading),
    FeatureState(
      status: Status.loaded,
      items: mockItems,
    ),
  ],
);
```

### Testing Complex State Changes

```dart
blocTest<FeatureCubit, FeatureState>(
  'updates specific fields without affecting others',
  build: () => FeatureCubit(mockRepo),
  seed: () => FeatureState(
    status: Status.loaded,
    items: [item1, item2],
    selectedId: 'id1',
  ),
  act: (cubit) => cubit.selectItem('id2'),
  expect: () => [
    isA<FeatureState>()
        .having((s) => s.selectedId, 'selectedId', 'id2')
        .having((s) => s.items, 'items', [item1, item2]) // Unchanged
        .having((s) => s.status, 'status', Status.loaded), // Unchanged
  ],
);
```

### Using Matchers for Flexible Assertions

```dart
blocTest<SearchCubit, SearchState>(
  'searches with any non-empty query',
  build: () => SearchCubit(mockRepo),
  act: (cubit) => cubit.search('flutter'),
  expect: () => [
    isA<SearchState>()
        .having((s) => s.isLoading, 'isLoading', true)
        .having((s) => s.query, 'query', isNotEmpty),
    isA<SearchState>()
        .having((s) => s.isLoading, 'isLoading', false)
        .having((s) => s.results, 'results', isNotEmpty),
  ],
);
```

## BLoC Testing with Events

### Basic BLoC Test

```dart
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<CounterIncremented>((event, emit) => emit(state + 1));
    on<CounterDecremented>((event, emit) => emit(state - 1));
  }
}

blocTest<CounterBloc, int>(
  'emits [1] when CounterIncremented is added',
  build: () => CounterBloc(),
  act: (bloc) => bloc.add(CounterIncremented()),
  expect: () => [1],
);
```

### Testing Multiple Events

```dart
blocTest<CounterBloc, int>(
  'emits [1, 2, 3] when CounterIncremented is added 3 times',
  build: () => CounterBloc(),
  act: (bloc) => bloc
    ..add(CounterIncremented())
    ..add(CounterIncremented())
    ..add(CounterIncremented()),
  expect: () => [1, 2, 3],
);
```

### Testing Event Order

```dart
blocTest<CounterBloc, int>(
  'handles mixed events correctly',
  build: () => CounterBloc(),
  act: (bloc) => bloc
    ..add(CounterIncremented())  // 1
    ..add(CounterIncremented())  // 2
    ..add(CounterDecremented())  // 1
    ..add(CounterIncremented()), // 2
  expect: () => [1, 2, 1, 2],
);
```

## Testing with fpdart TaskEither

### Mocking TaskEither Success

```dart
blocTest<FeatureCubit, FeatureState>(
  'handles TaskEither.right success',
  build: () {
    when(() => mockRepo.getData('id'))
        .thenAnswer((_) => TaskEither.right(mockData));
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadData('id'),
  expect: () => [
    const FeatureState(status: Status.loading),
    FeatureState(status: Status.loaded, data: mockData),
  ],
);
```

### Mocking TaskEither Failure

```dart
blocTest<FeatureCubit, FeatureState>(
  'handles TaskEither.left failure',
  build: () {
    when(() => mockRepo.getData('id'))
        .thenAnswer((_) => TaskEither.left(
          const FeatureFailure.serverError('Server error'),
        ));
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadData('id'),
  expect: () => [
    const FeatureState(status: Status.loading),
    isA<FeatureState>()
        .having((s) => s.status, 'status', Status.error)
        .having(
          (s) => s.failure,
          'failure',
          isA<FeatureFailure>(),
        ),
  ],
);
```

### Testing TaskEither with Fold

```dart
// In Cubit implementation
Future<void> loadData(String id) async {
  emit(state.copyWith(status: Status.loading));
  
  final result = await repository.getData(id).run();
  
  result.fold(
    (failure) => emit(state.copyWith(
      status: Status.error,
      failure: failure,
    )),
    (data) => emit(state.copyWith(
      status: Status.loaded,
      data: data,
    )),
  );
}

// Test both paths
group('loadData', () {
  blocTest<FeatureCubit, FeatureState>(
    'emits error state on failure',
    build: () {
      when(() => mockRepo.getData(any()))
          .thenAnswer((_) => TaskEither.left(testFailure));
      return FeatureCubit(mockRepo);
    },
    act: (cubit) => cubit.loadData('id'),
    expect: () => [
      const FeatureState(status: Status.loading),
      FeatureState(status: Status.error, failure: testFailure),
    ],
  );

  blocTest<FeatureCubit, FeatureState>(
    'emits loaded state on success',
    build: () {
      when(() => mockRepo.getData(any()))
          .thenAnswer((_) => TaskEither.right(testData));
      return FeatureCubit(mockRepo);
    },
    act: (cubit) => cubit.loadData('id'),
    expect: () => [
      const FeatureState(status: Status.loading),
      FeatureState(status: Status.loaded, data: testData),
    ],
  );
});
```

## Async Operations

### Testing Async Methods

```dart
blocTest<FeatureCubit, FeatureState>(
  'handles async operations',
  build: () {
    when(() => mockRepo.getData())
        .thenAnswer((_) async {
          await Future.delayed(const Duration(milliseconds: 100));
          return TaskEither.right(mockData);
        });
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadData(),
  expect: () => [
    const FeatureState(status: Status.loading),
    FeatureState(status: Status.loaded, data: mockData),
  ],
);
```

### Using Wait for Debounced Events

```dart
blocTest<SearchCubit, SearchState>(
  'debounces rapid search queries',
  build: () => SearchCubit(mockRepo),
  act: (cubit) async {
    cubit.search('f');
    await Future.delayed(const Duration(milliseconds: 100));
    cubit.search('fl');
    await Future.delayed(const Duration(milliseconds: 100));
    cubit.search('flu');
  },
  wait: const Duration(milliseconds: 400), // Wait for debounce
  expect: () => [
    SearchState(query: 'flu', status: Status.loaded),
  ],
);
```

### Testing with setUp for Async

```dart
blocTest<FeatureCubit, FeatureState>(
  'uses setUp for one-time async operations',
  build: () => FeatureCubit(mockRepo),
  setUp: () {
    when(() => mockRepo.getData())
        .thenAnswer((_) => TaskEither.right(mockData));
  },
  act: (cubit) => cubit.loadData(),
  expect: () => [
    const FeatureState(status: Status.loading),
    FeatureState(status: Status.loaded, data: mockData),
  ],
);
```

## Error Handling

### Testing Exception Handling

```dart
blocTest<FeatureCubit, FeatureState>(
  'handles exceptions gracefully',
  build: () {
    when(() => mockRepo.getData())
        .thenThrow(Exception('Network error'));
    return FeatureCubit(mockRepo);
  },
  act: (cubit) => cubit.loadData(),
  expect: () => [
    const FeatureState(status: Status.loading),
    isA<FeatureState>()
        .having((s) => s.status, 'status', Status.error)
        .having((s) => s.failure, 'failure', isA<FeatureFailure>()),
  ],
);
```

### Testing Different Failure Types

```dart
group('handles different failures', () {
  blocTest<FeatureCubit, FeatureState>(
    'network failure',
    build: () {
      when(() => mockRepo.getData())
          .thenAnswer((_) => TaskEither.left(
            const FeatureFailure.networkError(),
          ));
      return FeatureCubit(mockRepo);
    },
    act: (cubit) => cubit.loadData(),
    expect: () => [
      const FeatureState(status: Status.loading),
      isA<FeatureState>().having(
        (s) => s.failure,
        'failure',
        const FeatureFailure.networkError(),
      ),
    ],
  );

  blocTest<FeatureCubit, FeatureState>(
    'server failure',
    build: () {
      when(() => mockRepo.getData())
          .thenAnswer((_) => TaskEither.left(
            const FeatureFailure.serverError('500'),
          ));
      return FeatureCubit(mockRepo);
    },
    act: (cubit) => cubit.loadData(),
    expect: () => [
      const FeatureState(status: Status.loading),
      isA<FeatureState>().having(
        (s) => s.failure,
        'failure',
        const FeatureFailure.serverError('500'),
      ),
    ],
  );
});
```

## State Transitions

### Testing Complete State Lifecycles

```dart
blocTest<FormCubit, FormState>(
  'completes full form submission lifecycle',
  build: () {
    when(() => mockRepo.submit(any()))
        .thenAnswer((_) async {
          await Future.delayed(const Duration(milliseconds: 100));
          return TaskEither.right(unit);
        });
    return FormCubit(mockRepo);
  },
  act: (cubit) async {
    cubit.updateField('name', 'John');
    await Future.delayed(const Duration(milliseconds: 50));
    cubit.submit();
  },
  expect: () => [
    isA<FormState>()
        .having((s) => s.fields['name'], 'name', 'John')
        .having((s) => s.isValid, 'isValid', true),
    isA<FormState>()
        .having((s) => s.isSubmitting, 'isSubmitting', true),
    isA<FormState>()
        .having((s) => s.isSubmitting, 'isSubmitting', false)
        .having((s) => s.isSubmitted, 'isSubmitted', true),
  ],
);
```

### Skipping States

```dart
blocTest<FeatureCubit, FeatureState>(
  'skips initial loading state',
  build: () => FeatureCubit(mockRepo),
  skip: 1, // Skip first emitted state
  act: (cubit) => cubit.loadData(),
  expect: () => [
    FeatureState(status: Status.loaded, data: mockData),
  ],
);
```

## Complete Examples

### Weather Cubit Example

```dart
class WeatherCubit extends Cubit<WeatherState> {
  WeatherCubit(this._repository) : super(const WeatherState());

  final WeatherRepository _repository;

  Future<void> fetchWeather(String city) async {
    emit(state.copyWith(status: WeatherStatus.loading));

    final result = await _repository.getWeather(city).run();

    result.fold(
      (failure) => emit(state.copyWith(
        status: WeatherStatus.failure,
        failure: failure,
      )),
      (weather) => emit(state.copyWith(
        status: WeatherStatus.success,
        weather: weather,
      )),
    );
  }

  void toggleUnits() {
    if (state.weather == null) return;
    
    final newUnits = state.temperatureUnits == TemperatureUnits.celsius
        ? TemperatureUnits.fahrenheit
        : TemperatureUnits.celsius;
    
    emit(state.copyWith(temperatureUnits: newUnits));
  }
}

// Tests
void main() {
  late WeatherRepository mockRepository;
  late WeatherCubit cubit;

  setUp(() {
    mockRepository = MockWeatherRepository();
    cubit = WeatherCubit(mockRepository);
  });

  tearDown(() => cubit.close());

  group('WeatherCubit', () {
    const mockWeather = Weather(
      location: 'London',
      temperature: Temperature(value: 20),
      condition: WeatherCondition.cloudy,
    );

    test('initial state is correct', () {
      expect(
        cubit.state,
        const WeatherState(
          status: WeatherStatus.initial,
          temperatureUnits: TemperatureUnits.celsius,
        ),
      );
    });

    group('fetchWeather', () {
      blocTest<WeatherCubit, WeatherState>(
        'emits [loading, success] when weather fetched successfully',
        build: () {
          when(() => mockRepository.getWeather(any()))
              .thenAnswer((_) => TaskEither.right(mockWeather));
          return cubit;
        },
        act: (cubit) => cubit.fetchWeather('London'),
        expect: () => [
          const WeatherState(status: WeatherStatus.loading),
          const WeatherState(
            status: WeatherStatus.success,
            weather: mockWeather,
          ),
        ],
        verify: (_) {
          verify(() => mockRepository.getWeather('London')).called(1);
        },
      );

      blocTest<WeatherCubit, WeatherState>(
        'emits [loading, failure] when weather fetch fails',
        build: () {
          when(() => mockRepository.getWeather(any()))
              .thenAnswer((_) => TaskEither.left(
                const WeatherFailure.notFound(),
              ));
          return cubit;
        },
        act: (cubit) => cubit.fetchWeather('InvalidCity'),
        expect: () => [
          const WeatherState(status: WeatherStatus.loading),
          isA<WeatherState>()
              .having((s) => s.status, 'status', WeatherStatus.failure)
              .having((s) => s.failure, 'failure', isA<WeatherFailure>()),
        ],
      );
    });

    group('toggleUnits', () {
      blocTest<WeatherCubit, WeatherState>(
        'toggles from celsius to fahrenheit',
        build: () => cubit,
        seed: () => const WeatherState(
          status: WeatherStatus.success,
          weather: mockWeather,
          temperatureUnits: TemperatureUnits.celsius,
        ),
        act: (cubit) => cubit.toggleUnits(),
        expect: () => [
          isA<WeatherState>().having(
            (s) => s.temperatureUnits,
            'temperatureUnits',
            TemperatureUnits.fahrenheit,
          ),
        ],
      );

      blocTest<WeatherCubit, WeatherState>(
        'does nothing when weather is null',
        build: () => cubit,
        act: (cubit) => cubit.toggleUnits(),
        expect: () => [],
      );
    });
  });
}
```

## Best Practices

1. **Test state transitions, not implementation**
   - Focus on what states are emitted, not how
   
2. **Use descriptive test names**
   - Clearly explain the scenario being tested

3. **Mock dependencies, not the cubit/bloc**
   - Only mock external dependencies (repositories, services)

4. **Test both success and failure paths**
   - Don't forget error cases

5. **Use setUp and tearDown**
   - Initialize in setUp, clean up in tearDown

6. **Verify method calls**
   - Use `verify()` to ensure repository methods were called correctly

7. **Use matchers for flexibility**
   - `isA<T>().having()` for complex state assertions

8. **Close cubits/blocs in tearDown**
   - Prevents memory leaks and test pollution

9. **Test edge cases**
   - Empty data, null values, boundary conditions

10. **Keep tests focused**
    - One behavior per test
