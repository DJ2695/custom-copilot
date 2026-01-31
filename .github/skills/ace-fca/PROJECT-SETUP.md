# ACE-FCA Project Setup Guide

This guide helps you onboard ACE-FCA (Advanced Context Engineering for Coding Agents) methodology to your project.

## Prerequisites

- Git repository initialized
- Basic project structure in place
- GitHub Copilot or compatible AI coding agent

## Quick Setup (5 minutes)

### 1. Create Directory Structure

```bash
# From your project root
mkdir -p docs/{research,plans,adr}
```

### 2. Copy Templates

```bash
# Copy ADR template and README
cp .github/skills/ace-fca/templates/adr-template.md docs/adr/
cp .github/skills/ace-fca/templates/adr-directory-readme.md docs/adr/README.md

# Copy planning and research templates for reference
cp .github/skills/ace-fca/templates/research-template.md docs/
cp .github/skills/ace-fca/templates/plan-template.md docs/
```

### 3. Create First ADR

Document the decision to adopt ACE-FCA:

```bash
cp docs/adr/adr-template.md docs/adr/0001-adopt-ace-fca-methodology.md
```

Edit `docs/adr/0001-adopt-ace-fca-methodology.md`:

```markdown
# 0001. Adopt ACE-FCA Methodology for Development

**Date**: [Today's date]  
**Status**: Accepted  
**Deciders**: [Your team]

## Context

We need a structured approach to work with AI coding agents on this codebase.
ACE-FCA provides proven patterns for context management and implementation workflows.

## Decision

We will adopt the ACE-FCA (Advanced Context Engineering for Coding Agents) methodology
for all feature development, using the Research → Plan → Implement workflow.

## Options Considered

### Option 1: Ad-hoc AI usage
- Pro: No overhead
- Con: Inconsistent results, context pollution

### Option 2: ACE-FCA ⭐ SELECTED
- Pro: Proven patterns, better quality
- Con: Slight learning curve
- Why: Better long-term outcomes justify investment

## Consequences

✅ Consistent development workflow
✅ Better context management  
✅ Architectural decisions documented
❌ Small overhead for research/planning phases

## References

- ACE-FCA Skill: `.github/skills/ace-fca/SKILL.md`
```

### 4. Update Project README

Add to your `README.md`:

```markdown
## Development Workflow

This project uses [ACE-FCA methodology](.github/skills/ace-fca/SKILL.md) for development.

### Directory Structure
- `docs/research/` - Research phase outputs
- `docs/plans/` - Implementation plans
- `docs/adr/` - Architectural Decision Records

### Implementing Features

1. **Research**: Investigate and document (→ `docs/research/`)
2. **Plan**: Break down into tasks (→ `docs/plans/`)
3. **Implement**: Execute with TDD, document ADRs
```

### 5. Verify Setup

```bash
# Check directory structure
tree docs/

# Should show:
# docs/
# ├── adr/
# │   ├── README.md
# │   ├── adr-template.md
# │   └── 0001-adopt-ace-fca-methodology.md
# ├── plans/
# ├── research/
# ├── plan-template.md
# └── research-template.md
```

## Detailed Setup

### For Existing Codebases

When onboarding ACE-FCA to an existing project:

#### 1. Initial Research Phase

Create baseline understanding of the codebase:

```bash
# Use AI agent to research
# Agent prompt:
```

Research the codebase using ACE-FCA methodology.

Task: Create baseline documentation for this project.

Questions:
1. What is the overall architecture?
2. What are the key modules/components?
3. What testing patterns are used?
4. What are the main dependencies?
5. Are there any existing architectural patterns to follow?

Output: `docs/research/[DATE]-codebase-overview.md`
Use template: `docs/research-template.md`
```

#### 2. Document Current Architecture

Create ADRs for existing architectural decisions:

```bash
# Example ADRs to create:
docs/adr/0002-existing-database-choice.md
docs/adr/0003-existing-api-framework.md
docs/adr/0004-existing-authentication-method.md
```

This creates a baseline for future decisions.

#### 3. Set Up Testing Baseline

Document and verify test setup:

```bash
# Run existing tests
[your test command]

# Document in README or docs/testing.md:
- Test framework: [name]
- Coverage target: [percentage]
- Run tests: [command]
- Watch mode: [command]
```

### For New Projects

Starting fresh with ACE-FCA:

#### 1. Initial Setup
```bash
# Project structure
mkdir -p {src,tests,docs/{research,plans,adr}}

# Copy templates
cp .github/skills/ace-fca/templates/*.md docs/
cp docs/adr-template.md docs/adr/
```

#### 2. First Decisions as ADRs

Document initial technical choices:
- `0001-adopt-ace-fca-methodology.md`
- `0002-choose-[language/framework].md`
- `0003-choose-[database].md`
- `0004-choose-[testing-framework].md`

#### 3. Create Initial Plan

First feature as a demonstration:

```bash
cp docs/plan-template.md docs/plans/[DATE]-initial-setup-plan.md
```

## Integration with Git

### .gitignore

Add to `.gitignore` if needed:
```gitignore
# Keep research and plans in version control - they're valuable
# But you might want to ignore work-in-progress:
docs/research/*-wip.md
docs/plans/*-wip.md
```

### Git Hooks (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Ensure ADRs follow naming convention

for file in $(git diff --cached --name-only | grep '^docs/adr/[0-9]'); do
  if ! [[ $(basename "$file") =~ ^[0-9]{4}-.+\.md$ ]]; then
    echo "Error: ADR must match format NNNN-title.md: $file"
    exit 1
  fi
done
```

## Team Onboarding

### For Team Members

Share this checklist with new team members:

- [ ] Read [ACE-FCA SKILL.md](.github/skills/ace-fca/SKILL.md)
- [ ] Review existing ADRs in `docs/adr/`
- [ ] Read latest research docs in `docs/research/`
- [ ] Understand current implementation plans in `docs/plans/`
- [ ] Try the workflow on a small task

### Sample First Task

Give new team members a starter task:

```markdown
# Your First ACE-FCA Task

**Goal**: Add a simple validation function using ACE-FCA workflow

**Steps**:
1. Research: Look at existing validation patterns
   - Create `docs/research/[DATE]-validation-patterns.md`
   
2. Plan: Break down into tasks
   - Create `docs/plans/[DATE]-add-email-validation-plan.md`
   - Include 3-5 small tasks
   
3. Implement: Execute with TDD
   - One task at a time
   - Commit after each task
   - Update plan with progress

**Success**: Feature working, tests passing, docs updated
```

## Tooling Integration

### VS Code

Add to `.vscode/settings.json`:
```json
{
  "files.associations": {
    "**/docs/adr/*.md": "markdown",
    "**/docs/plans/*.md": "markdown",
    "**/docs/research/*.md": "markdown"
  },
  "markdown.extension.toc.levels": "2..3",
  "cSpell.words": [
    "ACE-FCA"
  ]
}
```

### Task Runners

Add to `package.json` (Node.js) or equivalent:
```json
{
  "scripts": {
    "adr:new": "cp docs/adr/adr-template.md docs/adr/$(printf '%04d' $(($(ls -1 docs/adr/[0-9]*.md 2>/dev/null | wc -l) + 1)))-new.md",
    "research:new": "cp docs/research-template.md docs/research/$(date +%Y-%m-%d)-new.md",
    "plan:new": "cp docs/plan-template.md docs/plans/$(date +%Y-%m-%d)-new.md"
  }
}
```

Usage:
```bash
npm run adr:new        # Creates next numbered ADR
npm run research:new   # Creates dated research doc
npm run plan:new       # Creates dated plan doc
```

## Validation Checklist

After setup, verify:

- [ ] Directory structure created (`docs/{research,plans,adr}`)
- [ ] Templates copied to docs directory
- [ ] First ADR created (adopting ACE-FCA)
- [ ] ADR README updated with project-specific info
- [ ] Project README documents ACE-FCA usage
- [ ] Testing baseline documented
- [ ] Team members notified of new workflow

## Common Customizations

### Adjust for Project Size

**Small projects** (<10k LOC):
- May skip research phase for simple features
- Combine multiple small tasks in one commit
- Lighter ADR requirements

**Large projects** (>100k LOC):
- Strict research phase for all features
- More detailed planning
- Comprehensive ADRs for all decisions

### Adjust for Team Size

**Solo developer**:
- ADRs can be more concise
- Research docs capture "why" for future you
- Plans ensure task completion

**Large team**:
- ADRs require review process
- Research shared across team
- Plans enable parallel work

## Troubleshooting

### Issue: Too much overhead

**Symptoms**: Research/planning taking longer than implementation

**Solutions**:
- Use lighter templates for simple features
- Time-box research phase (15 minutes max)
- Combine small related features into one plan

### Issue: ADRs not being used

**Symptoms**: Decisions made without documentation

**Solutions**:
- Add ADR creation to definition of done
- Make ADRs part of code review
- Template makes it quick (<10 minutes)

### Issue: Context still overwhelming

**Symptoms**: AI suggestions still generic or wrong

**Solutions**:
- Use subagents more aggressively
- Create more compressed research summaries
- Review context management principles in skill references

## Next Steps

After setup:

1. **Try the workflow** on a real feature
2. **Get team feedback** after first iteration
3. **Adjust templates** to fit your needs
4. **Document learnings** in ADRs or retrospectives
5. **Share results** with team

## Resources

- [SKILL.md](.github/skills/ace-fca/SKILL.md) - Full methodology
- [Context Management](references/context-management.md) - Deep dive on context optimization
- [Patterns & Anti-Patterns](references/patterns-antipatterns.md) - Proven approaches
- [Subagent Workflows](references/subagent-workflows.md) - Advanced coordination

## Support

For questions about ACE-FCA:
1. Review the references in `.github/skills/ace-fca/references/`
2. Check existing ADRs for examples
3. Ask your AI agent to reference the ACE-FCA skill

## Success Indicators

You'll know ACE-FCA is working when:
- ✅ Features planned before implementation
- ✅ Context issues reduced significantly
- ✅ ADRs answer "why" questions
- ✅ Implementation quality consistently high
- ✅ Less rework and fewer surprises
- ✅ Team can work in parallel effectively

Happy building! 🚀
