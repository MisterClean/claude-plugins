#!/bin/bash
# Chicago Data Portal curl examples
# Replace YOUR_TOKEN with your app token (optional but recommended)

# --- DISCOVERY ---

# Search catalog for datasets
curl "https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=building%20permits"

# Get dataset metadata (columns, types, descriptions)
curl "https://data.cityofchicago.org/api/views/ijzp-q8t2" | jq '.columns[] | {fieldName, dataTypeName}'

# --- BASIC QUERIES (Legacy GET) ---

# Recent crimes (JSON)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$limit=10&\$order=date%20DESC"

# Recent crimes (CSV)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.csv?\$limit=10&\$order=date%20DESC"

# Filter by date and type
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=date%20%3E=%20%272024-01-01%27%20AND%20primary_type%20=%20%27THEFT%27&\$limit=100"

# With app token
curl -H "X-App-Token: YOUR_TOKEN" \
  "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$limit=100"

# --- AGGREGATION ---

# Count crimes by type
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$select=primary_type,count(*)%20as%20total&\$group=primary_type&\$order=total%20DESC&\$limit=10"

# --- GEOSPATIAL ---

# Crimes within 1km of downtown (41.8781, -87.6298)
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$where=within_circle(location,41.8781,-87.6298,1000)&\$limit=50"

# --- PAGINATION ---

# Page 1
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$order=date%20DESC&\$limit=1000&\$offset=0"

# Page 2
curl "https://data.cityofchicago.org/resource/ijzp-q8t2.json?\$order=date%20DESC&\$limit=1000&\$offset=1000"

# --- FULL EXPORT (large datasets) ---

# Download entire dataset as CSV
curl -o crimes.csv "https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD"

# --- SODA3 POST (complex queries) ---

curl -X POST \
  -H "X-App-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT primary_type, count(*) as total WHERE date >= '\''2024-01-01'\'' GROUP BY primary_type ORDER BY total DESC",
    "page": {"pageNumber": 1, "pageSize": 100}
  }' \
  "https://data.cityofchicago.org/api/v3/views/ijzp-q8t2/query.json"
