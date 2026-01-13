# Popular Chicago Datasets

Quick reference for commonly requested datasets. Always verify columns via metadata endpoint before querying.

## Public Safety

| Dataset | ID | Key Columns | Update |
|---------|-----|-------------|--------|
| [Crimes - 2001 to Present](https://data.cityofchicago.org/d/ijzp-q8t2) | `ijzp-q8t2` | date, primary_type, description, ward, community_area, latitude, longitude | Daily |
| [Traffic Crashes - Crashes](https://data.cityofchicago.org/d/85ca-t3if) | `85ca-t3if` | crash_date, crash_type, injuries_total, latitude, longitude | Daily |

## City Services

| Dataset | ID | Key Columns | Update |
|---------|-----|-------------|--------|
| [311 Service Requests](https://data.cityofchicago.org/d/v6vf-nfxy) | `v6vf-nfxy` | sr_number, sr_type, created_date, status, ward, latitude, longitude | Daily |
| [Towed Vehicles](https://data.cityofchicago.org/d/ygr5-vcbg) | `ygr5-vcbg` | tow_date, make, color, plate, towed_to_address | Daily (90-day window) |

## Business & Permits

| Dataset | ID | Key Columns | Update |
|---------|-----|-------------|--------|
| [Building Permits](https://data.cityofchicago.org/d/ydr8-5enu) | `ydr8-5enu` | issue_date, permit_type, work_description, total_fee, latitude, longitude | Daily |
| [Business Licenses](https://data.cityofchicago.org/d/r5kz-chrr) | `r5kz-chrr` | license_id, doing_business_as_name, license_description, date_issued, ward | Daily |
| [Food Inspections](https://data.cityofchicago.org/d/4ijn-s7e5) | `4ijn-s7e5` | inspection_date, dba_name, facility_type, results, violations, latitude, longitude | Daily |

## Transportation

| Dataset | ID | Key Columns | Update |
|---------|-----|-------------|--------|
| [Divvy Trips](https://data.cityofchicago.org/d/fg6s-gzvg) | `fg6s-gzvg` | start_time, end_time, from_station_name, to_station_name, tripduration | Monthly |

## Quick Metadata Check

Get full schema for any dataset:
```bash
curl "https://data.cityofchicago.org/api/views/<ID>" | jq '.columns[] | {fieldName, dataTypeName, description}'
```

## Finding More Datasets

Search the catalog:
```
https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=YOUR_KEYWORDS
```

Or browse: https://data.cityofchicago.org
