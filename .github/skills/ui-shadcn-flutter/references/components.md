# shadcn_flutter Component Reference

Comprehensive reference for shadcn_flutter components. Always verify current API via context7.

---

## Buttons

### Button

The primary interactive element. Multiple variants available.

```dart
// Constructors
Button.primary({required Widget child, VoidCallback? onPressed, Widget? leading, Widget? trailing})
Button.secondary({...})
Button.outline({...})
Button.ghost({...})
Button.destructive({...})

// Usage
Button.primary(
  onPressed: () => handleAction(),
  leading: const Icon(LucideIcons.plus),
  child: const Text('Add Item'),
)

Button.outline(
  onPressed: null,  // Disabled state
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
```

---

## Form Inputs

### TextField

Text input field. **Different from Material's TextFormField.**

```dart
TextField(
  placeholder: const Text('Enter name'),  // NOT hintText
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
)
```

**Key Differences from Material:**
- Uses `placeholder` widget, not `decoration.hintText`
- Has `features` for extensible input features
- `border` is direct property, not via InputDecoration

### NumberInput

Dedicated numeric input.

```dart
NumberInput(
  value: quantity,
  onChanged: (value) => setState(() => quantity = value),
  min: 0,
  max: 100,
  step: 1,
)
```

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
)
```

**Key Properties:**
- `value` - Currently selected value
- `onChanged` - Selection callback
- `placeholder` - Shown when no selection
- `itemBuilder` - Renders selected value in closed state
- `popup` - Builder for dropdown content
- `filled` - Solid background style
- `canUnselect` - Allow deselection
- `autoClosePopover` - Auto-close on selection

### Checkbox

Boolean toggle with three states.

```dart
Checkbox(
  state: isChecked ? CheckboxState.checked : CheckboxState.unchecked,
  onChanged: (state) {
    setState(() => isChecked = state == CheckboxState.checked);
  },
)

// Tristate
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

### DatePicker / TimePicker

Date and time selection widgets.

```dart
DatePicker(
  value: selectedDate,
  onChanged: (date) => setState(() => selectedDate = date),
  mode: PromptMode.dialog,  // or .popover
  placeholder: const Text('Select date'),
)

TimePicker(
  value: selectedTime,
  onChanged: (time) => setState(() => selectedTime = time),
)
```

### InputOTP

One-time password input.

```dart
InputOTP(
  length: 6,
  onCompleted: (code) => verifyCode(code),
)
```

### ChipInput

Tag/chip input with suggestions.

```dart
ChipInput<String>(
  chips: selectedTags,
  onChanged: (tags) => setState(() => selectedTags = tags),
  chipBuilder: (context, tag) => Chip(child: Text(tag)),
  onSuggestionChoosen: (index) => addTag(suggestions[index]),
)
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
  destructive: false,  // true for error styling
)

Alert(
  leading: const Icon(LucideIcons.alertTriangle),
  title: const Text('Warning'),
  content: const Text('Something needs attention.'),
  destructive: true,
)
```

### Toast

Temporary notification. Use `showToast()` function.

```dart
showToast(
  context: context,
  location: ToastLocation.bottomRight,  // Position
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

## Layout & Containers

### Card

Content container with optional styling.

```dart
Card(
  filled: true,  // Solid background
  fillColor: theme.colorScheme.card,
  borderRadius: BorderRadius.circular(12),
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: content,
  ),
)
```

**Key Properties:**
- `filled` - Solid vs transparent background
- `fillColor` - Background color
- `borderRadius` - Corner rounding
- `borderColor` / `borderWidth` - Border styling
- `boxShadow` - Shadow effects

### OutlinedContainer

Bordered container.

```dart
OutlinedContainer(
  borderRadius: theme.borderRadiusMd,
  borderColor: theme.colorScheme.border,
  backgroundColor: theme.colorScheme.background,
  child: content,
)
```

### Accordion

Collapsible sections.

```dart
Accordion(
  children: [
    AccordionItem(
      trigger: (context, isExpanded) => AccordionTrigger(
        child: Text('Section 1'),
      ),
      content: AccordionContent(
        child: Text('Section 1 content'),
      ),
    ),
    AccordionItem(
      trigger: (context, isExpanded) => AccordionTrigger(
        child: Text('Section 2'),
      ),
      content: AccordionContent(
        child: Text('Section 2 content'),
      ),
    ),
  ],
)
```

### Tabs

Tabbed content.

```dart
Tabs(
  index: selectedIndex,
  onChanged: (index) => setState(() => selectedIndex = index),
  children: const [
    TabItem(
      header: Text('Tab 1'),
      child: Text('Content 1'),
    ),
    TabItem(
      header: Text('Tab 2'),
      child: Text('Content 2'),
    ),
  ],
)

// Separate tab list (for custom styling)
TabList(
  index: selectedIndex,
  onChanged: (index) => setState(() => selectedIndex = index),
  children: const [
    TabButton(child: Text('Overview')),
    TabButton(child: Text('Settings')),
    TabButton(child: Text('Advanced')),
  ],
)
```

### Steps / Stepper

Multi-step wizard.

```dart
Stepper(
  currentStep: currentStep,
  onStepTapped: (step) => setState(() => currentStep = step),
  steps: [
    Step(title: Text('Account'), content: AccountForm()),
    Step(title: Text('Profile'), content: ProfileForm()),
    Step(title: Text('Confirm'), content: ConfirmView()),
  ],
)
```

### Divider

Visual separator.

```dart
const Divider()           // Horizontal
const Divider(vertical: true)  // Vertical
```

### Resizable

Adjustable panels.

```dart
Resizable(
  children: [
    ResizablePane(
      initialSize: 200,
      minSize: 100,
      child: sidePanel,
    ),
    ResizablePane(
      child: mainContent,
    ),
  ],
)
```

---

## Surfaces & Overlays

### Dialog

Custom modal dialog.

```dart
showDialog(
  context: context,
  builder: (context) => Dialog(
    child: Container(
      constraints: const BoxConstraints(maxWidth: 400),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Dialog header
          // Dialog content
          // Dialog actions
        ],
      ),
    ),
  ),
);
```

### AlertDialog

Confirmation dialog with preset structure.

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: const Text('Confirm Action'),
    content: const Text('Are you sure you want to proceed?'),
    actions: [
      Button.ghost(
        onPressed: () => Navigator.pop(context),
        child: const Text('Cancel'),
      ),
      Button.primary(
        onPressed: () {
          // Handle confirmation
          Navigator.pop(context, true);
        },
        child: const Text('Confirm'),
      ),
    ],
  ),
);
```

### Sheet

Bottom or side sheet.

```dart
showSheet(
  context: context,
  side: SheetSide.bottom,  // or .left, .right, .top
  builder: (context) => SheetContent(
    child: Column(
      children: [
        // Sheet content
      ],
    ),
  ),
);
```

### Popover

Floating content anchored to trigger.

```dart
Popover(
  trigger: Button.outline(child: Text('Open')),
  content: (context) => PopoverContent(
    child: Text('Popover content'),
  ),
)
```

### Tooltip

Hover hint.

```dart
Tooltip(
  tooltip: (context) => const Text('Helpful tip'),
  child: IconButton.ghost(
    icon: const Icon(LucideIcons.helpCircle),
    onPressed: null,
  ),
)
```

### DropdownMenu

Action menu.

```dart
DropdownMenu(
  trigger: Button.ghost(child: const Icon(LucideIcons.moreVertical)),
  children: [
    MenuItem(
      leading: const Icon(LucideIcons.edit),
      child: const Text('Edit'),
      onPressed: () => handleEdit(),
    ),
    MenuItem(
      leading: const Icon(LucideIcons.trash),
      child: const Text('Delete'),
      onPressed: () => handleDelete(),
    ),
  ],
)
```

### ContextMenu

Right-click menu.

```dart
ContextMenu(
  child: targetWidget,
  items: [
    MenuItem(child: Text('Copy'), onPressed: () => copy()),
    MenuItem(child: Text('Paste'), onPressed: () => paste()),
    const MenuDivider(),
    MenuItem(child: Text('Delete'), onPressed: () => delete()),
  ],
)
```

---

## Data Display

### Avatar

User image with fallback.

```dart
Avatar(
  initials: 'JD',
  imageUrl: user.avatarUrl,
  size: AvatarSize.medium,  // small, medium, large
)

// Group of avatars
AvatarGroup(
  maxAvatars: 3,
  children: users.map((u) => Avatar(initials: u.initials)).toList(),
)
```

### Badge

Status indicator.

```dart
Badge(child: const Text('New'))
Badge(
  variant: BadgeVariant.destructive,
  child: const Text('Error'),
)
Badge(
  variant: BadgeVariant.outline,
  child: const Text('Draft'),
)
```

### Table

Data table.

```dart
Table(
  columns: const [
    TableColumn(child: Text('Name')),
    TableColumn(child: Text('Email')),
    TableColumn(child: Text('Status')),
  ],
  rows: items.map((item) => TableRow(
    cells: [
      TableCell(child: Text(item.name)),
      TableCell(child: Text(item.email)),
      TableCell(child: Badge(child: Text(item.status))),
    ],
  )).toList(),
)
```

### Calendar

Date calendar.

```dart
Calendar(
  initialView: CalendarView.now(),
  selectionMode: CalendarSelectionMode.single,
  onChanged: (value) {
    final date = (value as SingleCalendarValue).date;
    print('Selected: $date');
  },
)
```

---

## Navigation

### Breadcrumb

Path navigation.

```dart
Breadcrumb(
  children: [
    BreadcrumbItem(child: Text('Home'), onPressed: () => goHome()),
    BreadcrumbItem(child: Text('Products'), onPressed: () => goProducts()),
    BreadcrumbItem(child: Text('Details')),  // Current (no onPressed)
  ],
)
```

### Pagination

Page navigation.

```dart
Pagination(
  page: currentPage,
  totalPages: 10,
  onPageChanged: (page) => setState(() => currentPage = page),
)
```

### NavigationMenu

Complex navigation menu.

```dart
NavigationMenu(
  children: [
    NavigationMenuItem(
      child: Text('Products'),
      content: NavigationMenuContent(
        child: // Dropdown content
      ),
    ),
    NavigationMenuItem(
      child: Text('Pricing'),
      onPressed: () => navigate('/pricing'),
    ),
  ],
)
```

---

## Form System

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
      TextField(
        key: FormKey<String>('name'),
        placeholder: const Text('Name'),
      ),
      Gap(Spacing.lg),
      Button.primary(
        onPressed: () => controller.submit(),
        child: const Text('Submit'),
      ),
    ],
  ),
)
```

**FormController methods:**
- `submit()` - Trigger form submission
- `values` - Get all form values
- `revalidate()` - Re-run validation

### Validators

Built-in validators:

```dart
RequiredValidator()                    // Not empty
EmailValidator()                       // Valid email format
MinLengthValidator(8)                  // Minimum length
MaxLengthValidator(100)                // Maximum length
PatternValidator(r'^[a-z]+$')          // Regex pattern
```

---

## Animation Widgets

### AnimatedValueBuilder

Animate value changes.

```dart
AnimatedValueBuilder<double>(
  value: progress,
  duration: const Duration(milliseconds: 300),
  builder: (context, value, child) {
    return Container(
      width: value * 200,
      height: 20,
      color: Colors.blue,
    );
  },
)
```

### NumberTicker

Animated number display.

```dart
NumberTicker(
  value: count,
  duration: const Duration(milliseconds: 500),
)
```
