#!/bin/bash
# Chicago Data Portal curl examples
# Replace YOUR_TOKEN with your app token (optional but recommended)

# ============================================================
# DISCOVERY & METADATA
# ============================================================

# Search catalog for datasets by keyword
curl "https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=building%20permits"

# Get dataset metadata (columns, types, descriptions)
curl "https://data.cityofchicago.org/api/views/ijzp-q8t2" | jq '.columns[] | {fieldName, dataTypeName}'

# Get just column names
curl "https://data.cityofchicago.org/api/views/ijzp-q8t2" | jq '.columns[].fieldName'

# ============================================================
# BASIC QUERIES
# ============================================================

# Recent crimes (JSON, 10 most recent)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$limit=10&\$order=date%20DESC"

# Same query but CSV format
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?\$limit=10&\$order=date%20DESC"

# With app token (higher rate limits)
curl -H "X-App-Token: YOUR_TOKEN" \
  "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$limit=100"

# ============================================================
# FILTERING
# ============================================================

# Thefts in 2024
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=date%20%3E=%20%272024-01-01%27%20AND%20primary_type%20=%20%27THEFT%27&\$limit=100"

# Multiple crime types
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=primary_type%20IN%20(%27THEFT%27,%27BATTERY%27,%27ASSAULT%27)&\$limit=100"

# Specific ward
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=ward%20=%20%2742%27&\$limit=100"

# Date range
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=date%20%3E=%20%272024-01-01%27%20AND%20date%20%3C%20%272024-02-01%27&\$limit=1000"

# ============================================================
# AGGREGATION
# ============================================================

# Count crimes by type
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$select=primary_type,count(*)%20as%20total&\$group=primary_type&\$order=total%20DESC&\$limit=10"

# Count by ward
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$select=ward,count(*)%20as%20total&\$where=date%20%3E=%20%272024-01-01%27&\$group=ward&\$order=total%20DESC"

# Count by month
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$select=date_trunc_ym(date)%20as%20month,count(*)%20as%20total&\$where=date%20%3E=%20%272024-01-01%27&\$group=date_trunc_ym(date)&\$order=month"

# 311 requests by type (top 20)
curl "https://data.cityofchicago.org/resource/v6vf-nfxy.json?\$select=sr_type,count(*)%20as%20total&\$where=created_date%20%3E=%20%272024-01-01%27&\$group=sr_type&\$order=total%20DESC&\$limit=20"

# ============================================================
# GEOSPATIAL
# ============================================================

# Crimes within 1km of downtown (41.8781, -87.6298)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=within_circle(location,41.8781,-87.6298,1000)&\$limit=100"

# Crimes within 500m of Willis Tower
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=within_circle(location,41.8789,-87.6359,500)&\$order=date%20DESC&\$limit=50"

# Food inspections near Wrigley Field that failed
curl "https://data.cityofchicago.org/resource/4ijn-s7e5.json?\$where=within_circle(location,41.9484,-87.6553,500)%20AND%20results=%27Fail%27&\$limit=50"

# Bounding box (The Loop area)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=within_box(location,41.887,-87.6425,41.875,-87.619)&\$limit=100"

# ============================================================
# PAGINATION
# ============================================================

# Page 1 (first 1000)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$order=date%20DESC&\$limit=1000&\$offset=0"

# Page 2 (next 1000)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$order=date%20DESC&\$limit=1000&\$offset=1000"

# Page 3
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$order=date%20DESC&\$limit=1000&\$offset=2000"

# ============================================================
# FULL EXPORTS (large datasets)
# ============================================================

# Download entire dataset as CSV (WARNING: can be very large!)
curl -o crimes.csv "https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD"

# Download with filters (more practical)
curl -o thefts_2024.csv "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?\$where=date%20%3E=%20%272024-01-01%27%20AND%20primary_type=%27THEFT%27&\$limit=50000"

# ============================================================
# SPECIFIC DATASET EXAMPLES
# ============================================================

# Building permits in last 30 days
curl "https://data.cityofchicago.org/resource/ydr8-5enu.json?\$where=issue_date%20%3E=%20%272024-12-01%27&\$order=issue_date%20DESC&\$limit=100"

# Business licenses issued this year
curl "https://data.cityofchicago.org/resource/r5kz-chrr.json?\$where=date_issued%20%3E=%20%272024-01-01%27&\$order=date_issued%20DESC&\$limit=100"

# Towed vehicles (rolling 90-day window)
curl "https://data.cityofchicago.org/resource/ygr5-vcbg.json?\$order=tow_date%20DESC&\$limit=50"

# Traffic crashes with injuries
curl "https://data.cityofchicago.org/resource/85ca-t3if.json?\$where=injuries_total%20%3E%200&\$order=crash_date%20DESC&\$limit=100"

# ============================================================
# ADVANCED: SODA3 POST (for complex queries)
# ============================================================

curl -X POST \
  -H "X-App-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT primary_type, count(*) as total WHERE date >= '\''2024-01-01'\'' GROUP BY primary_type ORDER BY total DESC",
    "page": {"pageNumber": 1, "pageSize": 100}
  }' \
  "https://data.cityofchicago.org/api/v3/views/ijzp-q8t2/query.json"
