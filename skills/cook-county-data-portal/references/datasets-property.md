# Property & Taxation Datasets

Cook County property and taxation datasets from the Assessor's Office, Treasurer, and Recorder of Deeds.

## Assessor Datasets

### Assessed Values
| Field | Value |
|-------|-------|
| **Dataset** | [Assessor - Assessed Values](https://datacatalog.cookcountyil.gov/d/uzyt-m557) |
| **ID** | `uzyt-m557` |
| **Update** | Monthly |
| **Coverage** | 1999 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit Parcel Identification Number |
| `year` | number | Tax year |
| `class` | text | Property class code |
| `township_code` | text | 2-digit township code |
| `township_name` | text | Township name |
| `mailed_bldg` | number | Assessor mailed building value |
| `mailed_land` | number | Assessor mailed land value |
| `mailed_tot` | number | Assessor mailed total value |
| `certified_tot` | number | Certified total value (after Assessor appeals) |
| `board_tot` | number | Board of Review certified total value |

**Notes:**
- Values are assessed values, NOT market values
- Adjust by level of assessment to get market value (levels vary by property class)
- Three stages: mailed → certified → Board of Review certified

---

### Parcel Sales
| Field | Value |
|-------|-------|
| **Dataset** | [Assessor - Parcel Sales](https://datacatalog.cookcountyil.gov/d/wvhk-k5uv) |
| **ID** | `wvhk-k5uv` |
| **Update** | Monthly |
| **Coverage** | 1999 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit Parcel Identification Number |
| `year` | number | Year of sale |
| `sale_date` | calendar_date | Sale date (recorded, not executed) |
| `sale_price` | number | Sale price |
| `doc_no` | text | Document number (matches Clerk's records) |
| `deed_type` | text | Deed type (warranty, quitclaim, etc.) |
| `class` | text | Property class at time of sale |
| `township_code` | text | Township code |

**Notes:**
- Includes non-arms-length transactions
- Use filter columns (`sale_filter_*`) to recreate legacy filtering
- Document numbers can be used on Clerk's website for more details

---

### Parcel Universe
| Field | Value |
|-------|-------|
| **Dataset** | [Assessor - Parcel Universe](https://datacatalog.cookcountyil.gov/d/nj4t-kc8j) |
| **ID** | `nj4t-kc8j` |
| **Update** | Monthly |
| **Coverage** | All Cook County parcels |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit PIN |
| `pin10` | text | 10-digit PIN |
| `year` | number | Tax year |
| `class` | text | Property class |
| `triad_name` | text | Triad name (City, North, South) |
| `township_name` | text | Township name |
| `township_code` | text | Township code |
| `municipality_name` | text | Municipality name |
| `latitude` | number | Parcel centroid latitude |
| `longitude` | number | Parcel centroid longitude |

**Notes:**
- Complete parcel inventory with geographic and governmental data
- Use for joining other datasets by PIN
- Triads determine reassessment cycle

---

### Property Characteristics (Residential)
| Field | Value |
|-------|-------|
| **Dataset** | [Assessor - Single and Multi-Family Improvement Characteristics](https://datacatalog.cookcountyil.gov/d/x54s-btds) |
| **ID** | `x54s-btds` |
| **Update** | Monthly |
| **Coverage** | 1999 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit PIN |
| `year` | number | Tax year |
| `class` | text | Property class |
| `bldg_sf` | number | Building square footage |
| `rooms` | number | Number of rooms |
| `beds` | number | Number of bedrooms |
| `fbath` | number | Full bathrooms |
| `hbath` | number | Half bathrooms |
| `age` | number | Building age |
| `ext_wall` | text | Exterior wall material |
| `roof_cnst` | text | Roof construction |

**Notes:**
- Single and multi-family (less than 7 units) only
- Each row is one building (improvement) on a parcel
- Multiple rows per PIN means multiple buildings

---

### Parcel Addresses
| Field | Value |
|-------|-------|
| **Dataset** | [Assessor - Parcel Addresses](https://datacatalog.cookcountyil.gov/d/3723-97qp) |
| **ID** | `3723-97qp` |
| **Update** | Monthly |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit PIN |
| `year` | number | Tax year |
| `prop_address` | text | Property address |
| `prop_city` | text | City |
| `prop_zip` | text | ZIP code |

---

## Treasurer Datasets

### Annual Tax Sale
| Field | Value |
|-------|-------|
| **Dataset** | [Treasurer - Annual Tax Sale](https://datacatalog.cookcountyil.gov/d/55ju-2fs9) |
| **ID** | `55ju-2fs9` |
| **Update** | After each annual sale |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `pin` | text | 14-digit PIN |
| `tax_year` | number | Tax year |
| `total_amt` | number | Total amount owed |
| `bid_amt` | number | Winning bid amount |
| `sale_date` | calendar_date | Date of sale |

**Notes:**
- Delinquent property tax sales
- Buyer purchases tax lien, not the property

---

### Scavenger Tax Sale
| Field | Value |
|-------|-------|
| **Dataset** | [Treasurer - Scavenger Tax Sale](https://datacatalog.cookcountyil.gov/d/ydgz-vkrp) |
| **ID** | `ydgz-vkrp` |
| **Update** | After each sale |

**Notes:**
- For taxes delinquent 2+ years
- Similar structure to Annual Tax Sale

---

## Quick Metadata Check

Get full schema for any dataset:
```bash
curl "https://datacatalog.cookcountyil.gov/api/views/<ID>" | jq '.columns[] | {fieldName, dataTypeName, description}'
```

## Common Query Patterns

### Get assessed values for a specific PIN
```
$where=pin = '12345678901234' AND year = 2024
```

### Find all sales above $1M in a township
```
$where=sale_price > 1000000 AND township_code = '70'
$order=sale_price DESC
$limit=100
```

### Aggregate assessed values by township
```
$select=township_name, count(*) as parcels, sum(mailed_tot) as total_value
$where=year = 2024
$group=township_name
$order=total_value DESC
```

### Find recently sold properties
```
$where=sale_date >= '2024-01-01'
$order=sale_date DESC
$limit=1000
```

## Township Codes

| Code | Township |
|------|----------|
| 10 | Barrington |
| 11 | Berwyn |
| 12 | Bloom |
| 13 | Bremen |
| 14 | Calumet |
| 15 | Cicero |
| 16 | Elk Grove |
| 17 | Evanston |
| 18 | Hanover |
| 19 | Lemont |
| 20 | Leyden |
| 21 | Lyons |
| 22 | Maine |
| 23 | New Trier |
| 24 | Niles |
| 25 | Northfield |
| 26 | Norwood Park |
| 27 | Oak Park |
| 28 | Orland |
| 29 | Palatine |
| 30 | Palos |
| 31 | Proviso |
| 32 | Rich |
| 33 | River Forest |
| 34 | Riverside |
| 35 | Schaumburg |
| 36 | Stickney |
| 37 | Thornton |
| 38 | Wheeling |
| 70 | Chicago (South) |
| 71 | Chicago (North) |
| 72 | Chicago (West) |
| 73 | Chicago (Lake) |
| 74 | Chicago (Rogers Park) |
| 75 | Chicago (Jefferson) |
| 76 | Chicago (Lake View) |
| 77 | Hyde Park |
