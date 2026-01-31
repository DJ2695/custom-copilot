# shadcn_flutter UI Patterns

Common patterns and templates for building UI with shadcn_flutter.

---

## Page Structure

### Basic Page Layout

```dart
class MyPage extends StatelessWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      headers: [
        AppBar(
          title: const Text('Page Title'),
          actions: [
            IconButton.ghost(
              icon: const Icon(LucideIcons.settings),
              onPressed: () {},
            ),
          ],
        ),
      ],
      child: SingleChildScrollView(
        padding: EdgeInsets.all(24 * theme.scaling),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Section Title').h2(),
            Gap(Spacing.md),
            // Content here
          ],
        ),
      ),
    );
  }
}
```

### Page with Loading State

```dart
class DataPage extends StatefulWidget {
  const DataPage({super.key});

  @override
  State<DataPage> createState() => _DataPageState();
}

class _DataPageState extends State<DataPage> {
  bool _isLoading = true;
  List<Item> _items = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      _items = await fetchItems();
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      headers: [
        AppBar(
          title: const Text('Items'),
          actions: [
            IconButton.ghost(
              icon: const Icon(LucideIcons.refreshCw),
              onPressed: _loadData,
            ).ignoreSkeleton(),
          ],
        ),
      ],
      child: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          ..._items.map((item) => ItemCard(item: item)),
        ],
      ).asSkeleton(enabled: _isLoading),
    );
  }
}
```

---

## Form Patterns

### Basic Form

```dart
class BasicForm extends StatefulWidget {
  const BasicForm({super.key});

  @override
  State<BasicForm> createState() => _BasicFormState();
}

class _BasicFormState extends State<BasicForm> {
  final _controller = FormController();
  bool _isSubmitting = false;

  Future<void> _handleSubmit(Map<FormKey, dynamic> values) async {
    setState(() => _isSubmitting = true);
    try {
      final email = values[FormKey<String>('email')] as String;
      final name = values[FormKey<String>('name')] as String;
      await submitForm(email: email, name: name);
    } finally {
      setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      controller: _controller,
      onSubmit: _handleSubmit,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextField(
            key: FormKey<String>('email'),
            placeholder: const Text('Email'),
            validator: EmailValidator(),
            keyboardType: TextInputType.emailAddress,
          ),
          Gap(Spacing.md),
          TextField(
            key: FormKey<String>('name'),
            placeholder: const Text('Full Name'),
            validator: RequiredValidator(),
          ),
          Gap(Spacing.lg),
          Button.primary(
            onPressed: _isSubmitting ? null : () => _controller.submit(),
            child: _isSubmitting
                ? const CircularProgress(value: null)
                : const Text('Submit'),
          ),
        ],
      ),
    );
  }
}
```

### Form with Multiple Input Types

```dart
Form(
  controller: controller,
  onSubmit: handleSubmit,
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      // Text input
      TextField(
        key: FormKey<String>('username'),
        placeholder: const Text('Username'),
        validator: MinLengthValidator(3),
        features: [InputClearFeature()],
      ),
      Gap(Spacing.md),

      // Select dropdown
      Select<String>(
        key: FormKey<String>('role'),
        placeholder: const Text('Select role'),
        itemBuilder: (context, value) => Text(value),
        popup: (context) => SelectPopup(
          children: [
            SelectItem(value: 'admin', child: Text('Admin')),
            SelectItem(value: 'user', child: Text('User')),
            SelectItem(value: 'guest', child: Text('Guest')),
          ],
        ),
      ),
      Gap(Spacing.md),

      // Checkbox
      Row(
        children: [
          Checkbox(
            key: FormKey<CheckboxState>('terms'),
            state: CheckboxState.unchecked,
            onChanged: (state) {},
          ),
          Gap(Spacing.sm),
          const Text('I agree to the terms').small(),
        ],
      ),
      Gap(Spacing.md),

      // Date picker
      DatePicker(
        key: FormKey<DateTime>('birthdate'),
        placeholder: const Text('Select birth date'),
        mode: PromptMode.popover,
      ),
      Gap(Spacing.lg),

      Button.primary(
        onPressed: () => controller.submit(),
        child: const Text('Create Account'),
      ),
    ],
  ),
)
```

---

## Dialog Patterns

### Confirmation Dialog

```dart
Future<bool?> showConfirmDialog(
  BuildContext context, {
  required String title,
  required String message,
  String confirmText = 'Confirm',
  String cancelText = 'Cancel',
  bool isDestructive = false,
}) {
  return showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        Button.ghost(
          onPressed: () => Navigator.pop(context, false),
          child: Text(cancelText),
        ),
        isDestructive
            ? Button.destructive(
                onPressed: () => Navigator.pop(context, true),
                child: Text(confirmText),
              )
            : Button.primary(
                onPressed: () => Navigator.pop(context, true),
                child: Text(confirmText),
              ),
      ],
    ),
  );
}

// Usage
final confirmed = await showConfirmDialog(
  context,
  title: 'Delete Item',
  message: 'Are you sure you want to delete this item? This cannot be undone.',
  confirmText: 'Delete',
  isDestructive: true,
);
if (confirmed == true) {
  deleteItem();
}
```

### Form Dialog

```dart
Future<Map<String, dynamic>?> showFormDialog(BuildContext context) {
  final controller = FormController();
  
  return showDialog<Map<String, dynamic>>(
    context: context,
    builder: (context) => Dialog(
      child: Container(
        constraints: const BoxConstraints(maxWidth: 400),
        padding: const EdgeInsets.all(24),
        child: Form(
          controller: controller,
          onSubmit: (values) {
            Navigator.pop(context, values);
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('Add Item').h3(),
              Gap(Spacing.lg),
              TextField(
                key: FormKey<String>('name'),
                placeholder: const Text('Item name'),
                validator: RequiredValidator(),
              ),
              Gap(Spacing.md),
              TextField(
                key: FormKey<String>('description'),
                placeholder: const Text('Description'),
                maxLines: 3,
              ),
              Gap(Spacing.lg),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Button.ghost(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Cancel'),
                  ),
                  Gap(Spacing.sm),
                  Button.primary(
                    onPressed: () => controller.submit(),
                    child: const Text('Add'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    ),
  );
}
```

---

## Toast Patterns

### Success Toast

```dart
void showSuccessToast(BuildContext context, String message) {
  showToast(
    context: context,
    location: ToastLocation.bottomRight,
    builder: (context, overlay) => Toast(
      leading: Icon(LucideIcons.checkCircle).iconPrimary(),
      title: const Text('Success'),
      description: Text(message),
      trailing: IconButton.ghost(
        icon: const Icon(LucideIcons.x),
        onPressed: overlay.close,
      ),
    ),
  );
}
```

### Error Toast

```dart
void showErrorToast(BuildContext context, String message) {
  showToast(
    context: context,
    location: ToastLocation.bottomRight,
    builder: (context, overlay) => Toast(
      leading: Icon(LucideIcons.alertCircle).iconDestructiveForeground(),
      title: const Text('Error'),
      description: Text(message),
      trailing: IconButton.ghost(
        icon: const Icon(LucideIcons.x),
        onPressed: overlay.close,
      ),
    ),
  );
}
```

---

## List Patterns

### Basic List with Actions

```dart
ListView(
  padding: const EdgeInsets.all(16),
  children: items.map((item) => Card(
    filled: true,
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Avatar(initials: item.initials),
          Gap(Spacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.name).medium(),
                Text(item.subtitle).small().muted(),
              ],
            ),
          ),
          DropdownMenu(
            trigger: IconButton.ghost(
              icon: const Icon(LucideIcons.moreVertical),
            ),
            children: [
              MenuItem(
                leading: const Icon(LucideIcons.edit),
                child: const Text('Edit'),
                onPressed: () => editItem(item),
              ),
              MenuItem(
                leading: const Icon(LucideIcons.trash),
                child: const Text('Delete'),
                onPressed: () => deleteItem(item),
              ),
            ],
          ),
        ],
      ),
    ),
  )).toList(),
)
```

### Empty State

```dart
Widget buildEmptyState() {
  return Center(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(LucideIcons.inbox).iconX3Large().iconMutedForeground(),
        Gap(Spacing.md),
        const Text('No items yet').large().muted(),
        Gap(Spacing.sm),
        const Text('Add your first item to get started').small().muted(),
        Gap(Spacing.lg),
        Button.primary(
          leading: const Icon(LucideIcons.plus),
          onPressed: () => addItem(),
          child: const Text('Add Item'),
        ),
      ],
    ),
  ).withPadding(all: 48);
}
```

---

## Card Patterns

### Info Card

```dart
Card(
  filled: true,
  fillColor: theme.colorScheme.card,
  borderRadius: theme.borderRadiusMd,
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(LucideIcons.info).iconMutedForeground(),
            Gap(Spacing.sm),
            const Text('Information').semiBold(),
          ],
        ),
        Gap(Spacing.sm),
        const Text('This is some helpful information about the feature.')
            .small()
            .muted(),
      ],
    ),
  ),
)
```

### Stat Card

```dart
Card(
  filled: true,
  child: Padding(
    padding: const EdgeInsets.all(20),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('Total Revenue').small().muted(),
            Icon(LucideIcons.dollarSign).iconSmall().iconMutedForeground(),
          ],
        ),
        Gap(Spacing.sm),
        const Text('\$45,231.89').x2Large().bold(),
        Gap(Spacing.xs),
        Row(
          children: [
            Badge(
              variant: BadgeVariant.default,
              child: Text('+20.1%'),
            ),
            Gap(Spacing.xs),
            const Text('from last month').xSmall().muted(),
          ],
        ),
      ],
    ),
  ),
)
```

---

## Navigation Patterns

### Tab Navigation

```dart
class TabbedPage extends StatefulWidget {
  const TabbedPage({super.key});

  @override
  State<TabbedPage> createState() => _TabbedPageState();
}

class _TabbedPageState extends State<TabbedPage> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      headers: [
        AppBar(title: const Text('Dashboard')),
      ],
      child: Column(
        children: [
          TabList(
            index: _selectedIndex,
            onChanged: (index) => setState(() => _selectedIndex = index),
            children: const [
              TabButton(child: Text('Overview')),
              TabButton(child: Text('Analytics')),
              TabButton(child: Text('Settings')),
            ],
          ),
          Expanded(
            child: IndexedStack(
              index: _selectedIndex,
              children: const [
                OverviewTab(),
                AnalyticsTab(),
                SettingsTab(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Breadcrumb Navigation

```dart
Breadcrumb(
  separator: Icon(LucideIcons.chevronRight).iconSmall().iconMutedForeground(),
  children: [
    BreadcrumbItem(
      child: const Text('Home'),
      onPressed: () => navigateToHome(),
    ),
    BreadcrumbItem(
      child: const Text('Products'),
      onPressed: () => navigateToProducts(),
    ),
    BreadcrumbItem(
      child: const Text('Electronics'),
      onPressed: () => navigateToElectronics(),
    ),
    BreadcrumbItem(
      child: const Text('Laptop XYZ'),
      // No onPressed = current page
    ),
  ],
)
```

---

## Loading Patterns

### Skeleton Card List

```dart
Widget buildSkeletonList() {
  return ListView(
    padding: const EdgeInsets.all(16),
    children: List.generate(5, (index) => Card(
      filled: true,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Skeleton(width: 48, height: 48),
            Gap(Spacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Skeleton(width: 120, height: 16),
                  Gap(Spacing.xs),
                  Skeleton(width: 200, height: 12),
                ],
              ),
            ),
          ],
        ),
      ),
    )).toList(),
  );
}
```

### Full Page Skeleton

```dart
Widget build(BuildContext context) {
  return Scaffold(
    headers: [
      AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton.ghost(
            icon: const Icon(LucideIcons.settings),
            onPressed: () {},
          ).ignoreSkeleton(),
        ],
      ),
    ],
    child: SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          // Profile header
          Row(
            children: [
              Avatar(initials: user?.initials ?? '', size: AvatarSize.large),
              Gap(Spacing.md),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(user?.name ?? '').large().bold(),
                  Text(user?.email ?? '').small().muted(),
                ],
              ),
            ],
          ),
          Gap(Spacing.xl),
          // Content sections
          ...buildSections(),
        ],
      ).asSkeleton(enabled: isLoading),
    ),
  );
}
```

---

## Error Handling Patterns

### Error State Widget

```dart
Widget buildErrorState(String message, VoidCallback onRetry) {
  return Center(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(LucideIcons.alertTriangle)
            .iconX3Large()
            .iconDestructiveForeground(),
        Gap(Spacing.md),
        const Text('Something went wrong').large().semiBold(),
        Gap(Spacing.sm),
        Text(message).small().muted().center(),
        Gap(Spacing.lg),
        Button.outline(
          leading: const Icon(LucideIcons.refreshCw),
          onPressed: onRetry,
          child: const Text('Try Again'),
        ),
      ],
    ),
  ).withPadding(all: 48);
}
```

### Inline Error Alert

```dart
Alert(
  leading: const Icon(LucideIcons.alertCircle),
  title: const Text('Error'),
  content: Text(errorMessage),
  destructive: true,
)
```

---

## Best Practices

1. **Use Gap for spacing** - `Gap(Spacing.md)` instead of `SizedBox`
2. **Apply scaling** - `EdgeInsets.all(24 * theme.scaling)`
3. **Skeleton at container level** - One `.asSkeleton()` for groups
4. **Keep actions interactive** - Use `.ignoreSkeleton()` on buttons
5. **Use semantic components** - `Button.destructive()` for delete actions
6. **Consistent padding** - Use `.withPadding()` with standard values
7. **Theme colors only** - Never hardcode colors
8. **Text extensions** - `.bold().large()` instead of raw TextStyle
