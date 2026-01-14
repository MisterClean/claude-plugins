# Skills

This directory contains all available skills for Claude Code.

## Available Skills

| Skill | Description |
|-------|-------------|
| [chicago-data-portal](./chicago-data-portal/) | Query Chicago's open data using Socrata/SODA API |
| [cook-county-data-portal](./cook-county-data-portal/) | Query Cook County's open data (property, courts, medical examiner) |
| [us-census-data](./us-census-data/) | Query US Census Bureau API (ACS, Decennial, Population Estimates) |

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md              # Core instructions (auto-loaded when triggered)
├── references/           # Detailed docs (loaded on demand)
│   └── *.md
└── examples/             # Code snippets and templates
    └── *.py, *.sh, etc.
```

## Installing a Skill

Copy the skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/chicago-data-portal /path/to/your/project/.claude/plugins/
```

## Adding New Skills

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on creating and submitting new skills.
