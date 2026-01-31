# shadcn_flutter Theming Reference

Complete reference for theme configuration, color schemes, and responsive scaling.

---

## Accessing Theme

Always access theme through `Theme.of(context)`:

```dart
@override
Widget build(BuildContext context) {
  final theme = Theme.of(context);
  
  return Container(
    color: theme.colorScheme.primary,
    padding: EdgeInsets.all(16 * theme.scaling),
    child: Text(
      'Hello',
      style: theme.typography.base,
    ),
  );
}
```

---

## ThemeData Properties

### Core Properties

```dart
ThemeData(
  brightness: Brightness.light,       // Light or dark mode
  colorScheme: ColorSchemes.lightBlue, // Color palette
  typography: Typography(...),         // Text styles
  radius: 0.5,                         // Base border radius multiplier
  scaling: 1.0,                        // UI scaling factor
  surfaceBlur: 0.0,                    // Blur effect
  surfaceOpacity: 1.0,                 // Surface transparency
  iconTheme: IconThemeProperties(...), // Icon styling
)
```

### Border Radius Properties

Access pre-calculated border radius values:

```dart
theme.borderRadiusXs   // Extra small
theme.borderRadiusSm   // Small
theme.borderRadiusMd   // Medium (most common)
theme.borderRadiusLg   // Large
theme.borderRadiusXl   // Extra large
theme.borderRadiusXxl  // Extra extra large

// Raw radius values (double)
theme.radiusXs
theme.radiusSm
theme.radiusMd
theme.radiusLg
theme.radiusXl
theme.radiusXxl
```

### Scaling

Use `theme.scaling` for responsive sizing:

```dart
Container(
  padding: EdgeInsets.all(16 * theme.scaling),
  margin: EdgeInsets.symmetric(
    horizontal: 24 * theme.scaling,
    vertical: 12 * theme.scaling,
  ),
)
```

---

## Color Scheme

### Semantic Colors

```dart
// Primary - Main brand color
theme.colorScheme.primary
theme.colorScheme.primaryForeground

// Secondary - Supporting color
theme.colorScheme.secondary
theme.colorScheme.secondaryForeground

// Destructive - Errors, deletions, warnings
theme.colorScheme.destructive
theme.colorScheme.destructiveForeground

// Muted - Subdued, less important
theme.colorScheme.muted
theme.colorScheme.mutedForeground

// Accent - Highlights, emphasis
theme.colorScheme.accent
theme.colorScheme.accentForeground
```

### Surface Colors

```dart
// Background - Page/app background
theme.colorScheme.background
theme.colorScheme.foreground

// Card - Card surfaces
theme.colorScheme.card
theme.colorScheme.cardForeground

// Popover - Floating elements
theme.colorScheme.popover
theme.colorScheme.popoverForeground
```

### Utility Colors

```dart
// Border and input styling
theme.colorScheme.border   // Border color
theme.colorScheme.input    // Input field border
theme.colorScheme.ring     // Focus ring color
```

### Chart Colors

For data visualization:

```dart
theme.colorScheme.chart1
theme.colorScheme.chart2
theme.colorScheme.chart3
theme.colorScheme.chart4
theme.colorScheme.chart5
```

### Sidebar Colors

For navigation sidebars:

```dart
theme.colorScheme.sidebar
theme.colorScheme.sidebarForeground
theme.colorScheme.sidebarPrimary
theme.colorScheme.sidebarPrimaryForeground
theme.colorScheme.sidebarAccent
theme.colorScheme.sidebarAccentForeground
theme.colorScheme.sidebarBorder
theme.colorScheme.sidebarRing
```

---

## Pre-built Color Schemes

### Using ColorSchemes Class

```dart
// Static methods (adapt to ThemeMode)
ColorSchemes.defaultcolor(ThemeMode.light)
ColorSchemes.blue(ThemeMode.dark)
ColorSchemes.green(ThemeMode.light)
ColorSchemes.orange(ThemeMode.dark)
ColorSchemes.red(ThemeMode.light)
ColorSchemes.rose(ThemeMode.dark)
ColorSchemes.violet(ThemeMode.light)
ColorSchemes.yellow(ThemeMode.dark)

// Pre-defined constants
ColorSchemes.lightDefaultColor
ColorSchemes.darkDefaultColor
ColorSchemes.lightBlue
ColorSchemes.darkBlue
ColorSchemes.lightGreen
ColorSchemes.darkGreen
ColorSchemes.lightOrange
ColorSchemes.darkOrange
ColorSchemes.lightRed
ColorSchemes.darkRed
ColorSchemes.lightRose
ColorSchemes.darkRose
ColorSchemes.lightViolet
ColorSchemes.darkViolet
ColorSchemes.lightYellow
ColorSchemes.darkYellow
```

### Legacy Color Schemes

Additional color options:

```dart
LegacyColorSchemes.lightSlate()
LegacyColorSchemes.darkSlate()
LegacyColorSchemes.lightGray()
LegacyColorSchemes.darkGray()
LegacyColorSchemes.blue(ThemeMode.light)
LegacyColorSchemes.rose(ThemeMode.dark)
LegacyColorSchemes.violet(ThemeMode.light)
LegacyColorSchemes.red(ThemeMode.dark)
```

---

## Typography

### Size Variants

```dart
theme.typography.xSmall   // Extra small
theme.typography.small    // Small
theme.typography.base     // Base (default)
theme.typography.large    // Large
theme.typography.xLarge   // Extra large
theme.typography.x2Large  // 2x large
theme.typography.x3Large  // 3x large
theme.typography.x4Large  // 4x large
theme.typography.x5Large  // 5x large
theme.typography.x6Large  // 6x large
theme.typography.x7Large  // 7x large
theme.typography.x8Large  // 8x large
theme.typography.x9Large  // 9x large
```

### Weight Variants

```dart
theme.typography.thin       // 100
theme.typography.extraLight // 200
theme.typography.light      // 300
theme.typography.normal     // 400 (default)
theme.typography.medium     // 500
theme.typography.semiBold   // 600
theme.typography.bold       // 700
theme.typography.extraBold  // 800
theme.typography.black      // 900
```

### Semantic Styles

```dart
theme.typography.h1         // Heading 1
theme.typography.h2         // Heading 2
theme.typography.h3         // Heading 3
theme.typography.h4         // Heading 4
theme.typography.p          // Paragraph
theme.typography.lead       // Lead paragraph
theme.typography.textLarge  // Large text
theme.typography.textSmall  // Small text
theme.typography.textMuted  // Muted text
theme.typography.blockQuote // Block quote
theme.typography.inlineCode // Inline code
```

### Font Families

```dart
theme.typography.sans  // Sans-serif (default)
theme.typography.mono  // Monospace
```

### Scaling Typography

```dart
// Scale all font sizes
final scaledTypography = theme.typography.scale(1.2);

// Copy with modifications
final customTypography = theme.typography.copyWith(
  h1: () => TextStyle(fontSize: 48, fontWeight: FontWeight.bold),
  base: () => TextStyle(fontSize: 16),
);
```

---

## Theme Configuration

### Basic Setup

```dart
ShadcnApp(
  title: 'My App',
  theme: ThemeData(
    brightness: Brightness.light,
    colorScheme: ColorSchemes.lightBlue,
  ),
  darkTheme: ThemeData(
    brightness: Brightness.dark,
    colorScheme: ColorSchemes.darkBlue,
  ),
  themeMode: ThemeMode.system,
  home: MyHomePage(),
)
```

### Custom Theme

```dart
ThemeData(
  brightness: Brightness.light,
  colorScheme: ColorScheme(
    brightness: Brightness.light,
    background: Colors.white,
    foreground: Colors.black87,
    primary: const Color(0xFF3B82F6),
    primaryForeground: Colors.white,
    secondary: const Color(0xFFF1F5F9),
    secondaryForeground: Colors.black87,
    destructive: const Color(0xFFEF4444),
    destructiveForeground: Colors.white,
    muted: const Color(0xFFF1F5F9),
    mutedForeground: const Color(0xFF64748B),
    accent: const Color(0xFFF1F5F9),
    accentForeground: Colors.black87,
    border: const Color(0xFFE2E8F0),
    input: const Color(0xFFE2E8F0),
    ring: const Color(0xFF3B82F6),
    card: Colors.white,
    cardForeground: Colors.black87,
    popover: Colors.white,
    popoverForeground: Colors.black87,
    chart1: const Color(0xFF3B82F6),
    chart2: const Color(0xFF10B981),
    chart3: const Color(0xFFF59E0B),
    chart4: const Color(0xFF8B5CF6),
    chart5: const Color(0xFFEC4899),
  ),
  radius: 0.5,
  scaling: 1.0,
)
```

### Adaptive Scaling

```dart
// Create a scaled theme
final adaptiveScaling = AdaptiveScaling(
  radiusScaling: 1.0,
  sizeScaling: 1.2,  // Larger on tablets
  textScaling: 1.1,
);

final scaledTheme = adaptiveScaling.scale(baseTheme);
```

---

## Icon Theme

### IconThemeProperties

```dart
IconThemeProperties(
  small: 16.0,
  medium: 20.0,
  large: 24.0,
  xLarge: 28.0,
  x2Large: 32.0,
  x3Large: 36.0,
  x4Large: 40.0,
  xSmall: 12.0,
  x2Small: 10.0,
  x3Small: 8.0,
  x4Small: 6.0,
)

// Scaling icons
final scaledIcons = theme.iconTheme.scale(1.2);
```

---

## Common Patterns

### Themed Container

```dart
Container(
  decoration: BoxDecoration(
    color: theme.colorScheme.card,
    borderRadius: theme.borderRadiusMd,
    border: Border.all(color: theme.colorScheme.border),
  ),
  padding: EdgeInsets.all(16 * theme.scaling),
  child: content,
)
```

### Themed Text

```dart
Text(
  'Title',
  style: theme.typography.h2.copyWith(
    color: theme.colorScheme.foreground,
  ),
)

Text(
  'Subtitle',
  style: theme.typography.base.copyWith(
    color: theme.colorScheme.mutedForeground,
  ),
)
```

### Conditional Dark Mode

```dart
final isDark = theme.brightness == Brightness.dark;

Container(
  color: isDark 
    ? theme.colorScheme.card 
    : theme.colorScheme.background,
)
```

---

## Best Practices

1. **Always use theme colors** - Never hardcode colors
2. **Use semantic colors** - `destructive` for errors, `muted` for secondary info
3. **Apply scaling** - Use `theme.scaling` for spacing/sizing
4. **Use typography** - Access via `theme.typography`, not raw TextStyle
5. **Test both modes** - Verify light and dark themes
6. **Use border radius constants** - `theme.borderRadiusMd` instead of raw values
