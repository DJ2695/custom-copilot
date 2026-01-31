---
name: shadcn-design-patterns
description: 'Design beautiful UIs following shadcn/ui principles. Use when planning layouts, choosing components, composing forms/dialogs/pages, or making design decisions. Framework-agnostic patterns for shadcn implementations (React, Flutter, Vue, etc.).'
---

# shadcn Design Patterns

Framework-agnostic design patterns for building beautiful, accessible UIs with shadcn's design philosophy.

## When to Use This Skill

- Planning page or screen layouts
- Choosing the right component for a task
- Designing forms, dialogs, or complex interactions
- Making design decisions (colors, spacing, hierarchy)
- Building consistent, accessible UIs

**Pair with implementation skills** (ui-shadcn-flutter, shadcn-ui, etc.) for concrete code.

---

## Core Philosophy

1. **Minimalism** - Clean, uncluttered interfaces
2. **Composability** - Build complex UIs from simple primitives
3. **Accessibility-first** - ARIA patterns, keyboard navigation
4. **Semantic color** - Named colors convey meaning (primary, destructive, muted)
5. **Consistent spacing** - Systematic gaps using scaling multipliers
6. **Beautiful defaults** - Components look good out-of-the-box

---

## Quick Color Guide

**Semantic colors:**
- `primary` - Main actions, submit buttons, CTAs
- `secondary` - Supporting actions
- `destructive` - Delete, remove, dangerous actions
- `muted` - Subdued content, secondary text, disabled states
- `accent` - Highlights, selection, badges

**Pairing rule:** Always pair colors (primary + primaryForeground, card + cardForeground, etc.)

---

## Quick Spacing Guide

Use systematic spacing:
- `8px` - Tight (within elements)
- `16px` - Standard (between sections)
- `24px` - Loose (major sections)
- `32px` - Wide (page sections)

## Component Selection Guide

### Dialog vs Sheet vs Popover

**Use Dialog when:**
- Requires user's full attention (confirmation, critical info)
- User must respond before continuing
- Content is self-contained
- Small to medium content (fits viewport)

**Use Sheet when:**
- Large amount of content (scrollable)
- Contextual to current page
- Can be dismissed easily
- Forms, filters, settings panels

**Use Popover when:**
- Small, contextual information
- Doesn't block interaction with page
- Hover cards, tooltips with rich content
- Quick actions (color picker, date picker)

### Card vs OutlinedContainer

**Card vs OutlinedContainer:**
- Card: Elevated content, prominent grouping
- OutlinedContainer: Subtle borders, nested containers

**Alert vs Toast:**
- Alert: Inline, persistent messages
- Toast: Temporary notifications, auto-dismiss

**Sheet vs Dialog vs Popover:**
- Sheet: Large scrollable content, side/bottom panels
- Dialog: Modal, requires attention, blocking
- Popover: Small contextual content, non-blocking

---

## Reference Documentation

For detailed patterns:

- **[design-guide.md](references/design-guide.md)** - Color system, spacing, accessibility, composition
- **[layout-patterns.md](references/layout-patterns.md)** - Forms, pages, modals, lists, tables

## Rules

✅ **DO:**
- Use semantic colors (primary, destructive, muted)
- Pair colors correctly (primary + primaryForeground)
- Compose complex UIs from simple primitives
- Follow accessibility patterns (keyboard, focus, labels)
- Use consistent spacing throughout
- Provide empty states and loading states
- Make dangerous actions explicit (confirmation dialogs)

❌ **DON'T:**
- Use arbitrary colors outside the system
- Mix color pairings (e.g., primary bg + muted text)
- Create giant custom components (compose instead)
- Skip keyboard navigation support
- Use inconsistent spacing values
- Hide important actions behind multiple clicks
- Make destructive actions easy to trigger accidentally

---

## Pair with Implementation Skills

This skill provides **design patterns**. For concrete implementation:

- **Flutter**: Use `ui-shadcn-flutter` skill for Flutter widget APIs
- **React**: Use standard shadcn/ui component documentation
- **Other frameworks**: Adapt patterns to available shadcn implementation
primitives
- Follow accessibility patterns
- Use consistent spacing
- Provide empty states
- Confirm dangerous actions

❌ **DON'T:**
- Use arbitrary colors
- Mix color pairings
- Create giant monolithic components
- Skip keyboard navigation
- Use inconsistent spacing
- Make destructive actions easy to trigger