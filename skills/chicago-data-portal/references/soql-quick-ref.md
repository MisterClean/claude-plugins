# SoQL Quick Reference

## Aggregate Functions
| Function | Example |
|----------|---------|
| `count(*)` | `$select=count(*) as total` |
| `sum(column)` | `$select=sum(amount) as total_amount` |
| `avg(column)` | `$select=avg(fee) as avg_fee` |
| `min(column)` | `$select=min(date) as earliest` |
| `max(column)` | `$select=max(date) as latest` |
| `stddev_pop(column)` | Population standard deviation |
| `stddev_samp(column)` | Sample standard deviation |

## Date Functions
| Function | Example | Returns |
|----------|---------|---------|
| `date_extract_y(col)` | `date_extract_y(date)` | Year (2024) |
| `date_extract_m(col)` | `date_extract_m(date)` | Month (1-12) |
| `date_extract_d(col)` | `date_extract_d(date)` | Day (1-31) |
| `date_extract_dow(col)` | `date_extract_dow(date)` | Day of week (0=Sun) |
| `date_extract_hh(col)` | `date_extract_hh(date)` | Hour (0-23) |
| `date_trunc_y(col)` | `date_trunc_y(date)` | Truncate to year |
| `date_trunc_ym(col)` | `date_trunc_ym(date)` | Truncate to month |
| `date_trunc_ymd(col)` | `date_trunc_ymd(date)` | Truncate to day |

**Date comparison:**
```sql
$where=date >= '2024-01-01T00:00:00' AND date < '2025-01-01T00:00:00'
```

## Text Functions
| Function | Example |
|----------|---------|
| `upper(col)` | `upper(primary_type) = 'THEFT'` |
| `lower(col)` | `lower(status) = 'open'` |
| `starts_with(col, str)` | `starts_with(address, '123')` |
| `like` | `address like '%MICHIGAN%'` |
| `not like` | `address not like '%APT%'` |

## Geospatial Functions
| Function | Syntax |
|----------|--------|
| `within_circle` | `within_circle(location, lat, lon, radius_meters)` |
| `within_box` | `within_box(location, north_lat, west_lon, south_lat, east_lon)` |
| `within_polygon` | `within_polygon(location, 'MULTIPOLYGON(...)')` |
| `distance_in_meters` | `distance_in_meters(location, 'POINT(-87.6 41.8)')` |
| `intersects` | `intersects(geometry, 'POLYGON(...)')` |

**Radius example (1km from downtown):**
```sql
$where=within_circle(location, 41.8781, -87.6298, 1000)
```

## Comparison Operators
| Operator | Example |
|----------|---------|
| `=` | `ward = 42` |
| `!=` or `<>` | `status != 'CLOSED'` |
| `<`, `>`, `<=`, `>=` | `total_fee > 1000` |
| `IS NULL` | `latitude IS NULL` |
| `IS NOT NULL` | `latitude IS NOT NULL` |
| `IN (...)` | `primary_type IN ('THEFT', 'BATTERY')` |
| `NOT IN (...)` | `ward NOT IN (1, 2, 3)` |
| `BETWEEN` | `fee BETWEEN 100 AND 500` |

## Logical Operators
```sql
$where=year = 2024 AND ward = 42
$where=primary_type = 'THEFT' OR primary_type = 'BATTERY'
$where=NOT (status = 'CLOSED')
```

## System Fields
| Field | Description |
|-------|-------------|
| `:id` | Internal record ID |
| `:created_at` | Row creation timestamp |
| `:updated_at` | Row last modified timestamp |

**Include system fields:**
```
$select=:id, :updated_at, *
```

## URL Encoding
| Character | Encoded |
|-----------|---------|
| space | `%20` |
| `=` | `%3D` |
| `>` | `%3E` |
| `<` | `%3C` |
| `'` | `%27` |
| `,` | `%2C` |
