# Chicago Data Portal

Query and download datasets from the City of Chicago Open Data Portal using the Socrata SODA API and SoQL.

## Triggers

This skill activates when you ask Claude to:
- "query Chicago data"
- "find Chicago datasets"
- "get Chicago crime data"
- "download Chicago permits"
- "write a SODA query for Chicago"
- "search data.cityofchicago.org"

Or when you mention Chicago city data (311 requests, permits, licenses, inspections, crimes, traffic crashes, etc.).

## Installation

Copy this skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/chicago-data-portal /path/to/your/project/.claude/plugins/
```

Or install from the plugin marketplace:

```
/plugin marketplace add MisterClean/claude-plugins
/plugin install chicago-data-portal@misterclean-plugins
```

## Usage

Once installed, just ask Claude naturally:

> "Find me all building permits issued in the last month in Chicago"

> "Query the Chicago crime data for robberies in the Loop"

> "Get 311 service requests for potholes by ward"

> "Show me food inspections that failed near Wrigley Field"

Claude will automatically discover datasets, build SoQL queries, and retrieve data.

## Contents

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Core instructions and workflow |
| [references/popular-datasets.md](./references/popular-datasets.md) | Dataset lookup table with IDs and columns |
| [references/soql-quick-ref.md](./references/soql-quick-ref.md) | Complete SoQL syntax reference |
| [references/geospatial.md](./references/geospatial.md) | Location queries and coordinate systems |
| [examples/curl-examples.sh](./examples/curl-examples.sh) | Ready-to-run curl commands |
| [examples/python-query.py](./examples/python-query.py) | Python with requests + pandas |
| [examples/typescript-query.ts](./examples/typescript-query.ts) | TypeScript/JavaScript fetch examples |

## Popular Datasets

| Dataset | ID | Use Case |
|---------|-----|----------|
| Crimes | `ijzp-q8t2` | Crime analysis, safety research |
| 311 Service Requests | `v6vf-nfxy` | City services, complaints |
| Building Permits | `ydr8-5enu` | Construction, development |
| Food Inspections | `4ijn-s7e5` | Restaurant health scores |
| Traffic Crashes | `85ca-t3if` | Accident analysis |
| Business Licenses | `r5kz-chrr` | Business activity |

See [references/popular-datasets.md](./references/popular-datasets.md) for the full list.

## Authentication

Queries work without authentication but are rate-limited. For production use, get a free app token:

1. Sign up at https://data.cityofchicago.org/signup
2. Go to Developer Settings and create an app token
3. Add to your `.env` file: `CHICAGO_DATA_PORTAL_TOKEN=your_token_here`

## Resources

- [Chicago Data Portal](https://data.cityofchicago.org)
- [SODA API Documentation](https://dev.socrata.com/)
- [SoQL Reference](https://dev.socrata.com/docs/queries/)
- [Main Repository](../../README.md)
