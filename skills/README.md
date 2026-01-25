# Skills

This directory contains all available skills for Claude Code.

## Available Skills

| Skill | Description |
|-------|-------------|
| [chicago-data-portal](./chicago-data-portal/) | Query Chicago's open data using Socrata/SODA API |
| [cook-county-data-portal](./cook-county-data-portal/) | Query Cook County's open data (property, courts, medical examiner) |
| [gridstatus-api](./gridstatus-api/) | Query electricity grid data from US ISOs via GridStatus.io (455+ datasets) |
| [us-census-data](./us-census-data/) | Query US Census Bureau API (ACS, Decennial, Population Estimates) |

### gridstatus-api

<p align="center">
  <img src="./gridstatus-api/aickyg.jpg" alt="I know the American electricity grid" width="400">
</p>

Query real-time and historical electricity data from 10 US ISOs including ERCOT, CAISO, PJM, MISO, and more. Features include:
- **455+ datasets**: Load, LMP prices, fuel mix, forecasts, ancillary services
- **Energy calculations**: Convert MW to MWh with built-in formulas
- **Quick answers**: "How much electricity was consumed?" patterns
- **Reliable access**: curl-first approach with Python SDK fallback

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
