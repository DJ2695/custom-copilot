---
name: flutter-clean-architecture
description: 'Expert Flutter Clean Architecture implementation with BLoC/Cubit state management, AutoRoute navigation, fpdart functional programming, and Freezed models. Use when: creating new features/modules, implementing cubits/blocs, setting up repositories/datasources, configuring navigation routes, writing domain entities/failures, or any task involving Flutter project architecture. Keywords: flutter, bloc, cubit, autoroute, freezed, fpdart, repository, datasource, clean architecture, feature module.'
---

# Flutter Clean Architecture Skill

Implements Clean Architecture patterns for Flutter: BLoC state management, AutoRoute navigation, fpdart Either types, Freezed models, and ServiceLocator DI.

## When to Use This Skill

Trigger this skill when working on:
- **Feature creation**: New modules with full clean architecture structure
- **State management**: Implementing Cubit (simple) or Bloc (complex event handling)
- **Data layer**: Creating repositories, datasources, error handling
- **Navigation**: Setting up AutoRoute pages and router configuration
- **Domain modeling**: Writing entities, failures with Freezed
- **Architecture questions**: Project structure, DI, or error flow patterns

## Architecture Conventions

| Aspect | Required Pattern | ❌ Don't Use |
|--------|-----------------|-------------|
| **Routing** | AutoRoute (`@RoutePage`, `AppRouter`) | GoRouter |
| **DI** | `ServiceLocator.I<Type>()` | Raw `getIt` |
| **Either** | fpdart `TaskEither` with `.run()` | dartz |
| **Failures** | Domain-specific (AuthFailure, etc.) | Generic Failure |

## Templates Reference

All templates in `templates/` directory. Copy, replace `${Feature}`/`${feature}` placeholders, run build_runner:

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `cubit.dart.template` | Simple state (few methods) | Straightforward data fetching |
| `bloc.dart.template` | Complex events (debounce/throttle) | Advanced async flows |
| `repository.dart.template` | Domain interface | Abstract data operations |
| `repository_impl.dart.template` | Firebase/API implementation | Concrete data layer |
| `datasource.dart.template` | Remote data + exceptions | External API calls |
| `entity.dart.template` | Domain model (Freezed + JSON) | Data structures |
| `failure.dart.template` | Domain errors | Custom error types |
| `page.dart.template` | Route page + BlocProvider | New screen |

**Usage**: `${Feature}` → `FileUpload`, `${feature}` → `file_upload`, then `dart run build_runner build --delete-conflicting-outputs`

## Navigation (AutoRoute)

### Page Setup
```dart
@RoutePage()
class FeaturePage extends StatelessWidget {
  const FeaturePage({super.key, @PathParam('id') this.id});
  final String? id;
  // ...
}
```

### Router Config (`app/app.router.dart`)
```dart
@AutoRouterConfig()
class AppRouter extends RootStackRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(path: '/feature/:id', page: FeatureRoute.page),
  ];
}
```

### Navigate
```dart
context.router.navigate(FeatureRoute(id: '123'));  // Replace stack
context.router.push(FeatureRoute(id: '123'));     // Add to stack
context.router.pop();                              // Go back
```

## Dependency Injection (ServiceLocator)

**Location**: `core/di/service_locator.dart`

```dart
class ServiceLocator {
  static final GetIt I = GetIt.instance;

  static Future<void> setup() async {
    // DataSources - singleton
    I.registerLazySingleton<FeatureRemoteDataSource>(
      () => FeatureRemoteDataSource(firestore: I()),
    );

    // Repositories - singleton
    I.registerLazySingleton<FeatureRepository>(
      () => FeatureRepositoryFirebase(remoteDataSource: I()),
    );

    // Cubits/Blocs - factory (new instance each time)
    I.registerFactory<FeatureCubit>(() => FeatureCubit(I()));
  }
}

// Usage
final repo = ServiceLocator.I<FeatureRepository>();
```

## State Management

### Cubit vs Bloc Decision

| Choose Cubit | Choose Bloc |
|--------------|-------------|
| Simple data fetching | Complex event handling |
| 2-5 methods | Many distinct events |
| No transformations | Need debounce/throttle |
| Direct async calls | Event pipelines |

### Cubit Pattern
```dart
class FeatureCubit extends Cubit<FeatureState> {
  final FeatureRepository _repository;
  
  Future<void> load(String id) async {
    emit(state.copyWith(isLoading: true));
    final result = await _repository.get(id).run();  // ⚠️ .run()!
    result.fold(
      (failure) => emit(state.copyWith(failure: failure)),
      (data) => emit(state.copyWith(data: data, isLoading: false)),
    );
  }
}
```

### Bloc Pattern
```dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  FeatureBloc() : super(const FeatureState()) {
    on<LoadEvent>(_onLoad);
  }

  Future<void> _onLoad(LoadEvent event, Emitter emit) async {
    // Handle event
  }
}
```

## Repository Pattern

### Domain Interface
```dart
abstract class FeatureRepository {
  TaskEither<FeatureFailure, FeatureEntity> get(String id);
  TaskEither<FeatureFailure, List<FeatureEntity>> getAll();
  TaskEither<FeatureFailure, Unit> delete(String id);
}
```

### Data Implementation
```dart
class FeatureRepositoryFirebase implements FeatureRepository {
  final FeatureRemoteDataSource _dataSource;

  @override
  TaskEither<FeatureFailure, FeatureEntity> get(String id) {
    return TaskEither.tryCatch(
      () async => await _dataSource.fetch(id),
      (error, _) => _mapError(error),  // Convert to domain failure
    );
  }
}
```

## Error Flow

```
DataSource THROWS exception
    ↓
Repository CATCHES → Left(Failure)
    ↓
Cubit/Bloc receives Either → emits failure state
    ↓
UI shows error + retry option
```

### Domain Failures
```dart
abstract class FeatureFailure {
  const FeatureFailure(this.message);
  final String message;
}

class NotFoundFailure extends FeatureFailure {
  const NotFoundFailure() : super('Item not found');
}

class PermissionFailure extends FeatureFailure {
  const PermissionFailure() : super('Access denied');
}
```

## Feature Structure

Standard Clean Architecture folder organization:

```
features/${feature}/
├── data/
│   ├── datasources/${feature}_remote_datasource.dart
│   └── repositories/${feature}_repository_firebase.dart
├── domain/
│   ├── entities/${feature}_entity.dart
│   ├── failures/${feature}_failure.dart
│   └── repositories/${feature}_repository.dart
└── presentation/
    ├── bloc/${feature}_cubit.dart (or _bloc.dart)
    ├── pages/${feature}_page.dart
    └── widgets/${feature}_widget.dart
```

## Quick Rules

✅ **DO**
- Use AutoRoute for all navigation
- Use `ServiceLocator.I<Type>()` for DI
- Use fpdart `TaskEither` with `.run()`
- Create domain-specific failures
- Use templates as starting point
- Run build_runner after Freezed changes

❌ **DON'T**
- Use GoRouter
- Use raw `getIt`
- Use dartz
- Forget `.run()` on TaskEither
- Use generic Failure class
- Skip build_runner after code generation
