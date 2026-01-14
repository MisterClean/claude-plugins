# Census Geographies Reference

Complete guide to Census geography hierarchy, FIPS codes, and query syntax.

## Geography Hierarchy

Census geographies are hierarchical. When querying sub-state geographies, parent geographies must be specified with `in=`:

```
Nation
└── Region (4)
    └── Division (9)
        └── State (50 + DC + territories)
            ├── County (~3,200)
            │   ├── County Subdivision
            │   ├── Census Tract (~85,000)
            │   │   └── Block Group (~240,000)
            │   │       └── Block (~8 million) [Decennial only]
            │   └── Place (city/town)
            ├── Congressional District
            ├── State Legislative District (upper/lower)
            └── School District
```

**Cross-cutting geographies** (not strictly hierarchical):
- ZCTA (Zip Code Tabulation Area)
- Metropolitan/Micropolitan Statistical Area
- Combined Statistical Area
- Urban Area
- Public Use Microdata Area (PUMA)

## Query Syntax

### Basic Pattern
```
&for={target_geography}:{code_or_wildcard}
&in={parent_geography}:{code}
```

### Wildcard (*)
Use `*` to request all geographies at that level:
```
for=state:*                    # All states
for=county:*&in=state:17       # All counties in Illinois
```

### Specific Geography
Use FIPS code to request specific geography:
```
for=state:17                   # Illinois only
for=county:031&in=state:17     # Cook County, IL only
```

## State FIPS Codes

| State | FIPS | State | FIPS |
|-------|------|-------|------|
| Alabama | 01 | Montana | 30 |
| Alaska | 02 | Nebraska | 31 |
| Arizona | 04 | Nevada | 32 |
| Arkansas | 05 | New Hampshire | 33 |
| California | 06 | New Jersey | 34 |
| Colorado | 08 | New Mexico | 35 |
| Connecticut | 09 | New York | 36 |
| Delaware | 10 | North Carolina | 37 |
| District of Columbia | 11 | North Dakota | 38 |
| Florida | 12 | Ohio | 39 |
| Georgia | 13 | Oklahoma | 40 |
| Hawaii | 15 | Oregon | 41 |
| Idaho | 16 | Pennsylvania | 42 |
| Illinois | 17 | Rhode Island | 44 |
| Indiana | 18 | South Carolina | 45 |
| Iowa | 19 | South Dakota | 46 |
| Kansas | 20 | Tennessee | 47 |
| Kentucky | 21 | Texas | 48 |
| Louisiana | 22 | Utah | 49 |
| Maine | 23 | Vermont | 50 |
| Maryland | 24 | Virginia | 51 |
| Massachusetts | 25 | Washington | 53 |
| Michigan | 26 | West Virginia | 54 |
| Minnesota | 27 | Wisconsin | 55 |
| Mississippi | 28 | Wyoming | 56 |
| Missouri | 29 | | |

### Territories

| Territory | FIPS |
|-----------|------|
| Puerto Rico | 72 |
| U.S. Virgin Islands | 78 |
| Guam | 66 |
| American Samoa | 60 |
| Northern Mariana Islands | 69 |

## Common County FIPS Codes

### Large Metro Counties

| County | State | FIPS | Query |
|--------|-------|------|-------|
| Los Angeles, CA | 06 | 037 | `for=county:037&in=state:06` |
| Cook, IL (Chicago) | 17 | 031 | `for=county:031&in=state:17` |
| Harris, TX (Houston) | 48 | 201 | `for=county:201&in=state:48` |
| Maricopa, AZ (Phoenix) | 04 | 013 | `for=county:013&in=state:04` |
| San Diego, CA | 06 | 073 | `for=county:073&in=state:06` |
| Orange, CA | 06 | 059 | `for=county:059&in=state:06` |
| Miami-Dade, FL | 12 | 086 | `for=county:086&in=state:12` |
| Dallas, TX | 48 | 113 | `for=county:113&in=state:48` |
| Kings, NY (Brooklyn) | 36 | 047 | `for=county:047&in=state:36` |
| Queens, NY | 36 | 081 | `for=county:081&in=state:36` |
| Clark, NV (Las Vegas) | 32 | 003 | `for=county:003&in=state:32` |
| King, WA (Seattle) | 53 | 033 | `for=county:033&in=state:53` |

## Geography Syntax by Level

### Nation
```
for=us:*
```

### Region
```
for=region:*
for=region:1              # Northeast
for=region:2              # Midwest
for=region:3              # South
for=region:4              # West
```

### Division
```
for=division:*
for=division:3            # East North Central
```

### State
```
for=state:*
for=state:17              # Illinois
```

### County
```
for=county:*&in=state:17                    # All counties in IL
for=county:031&in=state:17                  # Cook County, IL
for=county:031,043,089&in=state:17          # Multiple counties
```

### County Subdivision
```
for=county%20subdivision:*&in=state:17&in=county:031
```

### Census Tract
```
for=tract:*&in=state:17&in=county:031       # All tracts in Cook County
for=tract:010100&in=state:17&in=county:031  # Specific tract
```

### Block Group
```
for=block%20group:*&in=state:17&in=county:031&in=tract:010100
for=block%20group:1&in=state:17&in=county:031&in=tract:010100
```

### Block (Decennial Census only)
```
for=block:*&in=state:17&in=county:031&in=tract:010100&in=block%20group:1
```

### Place (City/Town)
```
for=place:*&in=state:17                     # All places in IL
for=place:14000&in=state:17                 # Chicago (place code 14000)
```

### ZCTA (Zip Code Tabulation Area)
```
for=zip%20code%20tabulation%20area:*        # All ZCTAs
for=zip%20code%20tabulation%20area:60601    # Specific ZCTA
```

**Note:** ZCTAs are not nested within states. Query without `in=` filter, or filter results after.

### Congressional District
```
for=congressional%20district:*&in=state:17  # All CDs in IL
for=congressional%20district:07&in=state:17 # IL-7
```

### Metropolitan Statistical Area
```
for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:*
for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:16980  # Chicago-Naperville-Elgin
```

### School District
```
for=school%20district%20(unified):*&in=state:17
for=school%20district%20(elementary):*&in=state:17
for=school%20district%20(secondary):*&in=state:17
```

## URL Encoding

Spaces in geography names must be URL-encoded:

| Geography | Raw | URL-Encoded |
|-----------|-----|-------------|
| Block group | `block group` | `block%20group` |
| County subdivision | `county subdivision` | `county%20subdivision` |
| Congressional district | `congressional district` | `congressional%20district` |
| School district | `school district` | `school%20district` |
| ZCTA | `zip code tabulation area` | `zip%20code%20tabulation%20area` |
| MSA | `metropolitan statistical area/micropolitan statistical area` | `metropolitan%20statistical%20area/micropolitan%20statistical%20area` |

## GEOID Construction

Census GEOIDs are hierarchical concatenations of FIPS codes:

| Geography | GEOID Format | Example | Location |
|-----------|--------------|---------|----------|
| State | SS | 17 | Illinois |
| County | SSCCC | 17031 | Cook County, IL |
| Tract | SSCCCTTTTTT | 17031010100 | Tract 0101.00 in Cook County |
| Block Group | SSCCCTTTTTTG | 170310101001 | BG 1 in Tract 0101.00 |
| Block | SSCCCTTTTTTGBBB | 170310101001001 | Block 1001 in BG 1 |

**Legend:**
- SS = State FIPS (2 digits)
- CCC = County FIPS (3 digits)
- TTTTTT = Tract (6 digits, includes implied decimal)
- G = Block Group (1 digit)
- BBB = Block (4 digits, Decennial only)

## Geographic Availability by Dataset

| Geography Level | ACS 5-Year | ACS 1-Year | Decennial | PEP |
|-----------------|------------|------------|-----------|-----|
| Nation | ✓ | ✓ | ✓ | ✓ |
| Region | ✓ | ✓ | ✓ | ✓ |
| Division | ✓ | ✓ | ✓ | ✓ |
| State | ✓ | ✓ | ✓ | ✓ |
| County | ✓ | ✓* | ✓ | ✓ |
| Tract | ✓ | | ✓ | |
| Block Group | ✓ | | ✓ | |
| Block | | | ✓ | |
| Place | ✓ | ✓* | ✓ | |
| ZCTA | ✓ | | ✓ | |
| Congressional District | ✓ | ✓ | ✓ | |
| School District | ✓ | | ✓ | |
| MSA | ✓ | ✓ | ✓ | ✓ |

*ACS 1-Year only for areas with 65,000+ population

## Multiple Geographies in One Query

Request multiple specific geographies by comma-separating codes:

```bash
# Multiple states
for=state:17,18,55              # IL, IN, WI

# Multiple counties in a state
for=county:031,043,089&in=state:17   # Cook, DuPage, Kane counties

# Multiple tracts (same county)
for=tract:010100,010200,010300&in=state:17&in=county:031
```

## Discovering Geography Codes

**Geography endpoint** shows available geographies for a dataset:
```
https://api.census.gov/data/2022/acs/acs5/geography.json
```

**Query for geography names:**
Add `NAME` variable to any query to get human-readable geography names:
```
get=NAME,B01001_001E&for=county:*&in=state:17
```

Returns:
```json
["NAME", "B01001_001E", "state", "county"]
["Cook County, Illinois", "5169517", "17", "031"]
```
