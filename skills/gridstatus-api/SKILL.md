---
name: gridstatus-api
description: This skill should be used when the user asks to "get electricity data", "query grid data", "get LMP prices", "fetch load data", "get fuel mix", "query ERCOT data", "query CAISO data", "query PJM data", "get electricity prices", "analyze grid operations", "get ISO data", or mentions electricity market data (load, generation, pricing, LMP, fuel mix, ancillary services, etc.).
version: 1.0.0
---

# GridStatus API Skill

Query electricity grid data from US Independent System Operators (ISOs) using the GridStatus.io API. Access real-time and historical data for load, pricing (LMP), generation, fuel mix, and more.

## Quick Start

The GridStatus API is at `api.gridstatus.io/v1`. Queries require:
1. **API Key**: Set `GRIDSTATUS_API_KEY` environment variable
2. **Dataset ID**: e.g., `ercot_load`, `caiso_lmp_real_time_5_min`
3. **Parameters**: Time range, filters, limit

**API Key Setup**: Check for `GRIDSTATUS_API_KEY` in the user's `.env` file. If not present, instruct the user to:
1. Create account at https://www.gridstatus.io
2. Get API key from Settings page
3. Add to `.env`: `GRIDSTATUS_API_KEY=your_key_here`

**Free tier limit**: 1 million rows per month. Always use `limit` parameter to avoid exceeding quota.

## Supported ISOs

| ISO | Region | Key Datasets |
|-----|--------|--------------|
| ERCOT | Texas | `ercot_load`, `ercot_spp_*`, `ercot_fuel_mix` |
| CAISO | California | `caiso_load`, `caiso_lmp_*`, `caiso_fuel_mix` |
| PJM | Mid-Atlantic/Midwest | `pjm_load`, `pjm_lmp_*` |
| MISO | Midwest | `miso_load`, `miso_lmp_*` |
| NYISO | New York | `nyiso_load`, `nyiso_lmp_*` |
| ISO-NE | New England | `isone_load`, `isone_lmp_*` |
| SPP | Southwest/Central | `spp_load`, `spp_lmp_*` |

See `references/datasets-by-iso.md` for complete dataset catalog.

## Workflow

### Step 1: Clarify the Data Need

Ask the user:
- **Data type**: Load, prices (LMP), fuel mix, forecasts?
- **ISO/Region**: Which electricity market?
- **Time range**: Historical or recent? What date range?
- **Granularity**: 5-min, 15-min, hourly, daily?
- **Filters**: Specific locations, hubs, or zones?

### Step 2: Find the Dataset

Use `list_datasets()` to discover available datasets:

```python
from gridstatusio import GridStatusClient
client = GridStatusClient()
client.list_datasets(filter_term="ercot")  # Search by keyword
```

**Dataset naming convention**: `{iso}_{data_type}_{frequency}`
- `ercot_load` - ERCOT system load
- `caiso_lmp_real_time_5_min` - CAISO 5-minute real-time LMPs
- `pjm_lmp_day_ahead_hourly` - PJM day-ahead hourly LMPs

See `references/datasets-by-iso.md` for curated list of common datasets.

### Step 3: Build the Query

**Python SDK (recommended):**
```python
from gridstatusio import GridStatusClient

client = GridStatusClient()
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-02",
    limit=1000
)
```

**curl (direct API):**
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=1000"
```

### Step 4: Apply Filters and Transformations

**Filtering by column:**
```python
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="HB_HOUSTON",
    filter_operator="="
)
```

**Filter operators**: `=`, `!=`, `>`, `<`, `>=`, `<=`, `in`

**Multiple values:**
```python
df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    filter_column="location_type",
    filter_value=["HUB", "ZONE"],
    filter_operator="in"
)
```

**Resampling (aggregation):**
```python
df = client.get_dataset(
    dataset="caiso_load",
    start="2024-01-01",
    end="2024-01-07",
    resample="1 hour",
    resample_function="mean"
)
```

See `references/api-reference.md` for complete parameter documentation.

### Step 5: Handle Response

Results return as pandas DataFrame with columns specific to each dataset. Common columns:
- `interval_start_utc` / `interval_end_utc` - Time range (UTC)
- `interval_start_local` / `interval_end_local` - Local time (if timezone specified)
- `load_mw` - Load in megawatts
- `lmp` - Locational marginal price ($/MWh)
- `location` - Settlement point, hub, or zone name

## Common Query Patterns

### System Load
```python
# Get recent load for an ISO
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Central"
)
```

### Electricity Prices (LMP)
```python
# Real-time prices at a specific hub
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="HB_NORTH"
)
```

### Fuel Mix / Generation
```python
# Generation by fuel type
df = client.get_dataset(
    dataset="caiso_fuel_mix",
    start="2024-01-01",
    end="2024-01-02"
)
```

### Day-Ahead vs Real-Time Prices
```python
# Day-ahead hourly prices
da_df = client.get_dataset(
    dataset="pjm_lmp_day_ahead_hourly",
    start="2024-01-01",
    end="2024-01-02"
)

# Real-time 5-min prices
rt_df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02"
)
```

See `references/common-queries.md` for more query patterns.

## Output Format

Provide the user with:
1. **Dataset**: Name + description
2. **ISO**: Which market
3. **Time range**: Start/end dates
4. **Filters**: Any applied filters
5. **Query**: Python code or curl command
6. **Row limit note**: Reminder about free tier limits

### Example Response Format
```
Dataset: ercot_spp_real_time_15_min (ERCOT 15-minute real-time settlement point prices)
ISO: ERCOT (Texas)
Time Range: 2024-01-01 to 2024-01-02

Query:
from gridstatusio import GridStatusClient
client = GridStatusClient()
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="HB_HOUSTON",
    limit=10000
)

Note: Free tier allows 1M rows/month. This query returns ~96 rows/day per location.
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid/missing API key | Check `GRIDSTATUS_API_KEY` env var |
| 429 Rate Limited | Too many requests | Reduce query frequency, SDK auto-retries |
| Empty DataFrame | No data for filters/dates | Check date range, filter values |
| Unknown column error | Invalid filter_column | Use `list_datasets()` to verify columns |
| Row limit exceeded | Free tier quota | Add `limit` parameter, reduce date range |

## Rate Limiting

The SDK implements automatic exponential backoff for rate limits:
- Default: 5 retries with 2s base delay
- Configure: `GridStatusClient(max_retries=3, base_delay=1.0)`

## Additional Resources

### Reference Files
- **`references/datasets-by-iso.md`** - Complete dataset catalog by ISO
- **`references/api-reference.md`** - Full API parameter documentation
- **`references/common-queries.md`** - Ready-to-use query patterns

### Example Files
- **`examples/python-query.py`** - Python SDK examples
- **`examples/curl-examples.sh`** - curl command templates
