---
name: gridstatus-api
description: This skill should be used when the user asks to "get electricity data", "query grid data", "get LMP prices", "fetch load data", "get fuel mix", "query ERCOT data", "query CAISO data", "query PJM data", "get electricity prices", "analyze grid operations", "get ISO data", or mentions electricity market data (load, generation, pricing, LMP, fuel mix, ancillary services, etc.).
version: 1.1.0
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

**Free tier limit**: 500,000 rows per month (250 requests max). Always use `limit` parameter to avoid exceeding quota.

## Supported ISOs

| ISO | Region | Key Datasets |
|-----|--------|--------------|
| ERCOT | Texas | `ercot_load`, `ercot_spp_*`, `ercot_fuel_mix` |
| CAISO | California | `caiso_load`, `caiso_lmp_*`, `caiso_fuel_mix` |
| PJM | Mid-Atlantic/Midwest | `pjm_standardized_hourly`, `pjm_standardized_5_min`, `pjm_load`, `pjm_lmp_*` |
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

**Standardized datasets** (highly recommended for multi-metric analysis):
- `{iso}_standardized_hourly` - Combines load, fuel mix, and forecasts in one table
- `{iso}_standardized_5_min` - Same data at 5-minute resolution
- Zone-specific data in columns like `load.comed`, `load.zone_name`, `fuel_mix.solar`
- Example: `pjm_standardized_hourly` has 48 columns including all PJM zones

See `references/datasets-by-iso.md` for curated list of common datasets.

### Step 3: Build the Query

**Python SDK (recommended for most use cases):**
```python
from gridstatusio import GridStatusClient

client = GridStatusClient()
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Central",  # Optional: get local timestamps
    limit=1000
)
```

**curl (direct API - use when SDK has dependency issues):**
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/ercot_load/query?start_time=2024-01-01&end_time=2024-01-02&timezone=market&limit=1000"
```

**CRITICAL: Different parameter names for SDK vs API**
- **Python SDK**: Use `start` and `end` parameters
- **Direct API (curl)**: Use `start_time` and `end_time` parameters
- **Timezone**: Use `timezone="market"` for ISO's local time, or specific timezone like `"US/Central"`

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
- `load` - System load in MW
- `lmp` - Locational marginal price ($/MWh)
- `location` - Settlement point, hub, or zone name

**For standardized datasets:**
- Zone/area data is in nested columns: `load.comed`, `load.aep`, `load.zone_name`
- Fuel mix in columns: `fuel_mix.solar`, `fuel_mix.wind`, `fuel_mix.coal`
- These are NOT filterable fields - access them as DataFrame columns after fetching
- Use column notation: `df['load.comed']` to access zone-specific data

**Calculate energy consumption:**
- For hourly data: `energy_mwh = load_mw * 1.0` (MW × 1 hour)
- For 5-minute data: `energy_mwh = load_mw * (5/60)` (MW × 5/60 hours)
- Convert to GWh: `energy_gwh = energy_mwh / 1000`

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

### Zone-Specific Load (using standardized datasets)
```python
# Get load for a specific zone (e.g., ComEd in PJM)
df = client.get_dataset(
    dataset="pjm_standardized_hourly",
    start="2026-01-12",
    end="2026-01-13",
    timezone="market"
)
# Zone data is in columns: df['load.comed'], df['load.aep'], etc.
# Calculate total energy: (df['load.comed'] * 1.0).sum() / 1000 = GWh
```

```bash
# Same query using curl
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/pjm_standardized_hourly/query?start_time=2026-01-12&end_time=2026-01-13&timezone=market"
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

Note: Free tier allows 500K rows/month. This query returns ~96 rows/day per location.
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid/missing API key | Check `GRIDSTATUS_API_KEY` env var |
| "Missing API Key" | Wrong header format in curl | Use lowercase `x-api-key` header (not `X-API-Key`) |
| Empty DataFrame | Wrong date parameters | Use `start_time`/`end_time` for curl, `start`/`end` for SDK |
| Old data returned | Date not in dataset | Check dataset date range; recent data may not be available yet |
| "Unknown column" error | Wrong filter on standardized dataset | Zone data is in columns, not filterable - use `df['load.comed']` after fetching |
| 429 Rate Limited | Too many requests | Reduce query frequency, SDK auto-retries |
| Row limit exceeded | Free tier quota | Add `limit` parameter, reduce date range |
| ImportError (numpy) | Python dependency issues | Use curl instead of Python SDK |

**Data Availability Notes:**
- Datasets have different coverage periods; check date range before querying
- Recent data (last 1-2 days) may not be available yet in all datasets
- Use `timezone="market"` to get local time and avoid UTC conversion issues

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
