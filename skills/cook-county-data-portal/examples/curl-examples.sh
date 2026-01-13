#!/bin/bash
# Cook County Data Portal curl examples
# Replace YOUR_TOKEN with your app token (optional but recommended)

# --- DISCOVERY ---

# Search catalog for datasets
curl "https://api.us.socrata.com/api/catalog/v1?domains=datacatalog.cookcountyil.gov&q=assessor%20values"

# Get dataset metadata (columns, types, descriptions)
curl "https://datacatalog.cookcountyil.gov/api/views/uzyt-m557" | jq '.columns[] | {fieldName, dataTypeName}'

# --- PROPERTY QUERIES ---

# Get assessed values for a specific PIN
curl "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$where=pin%20=%20%2712345678901234%27%20AND%20year%20=%202024"

# Recent parcel sales above $1M
curl "https://datacatalog.cookcountyil.gov/resource/wvhk-k5uv.json?\$where=sale_price%20%3E%201000000&\$order=sale_date%20DESC&\$limit=100"

# Assessed values by township (aggregated)
curl "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$select=township_name,count(*)%20as%20parcels,sum(mailed_tot)%20as%20total_value&\$where=year%20=%202024&\$group=township_name&\$order=total_value%20DESC"

# --- MEDICAL EXAMINER QUERIES ---

# Recent homicides
curl "https://datacatalog.cookcountyil.gov/resource/cjeq-bs86.json?\$where=manner%20=%20%27HOMICIDE%27%20AND%20death_date%20%3E=%20%272024-01-01%27&\$order=death_date%20DESC&\$limit=100"

# Deaths by manner (aggregated)
curl "https://datacatalog.cookcountyil.gov/resource/cjeq-bs86.json?\$select=manner,count(*)%20as%20count&\$where=death_date%20%3E=%20%272024-01-01%27&\$group=manner&\$order=count%20DESC"

# Opioid-related deaths
curl "https://datacatalog.cookcountyil.gov/resource/cjeq-bs86.json?\$where=primarycause%20like%20%27%25OPIOID%25%27%20OR%20primarycause%20like%20%27%25FENTANYL%25%27&\$limit=100"

# --- COURTS/SENTENCING QUERIES ---

# Recent sentencing data
curl "https://datacatalog.cookcountyil.gov/resource/tg8v-tm6u.json?\$where=disposition_date%20%3E=%20%272024-01-01%27&\$order=disposition_date%20DESC&\$limit=100"

# Sentences by offense category
curl "https://datacatalog.cookcountyil.gov/resource/tg8v-tm6u.json?\$select=offense_category,count(*)%20as%20count&\$group=offense_category&\$order=count%20DESC&\$limit=20"

# --- PAYROLL QUERIES ---

# Highest paid employees (current quarter)
curl "https://datacatalog.cookcountyil.gov/resource/xu6t-uvny.json?\$where=fiscal_year%20=%202024&\$order=base_pay%20DESC&\$limit=50"

# Payroll by bureau
curl "https://datacatalog.cookcountyil.gov/resource/xu6t-uvny.json?\$select=bureau,sum(base_pay)%20as%20total_pay&\$where=fiscal_year%20=%202024&\$group=bureau&\$order=total_pay%20DESC"

# --- PROCUREMENT QUERIES ---

# Large contracts
curl "https://datacatalog.cookcountyil.gov/resource/qh8j-6k63.json?\$where=amount%20%3E%201000000&\$order=amount%20DESC&\$limit=50"

# Contracts by department
curl "https://datacatalog.cookcountyil.gov/resource/qh8j-6k63.json?\$select=lead_department,count(*)%20as%20contracts,sum(amount)%20as%20total&\$group=lead_department&\$order=total%20DESC"

# --- WITH APP TOKEN (recommended for production) ---

curl -H "X-App-Token: YOUR_TOKEN" \
  "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$limit=1000"

# --- GEOSPATIAL ---

# Medical examiner cases within 5km of downtown Chicago
curl "https://datacatalog.cookcountyil.gov/resource/cjeq-bs86.json?\$where=within_circle(location,41.8781,-87.6298,5000)&\$limit=100"

# --- PAGINATION ---

# Page 1
curl "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$where=year%20=%202024&\$order=pin&\$limit=1000&\$offset=0"

# Page 2
curl "https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json?\$where=year%20=%202024&\$order=pin&\$limit=1000&\$offset=1000"

# --- FULL EXPORT (large datasets) ---

# Download entire dataset as CSV
curl -o assessed_values.csv "https://datacatalog.cookcountyil.gov/api/views/uzyt-m557/rows.csv?accessType=DOWNLOAD"

# --- SODA3 POST (complex queries) ---

curl -X POST \
  -H "X-App-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT township_name, count(*) as count, avg(mailed_tot) as avg_value WHERE year = 2024 GROUP BY township_name ORDER BY avg_value DESC",
    "page": {"pageNumber": 1, "pageSize": 100}
  }' \
  "https://datacatalog.cookcountyil.gov/api/v3/views/uzyt-m557/query.json"
