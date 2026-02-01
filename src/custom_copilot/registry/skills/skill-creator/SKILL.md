---
name: skill-creator
description: 'Comprehensive guide for creating effective GitHub Copilot skills that extend agent capabilities with specialized knowledge, workflows, or tool integrations. Use when asked to: create/make/build/scaffold/initialize a new skill, update/modify an existing skill, validate a skill, learn about skill structure, understand how skills work, or get guidance on skill design patterns. Triggers on phrases like "create a skill", "new skill", "make a skill", "skill for X", "how do I create a skill", or "help me build a skill".'
---

# Skill Creator

A comprehensive guide for creating effective skills that extend GitHub Copilot agent capabilities through specialized knowledge, workflows, and tool integrations.

## About Skills

Skills are modular, self-contained packages that transform a general-purpose agent into a specialized agent equipped with procedural knowledge and domain expertise. Think of them as "onboarding guides" for specific domains or tasks.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

## When to Use This Skill

- User asks to "create a skill", "make a new skill", or "scaffold a skill"
- User wants to add specialized capabilities to their GitHub Copilot setup
- User needs help structuring a skill with bundled resources
- User wants to update or validate an existing skill
- User needs guidance on skill design patterns

## Core Principles

### 1. Concise is Key

The context window is a public good shared with system prompts, conversation history, and user requests.

**Default assumption: The agent is already very capable.** Only add context the agent doesn't already have. Challenge each piece of information: "Does the agent really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

**Token budgets for frequently-used skills:**
- **Very frequently loaded skills** (like common workflows): Target **<500 words** (~2-3 pages)
- **Frequently loaded skills**: Target **<1000 words** (~4-5 pages)
- **Specialized skills**: Can be longer but stay under 500 lines total

If your skill exceeds these targets, use progressive disclosure with references/ and templates/ directories.

### 2. Set Appropriate Degrees of Freedom

Match specificity to the task's fragility and variability:

- **High freedom (text instructions)**: Multiple valid approaches, context-dependent decisions
- **Medium freedom (pseudocode/parameterized scripts)**: Preferred patterns with acceptable variation
- **Low freedom (specific scripts)**: Fragile operations requiring exact sequences

### 3. Progressive Disclosure

Use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<500 lines)
3. **Bundled resources** - As needed by the agent (loaded on demand)

Keep SKILL.md under 500 lines. Split content into separate reference files when approaching this limit.

**When to move content out of SKILL.md:**
- **API documentation** → `references/api.md`
- **Comprehensive examples** → `references/examples.md`
- **Schema definitions** → `references/schema.md`
- **Starter code/boilerplate** → `templates/`
- **Long reference tables** → `references/`

**Keep in SKILL.md:**
- Core principles and workflow
- When to use / when NOT to use
- Quick reference (single table/list)
- One excellent minimal example
- Links to detailed references

## Skill Anatomy

Every skill consists of a required SKILL.md file and optional bundled resources:
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    ├── assets/           - Files used in output (templates, icons, fonts)
    └── templates/        - Starter code the agent modifies
```

### What NOT to Include

Do NOT create extraneous documentation:
- ❌ README.md
- ❌ INSTALLATION_GUIDE.md
- ❌ QUICK_REFERENCE.md
- ❌ CHANGELOG.md

The skill should only contain information needed for an AI agent to do the job.

## Skill Creation Process

Follow these steps in order:

### Step 1: Understand with Concrete Examples

Ask users for specific examples of how the skill will be used:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

Conclude when you have a clear sense of the functionality needed.

### Step 2: Plan Reusable Contents

Analyze each example to identify helpful resources:
- What scripts would prevent rewriting the same code?
- What references would provide needed schemas/documentation?
- What assets would provide reusable templates/boilerplate?

### Step 3: Create Skill Directory

Create a new folder with a lowercase, hyphenated name:
```bash
skills/<skill-name>/
└── SKILL.md          # Required
```

### Step 4: Write SKILL.md

#### Frontmatter Requirements

Every SKILL.md requires YAML frontmatter:
```yaml
---
name: <skill-name>
description: '<What it does>. Use when <specific triggers, scenarios, keywords>.'
---
```

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | 1-64 chars, lowercase letters/numbers/hyphens, matches folder name |
| `description` | **Yes** | 1-1024 chars, describes WHAT it does AND WHEN to use it |
| `license` | No | License name or reference to LICENSE.txt |
| `compatibility` | No | 1-500 chars, environment requirements |
| `metadata` | No | Key-value pairs for additional properties |
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental) |

#### Description Best Practices

**CRITICAL**: The `description` is the PRIMARY triggering mechanism. Include:

1. **WHAT** the skill does (capabilities)
2. **WHEN** to use it (triggers, scenarios, file types)
3. **Keywords** users might mention in prompts

**Good example:**
```yaml
description: 'Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks.'
```

**Poor example:**
```yaml
description: 'Document helpers'
```

#### Body Structure

**Writing Guidelines:** Always use imperative/infinitive form.

Recommended sections:
```markdown
# Title

Brief overview of what the skill does.

## When to Use This Skill

Reinforces description triggers with more detail.

## Prerequisites

Required tools, dependencies, environment setup.

## Step-by-Step Workflows

Numbered steps for common tasks.

## Troubleshooting

Common issues and solutions.

## References

Links to bundled documentation files.
```

### Step 5: Add Bundled Resources (If Needed)

#### Scripts (`scripts/`)

Executable code for deterministic reliability or repeatedly rewritten tasks.

**When to include**: Same code being rewritten repeatedly or deterministic reliability needed

**Example**: `scripts/rotate_pdf.py` for PDF rotation

**Benefits**: Token efficient, deterministic, may execute without loading into context

#### References (`references/`)

Documentation loaded into context to inform the agent's process.

**When to include**: For documentation the agent should reference while working

**Examples**: 
- `references/schema.md` - Database schemas
- `references/api_docs.md` - API specifications
- `references/policies.md` - Company policies

**Best practice**: If files are large (>10k words), include search patterns in SKILL.md

**Progressive Disclosure Patterns**:

**Pattern 1: High-level guide with references**
```markdown
## Advanced features

- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

**Pattern 3: Framework/variant organization**
```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

**Guidelines**:
- Avoid deeply nested references (keep one level deep from SKILL.md)
- For files >100 lines, include table of contents at top
- Information should live in SKILL.md OR references, not both

#### Assets (`assets/`)

Files used in the agent's output, not loaded into context.

**When to include**: Files needed in final output

**Examples**:
- `assets/logo.png` - Brand assets
- `assets/template.pptx` - PowerPoint templates
- `assets/frontend-template/` - HTML/React boilerplate
- `assets/font.ttf` - Typography

#### Templates (`templates/`)

Starter code the agent modifies and extends.

**When to include**: Scaffolds that need customization

**Examples**:
- `templates/starter.ts` - TypeScript project scaffold
- `templates/component.tsx` - React component template

### Step 6: Validate the Skill

Ensure the skill meets all requirements:

**Validation Checklist**:
- [ ] Folder name is lowercase with hyphens
- [ ] `name` field matches folder name exactly
- [ ] `description` is 10-1024 characters
- [ ] `description` explains WHAT and WHEN
- [ ] `description` is wrapped in single quotes
- [ ] Body content is under 500 lines
- [ ] **For frequently-used skills**: SKILL.md under 500 words (check with `wc -w`)
- [ ] **For very common skills**: SKILL.md under 500 words with heavy content in references/
- [ ] Long examples, API docs, or schemas moved to references/
- [ ] No extraneous files (README.md, etc.)
- [ ] Bundled assets are under 5MB each
- [ ] Scripts are tested and working
- [ ] References are properly linked from SKILL.md

### Step 7: Iterate

After testing the skill:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Complete Example Structure
```
my-awesome-skill/
├── SKILL.md                    # Required instructions
├── LICENSE.txt                 # Optional license file
├── scripts/
│   └── helper.py               # Executable automation
├── references/
│   ├── api-reference.md        # Detailed docs
│   └── examples.md             # Usage examples
├── assets/
│   └── diagram.png             # Static resources
└── templates/
    └── starter.ts              # Code scaffold
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not discovered | Improve description with more keywords and triggers |
| Validation fails on name | Ensure lowercase, no consecutive hyphens, matches folder |
| Description too short | Add capabilities, triggers, and keywords |
| Assets not found | Use relative paths from skill root |
| Skill triggers too often | Make description more specific to use cases |
| Skill never triggers | Add common user phrases to description |
| SKILL.md too long | Split detailed content into references/ files |
| Context bloat | Move examples and API docs to references/ |
| Frequently-used skill too long | Split into SKILL.md (<500 words) + references/, aim for minimal overview |
| Word count too high | Use `wc -w SKILL.md` to check; move detailed content to references/ |

## Quick Reference: Frontmatter Template
```yaml
---
name: your-skill-name
description: 'Brief capability summary. Use when [trigger 1], [trigger 2], or [specific scenario]. Supports [file types/frameworks].'
---
```

## Key Takeaways

1. **Description is critical** - It's the primary triggering mechanism
2. **Keep SKILL.md concise** - Under 500 lines; frequently-used skills under 500 words
3. **Progressive disclosure** - Load only what's needed when needed; move API docs, examples, schemas to references/
4. **Token efficiency matters** - Every word in a frequently-loaded skill costs tokens in every conversation
5. **Test bundled scripts** - Ensure they actually work before including
6. **Avoid duplication** - Information lives in SKILL.md OR references, not both
7. **No extraneous docs** - Only files needed for AI agent to do the job
8. **Iterate based on usage** - Improve after real-world testing