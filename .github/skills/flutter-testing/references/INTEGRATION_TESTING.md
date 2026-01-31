# Integration Testing Patterns

Comprehensive guide to Flutter integration testing for end-to-end flows, performance testing, and real device testing.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Basic Integration Tests](#basic-integration-tests)
- [Navigation Flows](#navigation-flows)
- [User Journeys](#user-journeys)
- [Performance Testing](#performance-testing)
- [Running Tests](#running-tests)
- [Firebase Test Lab](#firebase-test-lab)
- [Best Practices](#best-practices)

## Overview

Integration tests:
- Test complete app flows end-to-end
- Run on real devices or emulators
- Verify widgets work together correctly
- Test navigation and state management
- Measure app performance
- Validate critical user journeys

## Setup

### Add Dependencies

```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

### Directory Structure

```
my_app/
├── lib/
├── test/
└── integration_test/
    ├── app_test.dart
    ├── auth_flow_test.dart
    └── feature_flow_test.dart
```

### Basic Test File

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('App Integration Tests', () {
    testWidgets('basic app flow', (tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Test interactions
    });
  });
}
```

## Basic Integration Tests

### Testing App Launch

```dart
testWidgets('app launches successfully', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  expect(find.byType(MyApp), findsOneWidget);
  expect(find.byType(HomePage), findsOneWidget);
});
```

### Testing Simple Interactions

```dart
testWidgets('counter increments on button tap', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  expect(find.text('0'), findsOneWidget);

  await tester.tap(find.byIcon(Icons.add));
  await tester.pumpAndSettle();

  expect(find.text('1'), findsOneWidget);
});
```

### Testing Multiple Screens

```dart
testWidgets('navigates through multiple screens', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Home screen
  expect(find.text('Home'), findsOneWidget);

  // Navigate to detail
  await tester.tap(find.byKey(const Key('go_to_detail')));
  await tester.pumpAndSettle();

  // Detail screen
  expect(find.text('Detail'), findsOneWidget);

  // Navigate back
  await tester.tap(find.byIcon(Icons.arrow_back));
  await tester.pumpAndSettle();

  // Back on home
  expect(find.text('Home'), findsOneWidget);
});
```

## Navigation Flows

### Testing Bottom Navigation

```dart
testWidgets('bottom navigation switches tabs', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Home tab
  expect(find.text('Home Content'), findsOneWidget);

  // Tap settings tab
  await tester.tap(find.byIcon(Icons.settings));
  await tester.pumpAndSettle();

  // Settings tab
  expect(find.text('Settings Content'), findsOneWidget);
  expect(find.text('Home Content'), findsNothing);

  // Tap profile tab
  await tester.tap(find.byIcon(Icons.person));
  await tester.pumpAndSettle();

  // Profile tab
  expect(find.text('Profile Content'), findsOneWidget);
});
```

### Testing Drawer Navigation

```dart
testWidgets('drawer navigation works', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Open drawer
  await tester.tap(find.byIcon(Icons.menu));
  await tester.pumpAndSettle();

  expect(find.byType(Drawer), findsOneWidget);

  // Navigate to settings
  await tester.tap(find.text('Settings'));
  await tester.pumpAndSettle();

  expect(find.text('Settings Page'), findsOneWidget);
});
```

### Testing Deep Navigation

```dart
testWidgets('deep navigation with data passing', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Start on home
  expect(find.text('Home'), findsOneWidget);

  // Navigate to list
  await tester.tap(find.text('View List'));
  await tester.pumpAndSettle();

  // Tap first item
  await tester.tap(find.byKey(const Key('item_0')));
  await tester.pumpAndSettle();

  // Verify detail page with correct data
  expect(find.text('Detail for item 0'), findsOneWidget);

  // Navigate to edit
  await tester.tap(find.byIcon(Icons.edit));
  await tester.pumpAndSettle();

  // Verify edit page
  expect(find.text('Edit item 0'), findsOneWidget);
});
```

## User Journeys

### Authentication Flow

```dart
group('Authentication Flow', () {
  testWidgets('complete login flow', (tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    // Should show login screen
    expect(find.text('Login'), findsOneWidget);

    // Enter credentials
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_field')),
      'password123',
    );

    // Submit login
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();

    // Should navigate to home
    expect(find.text('Welcome'), findsOneWidget);
    expect(find.text('Login'), findsNothing);
  });

  testWidgets('logout flow', (tester) async {
    // Assume already logged in
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    // Open menu
    await tester.tap(find.byIcon(Icons.menu));
    await tester.pumpAndSettle();

    // Tap logout
    await tester.tap(find.text('Logout'));
    await tester.pumpAndSettle();

    // Should return to login
    expect(find.text('Login'), findsOneWidget);
  });
});
```

### CRUD Operations Flow

```dart
testWidgets('complete CRUD flow', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // CREATE
  await tester.tap(find.byIcon(Icons.add));
  await tester.pumpAndSettle();

  await tester.enterText(
    find.byKey(const Key('name_field')),
    'New Item',
  );
  await tester.tap(find.text('Save'));
  await tester.pumpAndSettle();

  expect(find.text('New Item'), findsOneWidget);

  // READ (already visible)
  expect(find.text('New Item'), findsOneWidget);

  // UPDATE
  await tester.tap(find.byKey(const Key('edit_button')));
  await tester.pumpAndSettle();

  await tester.enterText(
    find.byKey(const Key('name_field')),
    'Updated Item',
  );
  await tester.tap(find.text('Save'));
  await tester.pumpAndSettle();

  expect(find.text('Updated Item'), findsOneWidget);
  expect(find.text('New Item'), findsNothing);

  // DELETE
  await tester.tap(find.byKey(const Key('delete_button')));
  await tester.pumpAndSettle();

  await tester.tap(find.text('Confirm'));
  await tester.pumpAndSettle();

  expect(find.text('Updated Item'), findsNothing);
});
```

### Search and Filter Flow

```dart
testWidgets('search and filter flow', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Initially shows all items
  expect(find.text('Item 1'), findsOneWidget);
  expect(find.text('Item 2'), findsOneWidget);
  expect(find.text('Item 3'), findsOneWidget);

  // Enter search query
  await tester.enterText(
    find.byKey(const Key('search_field')),
    'Item 1',
  );
  await tester.pumpAndSettle(const Duration(milliseconds: 500));

  // Should show only matching items
  expect(find.text('Item 1'), findsOneWidget);
  expect(find.text('Item 2'), findsNothing);
  expect(find.text('Item 3'), findsNothing);

  // Clear search
  await tester.tap(find.byIcon(Icons.clear));
  await tester.pumpAndSettle();

  // All items visible again
  expect(find.text('Item 1'), findsOneWidget);
  expect(find.text('Item 2'), findsOneWidget);
});
```

### Form Submission Flow

```dart
testWidgets('complete form submission', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Fill form fields
  await tester.enterText(
    find.byKey(const Key('name_field')),
    'John Doe',
  );
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'john@example.com',
  );
  await tester.enterText(
    find.byKey(const Key('phone_field')),
    '1234567890',
  );

  // Select dropdown
  await tester.tap(find.byKey(const Key('category_dropdown')));
  await tester.pumpAndSettle();
  await tester.tap(find.text('Category A').last);
  await tester.pumpAndSettle();

  // Toggle checkbox
  await tester.tap(find.byKey(const Key('terms_checkbox')));
  await tester.pumpAndSettle();

  // Submit form
  await tester.tap(find.text('Submit'));
  await tester.pumpAndSettle();

  // Verify success message
  expect(find.text('Form submitted successfully'), findsOneWidget);
});
```

## Performance Testing

### Tracing Actions

```dart
testWidgets('scrolling performance', (tester) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  final listFinder = find.byType(Scrollable);
  final itemFinder = find.byKey(const ValueKey('item_50'));

  await binding.traceAction(() async {
    await tester.scrollUntilVisible(
      itemFinder,
      500.0,
      scrollable: listFinder,
    );
  }, reportKey: 'scrolling_timeline');

  expect(itemFinder, findsOneWidget);
});
```

### Measuring Frame Rendering

```dart
testWidgets('animation performance', (tester) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  await binding.watchPerformance(() async {
    await tester.tap(find.byKey(const Key('animate_button')));
    await tester.pumpAndSettle();
  }, reportKey: 'animation_performance');
});
```

### Memory Testing

```dart
testWidgets('memory usage during navigation', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Navigate through multiple screens
  for (int i = 0; i < 10; i++) {
    await tester.tap(find.text('Next'));
    await tester.pumpAndSettle();
  }

  // Navigate back
  for (int i = 0; i < 10; i++) {
    await tester.pageBack();
    await tester.pumpAndSettle();
  }

  // Verify we're back at start
  expect(find.text('Home'), findsOneWidget);
});
```

## Running Tests

### Run on Desktop

```bash
flutter test integration_test/app_test.dart
```

### Run on Android Device

```bash
flutter test integration_test/app_test.dart -d <device_id>
```

### Run on iOS Device

```bash
flutter test integration_test/app_test.dart -d <device_id>
```

### Run with Chrome (Web)

```bash
# Start chromedriver
chromedriver --port=4444

# Run tests
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/app_test.dart \
  -d chrome
```

### Run All Integration Tests

```bash
flutter test integration_test/
```

## Firebase Test Lab

### Android Setup

```bash
# Build debug APK
flutter build apk --debug

# Build test APK
cd android
./gradlew app:assembleAndroidTest
./gradlew app:assembleDebug -Ptarget=integration_test/app_test.dart
cd ..
```

### Upload to Firebase

Use Firebase Console:
1. Go to Test Lab
2. Upload APKs
3. Select devices
4. Run tests

### iOS Setup

```bash
# Build iOS app for testing
flutter build ios integration_test/app_test.dart --release

# Create payload folder
cd build/ios_integ/Build/Products/Release-iphoneos
mkdir Payload
cd Payload
ln -s ../Runner.app
cd ..
zip -r app.zip Payload
```

## Best Practices

### Use Keys for Critical Elements

```dart
// In widget code
ElevatedButton(
  key: const Key('submit_button'),
  child: const Text('Submit'),
)

// In test
await tester.tap(find.byKey(const Key('submit_button')));
```

### Wait for Animations

```dart
// Wait for all animations to complete
await tester.pumpAndSettle();

// Wait for specific duration
await tester.pump(const Duration(seconds: 1));

// Multiple pumps
await tester.pump();
await tester.pump();
```

### Handle Long Lists

```dart
testWidgets('scroll to item in long list', (tester) async {
  await tester.pumpWidget(const MyApp());

  await tester.scrollUntilVisible(
    find.text('Item 100'),
    500.0,
    scrollable: find.byType(Scrollable),
  );

  expect(find.text('Item 100'), findsOneWidget);
});
```

### Test Error Scenarios

```dart
testWidgets('handles network error gracefully', (tester) async {
  // Simulate offline mode
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  await tester.tap(find.text('Load Data'));
  await tester.pumpAndSettle();

  expect(find.text('Network Error'), findsOneWidget);
  expect(find.byType(RetryButton), findsOneWidget);
});
```

### Clean Up Between Tests

```dart
setUp(() async {
  // Clear app state before each test
  await clearDatabase();
  await clearCache();
});

tearDown(() async {
  // Clean up after tests
  await clearTestData();
});
```

### Group Related Tests

```dart
group('User Profile Flow', () {
  testWidgets('view profile', (tester) async {
    // Test
  });

  testWidgets('edit profile', (tester) async {
    // Test
  });

  testWidgets('change password', (tester) async {
    // Test
  });
});
```

### Test with Different Screen Sizes

```dart
testWidgets('responsive layout on tablet', (tester) async {
  tester.binding.window.physicalSizeTestValue = const Size(1024, 768);
  tester.binding.window.devicePixelRatioTestValue = 1.0;

  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();

  // Verify tablet layout
  expect(find.byType(TwoColumnLayout), findsOneWidget);

  addTearDown(tester.binding.window.clearPhysicalSizeTestValue);
});
```

### Mock External Services

```dart
testWidgets('integration test with mocked API', (tester) async {
  // Use mock server or dependency injection
  final mockApi = MockApiService();
  
  await tester.pumpWidget(
    MyApp(apiService: mockApi),
  );
  await tester.pumpAndSettle();

  // Test with mocked responses
});
```

## Tips

1. **Keep tests independent** - Each test should run in isolation
2. **Test critical paths first** - Focus on most important user journeys
3. **Use meaningful keys** - Makes finding widgets reliable
4. **Test on real devices** - Catch device-specific issues
5. **Monitor performance** - Use tracing for slow operations
6. **Test error states** - Network errors, validation, etc.
7. **Keep tests maintainable** - Extract common operations to helpers
8. **Run regularly** - Integrate into CI/CD pipeline
9. **Test accessibility** - Ensure app works with screen readers
10. **Document test scenarios** - Clear descriptions help maintenance
