# GridStatus API Reference

Complete reference for the GridStatus.io API and Python SDK.

> **Important**: The Python SDK is strongly recommended over direct curl/HTTP API calls. The free tier has issues with date filtering via curl - queries ignore date parameters and return stale sample data. The SDK handles this correctly.

## Authentication

### Environment Variable (Recommended)
```bash
export GRIDSTATUS_API_KEY=your_api_key
```

### Python SDK
```python
from gridstatusio import GridStatusClient

# Uses GRIDSTATUS_API_KEY env var
client = GridStatusClient()

# Or pass directly
client = GridStatusClient(api_key="your_api_key")
```

### HTTP API
```bash
# Header authentication
curl -H "x-api-key: YOUR_API_KEY" "https://api.gridstatus.io/v1/datasets"

# Query parameter (alternative)
curl "https://api.gridstatus.io/v1/datasets?api_key=YOUR_API_KEY"
```

## Base URL

```
https://api.gridstatus.io/v1
```

## Rate Limits

- **Free tier**: 500,000 rows per month, 250 requests max
- **Rate limits**: 1 req/sec, 30 req/min, 600 req/hour
- **Max rows per response**: 50,000
- **SDK auto-retry**: Exponential backoff on 429 responses

### Configuring Retries (Python SDK)
```python
client = GridStatusClient(
    max_retries=5,        # Default: 5
    base_delay=2.0,       # Default: 2.0 seconds
    exponential_base=2.0  # Default: 2.0
)
```

**Retry delay formula**: `delay = base_delay * (exponential_base ** retry_count)`

---

## Python SDK Methods

### `list_datasets()`

Discover available datasets.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filter_term` | str | None | Search term for dataset ID, name, or description |
| `return_list` | bool | False | Return list instead of printing |

**Examples:**
```python
# Print all datasets
client.list_datasets()

# Search for ERCOT datasets
client.list_datasets(filter_term="ercot")

# Get list of fuel mix datasets
datasets = client.list_datasets(filter_term="fuel_mix", return_list=True)
for d in datasets:
    print(f"{d.id}: {d.name}")
```

---

### `get_dataset()`

Primary method for retrieving data. Returns pandas DataFrame.

#### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dataset` | str | **Required** | Dataset identifier (e.g., `ercot_load`) |
| `start` | str | None | Start datetime (ISO format or natural language) |
| `end` | str | None | End datetime |
| `columns` | list | None | Specific columns to retrieve |
| `limit` | int | None | Maximum rows to return |
| `page_size` | int | None | Rows per API request (for pagination) |

**Time format examples:**
```python
# ISO format
start="2024-01-01T00:00:00"
start="2024-01-01"

# Natural language (SDK interprets)
start="yesterday"
start="7 days ago"
```

#### Filtering Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `filter_column` | str | Column to filter on |
| `filter_value` | str/list | Value(s) to match |
| `filter_operator` | str | Comparison operator |

**Filter operators:**
| Operator | Description | Example |
|----------|-------------|---------|
| `"="` | Equal to (default) | `filter_value="HB_HOUSTON"` |
| `"!="` | Not equal to | `filter_value="HB_HOUSTON"` |
| `">"` | Greater than | `filter_value=100` |
| `"<"` | Less than | `filter_value=100` |
| `">="` | Greater than or equal | `filter_value=0` |
| `"<="` | Less than or equal | `filter_value=1000` |
| `"in"` | Value in list | `filter_value=["HB_NORTH", "HB_SOUTH"]` |

**Filtering examples:**
```python
# Filter by location
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    filter_column="location",
    filter_value="HB_HOUSTON",
    filter_operator="="
)

# Filter by multiple locations
df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    filter_column="location_type",
    filter_value=["HUB", "ZONE"],
    filter_operator="in"
)

# Filter by price threshold
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    filter_column="spp",
    filter_value=100,
    filter_operator=">"
)
```

#### Resampling Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `resample` | str | Target frequency (e.g., `"1 hour"`, `"1 day"`) |
| `resample_by` | str/list | Column(s) to group by during resampling |
| `resample_function` | str | Aggregation function |

**Resampling functions:**
| Function | Description |
|----------|-------------|
| `"mean"` | Average (default) |
| `"sum"` | Total |
| `"min"` | Minimum |
| `"max"` | Maximum |
| `"stddev"` | Standard deviation |
| `"count"` | Count of values |
| `"variance"` | Variance |

**Resampling examples:**
```python
# Resample to hourly averages
df = client.get_dataset(
    dataset="caiso_load",
    start="2024-01-01",
    end="2024-01-07",
    resample="1 hour",
    resample_function="mean"
)

# Daily max prices by location
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-31",
    resample="1 day",
    resample_by="location",
    resample_function="max"
)
```

#### Timezone Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `timezone` | str | Convert timestamps to this timezone |
| `tz` | str | Deprecated alias for timezone |

**With timezone specified, output includes:**
- `interval_start_utc`, `interval_end_utc` - Original UTC times
- `interval_start_local`, `interval_end_local` - Converted local times

**Common timezones:**
| ISO | Timezone |
|-----|----------|
| ERCOT | `US/Central` |
| CAISO | `US/Pacific` |
| PJM | `US/Eastern` |
| MISO | `US/Central` |
| NYISO | `US/Eastern` |
| ISO-NE | `US/Eastern` |
| SPP | `US/Central` |

```python
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Central"
)
```

#### Pagination Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_cursor_pagination` | bool | True | Use cursor-based pagination (faster) |
| `sleep_time` | int | 0 | Delay (seconds) between page requests |

**Note**: Cursor pagination is 30-50% faster than offset pagination.

#### Output Control

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | bool/str | True | Logging level: `True`, `False`, `"info"`, `"debug"` |

#### publish_time Parameter

| Parameter | Type | Description |
|-----------|------|-------------|
| `publish_time` | str | Filter by data publication time |

Values:
- `"latest"` - Most recently published data
- `"latest_report"` - Latest report version
- ISO timestamp - Specific publication time

---

### `get_api_usage()`

Check current API usage against limits.

```python
usage = client.get_api_usage()
print(usage)
# Returns: {
#   "limit": 1000000,  # -1 if unlimited
#   "usage": 50000,
#   "period_start": "2024-01-01",
#   "period_end": "2024-01-31"
# }
```

---

### `get_daily_peak_report()`

Retrieve specialized daily peak reports (may require paid tier).

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `iso` | str | ISO identifier (`"ERCOT"`, `"CAISO"`, etc.) |
| `market_date` | str | Date for report (defaults to today) |

```python
report = client.get_daily_peak_report(iso="ERCOT", market_date="2024-07-15")
```

---

## HTTP API Endpoints

### Dataset Metadata API

The metadata API is essential for discovering datasets and understanding their structure.

#### List All Datasets
```
GET /v1/datasets?api_key=YOUR_KEY
```

Returns metadata for all 455+ available datasets.

**Response fields for each dataset:**
| Field | Description |
|-------|-------------|
| `id` | Dataset identifier (e.g., "pjm_load") |
| `name` | Human-readable name |
| `description` | What the data contains |
| `source` | ISO/data source (e.g., "pjm", "ercot") |
| `earliest_available_time_utc` | Start of data coverage |
| `latest_available_time_utc` | End of data coverage (near real-time for most) |
| `data_frequency` | Interval: "5_MINUTES", "15_MINUTES", "1_HOUR", etc. |
| `all_columns` | Array of column definitions with name and type |

**Example:**
```bash
curl "https://api.gridstatus.io/v1/datasets?api_key=$GRIDSTATUS_API_KEY"
```

**Response:**
```json
{
  "status_code": 200,
  "data": [
    {
      "id": "pjm_load",
      "name": "PJM Load",
      "description": "5-minute load data...",
      "earliest_available_time_utc": "2013-06-13T05:00:00+00:00",
      "latest_available_time_utc": "2026-01-25T23:45:00+00:00",
      "source": "pjm",
      "all_columns": [
        {"name": "interval_start_utc", "type": "timestamp"},
        {"name": "load", "type": "float"},
        ...
      ],
      "data_frequency": "5_MINUTES"
    },
    ...
  ]
}
```

#### Get Single Dataset Metadata
```
GET /v1/datasets/{dataset_id}?api_key=YOUR_KEY
```

Get detailed metadata for a specific dataset, including all column definitions.

**Example:**
```bash
curl "https://api.gridstatus.io/v1/datasets/pjm_load?api_key=$GRIDSTATUS_API_KEY"
```

#### Filtering Datasets (Client-Side)

The API returns all datasets; filter client-side by source/keyword:
```bash
# Find all ERCOT datasets
curl "https://api.gridstatus.io/v1/datasets?api_key=$GRIDSTATUS_API_KEY" | \
  jq '.data[] | select(.source == "ercot") | .id'

# Find datasets by name pattern
curl "https://api.gridstatus.io/v1/datasets?api_key=$GRIDSTATUS_API_KEY" | \
  jq '.data[] | select(.id | contains("fuel_mix")) | {id, name}'
```

### Query Dataset
```
GET /v1/datasets/{dataset_id}/query
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | string | Start datetime (ISO format) |
| `end` | string | End datetime |
| `limit` | integer | Max rows |
| `columns` | string | Comma-separated column names |
| `filter_column` | string | Column to filter |
| `filter_value` | string | Filter value |
| `filter_operator` | string | Filter operator |
| `resample` | string | Resample frequency |
| `resample_function` | string | Aggregation function |
| `timezone` | string | Target timezone |

**Example:**
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=100"
```

**Response:**
```json
{
  "status_code": 200,
  "data": [
    {
      "interval_start_utc": "2024-01-01T06:00:00+00:00",
      "interval_end_utc": "2024-01-01T06:05:00+00:00",
      "load": 45000
    },
    ...
  ],
  "meta": {
    "page": 1,
    "limit": 100,
    "page_size": 50000,
    "hasNextPage": true,
    "cursor": "abc123..."
  },
  "dataset_metadata": {
    "id": "ercot_load",
    "name": "ERCOT Load",
    "all_columns": [...]
  }
}
```

### Get API Usage
```
GET /v1/api_usage
```

---

## Common Column Names

### Time Columns
| Column | Description |
|--------|-------------|
| `interval_start_utc` | Interval start in UTC |
| `interval_end_utc` | Interval end in UTC |
| `interval_start_local` | Interval start in local TZ (if specified) |
| `interval_end_local` | Interval end in local TZ (if specified) |
| `time_utc` | Point-in-time timestamp (some datasets) |
| `publish_time_utc` | When data was published |

### Load Columns
| Column | Description |
|--------|-------------|
| `load` | System load in MW |
| `net_load` | Load minus renewable generation |

### Price Columns
| Column | Description |
|--------|-------------|
| `lmp` | Locational Marginal Price ($/MWh) |
| `spp` | Settlement Point Price - ERCOT ($/MWh) |
| `energy` | Energy component of LMP |
| `congestion` | Congestion component of LMP |
| `loss` | Loss component of LMP |

### Location Columns
| Column | Description |
|--------|-------------|
| `location` | Location name/ID |
| `location_type` | Type (Hub, Zone, Node, etc.) |
| `zone` | Zone name |
| `region` | Region name |

### Generation Columns
| Column | Description |
|--------|-------------|
| `coal` | Coal generation (MW) |
| `gas` | Natural gas generation (MW) |
| `nuclear` | Nuclear generation (MW) |
| `hydro` | Hydro generation (MW) |
| `wind` | Wind generation (MW) |
| `solar` | Solar generation (MW) |
| `other` | Other generation (MW) |

---

## Error Handling

### HTTP Status Codes
| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid/missing API key) |
| 404 | Dataset not found |
| 429 | Rate limited |
| 500 | Server error |

### Python SDK Exceptions
```python
try:
    df = client.get_dataset(...)
except Exception as e:
    if "401" in str(e):
        print("Invalid API key")
    elif "429" in str(e):
        print("Rate limited - try again later")
    elif "unknown column" in str(e).lower():
        print("Invalid filter column")
    else:
        raise
```

---

## Best Practices

### 1. Always Use Limits
```python
# Good - limits rows
df = client.get_dataset("ercot_load", limit=10000)

# Risky - could return millions of rows
df = client.get_dataset("ercot_load")
```

### 2. Use Date Ranges
```python
# Good - bounded date range
df = client.get_dataset(
    "ercot_load",
    start="2024-01-01",
    end="2024-01-07"
)
```

### 3. Filter Where Possible
```python
# Good - filter at API level
df = client.get_dataset(
    "ercot_spp_real_time_15_min",
    filter_column="location",
    filter_value="HB_HOUSTON"
)

# Less efficient - filter after retrieval
df = client.get_dataset("ercot_spp_real_time_15_min")
df = df[df["location"] == "HB_HOUSTON"]
```

### 4. Select Only Needed Columns
```python
df = client.get_dataset(
    "pjm_lmp_real_time_5_min",
    columns=["interval_start_utc", "location", "lmp"]
)
```

### 5. Use Resampling for Large Date Ranges
```python
# Get daily averages instead of 5-min data
df = client.get_dataset(
    "caiso_load",
    start="2023-01-01",
    end="2024-01-01",
    resample="1 day",
    resample_function="mean"
)
```
