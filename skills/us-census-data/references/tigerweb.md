# TIGERweb Geometry Reference

The Census Data API returns tabular data only. To get geographic boundaries (polygons, lines, points), use TIGERweb or download TIGER/Line shapefiles.

## TIGERweb REST API

TIGERweb provides Census boundaries as a GIS web service.

### Base URL
```
https://tigerweb.geo.census.gov/arcgis/rest/services/
```

### Available Services

| Service | Description | Use Case |
|---------|-------------|----------|
| `TIGERweb/tigerWMS_Current` | Current TIGER boundaries | Most queries |
| `TIGERweb/tigerWMS_ACS2023` | ACS 2023 vintage boundaries | Match ACS data |
| `TIGERweb/tigerWMS_Census2020` | 2020 Census boundaries | Match Decennial |
| `Census2020/Tracts_Blocks` | 2020 Tracts and Blocks | Block-level geometry |

### Layer IDs (tigerWMS_Current)

| Layer | ID | Description |
|-------|-----|-------------|
| States | 84 | State boundaries |
| Counties | 86 | County boundaries |
| Census Tracts | 8 | Tract boundaries |
| Block Groups | 10 | Block group boundaries |
| Places | 28 | Incorporated places |
| ZCTAs | 2 | Zip Code Tabulation Areas |
| Congressional Districts | 54 | 118th Congress |
| Metropolitan Statistical Areas | 76 | Metro/micro areas |

### Query Endpoint
```
https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/{layer_id}/query
```

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `where` | SQL-like filter | `STATE='17'` |
| `outFields` | Fields to return | `GEOID,NAME` or `*` |
| `f` | Output format | `geojson`, `json` |
| `returnGeometry` | Include shapes | `true` |
| `geometryType` | Geometry filter type | `esriGeometryEnvelope` |
| `geometry` | Bounding box or point | `-88,41,-87,42` |
| `inSR` | Input spatial reference | `4326` (WGS84) |
| `outSR` | Output spatial reference | `4326` (WGS84) |

## Example Queries

### Get All Counties in a State

**Illinois counties (state FIPS 17):**
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/86/query?where=STATE='17'&outFields=GEOID,NAME,ALAND&f=geojson&returnGeometry=true"
```

### Get Specific County Boundary

**Cook County, IL (GEOID 17031):**
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/86/query?where=GEOID='17031'&outFields=*&f=geojson&returnGeometry=true"
```

### Get All Tracts in a County

**Tracts in Cook County:**
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/8/query?where=STATE='17'+AND+COUNTY='031'&outFields=GEOID,NAME&f=geojson&returnGeometry=true"
```

### Get Geometry by Bounding Box

**Tracts within a bounding box:**
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/8/query?geometry=-87.7,41.8,-87.6,41.9&geometryType=esriGeometryEnvelope&inSR=4326&outFields=GEOID,NAME&f=geojson&returnGeometry=true"
```

### Get Block Groups in a Tract

**Block groups in tract 010100, Cook County, IL:**
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/10/query?where=STATE='17'+AND+COUNTY='031'+AND+TRACT='010100'&outFields=GEOID,BLKGRP&f=geojson&returnGeometry=true"
```

## Joining Census Data with Geometry

### Step 1: Query Census Data API
```bash
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY" > census_data.json
```

### Step 2: Query TIGERweb for Geometry
```bash
curl "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/86/query?where=STATE='17'&outFields=GEOID,NAME&f=geojson&returnGeometry=true" > geometry.geojson
```

### Step 3: Join on GEOID

**Python example:**
```python
import json
import pandas as pd

# Load census data
with open('census_data.json') as f:
    data = json.load(f)
df = pd.DataFrame(data[1:], columns=data[0])
df['GEOID'] = df['state'] + df['county']

# Load geometry
with open('geometry.geojson') as f:
    geo = json.load(f)

# Join by GEOID
for feature in geo['features']:
    geoid = feature['properties']['GEOID']
    match = df[df['GEOID'] == geoid]
    if not match.empty:
        feature['properties']['median_income'] = match.iloc[0]['B19013_001E']

# Save combined GeoJSON
with open('combined.geojson', 'w') as f:
    json.dump(geo, f)
```

## TIGER/Line Shapefiles

For bulk downloads or offline use, download TIGER/Line shapefiles directly.

### FTP Location
```
https://www2.census.gov/geo/tiger/
```

### Directory Structure
```
TIGER2023/
├── STATE/              # State boundaries
├── COUNTY/             # County boundaries
├── TRACT/              # Census tracts
├── BG/                 # Block groups
├── TABBLOCK20/         # 2020 blocks
├── PLACE/              # Places (cities)
├── ZCTA520/            # 5-digit ZCTAs
└── CD/                 # Congressional districts
```

### File Naming Convention
```
tl_2023_17_tract.zip    # 2023 tracts for Illinois (17)
tl_2023_17031_bg.zip    # 2023 block groups for Cook County (17031)
```

### Common Downloads

| Geography | URL Pattern |
|-----------|-------------|
| States | `https://www2.census.gov/geo/tiger/TIGER2023/STATE/tl_2023_us_state.zip` |
| Counties | `https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip` |
| Tracts (by state) | `https://www2.census.gov/geo/tiger/TIGER2023/TRACT/tl_2023_{state}_tract.zip` |
| Block Groups | `https://www2.census.gov/geo/tiger/TIGER2023/BG/tl_2023_{state}_bg.zip` |
| ZCTAs | `https://www2.census.gov/geo/tiger/TIGER2023/ZCTA520/tl_2023_us_zcta520.zip` |

## Cartographic Boundary Files

Simplified boundaries for mapping (smaller file sizes):

```
https://www2.census.gov/geo/tiger/GENZ2023/
```

| Type | Description |
|------|-------------|
| `cb_2023_us_state_500k.zip` | States, 1:500,000 scale |
| `cb_2023_us_county_500k.zip` | Counties, 1:500,000 scale |
| `cb_2023_{state}_tract_500k.zip` | Tracts, 1:500,000 scale |
| `cb_2023_{state}_bg_500k.zip` | Block groups, 1:500,000 scale |

## Coordinate Reference Systems

| System | EPSG Code | Use |
|--------|-----------|-----|
| WGS 84 | 4326 | Standard lat/lon, web mapping |
| NAD 83 | 4269 | US Census default |
| Web Mercator | 3857 | Google Maps, web tiles |

Specify with `outSR` parameter:
```
&outSR=4326    # WGS 84 (lat/lon)
```

## Geometry Response Formats

### GeoJSON (recommended)
```
&f=geojson
```
Returns standard GeoJSON FeatureCollection, compatible with most mapping libraries.

### Esri JSON
```
&f=json
```
Returns Esri-specific JSON format, useful for ArcGIS applications.

## Rate Limits and Best Practices

1. **Batch requests by state**: Don't request all US tracts in one query
2. **Use `outFields` wisely**: Only request needed fields
3. **Cache results**: Boundaries change infrequently (annually)
4. **Use cartographic boundaries for visualization**: Smaller files, faster rendering
5. **Use TIGER/Line for analysis**: More precise boundaries

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty results | Check GEOID format, layer ID, filter syntax |
| Timeout | Reduce geography scope (query one state at a time) |
| Missing geometry | Set `returnGeometry=true` |
| Wrong projection | Add `outSR=4326` for WGS84 lat/lon |
| Truncated results | Results may be paginated; check `exceededTransferLimit` |

## External Tools

- **QGIS**: Free GIS software for working with shapefiles
- **GeoPandas**: Python library for geospatial data
- **Mapshaper**: Online tool to simplify and convert shapefiles
- **Census Reporter**: Visual tool for exploring Census geographies
