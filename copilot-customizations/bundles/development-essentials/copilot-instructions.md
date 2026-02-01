# Development Essentials Bundle

This bundle provides essential development tools and workflows for software development teams.

## 🎯 What's Included

### Skills

#### test-driven-development
Enforces the RED-GREEN-REFACTOR TDD cycle for all feature and bugfix implementations.

**When to use:** Before implementing any feature or bugfix
**Workflow:**
1. Write a failing test first (RED)
2. Write minimal code to pass the test (GREEN)
3. Refactor while keeping tests green (REFACTOR)

**Example:**
```
Use the test-driven-development skill when implementing new features
```

#### systematic-debugging
Provides a systematic approach to debugging that focuses on root cause analysis.

**When to use:** When encountering bugs, test failures, or unexpected behavior
**Approach:**
1. Reproduce the issue reliably
2. Understand the expected vs actual behavior
3. Form hypotheses about the root cause
4. Test hypotheses systematically
5. Fix the root cause, not symptoms

#### skill-creator
Comprehensive guide for creating effective GitHub Copilot skills.

**When to use:** Creating or modifying GitHub Copilot skills
**Features:**
- Skill structure guidance
- Best practices
- Validation tools

#### subagent-driven-development
Execute implementation plans by dispatching fresh subagents for each independent task.

**When to use:** 
- You have an implementation plan with independent tasks
- Tasks can be done in sequence
- Need isolation between tasks

### Agents

#### skill-builder
Expert agent for creating and modifying GitHub Copilot skills following skill-creator guidelines.

**Usage:**
```
@skill-builder create a new skill for Python testing with pytest
```

### Prompts

#### git
Reusable prompt for Git operations and repository management.

**Usage:** Use for git-related tasks, commits, branches, and repository management

## 🚀 Getting Started

1. This bundle is installed in your `.github/` directory
2. All skills are automatically available to GitHub Copilot
3. Use the skill-builder agent to create custom skills
4. Follow TDD workflow for all implementations
5. Use systematic debugging when issues arise

## 💡 Recommended Workflow

### For New Features
1. Invoke `test-driven-development` skill
2. Write failing tests first
3. Implement minimal code
4. Refactor and improve
5. Use `git` prompt for commits

### For Debugging
1. Invoke `systematic-debugging` skill
2. Follow root cause analysis approach
3. Fix the underlying issue
4. Add tests to prevent regression

### For Creating Skills
1. Use `@skill-builder` agent or `skill-creator` skill
2. Follow the skill structure guidelines
3. Test the skill in realistic scenarios

## 📚 Best Practices

- **Always start with tests** - Use TDD for all implementations
- **Debug systematically** - Don't guess, investigate root causes
- **Create skills for repeated patterns** - Use skill-creator
- **Use subagents for complex tasks** - Keep contexts clean and focused
- **Commit frequently** - Use git prompt for good commit messages

## 🔗 Dependencies

All resources in this bundle are from the latest versions:
- ✓ skill-builder agent (agents/latest/)
- ✓ git prompt (prompts/latest/)
- ✓ test-driven-development skill (skills/latest/)
- ✓ systematic-debugging skill (skills/latest/)
- ✓ skill-creator skill (skills/latest/)
- ✓ subagent-driven-development skill (skills/latest/)

## 📖 Learn More

For detailed information on each skill, agent, or prompt, refer to their individual documentation in the `.github/` directory after installation.
