# Clean Architecture Testing

Comprehensive guide to testing Clean Architecture layers in Flutter: Domain, Data, and Presentation.

## Table of Contents

- [Overview](#overview)
- [Architecture Layers](#architecture-layers)
- [Domain Layer Testing](#domain-layer-testing)
- [Data Layer Testing](#data-layer-testing)
- [Presentation Layer Testing](#presentation-layer-testing)
- [Testing Dependencies](#testing-dependencies)
- [Complete Example](#complete-example)

## Overview

Clean Architecture separates concerns into layers:

```
Presentation (UI)
    ↓ (uses)
Domain (Business Logic)
    ↓ (uses)
Data (Implementation)
```

**Testing Strategy:**
- Domain: Pure logic, no dependencies
- Data: Mock external sources
- Presentation: Mock domain layer

## Architecture Layers

### Domain Layer
- Entities (business objects)
- Use Cases (business rules)
- Repository interfaces
- Failures (error types)

### Data Layer
- Repository implementations
- Data sources (remote/local)
- DTOs (data transfer objects)
- Mappers (DTO ↔ Entity)

### Presentation Layer
- BLoC/Cubit (state management)
- UI Widgets
- State classes

## Domain Layer Testing

### Testing Entities

```dart
// Domain entity
class User {
  const User({
    required this.id,
    required this.email,
    this.name,
  });

  final String id;
  final String email;
  final String? name;

  bool get hasName => name != null && name!.isNotEmpty;
  String get displayName => hasName ? name! : email;
}

// Tests
group('User Entity', () {
  test('hasName returns true when name exists', () {
    const user = User(id: '1', email: 'test@example.com', name: 'John');
    expect(user.hasName, isTrue);
  });

  test('hasName returns false when name is null', () {
    const user = User(id: '1', email: 'test@example.com');
    expect(user.hasName, isFalse);
  });

  test('displayName returns name when available', () {
    const user = User(id: '1', email: 'test@example.com', name: 'John');
    expect(user.displayName, 'John');
  });

  test('displayName returns email when name unavailable', () {
    const user = User(id: '1', email: 'test@example.com');
    expect(user.displayName, 'test@example.com');
  });
});
```

### Testing Use Cases

```dart
// Use case
class GetUserUseCase {
  const GetUserUseCase(this._repository);

  final UserRepository _repository;

  TaskEither<UserFailure, User> call(String userId) {
    if (userId.isEmpty) {
      return TaskEither.left(const UserFailure.invalidId());
    }
    return _repository.getUser(userId);
  }
}

// Tests
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepository;
  late GetUserUseCase useCase;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUserUseCase(mockRepository);
  });

  group('GetUserUseCase', () {
    const testUser = User(id: '1', email: 'test@example.com');

    test('returns user when repository succeeds', () async {
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) => TaskEither.right(testUser));

      final result = await useCase('1').run();

      expect(result.isRight(), isTrue);
      result.fold(
        (l) => fail('Should be right'),
        (r) => expect(r, testUser),
      );
      verify(() => mockRepository.getUser('1')).called(1);
    });

    test('returns failure when repository fails', () async {
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) => TaskEither.left(
            const UserFailure.notFound(),
          ));

      final result = await useCase('1').run();

      expect(result.isLeft(), isTrue);
      result.fold(
        (l) => expect(l, const UserFailure.notFound()),
        (r) => fail('Should be left'),
      );
    });

    test('returns invalid failure when userId is empty', () async {
      final result = await useCase('').run();

      expect(result.isLeft(), isTrue);
      result.fold(
        (l) => expect(l, const UserFailure.invalidId()),
        (r) => fail('Should be left'),
      );
      verifyNever(() => mockRepository.getUser(any()));
    });
  });
}
```

### Testing Complex Use Cases

```dart
// Use case with multiple steps
class UpdateUserProfileUseCase {
  const UpdateUserProfileUseCase(this._repository, this._validator);

  final UserRepository _repository;
  final UserValidator _validator;

  TaskEither<UserFailure, User> call(String userId, UserProfile profile) {
    return TaskEither.Do(($) async {
      // Validate input
      final validationResult = _validator.validate(profile);
      if (!validationResult.isValid) {
        return left(UserFailure.validation(validationResult.errors));
      }

      // Get current user
      final user = await $(
        _repository.getUser(userId).mapLeft((e) => e),
      );

      // Update profile
      final updatedUser = user.copyWith(
        name: profile.name,
        bio: profile.bio,
      );

      // Save changes
      await $(_repository.updateUser(updatedUser));

      return right(updatedUser);
    });
  }
}

// Tests
group('UpdateUserProfileUseCase', () {
  test('successfully updates user profile', () async {
    final profile = UserProfile(name: 'John', bio: 'Developer');
    final currentUser = User(id: '1', email: 'test@example.com');
    final updatedUser = currentUser.copyWith(
      name: profile.name,
      bio: profile.bio,
    );

    when(() => mockValidator.validate(profile))
        .thenReturn(ValidationResult.valid());
    when(() => mockRepository.getUser('1'))
        .thenAnswer((_) => TaskEither.right(currentUser));
    when(() => mockRepository.updateUser(any()))
        .thenAnswer((_) => TaskEither.right(unit));

    final result = await useCase('1', profile).run();

    expect(result.isRight(), isTrue);
    verify(() => mockValidator.validate(profile)).called(1);
    verify(() => mockRepository.getUser('1')).called(1);
    verify(() => mockRepository.updateUser(any())).called(1);
  });

  test('returns validation failure for invalid input', () async {
    final profile = UserProfile(name: '', bio: '');

    when(() => mockValidator.validate(profile))
        .thenReturn(ValidationResult.invalid(['Name required']));

    final result = await useCase('1', profile).run();

    expect(result.isLeft(), isTrue);
    verifyNever(() => mockRepository.getUser(any()));
  });
});
```

### Testing Failures

```dart
// Failure types
@freezed
class UserFailure with _$UserFailure {
  const factory UserFailure.notFound() = _NotFound;
  const factory UserFailure.networkError() = _NetworkError;
  const factory UserFailure.unauthorized() = _Unauthorized;
  const factory UserFailure.validation(List<String> errors) = _Validation;
}

// Tests
group('UserFailure', () {
  test('creates notFound failure', () {
    const failure = UserFailure.notFound();
    expect(failure, isA<_NotFound>());
  });

  test('validation failure contains errors', () {
    const errors = ['Email required', 'Password too short'];
    const failure = UserFailure.validation(errors);

    failure.when(
      notFound: () => fail('Wrong type'),
      networkError: () => fail('Wrong type'),
      unauthorized: () => fail('Wrong type'),
      validation: (e) => expect(e, errors),
    );
  });
});
```

## Data Layer Testing

### Testing Repository Implementations

See [REPOSITORY_TESTING.md](REPOSITORY_TESTING.md) for comprehensive repository testing patterns.

### Testing Data Sources

```dart
// Remote data source
class UserRemoteDataSource {
  const UserRemoteDataSource(this._client);

  final HttpClient _client;

  Future<UserDto> getUser(String id) async {
    final response = await _client.get('/users/$id');
    
    if (response.statusCode == 200) {
      return UserDto.fromJson(response.data);
    }
    throw ServerException(response.statusCode);
  }
}

// Tests
class MockHttpClient extends Mock implements HttpClient {}

void main() {
  late MockHttpClient mockClient;
  late UserRemoteDataSource dataSource;

  setUp(() {
    mockClient = MockHttpClient();
    dataSource = UserRemoteDataSource(mockClient);
  });

  group('UserRemoteDataSource', () {
    test('returns UserDto on 200 response', () async {
      when(() => mockClient.get('/users/1')).thenAnswer(
        (_) async => Response(
          statusCode: 200,
          data: {'id': '1', 'email': 'test@example.com'},
        ),
      );

      final result = await dataSource.getUser('1');

      expect(result.id, '1');
      expect(result.email, 'test@example.com');
    });

    test('throws ServerException on 500', () {
      when(() => mockClient.get(any())).thenAnswer(
        (_) async => Response(statusCode: 500, data: null),
      );

      expect(
        () => dataSource.getUser('1'),
        throwsA(isA<ServerException>()),
      );
    });
  });
}
```

### Testing DTOs and Mappers

```dart
// DTO
class UserDto {
  const UserDto({
    required this.id,
    required this.email,
    this.name,
  });

  final String id;
  final String email;
  final String? name;

  factory UserDto.fromJson(Map<String, dynamic> json) {
    return UserDto(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String?,
    );
  }

  User toDomain() {
    return User(id: id, email: email, name: name);
  }
}

// Tests
group('UserDto', () {
  test('fromJson creates UserDto correctly', () {
    final json = {
      'id': '1',
      'email': 'test@example.com',
      'name': 'John',
    };

    final dto = UserDto.fromJson(json);

    expect(dto.id, '1');
    expect(dto.email, 'test@example.com');
    expect(dto.name, 'John');
  });

  test('toDomain converts to User entity', () {
    const dto = UserDto(
      id: '1',
      email: 'test@example.com',
      name: 'John',
    );

    final user = dto.toDomain();

    expect(user.id, dto.id);
    expect(user.email, dto.email);
    expect(user.name, dto.name);
  });

  test('handles null name correctly', () {
    const dto = UserDto(id: '1', email: 'test@example.com');
    final user = dto.toDomain();

    expect(user.name, isNull);
  });
});
```

## Presentation Layer Testing

### Testing BLoC/Cubit

See [BLOC_CUBIT_TESTING.md](BLOC_CUBIT_TESTING.md) for comprehensive BLoC testing patterns.

### Testing State Classes

```dart
// State with Freezed
@freezed
class UserState with _$UserState {
  const factory UserState({
    @Default(Status.initial) Status status,
    User? user,
    UserFailure? failure,
  }) = _UserState;
}

// Tests
group('UserState', () {
  test('initial state has correct defaults', () {
    const state = UserState();

    expect(state.status, Status.initial);
    expect(state.user, isNull);
    expect(state.failure, isNull);
  });

  test('copyWith updates fields correctly', () {
    const initial = UserState();
    const user = User(id: '1', email: 'test@example.com');
    
    final updated = initial.copyWith(
      status: Status.loaded,
      user: user,
    );

    expect(updated.status, Status.loaded);
    expect(updated.user, user);
    expect(updated.failure, isNull);
  });

  test('equality works correctly', () {
    const state1 = UserState(status: Status.loading);
    const state2 = UserState(status: Status.loading);
    const state3 = UserState(status: Status.loaded);

    expect(state1, state2);
    expect(state1, isNot(state3));
  });
});
```

### Testing Widget Integration

See [WIDGET_TESTING.md](WIDGET_TESTING.md) for comprehensive widget testing patterns.

## Testing Dependencies

### Dependency Injection Testing

```dart
// Service locator setup
final getIt = GetIt.instance;

void setupDependencies() {
  // Data sources
  getIt.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(getIt()),
  );

  // Repositories
  getIt.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(getIt()),
  );

  // Use cases
  getIt.registerLazySingleton(() => GetUserUseCase(getIt()));
}

// Tests
group('Dependency Injection', () {
  setUp(() {
    setupDependencies();
  });

  tearDown(() {
    getIt.reset();
  });

  test('resolves UserRepository', () {
    final repository = getIt<UserRepository>();
    expect(repository, isA<UserRepositoryImpl>());
  });

  test('resolves GetUserUseCase with dependencies', () {
    final useCase = getIt<GetUserUseCase>();
    expect(useCase, isA<GetUserUseCase>());
  });
});
```

### Testing with Provider

```dart
testWidgets('provides dependencies correctly', (tester) async {
  final mockRepository = MockUserRepository();

  await tester.pumpWidget(
    RepositoryProvider<UserRepository>.value(
      value: mockRepository,
      child: BlocProvider(
        create: (context) => UserCubit(context.read<UserRepository>()),
        child: const MyApp(),
      ),
    ),
  );

  // Test with injected dependencies
});
```

## Complete Example

### Feature: User Profile

#### Domain Layer

```dart
// Entity
class UserProfile {
  const UserProfile({
    required this.userId,
    required this.name,
    required this.email,
    this.bio,
    this.avatarUrl,
  });

  final String userId;
  final String name;
  final String email;
  final String? bio;
  final String? avatarUrl;
}

// Repository interface
abstract class UserProfileRepository {
  TaskEither<ProfileFailure, UserProfile> getProfile(String userId);
  TaskEither<ProfileFailure, Unit> updateProfile(UserProfile profile);
}

// Use case
class GetUserProfileUseCase {
  const GetUserProfileUseCase(this._repository);

  final UserProfileRepository _repository;

  TaskEither<ProfileFailure, UserProfile> call(String userId) {
    return _repository.getProfile(userId);
  }
}
```

#### Domain Tests

```dart
void main() {
  late MockUserProfileRepository mockRepository;
  late GetUserProfileUseCase useCase;

  setUp(() {
    mockRepository = MockUserProfileRepository();
    useCase = GetUserProfileUseCase(mockRepository);
  });

  group('GetUserProfileUseCase', () {
    const testProfile = UserProfile(
      userId: '1',
      name: 'John Doe',
      email: 'john@example.com',
    );

    test('returns profile from repository', () async {
      when(() => mockRepository.getProfile('1'))
          .thenAnswer((_) => TaskEither.right(testProfile));

      final result = await useCase('1').run();

      expect(result.isRight(), isTrue);
      verify(() => mockRepository.getProfile('1')).called(1);
    });
  });
}
```

#### Data Layer

```dart
// DTO
class UserProfileDto {
  const UserProfileDto({
    required this.userId,
    required this.name,
    required this.email,
    this.bio,
    this.avatarUrl,
  });

  final String userId;
  final String name;
  final String email;
  final String? bio;
  final String? avatarUrl;

  factory UserProfileDto.fromJson(Map<String, dynamic> json) {
    return UserProfileDto(
      userId: json['user_id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      bio: json['bio'] as String?,
      avatarUrl: json['avatar_url'] as String?,
    );
  }

  UserProfile toDomain() {
    return UserProfile(
      userId: userId,
      name: name,
      email: email,
      bio: bio,
      avatarUrl: avatarUrl,
    );
  }
}

// Repository implementation
class UserProfileRepositoryImpl implements UserProfileRepository {
  const UserProfileRepositoryImpl(this._dataSource);

  final UserProfileDataSource _dataSource;

  @override
  TaskEither<ProfileFailure, UserProfile> getProfile(String userId) {
    return TaskEither.tryCatch(
      () async {
        final dto = await _dataSource.getProfile(userId);
        return dto.toDomain();
      },
      (error, stackTrace) => _mapError(error),
    );
  }

  ProfileFailure _mapError(Object error) {
    if (error is NetworkException) {
      return const ProfileFailure.network();
    }
    if (error is NotFoundException) {
      return const ProfileFailure.notFound();
    }
    return ProfileFailure.unknown(error.toString());
  }
}
```

#### Data Tests

```dart
void main() {
  late MockUserProfileDataSource mockDataSource;
  late UserProfileRepositoryImpl repository;

  setUp(() {
    mockDataSource = MockUserProfileDataSource();
    repository = UserProfileRepositoryImpl(mockDataSource);
  });

  group('UserProfileRepository', () {
    final testDto = UserProfileDto(
      userId: '1',
      name: 'John',
      email: 'john@example.com',
    );

    test('returns profile on success', () async {
      when(() => mockDataSource.getProfile('1'))
          .thenAnswer((_) async => testDto);

      final result = await repository.getProfile('1').run();

      expect(result.isRight(), isTrue);
      verify(() => mockDataSource.getProfile('1')).called(1);
    });

    test('returns network failure on NetworkException', () async {
      when(() => mockDataSource.getProfile(any()))
          .thenThrow(const NetworkException());

      final result = await repository.getProfile('1').run();

      expect(result.isLeft(), isTrue);
      result.fold(
        (l) => expect(l, const ProfileFailure.network()),
        (r) => fail('Should be left'),
      );
    });
  });
}
```

#### Presentation Layer

```dart
// Cubit
class UserProfileCubit extends Cubit<UserProfileState> {
  UserProfileCubit(this._getProfileUseCase)
      : super(const UserProfileState());

  final GetUserProfileUseCase _getProfileUseCase;

  Future<void> loadProfile(String userId) async {
    emit(state.copyWith(status: Status.loading));

    final result = await _getProfileUseCase(userId).run();

    result.fold(
      (failure) => emit(state.copyWith(
        status: Status.error,
        failure: failure,
      )),
      (profile) => emit(state.copyWith(
        status: Status.loaded,
        profile: profile,
      )),
    );
  }
}
```

#### Presentation Tests

```dart
void main() {
  late MockGetUserProfileUseCase mockUseCase;
  late UserProfileCubit cubit;

  setUp(() {
    mockUseCase = MockGetUserProfileUseCase();
    cubit = UserProfileCubit(mockUseCase);
  });

  tearDown(() => cubit.close());

  group('UserProfileCubit', () {
    const testProfile = UserProfile(
      userId: '1',
      name: 'John',
      email: 'john@example.com',
    );

    blocTest<UserProfileCubit, UserProfileState>(
      'loads profile successfully',
      build: () {
        when(() => mockUseCase('1'))
            .thenAnswer((_) => TaskEither.right(testProfile));
        return cubit;
      },
      act: (cubit) => cubit.loadProfile('1'),
      expect: () => [
        const UserProfileState(status: Status.loading),
        UserProfileState(status: Status.loaded, profile: testProfile),
      ],
    );
  });
}
```

## Best Practices

1. **Test each layer independently**
   - Domain tests don't depend on data layer
   - Data tests mock external dependencies
   - Presentation tests mock domain layer

2. **Use dependency injection**
   - Makes testing easier with mocks
   - Follows SOLID principles

3. **Keep domain layer pure**
   - No Flutter/external dependencies
   - Pure business logic

4. **Test error flows**
   - Each layer should handle failures

5. **Use TaskEither consistently**
   - Explicit error handling
   - Composable operations

6. **Test transformations**
   - DTO ↔ Entity conversions
   - State updates

7. **Mock external dependencies only**
   - Don't mock what you're testing

8. **Test use case orchestration**
   - Multiple repository calls
   - Business rule validation

9. **Keep tests focused**
   - One behavior per test

10. **Use descriptive names**
    - Test names explain the scenario
