# shadcn_flutter Essentials

80% use case components: forms, buttons, layout, feedback, and Material migration guide.

---

## Form Components

### TextField

Text input field. **Different from Material's TextFormField.**

```dart
TextField(
  placeholder: const Text('Enter email'),  // NOT hintText
  controller: _controller,
  onChanged: (value) => print(value),
  onSubmitted: (value) => submit(value),
  
  // Input features (unique to shadcn)
  features: [
    InputClearFeature(),      // Clear button
    InputRevalidateFeature(), // Auto-revalidate
  ],
  
  // Standard properties
  keyboardType: TextInputType.email,
  obscureText: true,  // For passwords
  maxLines: 3,        // Multiline
  enabled: true,
  readOnly: false,
  validator: RequiredValidator(),
)
```

**Key Differences from Material:**
- Uses `placeholder` widget, not `decoration.hintText`
- Has `features` for extensible input features
- `border` is direct property, not via InputDecoration

### Select<T>

Dropdown selection. **Very different from DropdownButton.**

```dart
Select<String>(
  value: selectedValue,
  onChanged: (value) => setState(() => selectedValue = value),
  placeholder: const Text('Select option'),
  
  // How to display selected value
  itemBuilder: (context, value) => Text(value),
  
  // Popup content (required)
  popup: (context) => SelectPopup(
    children: [
      SelectItem(value: 'a', child: Text('Option A')),
      SelectItem(value: 'b', child: Text('Option B')),
      SelectItem(value: 'c', child: Text('Option C')),
    ],
  ),
  
  filled: false,          // Solid background
  canUnselect: true,      // Allow deselection
  autoClosePopover: true, // Auto-close on selection
)
```

### Checkbox

Boolean toggle with three states.

```dart
Checkbox(
  state: isChecked ? CheckboxState.checked : CheckboxState.unchecked,
  onChanged: (state) {
    setState(() => isChecked = state == CheckboxState.checked);
  },
)

// Tristate (checked, unchecked, indeterminate)
Checkbox(
  state: CheckboxState.indeterminate,  // Mixed state
  tristate: true,
  onChanged: (state) => handleChange(state),
)
```

**CheckboxState enum:**
- `CheckboxState.unchecked`
- `CheckboxState.checked`
- `CheckboxState.indeterminate`

### Switch

Toggle switch.

```dart
Switch(
  value: isEnabled,
  onChanged: (value) => setState(() => isEnabled = value),
)
```

### RadioGroup<T>

Grouped radio buttons. **Not individual Radio widgets.**

```dart
RadioGroup<String>(
  value: selectedOption,
  onChanged: (value) => setState(() => selectedOption = value),
  children: [
    RadioItem(value: 'small', child: Text('Small')),
    RadioItem(value: 'medium', child: Text('Medium')),
    RadioItem(value: 'large', child: Text('Large')),
  ],
)
```

> ⚠️ **Import via shim** - RadioGroup conflicts with Flutter's built-in export

### Form & FormController

Unified form management.

```dart
final controller = FormController();

Form(
  controller: controller,
  onSubmit: (values) async {
    // values is Map<FormKey, dynamic>
    final email = values[FormKey<String>('email')] as String;
    await submitForm(email);
  },
  child: Column(
    children: [
      TextField(
        key: FormKey<String>('email'),
        placeholder: const Text('Email'),
        validator: RequiredValidator(),
      ),
      Gap(16),
      Button.primary(
        onPressed: () => controller.submit(),
        child: const Text('Submit'),
      ),
    ],
  ),
)
```

**Built-in Validators:**
- `RequiredValidator()` - Not empty
- `EmailValidator()` - Valid email format
- `MinLengthValidator(8)` - Minimum length
- `MaxLengthValidator(100)` - Maximum length
- `PatternValidator(r'^[a-z]+$')` - Regex pattern

---

## Buttons

### Button

The primary interactive element. Multiple variants available.

```dart
// Main action
Button.primary(
  onPressed: () => handleAction(),
  leading: const Icon(LucideIcons.plus),
  child: const Text('Add Item'),
)

// Secondary action
Button.secondary(
  onPressed: () => action(),
  child: const Text('Cancel'),
)

// Less emphasis
Button.outline(
  onPressed: () => action(),
  child: const Text('Learn More'),
)

// Minimal style
Button.ghost(
  onPressed: () => action(),
  child: const Text('Skip'),
)

// Dangerous action
Button.destructive(
  onPressed: () => delete(),
  child: const Text('Delete'),
)

// Disabled
Button.primary(
  onPressed: null,  // null = disabled
  child: const Text('Disabled'),
)
```

**Key Properties:**
- `child` - Button content (usually Text)
- `onPressed` - Tap callback (null = disabled)
- `leading` / `trailing` - Icons before/after content
- `enabled` - Explicit enable/disable
- `style` - Custom ButtonStyle
- `size` - `ButtonSize.normal`, `.small`, `.large`
- `density` - `ButtonDensity.normal`, `.dense`, `.icon`

### IconButton

Icon-only button with same variants.

```dart
IconButton.ghost(
  icon: const Icon(LucideIcons.x),
  onPressed: () => close(),
)

IconButton.outline(
  icon: const Icon(LucideIcons.settings),
  onPressed: () => openSettings(),
)

IconButton.destructive(
  icon: const Icon(LucideIcons.trash),
  onPressed: () => delete(),
)
```

---

## Layout & Containers

### Card

Content container with optional styling.

```dart
Card(
  filled: true,  // Solid background
  fillColor: theme.colorScheme.card,
  borderRadius: BorderRadius.circular(12),
  child: content.withPadding(all: 16),
)
```

**Key Properties:**
- `filled` - Solid vs transparent background
- `fillColor` - Background color
- `borderRadius` - Corner rounding
- `borderColor` / `borderWidth` - Border styling
- `boxShadow` - Shadow effects

### OutlinedContainer

Bordered container without elevation.

```dart
OutlinedContainer(
  borderRadius: theme.borderRadiusMd,
  borderColor: theme.colorScheme.border,
  backgroundColor: theme.colorScheme.background,
  child: content,
)
```

### Gap

Standard spacing widget.

```dart
Gap(8)   // Tight spacing
Gap(16)  // Standard spacing
Gap(24)  // Section spacing
Gap(32)  // Wide spacing
```

### Divider

Visual separator.

```dart
const Divider()           // Horizontal
const Divider(vertical: true)  // Vertical
```

---

## Feedback

### Alert

Inline alert message.

```dart
Alert(
  leading: const Icon(LucideIcons.info),
  title: const Text('Information'),
  content: const Text('This is an informational message.'),
)

Alert(
  leading: const Icon(LucideIcons.alertTriangle),
  title: const Text('Warning'),
  destructive: true,  // Error styling
  children: [
    Text('Something needs attention.'),
  ],
)
```

### Toast

Temporary notification. Use `showToast()` function.

```dart
showToast(
  context: context,
  location: ToastLocation.bottomRight,
  builder: (context, overlay) {
    return Toast(
      title: const Text('Success'),
      description: const Text('Item saved successfully'),
      trailing: IconButton.ghost(
        icon: const Icon(LucideIcons.x),
        onPressed: overlay.close,
      ),
    );
  },
);
```

**ToastLocation options:**
- `topLeft`, `topCenter`, `topRight`
- `bottomLeft`, `bottomCenter`, `bottomRight`

### Progress / CircularProgress

Loading indicators.

```dart
// Linear progress
Progress(value: 0.6)  // 60%
Progress(value: null) // Indeterminate

// Circular
CircularProgress(value: 0.3)
CircularProgress(value: null)  // Spinning
```

### Skeleton

Loading placeholder.

```dart
// Basic skeleton
Skeleton(width: 200, height: 20)

// Wrap existing widget
myWidget.asSkeleton()

// Keep interactive during skeleton
button.ignoreSkeleton()
```

---

## Dialogs

### AlertDialog

Confirmation dialog with preset structure.

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: const Text('Delete Item?'),
    content: const Text('This action cannot be undone.'),
    actions: [
      Button.ghost(
        onPressed: () => Navigator.pop(context),
        child: const Text('Cancel'),
      ),
      Button.destructive(
        onPressed: () {
          delete();
          Navigator.pop(context, true);
        },
        child: const Text('Delete'),
      ),
    ],
  ),
);
```

### Dialog

Custom modal dialog.

```dart
showDialog(
  context: context,
  builder: (context) => Dialog(
    child: Container(
      constraints: const BoxConstraints(maxWidth: 400),
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Custom Dialog'),
          Gap(16),
          // Custom content
        ],
      ),
    ),
  ),
);
```

### Sheet

Bottom or side sheet.

```dart
showSheet(
  context: context,
  side: SheetSide.bottom,  // or .left, .right, .top
  builder: (context) => Container(
    padding: const EdgeInsets.all(24),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Sheet Content'),
        // More content
      ],
    ),
  ),
);
```

---

## Material Migration

### TextField Migration

```dart
// ❌ Material
TextFormField(
  decoration: InputDecoration(
    hintText: 'Enter email',
    prefixIcon: Icon(Icons.email),
  ),
  validator: (value) => value!.isEmpty ? 'Required' : null,
)

// ✅ shadcn_flutter
TextField(
  placeholder: const Text('Enter email'),
  leading: const Icon(LucideIcons.mail),
  features: [InputClearFeature()],
  validator: RequiredValidator(),
)
```

### Select Migration

```dart
// ❌ Material
DropdownButton<String>(
  value: selected,
  items: options.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
  onChanged: (value) => setState(() => selected = value),
)

// ✅ shadcn_flutter
Select<String>(
  value: selected,
  onChanged: (value) => setState(() => selected = value),
  placeholder: const Text('Select option'),
  itemBuilder: (context, value) => Text(value),
  popup: (context) => SelectPopup(
    children: options.map((e) => SelectItem(value: e, child: Text(e))).toList(),
  ),
)
```

### Checkbox Migration

```dart
// ❌ Material
Checkbox(
  value: isChecked,
  onChanged: (value) => setState(() => isChecked = value ?? false),
)

// ✅ shadcn_flutter
Checkbox(
  state: isChecked ? CheckboxState.checked : CheckboxState.unchecked,
  onChanged: (state) {
    setState(() => isChecked = state == CheckboxState.checked);
  },
)
```

### Button Migration

```dart
// ❌ Material
ElevatedButton(
  onPressed: () => submit(),
  child: Text('Submit'),
)

OutlinedButton(
  onPressed: () => cancel(),
  child: Text('Cancel'),
)

// ✅ shadcn_flutter
Button.primary(
  onPressed: () => submit(),
  child: const Text('Submit'),
)

Button.outline(
  onPressed: () => cancel(),
  child: const Text('Cancel'),
)
```

### Dialog Migration

```dart
// ❌ Material
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: Text('Confirm'),
    content: Text('Delete item?'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(context), child: Text('Cancel')),
      ElevatedButton(onPressed: () => delete(), child: Text('Delete')),
    ],
  ),
);

// ✅ shadcn_flutter
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: const Text('Confirm'),
    content: const Text('Delete item?'),
    actions: [
      Button.ghost(
        onPressed: () => Navigator.pop(context),
        child: const Text('Cancel'),
      ),
      Button.destructive(
        onPressed: () => delete(),
        child: const Text('Delete'),
      ),
    ],
  ),
);
```

### SnackBar → Toast Migration

```dart
// ❌ Material
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text('Item saved')),
);

// ✅ shadcn_flutter
showToast(
  context: context,
  builder: (context, overlay) => Toast(
    title: const Text('Success'),
    description: const Text('Item saved'),
  ),
);
```

### Icon Migration

shadcn_flutter uses **LucideIcons** instead of Material Icons:

```dart
// Common mappings
Icons.add        → LucideIcons.plus
Icons.close      → LucideIcons.x
Icons.check      → LucideIcons.check
Icons.menu       → LucideIcons.menu
Icons.search     → LucideIcons.search
Icons.settings   → LucideIcons.settings
Icons.delete     → LucideIcons.trash
Icons.edit       → LucideIcons.edit or .pencil
Icons.home       → LucideIcons.home
Icons.person     → LucideIcons.user
Icons.email      → LucideIcons.mail
```

### Component Mapping

| Material | shadcn_flutter | Notes |
|----------|----------------|-------|
| `TextFormField` | `TextField` | Different API |
| `DropdownButton` | `Select<T>` | Requires popup builder |
| `Checkbox` | `Checkbox` | Uses `CheckboxState` enum |
| `Radio` | `RadioGroup` + `RadioItem` | Grouped approach |
| `ElevatedButton` | `Button.primary()` | Named variants |
| `OutlinedButton` | `Button.outline()` | Named variants |
| `TextButton` | `Button.ghost()` | Named variants |
| `IconButton` | `IconButton.*()` | Same variants |
| `AlertDialog` | `AlertDialog` | Similar structure |
| `SnackBar` | `Toast` | Use `showToast()` |
| `Card` | `Card` | Different properties |
| `LinearProgressIndicator` | `Progress` | Similar |
| `CircularProgressIndicator` | `CircularProgress` | Similar |
| `CircleAvatar` | `Avatar` | Uses initials + imageUrl |
| `TabBar` + `TabBarView` | `Tabs` | Combined widget |
