# SoQL Quick Reference

Complete syntax reference for Socrata Query Language (SoQL).

## Query Parameters

| Param | Purpose | Example |
|-------|---------|---------|
| `$select` | Columns/expressions to return | `$select=date, primary_type, count(*) as total` |
| `$where` | Filter rows | `$where=year = 2024 AND ward = 42` |
| `$group` | Group for aggregation | `$group=primary_type` |
| `$having` | Filter aggregated results | `$having=count(*) > 100` |
| `$order` | Sort results | `$order=date DESC` |
| `$limit` | Max rows (default 1000, max 50000) | `$limit=5000` |
| `$offset` | Skip rows for pagination | `$offset=1000` |

---

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
$where=(ward = 1 OR ward = 2) AND year = 2024
```

---

## Aggregate Functions

| Function | Example |
|----------|---------|
| `count(*)` | `$select=count(*) as total` |
| `count(column)` | `$select=count(arrest) as arrest_count` |
| `sum(column)` | `$select=sum(total_fee) as total_fees` |
| `avg(column)` | `$select=avg(fee) as avg_fee` |
| `min(column)` | `$select=min(date) as earliest` |
| `max(column)` | `$select=max(date) as latest` |
| `stddev_pop(column)` | Population standard deviation |
| `stddev_samp(column)` | Sample standard deviation |

**Aggregation example:**
```
$select=primary_type, count(*) as total, avg(community_area) as avg_area
&$group=primary_type
&$having=count(*) > 1000
&$order=total DESC
```

---

## Date Functions

### Extract Parts

| Function | Returns | Example |
|----------|---------|---------|
| `date_extract_y(col)` | Year (2024) | `date_extract_y(date) = 2024` |
| `date_extract_m(col)` | Month (1-12) | `date_extract_m(date) = 6` |
| `date_extract_d(col)` | Day (1-31) | `date_extract_d(date) = 15` |
| `date_extract_dow(col)` | Day of week (0=Sun, 6=Sat) | `date_extract_dow(date) = 0` |
| `date_extract_hh(col)` | Hour (0-23) | `date_extract_hh(date) = 14` |

### Truncate for Grouping

| Function | Truncates to |
|----------|--------------|
| `date_trunc_y(col)` | Year start (2024-01-01) |
| `date_trunc_ym(col)` | Month start (2024-06-01) |
| `date_trunc_ymd(col)` | Day start (2024-06-15) |

**Group by month example:**
```
$select=date_trunc_ym(date) as month, count(*) as total
&$group=date_trunc_ym(date)
&$order=month DESC
```

### Date Comparison

Use ISO 8601 format with single quotes:

```sql
-- Exact date
$where=date = '2024-06-15'

-- Date range
$where=date >= '2024-01-01' AND date < '2025-01-01'

-- With time
$where=date >= '2024-01-01T00:00:00' AND date < '2024-01-02T00:00:00'

-- Relative (this year)
$where=date_extract_y(date) = 2024
```

---

## Text Functions

| Function | Example |
|----------|---------|
| `upper(col)` | `upper(primary_type) = 'THEFT'` |
| `lower(col)` | `lower(status) = 'open'` |
| `starts_with(col, str)` | `starts_with(address, '123 N')` |
| `contains(col, str)` | `contains(description, 'VEHICLE')` |
| `like` | `address LIKE '%MICHIGAN%'` |
| `not like` | `address NOT LIKE '%APT%'` |

**LIKE wildcards:**
- `%` = any characters
- `_` = single character

```sql
-- Addresses on Michigan Ave
$where=address LIKE '%MICHIGAN%'

-- Starts with specific block
$where=address LIKE '100 N%'
```

---

## Geospatial Functions

See `references/geospatial.md` for detailed examples.

| Function | Syntax |
|----------|--------|
| `within_circle` | `within_circle(location, lat, lon, radius_meters)` |
| `within_box` | `within_box(location, north_lat, west_lon, south_lat, east_lon)` |
| `within_polygon` | `within_polygon(location, 'MULTIPOLYGON(...)')` |
| `distance_in_meters` | `distance_in_meters(location, 'POINT(lon lat)')` |
| `intersects` | `intersects(geometry, 'POLYGON(...)')` |

---

## System Fields

Every record has hidden system fields:

| Field | Description |
|-------|-------------|
| `:id` | Internal row ID |
| `:created_at` | When row was created |
| `:updated_at` | When row was last modified |

```sql
$select=:id, :updated_at, *
$where=:updated_at > '2024-01-01'
$order=:updated_at DESC
```

---

## URL Encoding

When building URLs, encode special characters:

| Character | Encoded |
|-----------|---------|
| space | `%20` or `+` |
| `=` | `%3D` |
| `>` | `%3E` |
| `<` | `%3C` |
| `'` | `%27` |
| `,` | `%2C` |
| `(` | `%28` |
| `)` | `%29` |

**Example:**
```
# Human readable
$where=date >= '2024-01-01' AND primary_type = 'THEFT'

# URL encoded
$where=date%20%3E=%20%272024-01-01%27%20AND%20primary_type%20=%20%27THEFT%27
```

---

## Common Query Patterns

### Recent records by date
```
$order=date DESC&$limit=100
```

### Count by category
```
$select=primary_type, count(*) as total
&$group=primary_type
&$order=total DESC
```

### Count by time period
```
$select=date_trunc_ym(date) as month, count(*) as total
&$where=date >= '2024-01-01'
&$group=date_trunc_ym(date)
&$order=month
```

### Filter + aggregate
```
$select=ward, count(*) as total
&$where=primary_type = 'THEFT' AND date >= '2024-01-01'
&$group=ward
&$order=total DESC
```

### Pagination
```
# Page 1
$order=date DESC&$limit=1000&$offset=0

# Page 2
$order=date DESC&$limit=1000&$offset=1000
```
