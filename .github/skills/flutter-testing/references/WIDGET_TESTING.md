# Widget Testing Patterns

Comprehensive guide to testing Flutter widgets with flutter_test, including finders, matchers, interactions, and BLoC integration.

## Table of Contents

- [Setup](#setup)
- [Basic Widget Testing](#basic-widget-testing)
- [Finders](#finders)
- [Matchers](#matchers)
- [User Interactions](#user-interactions)
- [Testing with BLoC](#testing-with-bloc)
- [Testing Forms](#testing-forms)
- [Testing Navigation](#testing-navigation)
- [Async Widget Testing](#async-widget-testing)
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
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('description of test', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(const MyWidget());

    // Find elements
    final finder = find.text('Hello');

    // Assert
    expect(finder, findsOneWidget);
  });
}
```

## Basic Widget Testing

### Simple Widget Test

```dart
testWidgets('MyWidget displays title and message', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: MyWidget(
        title: 'Test Title',
        message: 'Test Message',
      ),
    ),
  );

  expect(find.text('Test Title'), findsOneWidget);
  expect(find.text('Test Message'), findsOneWidget);
});
```

### Testing Widget Properties

```dart
testWidgets('button has correct properties', (tester) async {
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

  final button = tester.widget<ElevatedButton>(
    find.byType(ElevatedButton),
  );

  expect(button.onPressed, isNotNull);
  expect(find.text('Click Me'), findsOneWidget);
});
```

### Testing Widget Rendering

```dart
testWidgets('card displays content correctly', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Card(
          child: ListTile(
            leading: const Icon(Icons.person),
            title: const Text('John Doe'),
            subtitle: const Text('john@example.com'),
          ),
        ),
      ),
    ),
  );

  expect(find.byType(Card), findsOneWidget);
  expect(find.byType(ListTile), findsOneWidget);
  expect(find.byIcon(Icons.person), findsOneWidget);
  expect(find.text('John Doe'), findsOneWidget);
  expect(find.text('john@example.com'), findsOneWidget);
});
```

## Finders

### Finding by Text

```dart
testWidgets('finds text widgets', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            Text('Hello'),
            Text('World'),
          ],
        ),
      ),
    ),
  );

  expect(find.text('Hello'), findsOneWidget);
  expect(find.text('World'), findsOneWidget);
  expect(find.text('Flutter'), findsNothing);
});
```

### Finding by Type

```dart
testWidgets('finds widgets by type', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            const TextField(),
            ElevatedButton(onPressed: () {}, child: const Text('Submit')),
            const CircularProgressIndicator(),
          ],
        ),
      ),
    ),
  );

  expect(find.byType(TextField), findsOneWidget);
  expect(find.byType(ElevatedButton), findsOneWidget);
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

### Finding by Key

```dart
testWidgets('finds widgets by key', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            const TextField(key: Key('email_field')),
            const TextField(key: Key('password_field')),
            ElevatedButton(
              key: const Key('submit_button'),
              onPressed: () {},
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    ),
  );

  expect(find.byKey(const Key('email_field')), findsOneWidget);
  expect(find.byKey(const Key('password_field')), findsOneWidget);
  expect(find.byKey(const Key('submit_button')), findsOneWidget);
});
```

### Finding by Icon

```dart
testWidgets('finds icons', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          leading: const Icon(Icons.menu),
          actions: [
            IconButton(
              icon: const Icon(Icons.search),
              onPressed: () {},
            ),
          ],
        ),
      ),
    ),
  );

  expect(find.byIcon(Icons.menu), findsOneWidget);
  expect(find.byIcon(Icons.search), findsOneWidget);
});
```

### Finding by Widget Instance

```dart
testWidgets('finds specific widget instance', (tester) async {
  const widget = Text('Hello');
  
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: widget,
      ),
    ),
  );

  expect(find.byWidget(widget), findsOneWidget);
});
```

### Descendant and Ancestor Finders

```dart
testWidgets('finds widgets with descendant/ancestor', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            Card(
              child: Column(
                children: [
                  const Text('Title'),
                  ElevatedButton(
                    onPressed: () {},
                    child: const Text('Action'),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ),
  );

  // Find button that is a descendant of Card
  expect(
    find.descendant(
      of: find.byType(Card),
      matching: find.byType(ElevatedButton),
    ),
    findsOneWidget,
  );

  // Find Card that is ancestor of button
  expect(
    find.ancestor(
      of: find.byType(ElevatedButton),
      matching: find.byType(Card),
    ),
    findsOneWidget,
  );
});
```

## Matchers

### Basic Matchers

```dart
testWidgets('uses various matchers', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            const Text('Hello'),
            const Text('World'),
            const Text('Flutter'),
          ],
        ),
      ),
    ),
  );

  expect(find.text('Hello'), findsOneWidget);
  expect(find.text('Missing'), findsNothing);
  expect(find.byType(Text), findsNWidgets(3));
  expect(find.text('Hello'), findsWidgets);
  expect(find.byType(Text), findsAtLeastNWidgets(1));
});
```

### Custom Matchers

```dart
Matcher hasTextColor(Color color) {
  return isA<Text>().having(
    (text) => text.style?.color,
    'text color',
    color,
  );
}

testWidgets('uses custom matcher', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Text(
          'Red Text',
          style: TextStyle(color: Colors.red),
        ),
      ),
    ),
  );

  final textWidget = tester.widget<Text>(find.text('Red Text'));
  expect(textWidget, hasTextColor(Colors.red));
});
```

## User Interactions

### Tapping

```dart
testWidgets('handles tap events', (tester) async {
  int counter = 0;

  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ElevatedButton(
          onPressed: () => counter++,
          child: const Text('Tap Me'),
        ),
      ),
    ),
  );

  expect(counter, 0);

  await tester.tap(find.byType(ElevatedButton));
  await tester.pump();

  expect(counter, 1);
});
```

### Long Press

```dart
testWidgets('handles long press', (tester) async {
  bool longPressed = false;

  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: GestureDetector(
          onLongPress: () => longPressed = true,
          child: const Text('Long Press Me'),
        ),
      ),
    ),
  );

  await tester.longPress(find.text('Long Press Me'));
  await tester.pumpAndSettle();

  expect(longPressed, isTrue);
});
```

### Text Input

```dart
testWidgets('enters text in field', (tester) async {
  final controller = TextEditingController();

  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: TextField(
          controller: controller,
          key: const Key('text_field'),
        ),
      ),
    ),
  );

  await tester.enterText(
    find.byKey(const Key('text_field')),
    'Hello Flutter',
  );
  await tester.pump();

  expect(controller.text, 'Hello Flutter');
  expect(find.text('Hello Flutter'), findsOneWidget);
});
```

### Scrolling

```dart
testWidgets('scrolls to reveal hidden widget', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ListView.builder(
          itemCount: 100,
          itemBuilder: (context, index) {
            return ListTile(
              key: Key('item_$index'),
              title: Text('Item $index'),
            );
          },
        ),
      ),
    ),
  );

  // Item 50 not visible initially
  expect(find.text('Item 50'), findsNothing);

  // Scroll until visible
  await tester.scrollUntilVisible(
    find.text('Item 50'),
    500.0,
  );

  expect(find.text('Item 50'), findsOneWidget);
});
```

### Drag

```dart
testWidgets('performs drag gesture', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Draggable(
          feedback: Container(
            width: 100,
            height: 100,
            color: Colors.blue,
          ),
          child: Container(
            width: 100,
            height: 100,
            color: Colors.red,
          ),
        ),
      ),
    ),
  );

  await tester.drag(
    find.byType(Draggable),
    const Offset(100, 100),
  );
  await tester.pumpAndSettle();
});
```

## Testing with BLoC

### Mocking Cubit in Widget Test

```dart
class MockFeatureCubit extends Mock implements FeatureCubit {}

testWidgets('displays data from cubit', (tester) async {
  final mockCubit = MockFeatureCubit();

  when(() => mockCubit.state).thenReturn(
    FeatureState(
      status: Status.loaded,
      data: const Feature(id: '1', name: 'Test'),
    ),
  );
  when(() => mockCubit.stream).thenAnswer((_) => const Stream.empty());

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<FeatureCubit>(
        create: (_) => mockCubit,
        child: const FeaturePage(),
      ),
    ),
  );

  expect(find.text('Test'), findsOneWidget);
});
```

### Testing State Changes

```dart
testWidgets('updates UI when state changes', (tester) async {
  final mockCubit = MockFeatureCubit();
  final stateController = StreamController<FeatureState>();

  when(() => mockCubit.stream).thenAnswer((_) => stateController.stream);
  when(() => mockCubit.state).thenReturn(
    const FeatureState(status: Status.initial),
  );

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<FeatureCubit>(
        create: (_) => mockCubit,
        child: const FeaturePage(),
      ),
    ),
  );

  expect(find.byType(CircularProgressIndicator), findsNothing);

  // Emit loading state
  stateController.add(const FeatureState(status: Status.loading));
  await tester.pump();

  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  // Emit loaded state
  stateController.add(
    FeatureState(
      status: Status.loaded,
      data: const Feature(id: '1', name: 'Loaded'),
    ),
  );
  await tester.pumpAndSettle();

  expect(find.byType(CircularProgressIndicator), findsNothing);
  expect(find.text('Loaded'), findsOneWidget);

  stateController.close();
});
```

### Testing BLoC Interactions

```dart
testWidgets('triggers cubit method on button tap', (tester) async {
  final mockCubit = MockFeatureCubit();

  when(() => mockCubit.state).thenReturn(const FeatureState());
  when(() => mockCubit.stream).thenAnswer((_) => const Stream.empty());
  when(() => mockCubit.loadData()).thenAnswer((_) async {});

  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider<FeatureCubit>(
        create: (_) => mockCubit,
        child: const FeaturePage(),
      ),
    ),
  );

  await tester.tap(find.byKey(const Key('load_button')));
  await tester.pump();

  verify(() => mockCubit.loadData()).called(1);
});
```

### Multiple BLoC Providers

```dart
testWidgets('works with multiple providers', (tester) async {
  final mockAuthCubit = MockAuthCubit();
  final mockFeatureCubit = MockFeatureCubit();

  when(() => mockAuthCubit.state).thenReturn(
    const AuthState(isAuthenticated: true),
  );
  when(() => mockAuthCubit.stream).thenAnswer((_) => const Stream.empty());

  when(() => mockFeatureCubit.state).thenReturn(const FeatureState());
  when(() => mockFeatureCubit.stream).thenAnswer((_) => const Stream.empty());

  await tester.pumpWidget(
    MaterialApp(
      home: MultiBlocProvider(
        providers: [
          BlocProvider<AuthCubit>(create: (_) => mockAuthCubit),
          BlocProvider<FeatureCubit>(create: (_) => mockFeatureCubit),
        ],
        child: const FeaturePage(),
      ),
    ),
  );

  // Test widget with both providers
});
```

## Testing Forms

### Form Validation

```dart
testWidgets('validates form fields', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Form(
          child: Column(
            children: [
              TextFormField(
                key: const Key('email_field'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Email is required';
                  }
                  if (!value.contains('@')) {
                    return 'Invalid email';
                  }
                  return null;
                },
              ),
              ElevatedButton(
                key: const Key('submit_button'),
                onPressed: () {},
                child: const Text('Submit'),
              ),
            ],
          ),
        ),
      ),
    ),
  );

  // Submit without entering text
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pump();

  expect(find.text('Email is required'), findsOneWidget);

  // Enter invalid email
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'invalidemail',
  );
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pump();

  expect(find.text('Invalid email'), findsOneWidget);

  // Enter valid email
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pump();

  expect(find.text('Email is required'), findsNothing);
  expect(find.text('Invalid email'), findsNothing);
});
```

## Testing Navigation

### Basic Navigation

```dart
testWidgets('navigates to detail page', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: ElevatedButton(
          onPressed: () {},
          child: const Text('Go to Detail'),
        ),
      ),
      routes: {
        '/detail': (context) => const DetailPage(),
      },
    ),
  );

  await tester.tap(find.text('Go to Detail'));
  await tester.pumpAndSettle();

  expect(find.byType(DetailPage), findsOneWidget);
});
```

### Navigation with Arguments

```dart
testWidgets('passes arguments during navigation', (tester) async {
  String? receivedId;

  await tester.pumpWidget(
    MaterialApp(
      home: Builder(
        builder: (context) {
          return ElevatedButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => DetailPage(id: 'test-id'),
                ),
              );
            },
            child: const Text('Navigate'),
          );
        },
      ),
    ),
  );

  await tester.tap(find.text('Navigate'));
  await tester.pumpAndSettle();

  // Verify DetailPage received correct id
  final detailPage = tester.widget<DetailPage>(find.byType(DetailPage));
  expect(detailPage.id, 'test-id');
});
```

## Async Widget Testing

### Pump and PumpAndSettle

```dart
testWidgets('uses pump for single frame', (tester) async {
  await tester.pumpWidget(const MyWidget());
  
  // Advances by one frame
  await tester.pump();
  
  // Advances by specific duration
  await tester.pump(const Duration(seconds: 1));
});

testWidgets('uses pumpAndSettle for animations', (tester) async {
  await tester.pumpWidget(const MyAnimatedWidget());
  
  await tester.tap(find.byType(ElevatedButton));
  
  // Waits for all animations and timers to complete
  await tester.pumpAndSettle();
  
  expect(find.text('Animation Complete'), findsOneWidget);
});
```

### Testing FutureBuilder

```dart
testWidgets('tests FutureBuilder states', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: FutureBuilder<String>(
          future: Future.delayed(
            const Duration(milliseconds: 100),
            () => 'Data Loaded',
          ),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            }
            if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            }
            return Text(snapshot.data ?? 'No Data');
          },
        ),
      ),
    ),
  );

  // Initially loading
  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  // Wait for future to complete
  await tester.pumpAndSettle();

  // Data loaded
  expect(find.text('Data Loaded'), findsOneWidget);
  expect(find.byType(CircularProgressIndicator), findsNothing);
});
```

## Complete Examples

### Login Page Test

```dart
class MockAuthCubit extends Mock implements AuthCubit {}

void main() {
  late MockAuthCubit mockAuthCubit;

  setUp(() {
    mockAuthCubit = MockAuthCubit();
  });

  group('LoginPage', () {
    testWidgets('renders correctly', (tester) async {
      when(() => mockAuthCubit.state).thenReturn(const AuthState());
      when(() => mockAuthCubit.stream).thenAnswer((_) => const Stream.empty());

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider<AuthCubit>(
            create: (_) => mockAuthCubit,
            child: const LoginPage(),
          ),
        ),
      );

      expect(find.byKey(const Key('email_field')), findsOneWidget);
      expect(find.byKey(const Key('password_field')), findsOneWidget);
      expect(find.byKey(const Key('login_button')), findsOneWidget);
    });

    testWidgets('submits login on button press', (tester) async {
      when(() => mockAuthCubit.state).thenReturn(const AuthState());
      when(() => mockAuthCubit.stream).thenAnswer((_) => const Stream.empty());
      when(() => mockAuthCubit.login(any(), any()))
          .thenAnswer((_) async {});

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider<AuthCubit>(
            create: (_) => mockAuthCubit,
            child: const LoginPage(),
          ),
        ),
      );

      await tester.enterText(
        find.byKey(const Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'password123',
      );

      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pump();

      verify(() => mockAuthCubit.login('test@example.com', 'password123'))
          .called(1);
    });

    testWidgets('shows loading indicator when authenticating', (tester) async {
      when(() => mockAuthCubit.state).thenReturn(
        const AuthState(status: AuthStatus.authenticating),
      );
      when(() => mockAuthCubit.stream).thenAnswer((_) => const Stream.empty());

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider<AuthCubit>(
            create: (_) => mockAuthCubit,
            child: const LoginPage(),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows error message on failure', (tester) async {
      final controller = StreamController<AuthState>();

      when(() => mockAuthCubit.state).thenReturn(const AuthState());
      when(() => mockAuthCubit.stream).thenAnswer((_) => controller.stream);

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider<AuthCubit>(
            create: (_) => mockAuthCubit,
            child: const LoginPage(),
          ),
        ),
      );

      controller.add(
        const AuthState(
          status: AuthStatus.failure,
          errorMessage: 'Invalid credentials',
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Invalid credentials'), findsOneWidget);

      controller.close();
    });
  });
}
```

## Best Practices

1. **Always wrap widgets in MaterialApp or WidgetsApp**
   - Provides necessary context for Material widgets

2. **Use keys for reliable widget finding**
   - Especially important for similar widgets

3. **Use `pumpAndSettle()` after async operations**
   - Ensures all animations and timers complete

4. **Mock BLoC/Cubit dependencies**
   - Don't use real cubits in widget tests

5. **Test user flows, not implementation**
   - Focus on what users see and do

6. **Use descriptive keys**
   - Makes tests more maintainable

7. **Clean up resources**
   - Close streams and controllers

8. **Test accessibility**
   - Ensure widgets work with screen readers

9. **Test different screen sizes**
   - Use `tester.binding.window.physicalSizeTestValue`

10. **Keep tests focused**
    - One behavior per test
