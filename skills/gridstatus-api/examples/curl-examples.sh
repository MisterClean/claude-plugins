#!/bin/bash
#
# GridStatus API - curl Examples
#
# Prerequisites:
#   - curl
#   - jq (optional, for JSON formatting)
#
# Authentication:
#   export GRIDSTATUS_API_KEY=your_api_key
#

# Check for API key
if [ -z "$GRIDSTATUS_API_KEY" ]; then
    echo "Error: Set GRIDSTATUS_API_KEY environment variable"
    echo "  export GRIDSTATUS_API_KEY=your_api_key"
    exit 1
fi

BASE_URL="https://api.gridstatus.io/v1"

# =============================================================================
# Helper function for pretty output
# =============================================================================
gridstatus_query() {
    local endpoint="$1"
    echo "Querying: $endpoint"
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "$endpoint" | python3 -m json.tool 2>/dev/null || cat
    echo ""
}

# =============================================================================
# Example 1: List All Datasets
# =============================================================================
list_datasets() {
    echo "=== List All Datasets ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets" | \
        python3 -c "
import json, sys
data = json.load(sys.stdin)
for d in data['data'][:10]:
    print(f\"{d['id']}: {d['name']}\")
print(f\"... and {len(data['data']) - 10} more\")
"
    echo ""
}

# =============================================================================
# Example 2: Basic Load Query
# =============================================================================
load_query() {
    echo "=== ERCOT Load Query ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=5" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 3: Price Query with Filter
# =============================================================================
price_query() {
    echo "=== ERCOT Houston Hub Prices ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/ercot_spp_real_time_15_min/query?start=2024-01-01&end=2024-01-02&filter_column=location&filter_value=HB_HOUSTON&limit=5" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 4: Query with Resampling
# =============================================================================
resampled_query() {
    echo "=== Daily Average CAISO Load ==="
    # Note: URL encode spaces as %20
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/caiso_load/query?start=2024-01-01&end=2024-01-07&resample=1%20day&resample_function=mean" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 5: Fuel Mix Query
# =============================================================================
fuel_mix_query() {
    echo "=== ERCOT Fuel Mix ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/ercot_fuel_mix/query?limit=3" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 6: PJM LMP Query
# =============================================================================
pjm_lmp_query() {
    echo "=== PJM Western Hub LMP ==="
    # Note: URL encode spaces as %20
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/pjm_lmp_real_time_5_min/query?start=2024-01-01&end=2024-01-02&filter_column=location&filter_value=WESTERN%20HUB&limit=5" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 7: CAISO LMP Query
# =============================================================================
caiso_lmp_query() {
    echo "=== CAISO LMP Day Ahead ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/caiso_lmp_day_ahead_hourly/query?start=2024-01-01&end=2024-01-02&limit=5" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 8: Get Dataset Metadata
# =============================================================================
dataset_metadata() {
    echo "=== Dataset Metadata for ercot_load ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets" | \
        python3 -c "
import json, sys
data = json.load(sys.stdin)
for d in data['data']:
    if d['id'] == 'ercot_load':
        print(f\"ID: {d['id']}\")
        print(f\"Name: {d['name']}\")
        print(f\"Description: {d['description']}\")
        print(f\"Earliest: {d['earliest_available_time_utc']}\")
        print(f\"Latest: {d['latest_available_time_utc']}\")
        print(f\"Frequency: {d.get('data_frequency', 'N/A')}\")
        print('Columns:')
        for col in d['all_columns']:
            print(f\"  - {col['name']} ({col['type']})\")
        break
"
    echo ""
}

# =============================================================================
# Example 9: Check API Usage
# =============================================================================
check_usage() {
    echo "=== API Usage ==="
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/api_usage" | \
        python3 -m json.tool
    echo ""
}

# =============================================================================
# Example 10: Export to CSV (pipe to file)
# =============================================================================
export_csv() {
    echo "=== Export to CSV ==="
    echo "Saving ERCOT load data to ercot_load.csv..."
    curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
        "$BASE_URL/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=100" | \
        python3 -c "
import json, sys, csv

data = json.load(sys.stdin)
rows = data['data']

if rows:
    writer = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
" > ercot_load.csv
    echo "Saved to ercot_load.csv"
    head -5 ercot_load.csv
    echo ""
}

# =============================================================================
# Quick reference - copy-paste commands
# =============================================================================
quick_reference() {
    echo "=== Quick Reference - Copy-Paste Commands ==="
    echo ""
    echo "# List datasets:"
    echo 'curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "https://api.gridstatus.io/v1/datasets"'
    echo ""
    echo "# Query ERCOT load:"
    echo 'curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "https://api.gridstatus.io/v1/datasets/ercot_load/query?start=2024-01-01&end=2024-01-02&limit=100"'
    echo ""
    echo "# Query with filter:"
    echo 'curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "https://api.gridstatus.io/v1/datasets/ercot_spp_real_time_15_min/query?filter_column=location&filter_value=HB_HOUSTON&limit=100"'
    echo ""
    echo "# Query with resampling:"
    echo 'curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "https://api.gridstatus.io/v1/datasets/caiso_load/query?start=2024-01-01&end=2024-01-07&resample=1%20hour&resample_function=mean"'
    echo ""
    echo "# Check API usage:"
    echo 'curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" "https://api.gridstatus.io/v1/api_usage"'
    echo ""
}

# =============================================================================
# Main
# =============================================================================
echo "GridStatus API curl Examples"
echo "============================"
echo ""

# Run examples (uncomment as needed)
# list_datasets
# load_query
# price_query
# resampled_query
# fuel_mix_query
# pjm_lmp_query
# caiso_lmp_query
# dataset_metadata
# check_usage
# export_csv

# Always show quick reference
quick_reference

echo ""
echo "Done!"
