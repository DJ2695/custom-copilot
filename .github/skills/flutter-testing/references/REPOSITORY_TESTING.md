# Repository Testing Patterns

Comprehensive guide to testing repositories and data sources in Clean Architecture with fpdart TaskEither.

## Table of Contents

- [Overview](#overview)
- [Repository Pattern](#repository-pattern)
- [Testing Repositories](#testing-repositories)
- [Testing DataSources](#testing-datasources)
- [Testing with TaskEither](#testing-with-taskeither)
- [Testing Transformations](#testing-transformations)
- [Error Handling](#error-handling)
- [Complete Examples](#complete-examples)

## Overview

In Clean Architecture, repositories:
- Abstract data sources from domain layer
- Return fpdart TaskEither for error handling
- Transform DTOs to domain entities
- Handle exceptions gracefully

## Repository Pattern

### Repository Interface (Domain Layer)

```dart
abstract class FeatureRepository {
  TaskEither<FeatureFailure, Feature> getFeature(String id);
  TaskEither<FeatureFailure, List<Feature>> getFeatures();
  TaskEither<FeatureFailure, Unit> saveFeature(Feature feature);
  TaskEither<FeatureFailure, Unit> deleteFeature(String id);
}
```

### Repository Implementation (Data Layer)

```dart
class FeatureRepositoryImpl implements FeatureRepository {
  FeatureRepositoryImpl(this._remoteDataSource, this._localDataSource);

  final FeatureRemoteDataSource _remoteDataSource;
  final FeatureLocalDataSource _localDataSource;

  @override
  TaskEither<FeatureFailure, Feature> getFeature(String id) {
    return TaskEither.tryCatch(
      () async {
        final dto = await _remoteDataSource.getFeature(id);
        return dto.toDomain();
      },
      (error, stackTrace) => _handleError(error),
    );
  }

  FeatureFailure _handleError(Object error) {
    if (error is NetworkException) {
      return const FeatureFailure.networkError();
    }
    if (error is NotFoundException) {
      return const FeatureFailure.notFound();
    }
    return FeatureFailure.serverError(error.toString());
  }
}
```

## Testing Repositories

### Basic Repository Test Setup

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';

class MockFeatureRemoteDataSource extends Mock 
    implements FeatureRemoteDataSource {}

class MockFeatureLocalDataSource extends Mock 
    implements FeatureLocalDataSource {}

void main() {
  late MockFeatureRemoteDataSource mockRemoteDataSource;
  late MockFeatureLocalDataSource mockLocalDataSource;
  late FeatureRepositoryImpl repository;

  setUp(() {
    mockRemoteDataSource = MockFeatureRemoteDataSource();
    mockLocalDataSource = MockFeatureLocalDataSource();
    repository = FeatureRepositoryImpl(
      mockRemoteDataSource,
      mockLocalDataSource,
    );
  });

  group('FeatureRepository', () {
    // Tests go here
  });
}
```

### Testing Successful Data Retrieval

```dart
group('getFeature', () {
  const testId = 'test-id';
  final testDto = FeatureDto(
    id: testId,
    name: 'Test Feature',
    createdAt: '2024-01-01T00:00:00Z',
  );
  final expectedFeature = Feature(
    id: testId,
    name: 'Test Feature',
    createdAt: DateTime.parse('2024-01-01T00:00:00Z'),
  );

  test('returns Feature when remote data source succeeds', () async {
    when(() => mockRemoteDataSource.getFeature(testId))
        .thenAnswer((_) async => testDto);

    final result = await repository.getFeature(testId).run();

    expect(result.isRight(), isTrue);
    result.fold(
      (failure) => fail('Should return right'),
      (feature) {
        expect(feature.id, expectedFeature.id);
        expect(feature.name, expectedFeature.name);
        expect(feature.createdAt, expectedFeature.createdAt);
      },
    );

    verify(() => mockRemoteDataSource.getFeature(testId)).called(1);
  });
});
```

### Testing Error Cases

```dart
test('returns NetworkError when network fails', () async {
  when(() => mockRemoteDataSource.getFeature(any()))
      .thenThrow(const NetworkException('No connection'));

  final result = await repository.getFeature('id').run();

  expect(result.isLeft(), isTrue);
  result.fold(
    (failure) => expect(failure, const FeatureFailure.networkError()),
    (feature) => fail('Should return left'),
  );
});

test('returns NotFound when resource not found', () async {
  when(() => mockRemoteDataSource.getFeature(any()))
      .thenThrow(const NotFoundException('Feature not found'));

  final result = await repository.getFeature('id').run();

  expect(result.isLeft(), isTrue);
  result.fold(
    (failure) => expect(failure, const FeatureFailure.notFound()),
    (feature) => fail('Should return left'),
  );
});

test('returns ServerError for unexpected exceptions', () async {
  when(() => mockRemoteDataSource.getFeature(any()))
      .thenThrow(Exception('Unexpected error'));

  final result = await repository.getFeature('id').run();

  expect(result.isLeft(), isTrue);
  result.fold(
    (failure) {
      expect(failure, isA<FeatureFailure>());
      failure.when(
        networkError: () => fail('Wrong failure type'),
        notFound: () => fail('Wrong failure type'),
        serverError: (message) => expect(message, contains('Unexpected')),
      );
    },
    (feature) => fail('Should return left'),
  );
});
```

### Testing List Operations

```dart
group('getFeatures', () {
  final testDtos = [
    FeatureDto(id: '1', name: 'Feature 1'),
    FeatureDto(id: '2', name: 'Feature 2'),
  ];

  test('returns list of Features', () async {
    when(() => mockRemoteDataSource.getFeatures())
        .thenAnswer((_) async => testDtos);

    final result = await repository.getFeatures().run();

    expect(result.isRight(), isTrue);
    result.fold(
      (failure) => fail('Should return right'),
      (features) {
        expect(features.length, 2);
        expect(features[0].id, '1');
        expect(features[1].id, '2');
      },
    );
  });

  test('returns empty list when no data', () async {
    when(() => mockRemoteDataSource.getFeatures())
        .thenAnswer((_) async => []);

    final result = await repository.getFeatures().run();

    expect(result.isRight(), isTrue);
    result.fold(
      (failure) => fail('Should return right'),
      (features) => expect(features, isEmpty),
    );
  });
});
```

### Testing Write Operations

```dart
group('saveFeature', () {
  final testFeature = Feature(
    id: 'test-id',
    name: 'Test Feature',
  );

  test('saves feature successfully', () async {
    when(() => mockRemoteDataSource.saveFeature(any()))
        .thenAnswer((_) async => unit);

    final result = await repository.saveFeature(testFeature).run();

    expect(result.isRight(), isTrue);
    verify(() => mockRemoteDataSource.saveFeature(any())).called(1);
  });

  test('returns failure when save fails', () async {
    when(() => mockRemoteDataSource.saveFeature(any()))
        .thenThrow(const NetworkException('Save failed'));

    final result = await repository.saveFeature(testFeature).run();

    expect(result.isLeft(), isTrue);
  });
});

group('deleteFeature', () {
  const testId = 'test-id';

  test('deletes feature successfully', () async {
    when(() => mockRemoteDataSource.deleteFeature(testId))
        .thenAnswer((_) async => unit);

    final result = await repository.deleteFeature(testId).run();

    expect(result.isRight(), isTrue);
    verify(() => mockRemoteDataSource.deleteFeature(testId)).called(1);
  });
});
```

## Testing DataSources

### Remote DataSource Test

```dart
class MockHttpClient extends Mock implements HttpClient {}

void main() {
  late MockHttpClient mockHttpClient;
  late FeatureRemoteDataSource dataSource;

  setUp(() {
    mockHttpClient = MockHttpClient();
    dataSource = FeatureRemoteDataSourceImpl(mockHttpClient);
  });

  group('FeatureRemoteDataSource', () {
    test('returns FeatureDto on successful request', () async {
      when(() => mockHttpClient.get(any())).thenAnswer(
        (_) async => Response(
          statusCode: 200,
          body: json.encode({
            'id': 'test-id',
            'name': 'Test Feature',
          }),
        ),
      );

      final result = await dataSource.getFeature('test-id');

      expect(result.id, 'test-id');
      expect(result.name, 'Test Feature');
    });

    test('throws NetworkException on connection error', () async {
      when(() => mockHttpClient.get(any()))
          .thenThrow(const SocketException('No internet'));

      expect(
        () => dataSource.getFeature('id'),
        throwsA(isA<NetworkException>()),
      );
    });

    test('throws ServerException on 500 error', () async {
      when(() => mockHttpClient.get(any())).thenAnswer(
        (_) async => Response(statusCode: 500, body: 'Server error'),
      );

      expect(
        () => dataSource.getFeature('id'),
        throwsA(isA<ServerException>()),
      );
    });

    test('throws NotFoundException on 404 error', () async {
      when(() => mockHttpClient.get(any())).thenAnswer(
        (_) async => Response(statusCode: 404, body: 'Not found'),
      );

      expect(
        () => dataSource.getFeature('id'),
        throwsA(isA<NotFoundException>()),
      );
    });
  });
}
```

### Local DataSource Test

```dart
class MockSharedPreferences extends Mock implements SharedPreferences {}

void main() {
  late MockSharedPreferences mockPrefs;
  late FeatureLocalDataSource dataSource;

  setUp(() {
    mockPrefs = MockSharedPreferences();
    dataSource = FeatureLocalDataSourceImpl(mockPrefs);
  });

  group('FeatureLocalDataSource', () {
    test('caches feature locally', () async {
      final testDto = FeatureDto(id: '1', name: 'Test');
      
      when(() => mockPrefs.setString(any(), any()))
          .thenAnswer((_) async => true);

      await dataSource.cacheFeature(testDto);

      verify(() => mockPrefs.setString(
        'feature_1',
        any(that: contains('"id":"1"')),
      )).called(1);
    });

    test('retrieves cached feature', () async {
      when(() => mockPrefs.getString('feature_1')).thenReturn(
        json.encode({'id': '1', 'name': 'Cached'}),
      );

      final result = await dataSource.getCachedFeature('1');

      expect(result.id, '1');
      expect(result.name, 'Cached');
    });

    test('throws CacheException when cache empty', () async {
      when(() => mockPrefs.getString(any())).thenReturn(null);

      expect(
        () => dataSource.getCachedFeature('1'),
        throwsA(isA<CacheException>()),
      );
    });
  });
}
```

## Testing with TaskEither

### Testing TaskEither Chains

```dart
test('chains TaskEither operations', () async {
  when(() => mockRemoteDataSource.getFeature('id'))
      .thenAnswer((_) async => testDto);
  when(() => mockLocalDataSource.cacheFeature(any()))
      .thenAnswer((_) async => unit);

  final result = await repository
      .getFeature('id')
      .flatMap((feature) => repository.cacheFeature(feature))
      .run();

  expect(result.isRight(), isTrue);
  verify(() => mockRemoteDataSource.getFeature('id')).called(1);
  verify(() => mockLocalDataSource.cacheFeature(any())).called(1);
});
```

### Testing TaskEither with Fold

```dart
test('handles both success and failure with fold', () async {
  when(() => mockRemoteDataSource.getFeature(any()))
      .thenThrow(const NetworkException('Error'));

  final result = await repository.getFeature('id').run();

  final message = result.fold(
    (failure) => 'Failed: ${failure.toString()}',
    (feature) => 'Success: ${feature.name}',
  );

  expect(message, contains('Failed'));
});
```

### Testing TaskEither Map

```dart
test('maps successful result', () async {
  when(() => mockRemoteDataSource.getFeature('id'))
      .thenAnswer((_) async => testDto);

  final result = await repository
      .getFeature('id')
      .map((feature) => feature.name.toUpperCase())
      .run();

  expect(result.isRight(), isTrue);
  result.fold(
    (failure) => fail('Should be right'),
    (name) => expect(name, 'TEST FEATURE'),
  );
});
```

## Testing Transformations

### DTO to Domain Entity

```dart
group('DTO transformations', () {
  test('converts DTO to domain entity correctly', () {
    final dto = FeatureDto(
      id: 'id',
      name: 'Name',
      createdAt: '2024-01-01T00:00:00Z',
      metadata: {'key': 'value'},
    );

    final entity = dto.toDomain();

    expect(entity.id, dto.id);
    expect(entity.name, dto.name);
    expect(entity.createdAt, DateTime.parse(dto.createdAt));
    expect(entity.metadata['key'], 'value');
  });

  test('handles nullable fields correctly', () {
    final dto = FeatureDto(
      id: 'id',
      name: 'Name',
      description: null,
    );

    final entity = dto.toDomain();

    expect(entity.description, isNull);
  });
});
```

### Domain Entity to DTO

```dart
test('converts domain entity to DTO', () {
  final entity = Feature(
    id: 'id',
    name: 'Name',
    createdAt: DateTime.parse('2024-01-01T00:00:00Z'),
  );

  final dto = FeatureDto.fromDomain(entity);

  expect(dto.id, entity.id);
  expect(dto.name, entity.name);
  expect(dto.createdAt, '2024-01-01T00:00:00.000Z');
});
```

## Error Handling

### Testing Exception to Failure Mapping

```dart
group('error handling', () {
  test('maps NetworkException to NetworkFailure', () async {
    when(() => mockRemoteDataSource.getFeature(any()))
        .thenThrow(const NetworkException('No connection'));

    final result = await repository.getFeature('id').run();

    result.fold(
      (failure) => expect(failure, const FeatureFailure.networkError()),
      (_) => fail('Should be failure'),
    );
  });

  test('maps generic Exception to ServerFailure', () async {
    when(() => mockRemoteDataSource.getFeature(any()))
        .thenThrow(Exception('Unknown error'));

    final result = await repository.getFeature('id').run();

    result.fold(
      (failure) => expect(failure, isA<FeatureFailure>()),
      (_) => fail('Should be failure'),
    );
  });
});
```

## Complete Examples

### Complete Repository Test Suite

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';

class MockFeatureRemoteDataSource extends Mock 
    implements FeatureRemoteDataSource {}

void main() {
  late MockFeatureRemoteDataSource mockDataSource;
  late FeatureRepositoryImpl repository;

  setUp(() {
    mockDataSource = MockFeatureRemoteDataSource();
    repository = FeatureRepositoryImpl(mockDataSource);
  });

  group('FeatureRepository', () {
    group('getFeature', () {
      const testId = 'test-id';
      final testDto = FeatureDto(id: testId, name: 'Test');
      final expectedFeature = testDto.toDomain();

      test('returns Feature on success', () async {
        when(() => mockDataSource.getFeature(testId))
            .thenAnswer((_) async => testDto);

        final result = await repository.getFeature(testId).run();

        expect(result.isRight(), isTrue);
        result.fold(
          (l) => fail('Should be right'),
          (r) => expect(r, expectedFeature),
        );
        verify(() => mockDataSource.getFeature(testId)).called(1);
      });

      test('returns NetworkFailure on NetworkException', () async {
        when(() => mockDataSource.getFeature(any()))
            .thenThrow(const NetworkException());

        final result = await repository.getFeature(testId).run();

        expect(result.isLeft(), isTrue);
        result.fold(
          (l) => expect(l, const FeatureFailure.networkError()),
          (r) => fail('Should be left'),
        );
      });

      test('returns NotFoundFailure on NotFoundException', () async {
        when(() => mockDataSource.getFeature(any()))
            .thenThrow(const NotFoundException());

        final result = await repository.getFeature(testId).run();

        expect(result.isLeft(), isTrue);
        result.fold(
          (l) => expect(l, const FeatureFailure.notFound()),
          (r) => fail('Should be left'),
        );
      });
    });

    group('getFeatures', () {
      final testDtos = [
        FeatureDto(id: '1', name: 'One'),
        FeatureDto(id: '2', name: 'Two'),
      ];

      test('returns list of Features', () async {
        when(() => mockDataSource.getFeatures())
            .thenAnswer((_) async => testDtos);

        final result = await repository.getFeatures().run();

        expect(result.isRight(), isTrue);
        result.fold(
          (l) => fail('Should be right'),
          (r) {
            expect(r.length, 2);
            expect(r[0].id, '1');
            expect(r[1].id, '2');
          },
        );
      });

      test('returns empty list when no data', () async {
        when(() => mockDataSource.getFeatures())
            .thenAnswer((_) async => []);

        final result = await repository.getFeatures().run();

        expect(result.isRight(), isTrue);
        result.fold(
          (l) => fail('Should be right'),
          (r) => expect(r, isEmpty),
        );
      });
    });

    group('saveFeature', () {
      final testFeature = Feature(id: 'id', name: 'Test');

      test('saves successfully', () async {
        when(() => mockDataSource.saveFeature(any()))
            .thenAnswer((_) async => unit);

        final result = await repository.saveFeature(testFeature).run();

        expect(result.isRight(), isTrue);
        verify(() => mockDataSource.saveFeature(any())).called(1);
      });

      test('handles save failure', () async {
        when(() => mockDataSource.saveFeature(any()))
            .thenThrow(const NetworkException());

        final result = await repository.saveFeature(testFeature).run();

        expect(result.isLeft(), isTrue);
      });
    });
  });
}
```

## Best Practices

1. **Mock data sources, not repositories**
   - Repositories are what you're testing

2. **Test both success and failure paths**
   - Network errors, not found, server errors, etc.

3. **Verify data source calls**
   - Ensure methods called with correct arguments

4. **Test data transformations**
   - DTO to entity conversions

5. **Use TaskEither.tryCatch**
   - Handles exceptions gracefully

6. **Test TaskEither operations**
   - flatMap, map, fold, etc.

7. **Keep tests focused**
   - One behavior per test

8. **Use descriptive test names**
   - Clearly explain what's being tested

9. **Test edge cases**
   - Empty lists, null values, etc.

10. **Isolate repository tests**
    - Don't depend on real data sources
