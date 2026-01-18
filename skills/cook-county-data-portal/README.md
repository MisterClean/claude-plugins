# Cook County Data Portal

Query and download datasets from the Cook County Open Data Portal using the Socrata Open Data API (SODA) and SoQL.

## Triggers

This skill activates when you ask Claude to:
- "query Cook County data"
- "find Cook County datasets"
- "get property assessments"
- "download parcel data"
- "search datacatalog.cookcountyil.gov"
- "get medical examiner data"
- "find court cases"
- "query State's Attorney data"

Or when you mention Cook County government data (assessor, treasurer, courts, payroll, medical examiner, etc.).

## Installation

Copy this skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/cook-county-data-portal /path/to/your/project/.claude/plugins/
```

Or clone the entire repo and reference it in your Claude Code settings for global access.

## Usage

Once installed, just ask Claude naturally:

> "Get the assessed value for PIN 14-08-203-015-0000"

> "Find all medical examiner cases from last year"

> "Query property tax appeals in Northfield township"

Claude will automatically use this skill to discover datasets, build SoQL queries, and retrieve the data.

## Contents

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Core instructions and workflow |
| [references/datasets-property.md](./references/datasets-property.md) | Assessor, Treasurer, parcel data |
| [references/datasets-courts.md](./references/datasets-courts.md) | State's Attorney, sentencing |
| [references/datasets-health.md](./references/datasets-health.md) | Medical Examiner cases |
| [references/datasets-finance.md](./references/datasets-finance.md) | Payroll, procurement, budgets |
| [references/soql-quick-ref.md](./references/soql-quick-ref.md) | SoQL syntax reference |
| [examples/curl-examples.sh](./examples/curl-examples.sh) | Sample curl commands |
| [examples/python-query.py](./examples/python-query.py) | Python query example |

## Resources

- [Cook County Data Portal](https://datacatalog.cookcountyil.gov)
- [SODA API Documentation](https://dev.socrata.com/)
- [Main Repository](../../README.md)
