# shadcn Layout Patterns

Common layout patterns for pages, forms, modals, and data displays.

---

## Form Design Patterns

### Layout Principles

**Single-column for most forms:**
```
┌─────────────────┐
│ [Label]         │
│ [Input]         │
│                 │
│ [Label]         │
│ [Input]         │
│                 │
│ [Submit Button] │
└─────────────────┘
```

**Multi-column for short, related fields:**
```
┌────────────┬────────────┐
│ [First]    │ [Last]     │
│            │            │
│ [Email (full width)]   │
│                        │
│ [Submit Button]        │
└────────────────────────┘
```

### Field Structure

Standard field pattern:
1. **Label** (above input, left-aligned)
2. **Input** (TextField, Select, etc.)
3. **Helper text** (optional, muted)
4. **Error message** (destructive color, appears on validation failure)

### Validation Patterns

**Inline validation:**
- Show errors after field loses focus (onBlur)
- Clear errors as user fixes them (onChange)
- Use destructive color for error text and border
- Include error icon for clarity

**Form-level validation:**
- Validate all fields on submit
- Scroll to first error
- Show summary Alert at top if multiple errors

### Multi-Step Forms

Use `Steps` or `Stepper` component:
```
[1 Personal Info] → [2 Address] → [3 Payment] → [4 Review]
```

**Pattern:**
1. Show current step prominently
2. Allow navigation to completed steps
3. Disable future steps until current is valid
4. Show progress indicator
5. Provide "Save & Continue" + "Back" buttons

---

## Layout Patterns

### Settings Page

```
┌─────────────────────────────────┐
│ Page Title                      │
│ Description                     │
├─────────────────────────────────┤
│ ┌─ Section Card ─────────────┐ │
│ │ Heading                     │ │
│ │ Description                 │ │
│ │                             │ │
│ │ [Setting Option 1]          │ │
│ │ [Setting Option 2]          │ │
│ │                             │ │
│ │           [Save Button]     │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─ Another Section ──────────┐ │
│ │ ...                         │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

**Pattern:**
- Group related settings in Cards
- Use `Separator` between logical groups
- Show save button per card or global at bottom
- Use muted text for descriptions

### Dashboard Layout

```
┌─────────────────────────────────────┐
│ [Header with title and actions]     │
├──────────────┬──────────────────────┤
│ [Stat Card]  │ [Stat Card]          │
├──────────────┼──────────────────────┤
│ [Chart Card]                        │
├─────────────────────────────────────┤
│ [Table/List with pagination]        │
└─────────────────────────────────────┘
```

**Pattern:**
- Use Card for each data grouping
- Stats at top (key metrics)
- Charts/visualizations in middle
- Detailed data (tables) at bottom
- Responsive: stack cards on mobile

### Empty States

Always design for empty states:

```
┌─────────────────────┐
│                     │
│     [Icon]          │
│                     │
│  No items yet       │
│  Get started by...  │
│                     │
│  [Primary Button]   │
└─────────────────────┘
```

**Pattern:**
- Center the content vertically
- Use appropriate icon (not just text)
- Explain why it's empty
- Provide clear action to populate

---

## Modal Patterns

### Confirmation Dialog

```
┌──────────────────────┐
│ Delete Item?         │
│                      │
│ This action cannot   │
│ be undone.           │
│                      │
│ [Cancel] [Delete]    │
└──────────────────────┘
```

**Pattern:**
- Clear, direct title (question or statement)
- Brief explanation of consequence
- Destructive action on right (Delete, Remove)
- Safe action on left (Cancel)
- Use `Button.destructive` for dangerous action

### Form Dialog

```
┌──────────────────────┐
│ Add New Item     [X] │
│                      │
│ [Name]               │
│ [_____________]      │
│                      │
│ [Description]        │
│ [_____________]      │
│ [_____________]      │
│                      │
│ [Cancel] [Add]       │
└──────────────────────┘
```

**Pattern:**
- Close button (X) in top-right
- Form fields follow standard field structure
- Actions at bottom (Cancel + Submit)
- Primary action on right
- Consider Sheet for longer forms

---

## List & Table Patterns

### Simple List

```
┌─────────────────────────┐
│ [Item 1]         [>]    │
│ [Item 2]         [>]    │
│ [Item 3]         [>]    │
└─────────────────────────┘
```

**Pattern:**
- Use Card or OutlinedContainer for list container
- Separator between items
- Chevron or action icon on right if clickable
- Show item count if relevant

### Data Table

```
┌─────────────────────────────┐
│ Name          Status  Action│
├─────────────────────────────┤
│ John Doe      Active  [...]│
│ Jane Smith    Pending [...]│
│                             │
│ Page 1 of 5   [< 1 2 3 >]  │
└─────────────────────────────┘
```

**Pattern:**
- Headers with sort indicators
- Row actions (kebab menu or icon buttons)
- Pagination at bottom
- Selection checkboxes if batch actions available
- Use muted text for secondary data
- Empty state when no data
