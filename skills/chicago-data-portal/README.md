# Chicago Data Portal

Query and download datasets from the City of Chicago Data Portal using the Socrata Open Data API (SODA) and SoQL.

## Triggers

This skill activates when you ask Claude to:
- "query Chicago data"
- "find Chicago datasets"
- "get Chicago crime data"
- "download Chicago permits"
- "write a SODA query for Chicago"
- "search data.cityofchicago.org"

Or when you mention Chicago city data (311 requests, permits, licenses, inspections, crimes, etc.).

## Installation

Copy this skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/chicago-data-portal /path/to/your/project/.claude/plugins/
```

Or clone the entire repo and reference it in your Claude Code settings for global access.

## Usage

Once installed, just ask Claude naturally:

> "Find me all building permits issued in the last month in Chicago"

> "Query the Chicago crime data for robberies in the Loop"

> "Get 311 service requests for potholes by ward"

Claude will automatically use this skill to discover datasets, build SoQL queries, and retrieve the data.

## Contents

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Core instructions and workflow |
| [references/popular-datasets.md](./references/popular-datasets.md) | Commonly requested datasets with IDs |
| [references/soql-quick-ref.md](./references/soql-quick-ref.md) | SoQL syntax reference |
| [examples/curl-examples.sh](./examples/curl-examples.sh) | Sample curl commands |
| [examples/python-query.py](./examples/python-query.py) | Python query example |

## Resources

- [Chicago Data Portal](https://data.cityofchicago.org)
- [SODA API Documentation](https://dev.socrata.com/)
- [Main Repository](../../README.md)
