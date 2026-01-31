# shadcn_flutter Advanced Components

Edge case and specialized components used less frequently.

---

## Specialized Form Inputs

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

### NumberInput

Dedicated numeric input with increment/decrement.

```dart
NumberInput(
  value: quantity,
  onChanged: (value) => setState(() => quantity = value),
  min: 0,
  max: 100,
  step: 1,
)
```

### InputOTP

One-time password input.

```dart
InputOTP(
  length: 6,
  onCompleted: (code) => verifyCode(code),
  obscureText: false,
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
  suggestions: ['tag1', 'tag2', 'tag3'],
)
```

---

## Advanced Layout

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
      child: Page1(),
    ),
    TabItem(
      header: Text('Tab 2'),
      child: Page2(),
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
Steps(
  currentStep: currentStep,
  children: [
    StepItem(
      title: 'Personal Info',
      description: 'Enter your details',
      content: PersonalInfoForm(),
    ),
    StepItem(
      title: 'Address',
      description: 'Your location',
      content: AddressForm(),
    ),
    StepItem(
      title: 'Confirm',
      content: ConfirmView(),
    ),
  ],
)

// Alternative with Stepper
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

### Resizable

Adjustable panels.

```dart
Resizable(
  children: [
    ResizablePane(
      initialSize: 200,
      minSize: 100,
      maxSize: 400,
      child: sidePanel,
    ),
    ResizablePane(
      child: mainContent,
    ),
  ],
)
```

### Scaffold

Page structure with headers/footers.

```dart
Scaffold(
  header: Container(
    padding: const EdgeInsets.all(16),
    child: Text('Header'),
  ),
  footer: Container(
    padding: const EdgeInsets.all(16),
    child: Text('Footer'),
  ),
  child: mainContent,
)
```

---

## Advanced Overlays

### Popover

Floating content anchored to trigger.

```dart
Popover(
  trigger: Button.outline(child: Text('Open')),
  content: (context) => PopoverContent(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Popover content'),
        Gap(8),
        Button.primary(
          onPressed: () => action(),
          child: Text('Action'),
        ),
      ],
    ),
  ),
  side: PopoverSide.bottom,  // Placement
  align: PopoverAlign.center, // Alignment
)
```

### HoverCard

Rich hover content.

```dart
HoverCard(
  trigger: Text('Hover me'),
  content: (context) => HoverCardContent(
    child: Column(
      children: [
        Avatar(initials: 'JD'),
        Text('John Doe'),
        Text('Software Engineer').small().muted(),
      ],
    ),
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
  side: TooltipSide.top,
)
```

### DropdownMenu

Action menu.

```dart
DropdownMenu(
  trigger: Button.ghost(
    child: const Icon(LucideIcons.moreVertical),
  ),
  children: [
    MenuItem(
      leading: const Icon(LucideIcons.edit),
      child: const Text('Edit'),
      onPressed: () => handleEdit(),
    ),
    const MenuDivider(),
    MenuItem(
      leading: const Icon(LucideIcons.trash),
      child: const Text('Delete'),
      onPressed: () => handleDelete(),
      destructive: true,
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
    MenuItem(
      child: Text('Delete'),
      onPressed: () => delete(),
      destructive: true,
    ),
  ],
)
```

### Drawer

Side navigation panel.

```dart
// In Scaffold or custom
Drawer(
  child: Column(
    children: [
      DrawerHeader(child: Text('Menu')),
      ListTile(title: Text('Home'), onTap: () => navigate('/home')),
      ListTile(title: Text('Settings'), onTap: () => navigate('/settings')),
    ],
  ),
)
```

---

## Data Display

### Avatar / AvatarGroup

User images with fallback.

```dart
Avatar(
  initials: 'JD',
  imageUrl: user.avatarUrl,
  size: AvatarSize.medium,  // small, medium, large
  shape: AvatarShape.circle, // or .square
)

// Group of avatars
AvatarGroup(
  maxAvatars: 3,
  overflowWidget: Badge(child: Text('+2')),
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

Badge(
  variant: BadgeVariant.secondary,
  child: const Text('Beta'),
)
```

### Table / DataTable

Data tables.

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

// Interactive table with sorting
DataTable(
  columns: [
    DataColumn(
      label: Text('Name'),
      onSort: (columnIndex, ascending) => sort('name', ascending),
    ),
    DataColumn(label: Text('Email')),
  ],
  rows: items.map((item) => DataRow(
    cells: [
      DataCell(Text(item.name)),
      DataCell(Text(item.email)),
    ],
    onSelectChanged: (selected) => handleSelection(item, selected),
  )).toList(),
  sortColumnIndex: 0,
  sortAscending: true,
)
```

### Calendar

Date calendar.

```dart
Calendar(
  initialView: CalendarView.now(),
  selectionMode: CalendarSelectionMode.single,  // or .multiple, .range
  onChanged: (value) {
    if (value is SingleCalendarValue) {
      print('Selected: ${value.date}');
    } else if (value is RangeCalendarValue) {
      print('Range: ${value.start} - ${value.end}');
    }
  },
)
```

---

## Navigation

### Breadcrumb

Path navigation.

```dart
Breadcrumb(
  separator: const Icon(LucideIcons.chevronRight, size: 16),
  children: [
    BreadcrumbItem(
      child: Text('Home'),
      onPressed: () => navigate('/'),
    ),
    BreadcrumbItem(
      child: Text('Products'),
      onPressed: () => navigate('/products'),
    ),
    BreadcrumbItem(
      child: Text('Details'),
    ),  // Current page (no onPressed)
  ],
)
```

### Pagination

Page navigation.

```dart
Pagination(
  page: currentPage,
  totalPages: totalPages,
  onPageChanged: (page) => setState(() => currentPage = page),
  siblingsCount: 1,  // Pages shown around current
  boundaryCount: 1,  // Pages at start/end
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
        child: Column(
          children: [
            MenuItem(child: Text('Product A'), onPressed: () => nav('/a')),
            MenuItem(child: Text('Product B'), onPressed: () => nav('/b')),
          ],
        ),
      ),
    ),
    NavigationMenuItem(
      child: Text('Pricing'),
      onPressed: () => navigate('/pricing'),
    ),
  ],
)
```

### Menubar

Application menu bar.

```dart
Menubar(
  children: [
    MenubarMenu(
      label: const Text('File'),
      children: [
        MenuItem(child: Text('New'), onPressed: () => newFile()),
        MenuItem(child: Text('Open'), onPressed: () => openFile()),
        const MenuDivider(),
        MenuItem(child: Text('Exit'), onPressed: () => exit()),
      ],
    ),
    MenubarMenu(
      label: const Text('Edit'),
      children: [
        MenuItem(child: Text('Undo'), onPressed: () => undo()),
        MenuItem(child: Text('Redo'), onPressed: () => redo()),
      ],
    ),
  ],
)
```

---

## Animation

### AnimatedValueBuilder

Animate value changes.

```dart
AnimatedValueBuilder<double>(
  value: progress,
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  builder: (context, value, child) {
    return Container(
      width: value * 200,
      height: 20,
      color: theme.colorScheme.primary,
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
  curve: Curves.easeOut,
  style: theme.typography.large,
)
```

---

## Specialized Widgets

### Command

Command palette / search.

```dart
Command(
  placeholder: 'Type a command...',
  onSearch: (query) => searchCommands(query),
  children: [
    CommandGroup(
      heading: const Text('Suggestions'),
      children: [
        CommandItem(
          leading: Icon(LucideIcons.calendar),
          child: Text('Calendar'),
          onPressed: () => openCalendar(),
        ),
        CommandItem(
          leading: Icon(LucideIcons.search),
          child: Text('Search'),
          onPressed: () => search(),
        ),
      ],
    ),
  ],
)
```

### Carousel

Image/content carousel.

```dart
Carousel(
  itemCount: images.length,
  itemBuilder: (context, index) {
    return Image.network(images[index]);
  },
  autoPlay: true,
  autoPlayInterval: const Duration(seconds: 3),
)
```

### Collapsible

Toggle visibility.

```dart
Collapsible(
  trigger: (context, isOpen) => Button.ghost(
    child: Text(isOpen ? 'Hide' : 'Show'),
  ),
  child: Container(
    padding: const EdgeInsets.all(16),
    child: Text('Hidden content'),
  ),
)
```

### Separator

Divider with optional label.

```dart
// Simple separator
const Separator()

// With label
Separator(
  label: const Text('OR'),
  orientation: Orientation.horizontal,
)
```

### ScrollArea

Custom scrollable area.

```dart
ScrollArea(
  child: Container(
    height: 500,
    child: longContent,
  ),
)
```

---

## Chart Components

### Chart

Basic chart wrapper.

```dart
Chart(
  data: chartData,
  config: ChartConfig(
    type: ChartType.line,  // or .bar, .pie
    xAxis: ChartAxis(label: 'Month'),
    yAxis: ChartAxis(label: 'Revenue'),
  ),
)
```

---

## No Direct Material Equivalent

These components have no Material counterpart:

- **InputOTP** - Build OTP input from scratch in Material
- **ChipInput** - Use Chips + TextField manually
- **HoverCard** - Custom implementation
- **Popover** - Similar to PopupMenuButton but more flexible
- **Command** - Command palette pattern
- **Carousel** - Use package like carousel_slider
- **Resizable** - Custom drag/resize logic
- **NavigationMenu** - Complex nested menu
- **Menubar** - Application menu bar
- **Collapsible** - AnimatedContainer manually
