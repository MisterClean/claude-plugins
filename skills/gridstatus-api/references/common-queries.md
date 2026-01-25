# Common Query Patterns

Ready-to-use query patterns for common electricity data analysis tasks.

---

## Energy Consumption Calculations

Converting load (MW) to energy (MWh) is one of the most common operations.

### Formula Reference

| Data Interval | Multiplier | Formula |
|---------------|------------|---------|
| 5 minutes | 5/60 = 0.0833 | `energy_MWh = load_MW × 0.0833` |
| 15 minutes | 15/60 = 0.25 | `energy_MWh = load_MW × 0.25` |
| 1 hour | 1 | `energy_MWh = load_MW × 1` |

### Total Energy in Last Complete Hour (curl)

```bash
# Get last 12 intervals of 5-min data (= 1 hour)
# Replace timestamps with actual times
curl "https://api.gridstatus.io/v1/datasets/pjm_load/query?\
start_time=2026-01-25T17:00:00&end_time=2026-01-25T18:00:00&\
timezone=market&api_key=$GRIDSTATUS_API_KEY"

# Then calculate: sum(load × 5/60) for each row = total MWh
# Example: 12 intervals averaging 128,000 MW = ~128,000 MWh/hour
```

### Total Energy Calculation (Python)

```python
# For 5-minute data
df = client.get_dataset(
    dataset="pjm_load",
    start="2026-01-25T17:00:00",
    end="2026-01-25T18:00:00",
    timezone="market"
)

# Calculate energy for 5-min intervals
df['energy_mwh'] = df['load'] * (5/60)
total_mwh = df['energy_mwh'].sum()
total_gwh = total_mwh / 1000

print(f"Total energy: {total_mwh:,.0f} MWh ({total_gwh:,.1f} GWh)")
```

### Most Recent Data Point

```bash
# Get the latest available data point
curl "https://api.gridstatus.io/v1/datasets/pjm_load/query?\
order=desc&limit=1&timezone=market&api_key=$GRIDSTATUS_API_KEY"
```

```python
# Python - get most recent load
df = client.get_dataset(
    dataset="pjm_load",
    start="1 hour ago",
    timezone="market",
    limit=1
)
# Note: SDK doesn't support order=desc, so filter to latest timestamp
latest = df.loc[df['interval_start_utc'].idxmax()]
```

---

## System Load Analysis

### Get Recent Load for Any ISO

```python
from gridstatusio import GridStatusClient

client = GridStatusClient()

# ERCOT
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Central",
    limit=10000
)

# CAISO
df = client.get_dataset(
    dataset="caiso_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Pacific",
    limit=10000
)

# PJM
df = client.get_dataset(
    dataset="pjm_load",
    start="2024-01-01",
    end="2024-01-02",
    timezone="US/Eastern",
    limit=10000
)
```

### Daily Peak Load

```python
# Get daily max load
df = client.get_dataset(
    dataset="ercot_load",
    start="2024-01-01",
    end="2024-01-31",
    resample="1 day",
    resample_function="max"
)
```

### Hourly Average Load

```python
df = client.get_dataset(
    dataset="caiso_load",
    start="2024-01-01",
    end="2024-01-07",
    resample="1 hour",
    resample_function="mean"
)
```

### Load by Zone

```python
# ERCOT load by weather zone
df = client.get_dataset(
    dataset="ercot_load_by_weather_zone",
    start="2024-01-01",
    end="2024-01-02",
    limit=10000
)

# MISO zonal load
df = client.get_dataset(
    dataset="miso_zonal_load_hourly",
    start="2024-01-01",
    end="2024-01-02",
    limit=10000
)
```

---

## Electricity Pricing (LMP/SPP)

### Hub Prices

```python
# ERCOT hub prices (HB_HOUSTON, HB_NORTH, HB_SOUTH, HB_WEST)
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="HB_HOUSTON",
    filter_operator="="
)

# PJM Western Hub
df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="WESTERN HUB",
    filter_operator="="
)

# CAISO SP15 hub
df = client.get_dataset(
    dataset="caiso_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value="TH_SP15_GEN-APND",
    filter_operator="="
)
```

### Multiple Hubs Comparison

```python
# All ERCOT hubs
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location",
    filter_value=["HB_HOUSTON", "HB_NORTH", "HB_SOUTH", "HB_WEST"],
    filter_operator="in",
    limit=50000
)
```

### Day-Ahead vs Real-Time Prices

```python
# Day-ahead prices
da_df = client.get_dataset(
    dataset="pjm_lmp_day_ahead_hourly",
    start="2024-01-01",
    end="2024-01-07",
    filter_column="location",
    filter_value="WESTERN HUB"
)

# Real-time prices (same period)
rt_df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-07",
    filter_column="location",
    filter_value="WESTERN HUB",
    resample="1 hour",
    resample_function="mean"
)

# Or use DART (day-ahead minus real-time) directly
dart_df = client.get_dataset(
    dataset="pjm_lmp_dart_5_min",
    start="2024-01-01",
    end="2024-01-07",
    filter_column="location",
    filter_value="WESTERN HUB"
)
```

### Price Statistics

```python
# Daily price statistics
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-31",
    filter_column="location",
    filter_value="HB_HOUSTON",
    resample="1 day",
    resample_function="max"  # or "mean", "min", "stddev"
)
```

### High Price Events

```python
# Find prices above $100/MWh
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2024-01-01",
    end="2024-01-31",
    filter_column="spp",
    filter_value=100,
    filter_operator=">",
    limit=50000
)
```

### Zonal Prices

```python
# NYISO zones (A through K)
df = client.get_dataset(
    dataset="nyiso_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location_type",
    filter_value="ZONE",
    filter_operator="="
)

# PJM zones
df = client.get_dataset(
    dataset="pjm_lmp_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02",
    filter_column="location_type",
    filter_value="ZONE",
    filter_operator="="
)
```

---

## Generation / Fuel Mix

### System-Wide Fuel Mix

```python
# ERCOT fuel mix
df = client.get_dataset(
    dataset="ercot_fuel_mix",
    start="2024-01-01",
    end="2024-01-02",
    limit=10000
)

# CAISO fuel mix
df = client.get_dataset(
    dataset="caiso_fuel_mix",
    start="2024-01-01",
    end="2024-01-02",
    limit=10000
)
```

### Hourly Generation by Fuel Type

```python
df = client.get_dataset(
    dataset="pjm_fuel_mix_hourly",
    start="2024-01-01",
    end="2024-01-07"
)
```

### Detailed Fuel Mix

```python
# ERCOT detailed (more granular fuel categories)
df = client.get_dataset(
    dataset="ercot_fuel_mix_detailed",
    start="2024-01-01",
    end="2024-01-02"
)

# SPP detailed
df = client.get_dataset(
    dataset="spp_fuel_mix_detailed",
    start="2024-01-01",
    end="2024-01-02"
)
```

---

## Forecasts

### Load Forecasts

```python
# ERCOT load forecast
df = client.get_dataset(
    dataset="ercot_load_forecast",
    start="2024-01-01",
    end="2024-01-07"
)

# CAISO day-ahead load forecast
df = client.get_dataset(
    dataset="caiso_load_forecast_dam",
    start="2024-01-01",
    end="2024-01-07"
)

# PJM load forecast (multiple horizons)
df = client.get_dataset(
    dataset="pjm_load_forecast_hourly",
    start="2024-01-01",
    end="2024-01-07"
)
```

### Solar/Wind Forecasts

```python
# ERCOT wind forecast
df = client.get_dataset(
    dataset="ercot_wind_actual_and_forecast_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

# ERCOT solar forecast
df = client.get_dataset(
    dataset="ercot_solar_actual_and_forecast_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

# CAISO renewable forecast
df = client.get_dataset(
    dataset="caiso_renewables_forecast_dam",
    start="2024-01-01",
    end="2024-01-07"
)
```

---

## Ancillary Services

### Ancillary Service Prices

```python
# ERCOT AS prices
df = client.get_dataset(
    dataset="ercot_as_prices",
    start="2024-01-01",
    end="2024-01-07"
)

# PJM regulation prices
df = client.get_dataset(
    dataset="pjm_regulation_prices_5_min",
    start="2024-01-01",
    end="2024-01-02"
)

# CAISO AS prices
df = client.get_dataset(
    dataset="caiso_as_prices",
    start="2024-01-01",
    end="2024-01-07"
)
```

### Reserve Monitoring

```python
# ERCOT real-time AS monitor
df = client.get_dataset(
    dataset="ercot_real_time_as_monitor",
    start="2024-01-01",
    end="2024-01-02"
)

# PJM operational reserves
df = client.get_dataset(
    dataset="pjm_operational_reserves",
    start="2024-01-01",
    end="2024-01-02"
)
```

---

## Interchange / Tie Flows

### Inter-regional Flows

```python
# CAISO net interchange
df = client.get_dataset(
    dataset="caiso_net_interchange_real_time",
    start="2024-01-01",
    end="2024-01-02"
)

# PJM tie flows
df = client.get_dataset(
    dataset="pjm_tie_flows_5_min",
    start="2024-01-01",
    end="2024-01-02"
)

# MISO interchange
df = client.get_dataset(
    dataset="miso_interchange_5_min",
    start="2024-01-01",
    end="2024-01-02"
)
```

---

## Constraints

### Binding Transmission Constraints

```python
# CAISO binding constraints
df = client.get_dataset(
    dataset="caiso_branch_shadow_prices_rtm_5_min",
    start="2024-01-01",
    end="2024-01-02"
)

# PJM transmission constraints
df = client.get_dataset(
    dataset="pjm_transmission_constraints_day_ahead_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

# MISO binding constraints
df = client.get_dataset(
    dataset="miso_binding_constraints_real_time_5_min",
    start="2024-01-01",
    end="2024-01-02"
)
```

---

## Cross-ISO Analysis

### Latest Data for All ISOs

```python
# Get latest snapshot for all ISOs
df = client.get_dataset(
    dataset="isos_latest",
    limit=1000
)
```

### Standardized Data (for comparison)

```python
# Standardized hourly data - easier cross-ISO comparison
ercot = client.get_dataset(
    dataset="ercot_standardized_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

caiso = client.get_dataset(
    dataset="caiso_standardized_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

pjm = client.get_dataset(
    dataset="pjm_standardized_hourly",
    start="2024-01-01",
    end="2024-01-07"
)
```

### EIA Regional Data

```python
# National/regional data from EIA
df = client.get_dataset(
    dataset="eia_regional_hourly",
    start="2024-01-01",
    end="2024-01-07"
)

# Fuel mix by region
df = client.get_dataset(
    dataset="eia_fuel_mix_hourly",
    start="2024-01-01",
    end="2024-01-07"
)
```

---

## curl Examples

### Basic Query
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=100"
```

### With Filter
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/ercot_spp_real_time_15_min/query?start=2024-01-01&end=2024-01-02&filter_column=location&filter_value=HB_HOUSTON&limit=100"
```

### With Resampling
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/caiso_load/query?start=2024-01-01&end=2024-01-07&resample=1%20hour&resample_function=mean&limit=200"
```

### List All Datasets
```bash
curl -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets"
```

---

## Query Optimization Tips

### 1. Use Appropriate Time Ranges
```python
# For 5-min data, limit to 1-2 days at a time
df = client.get_dataset("ercot_load", start="2024-01-01", end="2024-01-02")

# For hourly data, can go longer
df = client.get_dataset("pjm_lmp_day_ahead_hourly", start="2024-01-01", end="2024-01-31")
```

### 2. Filter at API Level
```python
# Good - filter on server
df = client.get_dataset(
    "ercot_spp_real_time_15_min",
    filter_column="location",
    filter_value="HB_HOUSTON"
)

# Less efficient - downloads all, then filters
df = client.get_dataset("ercot_spp_real_time_15_min")
df = df[df["location"] == "HB_HOUSTON"]
```

### 3. Resample for Long Periods
```python
# For yearly analysis, resample to daily
df = client.get_dataset(
    "ercot_load",
    start="2023-01-01",
    end="2024-01-01",
    resample="1 day",
    resample_function="mean"
)
```

### 4. Monitor Usage
```python
# Check remaining quota
usage = client.get_api_usage()
print(f"Used: {usage['usage']} / {usage['limit']}")
```
