# Claude Plugins

An open source collection of Claude Code plugins (skills) that extend Claude's capabilities with domain-specific knowledge and workflows.

## Repository Structure

```
claude-plugins/
├── skills/                     # All skills live here
│   └── <skill-name>/
│       ├── SKILL.md            # Core instructions (loaded into context)
│       ├── references/         # Detailed docs (loaded on demand)
│       └── examples/           # Code snippets and templates
├── README.md                   # Public-facing documentation
├── CONTRIBUTING.md             # Guidelines for contributors
├── CHANGELOG.md                # Version history
└── LICENSE                     # MIT
```

## Skill Anatomy

Each skill has:
- **SKILL.md**: Main file with YAML frontmatter (`name`, `description`, `version`) and markdown body containing workflows, examples, and troubleshooting
- **references/**: Deep-dive documentation loaded when Claude needs more detail
- **examples/**: Working code that Claude can adapt

## Key Conventions

### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: This skill should be used when the user asks to "specific phrase 1", "specific phrase 2", or mentions specific-topic.
version: 1.0.0
---
```

The `description` field should contain specific trigger phrases users would say, not vague descriptions.

### Content Guidelines
- Verify APIs/endpoints before documenting - never guess
- Include working curl commands and code snippets
- Document common errors and edge cases
- Keep SKILL.md concise; put detailed docs in `references/`

## Working on This Repo

When adding a new skill:
1. Create folder: `skills/<skill-name>/`
2. Add `SKILL.md` with proper frontmatter
3. Add `references/` and `examples/` as needed
4. Update `skills/README.md` with the new skill
5. Update `CHANGELOG.md`

When modifying existing skills:
- Bump version in frontmatter according to semver
- Update CHANGELOG.md
