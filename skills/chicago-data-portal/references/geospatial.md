# Geospatial Queries

Chicago datasets with location data support powerful spatial queries. Most datasets have a `location` column (Point type) with lat/lon coordinates.

## Coordinate Ordering Warning

**Different functions use different coordinate orders:**

| Function | Order | Example |
|----------|-------|---------|
| `within_circle` | lat, lon | `within_circle(location, 41.8781, -87.6298, 1000)` |
| `within_box` | north_lat, west_lon, south_lat, east_lon | `within_box(location, 42.0, -87.9, 41.6, -87.5)` |
| WKT (POLYGON, POINT) | lon, lat | `'POINT(-87.6298 41.8781)'` |
| GeoJSON | lon, lat | `[-87.6298, 41.8781]` |

**Remember:** SoQL functions use `lat, lon` but WKT/GeoJSON use `lon, lat`.

## Functions

### within_circle

Find records within a radius (in meters) of a point:

```sql
$where=within_circle(location, {lat}, {lon}, {radius_meters})
```

**Examples:**
```sql
-- Crimes within 500m of Willis Tower (41.8789, -87.6359)
$where=within_circle(location, 41.8789, -87.6359, 500)

-- 311 requests within 1km of Wrigley Field (41.9484, -87.6553)
$where=within_circle(location, 41.9484, -87.6553, 1000)
```

### within_box

Find records within a bounding box:

```sql
$where=within_box(location, {north_lat}, {west_lon}, {south_lat}, {east_lon})
```

**Example:**
```sql
-- The Loop (roughly)
$where=within_box(location, 41.8870, -87.6425, 41.8750, -87.6190)
```

### within_polygon

Find records within an arbitrary polygon using WKT (Well-Known Text):

```sql
$where=within_polygon(location, 'MULTIPOLYGON((({lon1} {lat1}, {lon2} {lat2}, ...)))')
```

**Note:** Coordinates in WKT are `lon lat` (longitude first), opposite of the other functions.

**Example:**
```sql
-- Triangle in downtown
$where=within_polygon(location, 'MULTIPOLYGON(((-87.63 41.88, -87.62 41.88, -87.625 41.875, -87.63 41.88)))')
```

### distance_in_meters

Calculate distance from a point (useful for sorting by proximity):

```sql
$select=*, distance_in_meters(location, 'POINT({lon} {lat})') as distance
$order=distance ASC
```

**Example:**
```sql
-- Nearest food inspections to an address
$select=dba_name, address, results, distance_in_meters(location, 'POINT(-87.6298 41.8781)') as distance
&$order=distance ASC
&$limit=20
```

### intersects

Check if geometries overlap (for datasets with polygon geometry):

```sql
$where=intersects(the_geom, 'POLYGON(({lon1} {lat1}, ...))')
```

## Common Chicago Locations

| Location | Latitude | Longitude |
|----------|----------|-----------|
| City Hall | 41.8838 | -87.6319 |
| Willis Tower | 41.8789 | -87.6359 |
| Wrigley Field | 41.9484 | -87.6553 |
| Soldier Field | 41.8623 | -87.6167 |
| O'Hare Airport | 41.9742 | -87.9073 |
| Midway Airport | 41.7868 | -87.7522 |
| Navy Pier | 41.8917 | -87.6086 |
| Millennium Park | 41.8826 | -87.6226 |
| United Center | 41.8807 | -87.6742 |
| University of Chicago | 41.7886 | -87.5987 |

## Combining Spatial with Other Filters

```sql
-- Thefts in 2024 within 1km of downtown
$where=within_circle(location, 41.8781, -87.6298, 1000)
  AND date >= '2024-01-01'
  AND primary_type = 'THEFT'
$limit=500
```

## Checking for Location Data

Not all records have coordinates. Filter out nulls:

```sql
$where=location IS NOT NULL AND within_circle(location, 41.8781, -87.6298, 1000)
```

Or check for null lat/lon:

```sql
$where=latitude IS NOT NULL AND longitude IS NOT NULL
```

## Full URL Example

```bash
# Food inspections that failed within 500m of a location
curl "https://data.cityofchicago.org/resource/4ijn-s7e5.json?\$where=within_circle(location,41.8838,-87.6319,500)%20AND%20results=%27Fail%27&\$limit=50"
```
