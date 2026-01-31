# Ready-to-Use Instruction File Examples

## General Coding Standards

```markdown
---
applyTo: "**"
---

# General Coding Standards

## Naming Conventions

- Use PascalCase for classes, interfaces, types, and enums
- Use camelCase for variables, functions, and methods
- Use SCREAMING_SNAKE_CASE for constants
- Use descriptive names that reveal intent
- Avoid abbreviations unless universally understood

## Code Organization

- Keep files focused on a single concept
- Limit files to 300 lines (split if larger)
- Group related imports together
- Order: external imports → internal imports → relative imports

## Functions

- Keep functions under 50 lines
- Single responsibility per function
- Maximum 4 parameters (use object for more)
- Return early to reduce nesting

## Error Handling

- Never silently swallow errors
- Use typed exceptions/errors
- Log with context (what, where, why)
- Provide actionable error messages

## Comments

- Write self-documenting code first
- Comment WHY, not WHAT
- Keep comments up to date
- Remove commented-out code
```

---

## Python Standards

```markdown
---
applyTo: "**/*.py"
---

# Python Coding Standards

Apply [general standards](./general-coding.instructions.md).

## Style

- Follow PEP 8
- Line length: 88 characters (Black default)
- Use 4 spaces for indentation

## Type Hints

- Required for all function signatures
- Use `typing` module for complex types
- Use `Optional` for nullable types
- Use `TypeAlias` for complex type definitions

## Documentation

- Docstrings for all public functions/classes
- Use Google or NumPy docstring format
- Include Args, Returns, Raises sections

## Imports

```python
# Standard library
import os
from pathlib import Path

# Third-party
import pandas as pd
from pydantic import BaseModel

# Local
from .models import User
```

## Best Practices

- Use context managers for resources
- Prefer list comprehensions for simple transforms
- Use dataclasses or Pydantic for data structures
- Use `pathlib.Path` over `os.path`
```

---

## TypeScript Standards

```markdown
---
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript Coding Standards

Apply [general standards](./general-coding.instructions.md).

## Type Safety

- Avoid `any` - use `unknown` if type is uncertain
- Define explicit return types for functions
- Use interfaces for object shapes
- Use type guards for runtime checks

## Null Handling

- Use optional chaining: `obj?.property`
- Use nullish coalescing: `value ?? default`
- Avoid non-null assertions (`!`) unless necessary

## Async Code

- Always handle Promise rejections
- Use async/await over raw Promises
- Avoid nested callbacks

## Interfaces vs Types

```typescript
// Use interfaces for object shapes
interface User {
  id: string;
  name: string;
}

// Use types for unions, intersections, primitives
type Status = 'pending' | 'active' | 'completed';
type Nullable<T> = T | null;
```

## Imports

- Use named exports over default exports
- Use barrel files (index.ts) for public APIs
- Avoid circular dependencies
```

---

## React Standards

```markdown
---
applyTo: "**/*.tsx,**/components/**/*.ts"
---

# React Coding Standards

Apply [TypeScript standards](./typescript-coding.instructions.md).

## Components

- Use functional components with hooks
- One component per file
- Component name matches filename
- Keep components under 200 lines

## Props

```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

export function Button({ label, onClick, disabled = false, variant = 'primary' }: ButtonProps) {
  // ...
}
```

## Hooks

- Follow hooks rules (no conditional hooks)
- Extract complex logic to custom hooks
- Name custom hooks with `use` prefix
- Keep hook dependencies accurate

## State Management

- Lift state to lowest common parent
- Use context for truly global state
- Prefer composition over prop drilling

## Performance

- Memoize expensive computations: `useMemo`
- Memoize callbacks: `useCallback`
- Use `React.memo` for pure components
- Avoid inline object/array definitions in JSX
```

---

## Testing Standards

```markdown
---
applyTo: "**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/tests/**"
---

# Testing Standards

## Structure

- Use AAA pattern: Arrange, Act, Assert
- One concept per test
- Descriptive test names: "should [behavior] when [condition]"

## Naming

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', () => {});
    it('should throw error when email is invalid', () => {});
    it('should hash password before saving', () => {});
  });
});
```

## Mocking

- Mock external dependencies only
- Use dependency injection for testability
- Reset mocks between tests
- Prefer spies over stubs when verifying calls

## Coverage

- Aim for 80%+ coverage on business logic
- Test edge cases and error paths
- Don't test implementation details

## Test Data

- Use factory functions for test data
- Keep test data minimal and focused
- Avoid sharing mutable state between tests
```

---

## Documentation Standards

```markdown
---
applyTo: "docs/**/*.md,**/*.mdx"
---

# Documentation Standards

## Writing Style

- Use present tense: "Returns" not "Will return"
- Use active voice: "The function validates" not "Validation is performed"
- Be direct: Avoid "basically", "simply", "just"
- Write for scanning: Headers, bullets, tables

## Structure

```markdown
# Title

Brief overview (1-2 sentences).

## Prerequisites

- Required knowledge
- Required setup

## Getting Started

Step-by-step guide.

## API Reference

Detailed documentation.

## Examples

Code samples.

## Troubleshooting

Common issues and solutions.
```

## Code Examples

- Test all examples before publishing
- Include comments for complex parts
- Show both input and expected output
- Use realistic but minimal data

## Markdown

- One sentence per line (easier diffs)
- Use fenced code blocks with language
- Add alt text to images
- Use relative links for internal docs
```
