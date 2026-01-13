# SoQL Quick Reference

## Aggregate Functions
| Function | Example |
|----------|---------|
| `count(*)` | `$select=count(*) as total` |
| `sum(column)` | `$select=sum(amount) as total_amount` |
| `avg(column)` | `$select=avg(base_pay) as avg_pay` |
| `min(column)` | `$select=min(year) as earliest` |
| `max(column)` | `$select=max(year) as latest` |
| `stddev_pop(column)` | Population standard deviation |
| `stddev_samp(column)` | Sample standard deviation |

## Date Functions
| Function | Example | Returns |
|----------|---------|---------|
| `date_extract_y(col)` | `date_extract_y(death_date)` | Year (2024) |
| `date_extract_m(col)` | `date_extract_m(death_date)` | Month (1-12) |
| `date_extract_d(col)` | `date_extract_d(death_date)` | Day (1-31) |
| `date_extract_dow(col)` | `date_extract_dow(death_date)` | Day of week (0=Sun) |
| `date_extract_hh(col)` | `date_extract_hh(death_date)` | Hour (0-23) |
| `date_trunc_y(col)` | `date_trunc_y(death_date)` | Truncate to year |
| `date_trunc_ym(col)` | `date_trunc_ym(death_date)` | Truncate to month |
| `date_trunc_ymd(col)` | `date_trunc_ymd(death_date)` | Truncate to day |

**Date comparison:**
```sql
$where=death_date >= '2024-01-01T00:00:00' AND death_date < '2025-01-01T00:00:00'
```

## Text Functions
| Function | Example |
|----------|---------|
| `upper(col)` | `upper(manner) = 'HOMICIDE'` |
| `lower(col)` | `lower(status) = 'active'` |
| `starts_with(col, str)` | `starts_with(pin, '12')` |
| `like` | `vendor_name like '%CONSTRUCTION%'` |
| `not like` | `description not like '%AMENDMENT%'` |

## Geospatial Functions
| Function | Syntax |
|----------|--------|
| `within_circle` | `within_circle(location, lat, lon, radius_meters)` |
| `within_box` | `within_box(location, north_lat, west_lon, south_lat, east_lon)` |
| `within_polygon` | `within_polygon(location, 'MULTIPOLYGON(...)')` |
| `distance_in_meters` | `distance_in_meters(location, 'POINT(-87.6 41.8)')` |
| `intersects` | `intersects(geometry, 'POLYGON(...)')` |

**Radius example (5km from downtown Chicago):**
```sql
$where=within_circle(location, 41.8781, -87.6298, 5000)
```

## Comparison Operators
| Operator | Example |
|----------|---------|
| `=` | `year = 2024` |
| `!=` or `<>` | `manner != 'NATURAL'` |
| `<`, `>`, `<=`, `>=` | `sale_price > 500000` |
| `IS NULL` | `latitude IS NULL` |
| `IS NOT NULL` | `latitude IS NOT NULL` |
| `IN (...)` | `township_code IN ('70', '71', '72')` |
| `NOT IN (...)` | `manner NOT IN ('NATURAL', 'UNDETERMINED')` |
| `BETWEEN` | `age BETWEEN 18 AND 65` |

## Logical Operators
```sql
$where=year = 2024 AND township_code = '70'
$where=manner = 'HOMICIDE' OR manner = 'SUICIDE'
$where=NOT (class = '299')
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
| `&` | `%26` |
| `+` | `%2B` |

## Query Parameters Summary

| Param | Purpose | Example |
|-------|---------|---------|
| `$select` | Columns to return | `$select=pin,year,mailed_tot` |
| `$where` | Filter rows | `$where=year=2024` |
| `$group` | Aggregate | `$group=township_code` |
| `$having` | Filter aggregates | `$having=count(*)>100` |
| `$order` | Sort results | `$order=year DESC` |
| `$limit` | Max rows (default 1000) | `$limit=5000` |
| `$offset` | Skip rows | `$offset=1000` |

## Common Patterns

### Pagination
```
$order=year DESC, pin&$limit=1000&$offset=0   # Page 1
$order=year DESC, pin&$limit=1000&$offset=1000 # Page 2
```

### Case-insensitive text search
```
$where=upper(vendor_name) like '%SMITH%'
```

### Date range
```
$where=sale_date >= '2024-01-01' AND sale_date < '2025-01-01'
```

### Null-safe comparison
```
$where=coalesce(amount, 0) > 1000
```

### Distinct values
```
$select=distinct township_name
```

### Count with grouping
```
$select=manner, count(*) as count
$group=manner
$order=count DESC
```
