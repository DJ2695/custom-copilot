# shadcn_flutter Extensions Reference

Comprehensive reference for Widget, Text, and Icon extensions.

---

## Widget Extensions (WidgetExtension)

Extensions available on any `Widget`.

### Layout Extensions

#### center

Centers the widget within its parent.

```dart
myWidget.center()
myWidget.center(key: Key('centered'))
```

#### expanded

Makes widget fill available space in Flex layouts (Row/Column).

```dart
myWidget.expanded()
myWidget.expanded(flex: 2)  // With flex factor
```

#### positioned

Positions widget absolutely within a Stack.

```dart
myWidget.positioned(
  left: 10,
  top: 20,
  right: null,
  bottom: null,
)
```

#### sized

Sets explicit dimensions.

```dart
myWidget.sized(width: 100, height: 50)
myWidget.sized(width: 200)  // Only width
myWidget.sized(height: 100) // Only height
```

#### constrained

Applies min/max constraints.

```dart
myWidget.constrained(
  minWidth: 50,
  maxWidth: 300,
  minHeight: 50,
  maxHeight: 200,
)

// Shorthand for exact size
myWidget.constrained(width: 100, height: 100)
```

#### intrinsic

Uses intrinsic sizing.

```dart
myWidget.intrinsic()
myWidget.intrinsic(stepWidth: 10, stepHeight: 10)
myWidget.intrinsicHeight()
myWidget.intrinsicWidth()
```

---

### Padding & Margin

#### withPadding

Adds padding around widget.

```dart
// Individual sides
myWidget.withPadding(top: 8, bottom: 8, left: 16, right: 16)

// Symmetric
myWidget.withPadding(horizontal: 16, vertical: 8)

// All sides
myWidget.withPadding(all: 16)

// EdgeInsetsGeometry
myWidget.withPadding(padding: const EdgeInsets.only(top: 20))
```

#### withMargin

Adds margin around widget.

```dart
// Same API as withPadding
myWidget.withMargin(all: 8)
myWidget.withMargin(horizontal: 16, vertical: 8)
myWidget.withMargin(top: 10, bottom: 20)
```

---

### Clipping Extensions

#### clip

Hard edge clipping.

```dart
myWidget.clip()
myWidget.clip(clipBehavior: Clip.antiAlias)
```

#### clipOval

Clips to oval/circle shape.

```dart
myWidget.clipOval()
myWidget.clipOval(clipBehavior: Clip.antiAliasWithSaveLayer)
```

#### clipRRect

Clips with rounded corners.

```dart
myWidget.clipRRect(borderRadius: BorderRadius.circular(12))
myWidget.clipRRect(
  borderRadius: BorderRadius.circular(8),
  clipBehavior: Clip.antiAlias,
)
```

#### clipPath

Clips with custom path.

```dart
myWidget.clipPath(clipper: MyCustomClipper())
```

---

### Skeleton Extensions

For loading states.

#### asSkeleton

Converts widget to skeleton placeholder.

```dart
// Basic skeleton
myWidget.asSkeleton()

// With configuration
myWidget.asSkeleton(
  enabled: isLoading,
  leaf: false,
  replacement: customSkeleton,
  unite: false,
)
```

#### asSkeletonSliver

For sliver layouts.

```dart
mySliverWidget.asSkeletonSliver()
mySliverWidget.asSkeletonSliver(enabled: isLoading)
```

#### ignoreSkeleton

Keeps widget interactive during skeleton mode.

```dart
button.ignoreSkeleton()  // Button stays clickable
```

#### excludeSkeleton

Excludes widget from skeleton effects.

```dart
importantWidget.excludeSkeleton()
importantWidget.excludeSkeleton(exclude: true)
```

---

## Text Extensions (TextExtension)

Extensions for styling Text widgets.

### Size Modifiers

```dart
text.xSmall    // Extra small (12px typical)
text.small     // Small (14px)
text.base      // Base/normal (16px)
text.large     // Large (18px)
text.xLarge    // Extra large (20px)
text.x2Large   // 2x large
text.x3Large   // 3x large
text.x4Large   // 4x large
text.x5Large   // 5x large
text.x6Large   // 6x large
text.x7Large   // 7x large
text.x8Large   // 8x large
text.x9Large   // 9x large
```

**Usage:**

```dart
const Text('Small text').small()
const Text('Large heading').x2Large()
```

### Weight Modifiers

```dart
text.thin        // Weight 100
text.extraLight  // Weight 200
text.light       // Weight 300
text.normal      // Weight 400
text.medium      // Weight 500
text.semiBold    // Weight 600
text.bold        // Weight 700
text.extraBold   // Weight 800
text.black       // Weight 900
```

**Usage:**

```dart
const Text('Bold text').bold()
const Text('Medium weight').medium()
const Text('Light text').light()
```

### Style Modifiers

```dart
text.italic       // Italic style
text.underline    // Underlined
text.strikeThrough // Strikethrough
text.mono         // Monospace font
text.code         // Code styling
text.inlineCode   // Inline code
```

### Semantic Modifiers

```dart
text.h1          // Heading 1 style
text.h2          // Heading 2 style
text.h3          // Heading 3 style
text.h4          // Heading 4 style
text.p           // Paragraph style
text.lead        // Lead paragraph
text.blockQuote  // Block quote style
text.textLarge   // Large text
text.textSmall   // Small text
text.textMuted   // Muted/subdued
```

### Color Modifiers

```dart
text.muted               // Muted foreground color
text.foreground          // Standard foreground
text.primaryForeground   // Primary color
text.secondaryForeground // Secondary color
```

### Alignment & Overflow

```dart
text.textCenter   // Center aligned
text.ellipsis     // Truncate with ellipsis
text.singleLine   // Single line with ellipsis
```

### Chaining Modifiers

```dart
const Text('Important')
  .large()
  .bold()
  .primaryForeground

const Text('Subtitle')
  .small()
  .muted()

const Text('Error message')
  .base()
  .medium()
  // Note: destructive color via theme
```

---

## Icon Extensions (IconExtension)

Extensions for styling Icon widgets.

### Size Modifiers

```dart
icon.iconX4Small   // Extra extra extra extra small
icon.iconX3Small   // Extra extra extra small
icon.iconX2Small   // Extra extra small
icon.iconXSmall    // Extra small
icon.iconSmall     // Small
icon.iconMedium    // Medium (default)
icon.iconLarge     // Large
icon.iconXLarge    // Extra large
icon.iconX2Large   // 2x large
icon.iconX3Large   // 3x large
icon.iconX4Large   // 4x large
```

**Usage:**

```dart
Icon(LucideIcons.check).iconLarge()
Icon(LucideIcons.x).iconSmall()
```

### Color Modifiers

```dart
icon.iconPrimary()            // Primary color
icon.iconPrimaryForeground()  // Primary foreground
icon.iconSecondary()          // Secondary color
icon.iconSecondaryForeground() // Secondary foreground
icon.iconMutedForeground()    // Muted color
icon.iconDestructiveForeground() // Destructive color
```

**Usage:**

```dart
Icon(LucideIcons.alertTriangle).iconDestructiveForeground()
Icon(LucideIcons.info).iconMutedForeground()
Icon(LucideIcons.check).iconPrimary().iconLarge()
```

---

## Common Patterns

### Loading State Card

```dart
Card(
  filled: true,
  child: Column(
    children: [
      const Text('Title').bold().large(),
      Gap(Spacing.sm),
      const Text('Description').muted(),
    ],
  ),
).withPadding(all: 16).asSkeleton(enabled: isLoading)
```

### Centered Content

```dart
Column(
  children: [
    const Text('Centered').xLarge().bold(),
    Gap(Spacing.md),
    Button.primary(
      onPressed: () {},
      child: const Text('Action'),
    ).ignoreSkeleton(),
  ],
).center().withPadding(all: 24)
```

### Responsive Container

```dart
Container(
  child: content,
)
.withPadding(horizontal: 16, vertical: 12)
.constrained(maxWidth: 600)
.center()
```

### Icon Button Styling

```dart
IconButton.ghost(
  icon: Icon(LucideIcons.settings).iconMedium(),
  onPressed: () {},
)

IconButton.destructive(
  icon: Icon(LucideIcons.trash).iconSmall().iconDestructiveForeground(),
  onPressed: () {},
)
```

### Styled Headings

```dart
// Page title
const Text('Dashboard').h1()

// Section title
const Text('Recent Activity').h3()

// Muted subtitle
const Text('Last updated 5 minutes ago').textSmall().muted()
```

### Skeleton Loading

```dart
ListView(
  children: [
    // Header stays interactive
    Row(
      children: [
        const Text('Users').h2(),
        const Spacer(),
        Button.outline(
          child: const Text('Refresh'),
          onPressed: refresh,
        ).ignoreSkeleton(),
      ],
    ),
    
    // List items skeleton
    ...items.map((item) => ListItem(item: item).asSkeleton(
      enabled: isLoading,
    )),
  ],
)
```

---

## Best Practices

1. **Chain extensions** - Combine size, weight, and color: `.large().bold().muted()`
2. **Use semantic modifiers** - Prefer `.h1()` over manual styling
3. **Apply skeleton at container level** - One `.asSkeleton()` for groups
4. **Keep buttons interactive** - Use `.ignoreSkeleton()` on actions
5. **Consistent padding** - Use `.withPadding()` with spacing constants
6. **Responsive layouts** - Combine `.constrained()` with `.center()`
