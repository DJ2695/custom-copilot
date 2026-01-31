# Material to shadcn_flutter Mapping

Complete reference for migrating from Flutter Material widgets to shadcn_flutter equivalents.

---

## Form Inputs

| Material Widget | shadcn_flutter | Key Differences |
|-----------------|----------------|-----------------|
| `TextFormField` | `TextField` | Uses `placeholder` widget, not `decoration.hintText`. Has `features` array for extensibility |
| `TextField` (Material) | `TextField` | Same name, different API. No InputDecoration |
| `DropdownButton<T>` | `Select<T>` | Requires `popup` builder function, uses `SelectItem` children |
| `DropdownButtonFormField<T>` | `Select<T>` + Form | Combine with Form system for validation |
| `Checkbox` | `Checkbox` | Uses `CheckboxState` enum instead of `bool?` |
| `Switch` | `Switch` | Similar API, different styling |
| `Radio<T>` | `RadioGroup<T>` + `RadioItem` | Grouped approach instead of individual widgets |
| `Slider` | `Slider` | Similar API |
| `showDatePicker()` | `DatePicker` | Widget-based, not function. Has `PromptMode` |
| `showTimePicker()` | `TimePicker` | Widget-based, not function |

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
  tristate: true,  // bool? value
  onChanged: (value) => setState(() => isChecked = value),
)

// ✅ shadcn_flutter
Checkbox(
  state: isChecked 
    ? CheckboxState.checked 
    : CheckboxState.unchecked,
  tristate: true,  // Supports indeterminate
  onChanged: (state) {
    setState(() => isChecked = state == CheckboxState.checked);
  },
)
```

### Radio Migration

```dart
// ❌ Material
Column(
  children: [
    Radio<String>(value: 'a', groupValue: selected, onChanged: (v) => setState(() => selected = v)),
    Radio<String>(value: 'b', groupValue: selected, onChanged: (v) => setState(() => selected = v)),
  ],
)

// ✅ shadcn_flutter
RadioGroup<String>(
  value: selected,
  onChanged: (value) => setState(() => selected = value),
  children: [
    RadioItem(value: 'a', child: Text('Option A')),
    RadioItem(value: 'b', child: Text('Option B')),
  ],
)
```

---

## Buttons

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `ElevatedButton` | `Button.primary()` | Main CTA |
| `OutlinedButton` | `Button.outline()` | Bordered style |
| `TextButton` | `Button.ghost()` | Minimal style |
| `FilledButton` | `Button.secondary()` | Secondary emphasis |
| `IconButton` | `IconButton.*()` | Same variants as Button |
| `FloatingActionButton` | Custom | No direct equivalent |

### Button Migration

```dart
// ❌ Material
ElevatedButton(
  onPressed: () => submit(),
  child: Text('Submit'),
)

// ✅ shadcn_flutter
Button.primary(
  onPressed: () => submit(),
  child: const Text('Submit'),
)

// With icon
Button.primary(
  onPressed: () => submit(),
  leading: const Icon(LucideIcons.check),
  child: const Text('Submit'),
)
```

---

## Dialogs & Overlays

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `AlertDialog` | `AlertDialog` | Similar structure |
| `SimpleDialog` | `Dialog` | Custom content |
| `showDialog()` | `showDialog()` | Same function |
| `showModalBottomSheet()` | `showSheet()` | Uses `SheetSide` |
| `Tooltip` | `Tooltip` | Different API |
| `PopupMenuButton` | `DropdownMenu` | Different structure |
| `SnackBar` | `Toast` | Use `showToast()` |

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
    trailing: IconButton.ghost(
      icon: const Icon(LucideIcons.x),
      onPressed: overlay.close,
    ),
  ),
);
```

---

## Navigation

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `TabBar` + `TabBarView` | `Tabs` / `TabList` | Combined widget |
| `Drawer` | `Drawer` | Similar |
| `NavigationBar` | `NavigationMenu` | Different API |
| `AppBar` | `Scaffold` header | Part of Scaffold |

### Tabs Migration

```dart
// ❌ Material
DefaultTabController(
  length: 2,
  child: Column(
    children: [
      TabBar(tabs: [Tab(text: 'Tab 1'), Tab(text: 'Tab 2')]),
      Expanded(
        child: TabBarView(
          children: [Page1(), Page2()],
        ),
      ),
    ],
  ),
)

// ✅ shadcn_flutter
Tabs(
  index: selectedIndex,
  onChanged: (index) => setState(() => selectedIndex = index),
  children: const [
    TabItem(header: Text('Tab 1'), child: Page1()),
    TabItem(header: Text('Tab 2'), child: Page2()),
  ],
)
```

---

## Layout & Containers

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `Card` | `Card` | Different properties |
| `ExpansionPanel` | `Accordion` | Uses AccordionItem |
| `Divider` | `Divider` | Similar |
| `ListTile` | Custom | No direct equivalent |
| `Stepper` | `Steps` / `Stepper` | Different API |

### Card Migration

```dart
// ❌ Material
Card(
  elevation: 2,
  child: Padding(
    padding: EdgeInsets.all(16),
    child: content,
  ),
)

// ✅ shadcn_flutter
Card(
  filled: true,
  fillColor: theme.colorScheme.card,
  borderRadius: theme.borderRadiusMd,
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: content,
  ),
)
```

---

## Feedback & Status

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `LinearProgressIndicator` | `Progress` | Similar |
| `CircularProgressIndicator` | `CircularProgress` | Similar |
| `Badge` | `Badge` | Different variants |
| `Chip` | `Badge` / `ChipInput` | Depends on use case |

---

## Data Display

| Material Widget | shadcn_flutter | Notes |
|-----------------|----------------|-------|
| `DataTable` | `Table` / `DataTable` | Different structure |
| `CircleAvatar` | `Avatar` | Uses initials + imageUrl |

### Avatar Migration

```dart
// ❌ Material
CircleAvatar(
  backgroundImage: NetworkImage(user.avatarUrl),
  child: Text(user.initials),
)

// ✅ shadcn_flutter
Avatar(
  initials: user.initials,
  imageUrl: user.avatarUrl,
  size: AvatarSize.medium,
)
```

---

## Icons

shadcn_flutter uses **LucideIcons** instead of Material Icons:

```dart
// ❌ Material
Icon(Icons.add)
Icon(Icons.close)
Icon(Icons.check)
Icon(Icons.settings)

// ✅ shadcn_flutter
Icon(LucideIcons.plus)
Icon(LucideIcons.x)
Icon(LucideIcons.check)
Icon(LucideIcons.settings)
```

Common icon mappings:
- `Icons.add` → `LucideIcons.plus`
- `Icons.close` → `LucideIcons.x`
- `Icons.menu` → `LucideIcons.menu`
- `Icons.search` → `LucideIcons.search`
- `Icons.settings` → `LucideIcons.settings`
- `Icons.delete` → `LucideIcons.trash`
- `Icons.edit` → `LucideIcons.edit` or `LucideIcons.pencil`
- `Icons.home` → `LucideIcons.home`
- `Icons.person` → `LucideIcons.user`
- `Icons.email` → `LucideIcons.mail`

---

## No Direct Equivalent

These Material widgets have no direct shadcn_flutter equivalent - build custom:

- `FloatingActionButton` - Use positioned `Button.primary()`
- `ListTile` - Build with Row/Column
- `ExpansionTile` - Use `Accordion`
- `BottomNavigationBar` - Use `Tabs` or custom
- `NavigationRail` - Build custom sidebar
- `RefreshIndicator` - Use package or custom
