---
name: ui-shadcn-flutter
description: 'Build UI with shadcn_flutter components. Use when creating pages, widgets, forms, dialogs, layouts, or any UI element. Covers component APIs, theming, and Material-to-shadcn mapping.'
---

# shadcn_flutter UI Development

Build beautiful, consistent UI using shadcn_flutter - a Flutter implementation of shadcn/ui with 70+ components.

## When to Use This Skill

- Creating new pages or screens
- Building reusable widgets
- Implementing forms with validation
- Adding dialogs, toasts, sheets
- Theming and styling
- Any Flutter UI work with shadcn_flutter

---

## Critical: RadioGroup Export Collision

shadcn_flutter exports a `RadioGroup` that collides with Flutter's built-in. **Always import via project shim:**

```dart
// lib/shared/shadcn.dart (create this shim)
export 'package:shadcn_flutter/shadcn_flutter.dart' hide RadioGroup;

// In your files
import 'package:myapp/shared/shadcn.dart';
```

---

## Theme Access (High-Frequency)

Most common theme patterns:

```dart
@override
Widget build(BuildContext context) {
  final theme = Theme.of(context);
  final scaling = theme.scaling;  // Responsive multiplier
  
  // Colors
  final primary = theme.colorScheme.primary;
  final foreground = theme.colorScheme.foreground;
  final muted = theme.colorScheme.mutedForeground;
  
  // Typography
  final textStyle = theme.typography.base;
  
  return Container(
    padding: EdgeInsets.all(16 * scaling),
    color: theme.colorScheme.card,
    child: Text('Hello', style: textStyle),
  );
}
```

### Essential Color Scheme

```dart
// Most common
theme.colorScheme.primary         // Brand color
theme.colorScheme.foreground      // Primary text
theme.colorScheme.mutedForeground // Secondary text
theme.colorScheme.destructive     // Errors
theme.colorScheme.background      // Page bg
theme.colorScheme.card            // Card bg
```

**Pairing rule:** primary + primaryForeground, card + cardForeground

---

## Essential Components (Quick Reference)

### Forms

```dart
TextField(
  placeholder: const Text('Email'),  // NOT hintText
  features: [InputClearFeature()],
)

Select<String>(
  value: selected,
  itemBuilder: (ctx, val) => Text(val),
  popup: (ctx) => SelectPopup(
    children: [SelectItem(value: 'a', child: Text('A'))],
  ),
  onChanged: (val) => setState(() => selected = val),
)

Checkbox(
  state: checked ? CheckboxState.checked : CheckboxState.unchecked,
  onChanged: (state) => setState(() => checked = state == CheckboxState.checked),
)
```

### Buttons

```dart
Button.primary(onPressed: () {}, child: Text('Submit'))
Button.outline(onPressed: () {}, child: Text('Cancel'))
Button.ghost(onPressed: () {}, child: Text('Skip'))
Button.destructive(onPressed: () {}, child: Text('Delete'))
```

### Feedback

```dart
showToast(
  context: context,
  builder: (ctx, overlay) => Toast(
    title: Text('Success'),
  ),
);

Alert(
  leading: Icon(LucideIcons.info),
  title: Text('Note'),
)
```

---

## Common Extensions (Quick Reference)

```dart
// Text
text.small().semiBold().muted()

// Widget
widget.withPadding(all: 16)
widget.center()
widget.asSkeleton()
```

---

## Quick Material Migration

| Material | shadcn_flutter |
|----------|----------------|
| `TextFormField` | `TextField` (uses `placeholder`) |
| `DropdownButton` | `Select<T>` (uses `popup` builder) |
| `Checkbox` | `Checkbox` (uses `CheckboxState`) |
| `ElevatedButton` | `Button.primary()` |
| `Icons.add` | `LucideIcons.plus` |

---

## Reference Documentation

- **[essentials.md](references/essentials.md)** - Forms, buttons, layout, feedback + Material migration
- **[advanced-components.md](references/advanced-components.md)** - Edge case widgets
- **[theming.md](references/theming.md)** - Complete theme configuration
- **[extensions.md](references/extensions.md)** - All extensions
- **[patterns.md](references/patterns.md)** - UI patterns and recipes

---

## Rules

✅ **DO:** Use theme colors, `Gap()` for spacing, `theme.scaling` for responsive sizing, import via shim

❌ **DON'T:** Hardcode colors/pixels, guess APIs, import shadcn_flutter directly
