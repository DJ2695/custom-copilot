# shadcn Design Guide

Comprehensive design patterns and guidelines for building beautiful, accessible UIs with shadcn.

---

## Color Philosophy

### Semantic Color System

shadcn uses **meaning-based colors**, not generic ones:

| Color | Purpose | When to Use |
|-------|---------|-------------|
| **primary** | Main actions, branding | Submit buttons, primary CTAs, key links |
| **secondary** | Supporting actions | Secondary buttons, less important actions |
| **destructive** | Dangerous actions | Delete, remove, cancel subscriptions |
| **muted** | Backgrounds, subdued content | Less important text, placeholder content, disabled states |
| **accent** | Highlights, selection | Selected items, hover states, badges |

### Foreground/Background Pairing

**RULE**: Every color has a matching foreground for contrast.

```
primary / primaryForeground
destructive / destructiveForeground
muted / mutedForeground
accent / accentForeground
background / foreground
card / cardForeground
```

**Example pattern:**
- Card background: `card` color
- Card text: `cardForeground` color
- Never mix pairings (e.g., don't use `primary` with `mutedForeground`)

### When to Use Each Variant

**Buttons:**
- `primary` - Main action on page (submit form, create item)
- `secondary` - Secondary action (cancel, go back)
- `outline` - Less emphasis, alternative action
- `ghost` - Minimal emphasis, inline actions
- `destructive` - Delete, remove, dangerous irreversible actions

**Text:**
- `foreground` - Main content text
- `mutedForeground` - Secondary text, captions, metadata
- `primaryForeground` - Text on primary-colored backgrounds

---

## Spacing System

### Consistent Gap Usage

Use **systematic spacing** with a base unit (typically 4px or 8px scaled):

```
Gap(8)   // Tight spacing (within related elements)
Gap(16)  // Standard spacing (between sections)
Gap(24)  // Loose spacing (major sections)
Gap(32)  // Wide spacing (page sections)
```

### Scaling Multiplier

For responsive design, use a `scaling` factor:

```
padding = baseValue * scaling
```

This keeps proportions consistent across screen sizes.

### Spacing Patterns

| Scenario | Spacing |
|----------|---------|
| Form field labels → input | 8px |
| Between form fields | 16px |
| Between form sections | 24-32px |
| Card padding | 16-24px |
| Dialog padding | 24px |
| Page margins | 24-48px |

---

## Accessibility Patterns

### Keyboard Navigation

**Standard expectations:**
- `Tab` - Move to next interactive element
- `Shift+Tab` - Move to previous
- `Enter` / `Space` - Activate button/control
- `Esc` - Close dialog/popover/dropdown
- Arrow keys - Navigate within lists, menus, tabs

**Ensure:**
- All interactive elements are keyboard accessible
- Focus visible indicator on all focusable elements
- Tab order matches visual order

### Focus Management

**Dialog/Modal patterns:**
1. When opened, focus first interactive element (or close button)
2. Trap focus within modal (Tab cycles within)
3. On close, return focus to trigger element

**Form patterns:**
1. Auto-focus first field when form appears
2. On validation error, focus first invalid field
3. After submit, focus confirmation message or next step

### Screen Reader Support

**Label all inputs:**
- Use Label widget with `htmlFor` or wrap input
- Provide `aria-label` for icon-only buttons

**Use semantic structure:**
- Headings for sections (`h1`, `h2`, etc.)
- Lists for list content
- Proper button vs link semantics

**Provide feedback:**
- Announce loading states
- Announce success/error after actions
- Include visually hidden status messages when needed

---

## Composition Principles

### Build from Primitives

shadcn encourages **composing complex UIs** from simple components:

**Bad:** One giant custom component

**Good:** Compose from Card, Button, TextField, etc.

**Example - User Profile Card:**
```
Card
  ├─ Avatar
  ├─ Text (name)
  ├─ Text.muted (email)
  ├─ Separator
  └─ Button.outline (Edit Profile)
```

### Layering

Visual hierarchy through elevation and borders:

1. **Background** - Base page background
2. **Card** - Elevated content grouping
3. **Popover/Dialog** - Highest elevation, temporary overlay

**Avoid:**
- Card inside Card (use OutlinedContainer for nesting)
- Too many elevation levels (keep it simple)

### Consistency

**Use the same pattern for similar tasks:**
- All delete actions use `Button.destructive`
- All optional fields have "(optional)" in label
- All forms follow same field structure
- All errors use same style and placement
