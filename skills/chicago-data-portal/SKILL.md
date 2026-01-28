---
name: chicago-data-portal
description: This skill should be used when the user asks to "query Chicago data", "find Chicago datasets", "get Chicago crime data", "download Chicago permits", "write a SODA query for Chicago", "search data.cityofchicago.org", or mentions Chicago city data (311, permits, licenses, inspections, crimes, etc.).
version: 1.2.0
---

# Chicago Data Portal Skill

Query Chicago's open data at `data.cityofchicago.org` using the Socrata SODA API.

## Quick Reference

| Action | Endpoint |
|--------|----------|
| Query data | `GET https://data.cityofchicago.org/resource/{ID}.json?$where=...` |
| Get schema | `GET https://data.cityofchicago.org/api/views/{ID}` |
| Search catalog | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=...` |
| Download CSV | `GET https://data.cityofchicago.org/api/views/{ID}/rows.csv?accessType=DOWNLOAD` |

## Auth Check

Look for `CHICAGO_DATA_PORTAL_TOKEN` in `.env`. If found, add header `X-App-Token: {token}`. Queries work without tokens but are rate-limited. Get one free at https://data.cityofchicago.org/signup.

## Workflow

### 1. Find the Dataset

Check `references/popular-datasets.md` first - it has the most common ones. Otherwise search:

```bash
curl "https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=YOUR_KEYWORDS"
```

Extract the 4x4 ID (e.g., `ijzp-q8t2`) from results.

### 2. Get Column Names

**Always fetch metadata before building queries:**

```bash
curl "https://data.cityofchicago.org/api/views/{ID}" | jq '.columns[] | {fieldName, dataTypeName}'
```

### 3. Build Query

```
https://data.cityofchicago.org/resource/{ID}.json?$select=col1,col2&$where=...&$limit=1000
```

**Core parameters:** `$select`, `$where`, `$group`, `$having`, `$order`, `$limit`, `$offset`

See `references/soql-quick-ref.md` for syntax details.

### 4. Handle Large Results

Default max is 1000 rows. For pagination, always include `$order` for stable results:

```
$order=date DESC&$limit=1000&$offset=0    # Page 1
$order=date DESC&$limit=1000&$offset=1000 # Page 2
```

## Essential SoQL

```sql
-- Date filter (ISO format)
$where=date >= '2024-01-01' AND date < '2025-01-01'

-- Text (case-insensitive)
$where=upper(primary_type) = 'THEFT'

-- Multiple values
$where=primary_type IN ('THEFT', 'BATTERY', 'ASSAULT')

-- Aggregation
$select=primary_type, count(*) as total&$group=primary_type&$order=total DESC

-- Geospatial (within 1km of a point)
$where=within_circle(location, 41.8781, -87.6298, 1000)
```

## Output Template

Always provide:

```
**Dataset:** {Name} ({ID})
{portal_link}

**Query:**
{formatted_soql}

**Run it:**
curl "{full_url}"

**Notes:** {update frequency, timezone (America/Chicago), any caveats}
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| 404 / unknown column | Wrong ID or column name. Check `/api/views/{ID}` |
| Empty results | Filters too strict, wrong date format, or all nulls |
| 429 throttled | Add `X-App-Token` header |
| Encoding errors | URL-encode: space=%20, >=%3E, '=%27 |

## References

- `references/popular-datasets.md` - Dataset IDs organized by category
- `references/soql-quick-ref.md` - Full SoQL syntax
- `references/geospatial.md` - Location queries and coordinate systems
- `examples/` - Working code in Python, JavaScript, and curl
