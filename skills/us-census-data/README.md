# US Census Data

Query demographic, economic, housing, and population data from the US Census Bureau API. Supports American Community Survey (ACS), Decennial Census, and Population Estimates.

## Triggers

This skill activates when you ask Claude to:
- "get Census data"
- "query American Community Survey"
- "find ACS data"
- "get population by state"
- "query Decennial Census"
- "find Census variables"
- "get median income data"
- "download demographic data"

Or when you mention US Census Bureau data (demographics, income, poverty, education, housing, population estimates, etc.).

## Installation

Copy this skill folder to your project's `.claude/plugins/` directory:

```bash
cp -r skills/us-census-data /path/to/your/project/.claude/plugins/
```

Or clone the entire repo and reference it in your Claude Code settings for global access.

## API Key Setup

The Census API requires a key for production use:

1. Register at https://api.census.gov/data/key_signup.html
2. Add to your `.env` file: `CENSUS_API_KEY=your_key_here`

## Usage

Once installed, just ask Claude naturally:

> "Get median household income by county for Illinois"

> "What's the population of Chicago by census tract?"

> "Find poverty rates for all states from ACS 5-year"

Claude will automatically use this skill to select the right dataset, find variable codes, and construct the API query.

## Contents

| File | Description |
|------|-------------|
| [SKILL.md](./SKILL.md) | Core instructions and workflow |
| [references/datasets.md](./references/datasets.md) | Available Census datasets |
| [references/geographies.md](./references/geographies.md) | Geography levels and FIPS codes |
| [references/popular-variables.md](./references/popular-variables.md) | Common variable codes |
| [references/tigerweb.md](./references/tigerweb.md) | Geographic boundary data |
| [examples/curl-examples.sh](./examples/curl-examples.sh) | Sample curl commands |
| [examples/python-query.py](./examples/python-query.py) | Python query example |

## Resources

- [Census API Documentation](https://www.census.gov/data/developers/guidance.html)
- [Census Data Explorer](https://data.census.gov)
- [Main Repository](../../README.md)
