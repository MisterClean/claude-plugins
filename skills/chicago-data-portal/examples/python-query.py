"""Chicago Data Portal query examples using requests + pandas."""

import os
from typing import Any, Iterator

import pandas as pd
import requests

# Optional: Load from .env or environment
APP_TOKEN = os.getenv("CHICAGO_DATA_PORTAL_TOKEN")
HEADERS = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

BASE_URL = "https://data.cityofchicago.org/resource"
METADATA_URL = "https://data.cityofchicago.org/api/views"


def query_dataset(dataset_id: str, params: dict) -> pd.DataFrame:
    """Query a Chicago dataset and return as DataFrame."""
    url = f"{BASE_URL}/{dataset_id}.json"
    resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def get_metadata(dataset_id: str) -> dict:
    """Fetch dataset metadata including columns."""
    url = f"{METADATA_URL}/{dataset_id}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def paginate_dataset(
    dataset_id: str, params: dict, page_size: int = 1000
) -> Iterator[pd.DataFrame]:
    """Generator that yields pages of results."""
    offset = 0
    while True:
        page_params = {**params, "$limit": page_size, "$offset": offset}
        df = query_dataset(dataset_id, page_params)
        if df.empty:
            break
        yield df
        offset += page_size
        if len(df) < page_size:
            break


def get_all_results(dataset_id: str, params: dict, page_size: int = 1000) -> pd.DataFrame:
    """Fetch all pages and concatenate into single DataFrame."""
    all_dfs = list(paginate_dataset(dataset_id, params, page_size))
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()


# ============================================================
# Example 1: Recent crimes in a ward
# ============================================================
def example_recent_crimes():
    """Get recent crimes in a specific ward."""
    crimes = query_dataset(
        "ijzp-q8t2",
        {
            "$select": "date, primary_type, description, block, latitude, longitude",
            "$where": "date >= '2024-01-01' AND ward = '42'",
            "$order": "date DESC",
            "$limit": 100,
        },
    )
    print(f"Found {len(crimes)} crimes")
    print(crimes.head())
    return crimes


# ============================================================
# Example 2: 311 requests by type (aggregated)
# ============================================================
def example_311_by_type():
    """Get 311 service requests aggregated by type."""
    requests_by_type = query_dataset(
        "v6vf-nfxy",
        {
            "$select": "sr_type, count(*) as total",
            "$where": "created_date >= '2024-01-01'",
            "$group": "sr_type",
            "$order": "total DESC",
            "$limit": 20,
        },
    )
    print("Top 311 request types:")
    print(requests_by_type)
    return requests_by_type


# ============================================================
# Example 3: Geospatial - crimes near a location
# ============================================================
def example_crimes_near_location(lat: float, lon: float, radius_m: int):
    """Get crimes within a radius of a point."""
    crimes = query_dataset(
        "ijzp-q8t2",
        {
            "$where": f"within_circle(location, {lat}, {lon}, {radius_m})",
            "$order": "date DESC",
            "$limit": 100,
        },
    )
    print(f"Found {len(crimes)} crimes within {radius_m}m of ({lat}, {lon})")
    return crimes


# ============================================================
# Example 4: Time series - monthly crime counts
# ============================================================
def example_monthly_crime_counts():
    """Get crime counts by month."""
    monthly = query_dataset(
        "ijzp-q8t2",
        {
            "$select": "date_trunc_ym(date) as month, count(*) as total",
            "$where": "date >= '2024-01-01'",
            "$group": "date_trunc_ym(date)",
            "$order": "month",
        },
    )
    print("Monthly crime counts:")
    print(monthly)
    return monthly


# ============================================================
# Example 5: Inspect dataset columns before querying
# ============================================================
def example_inspect_dataset(dataset_id: str):
    """Print column information for a dataset."""
    meta = get_metadata(dataset_id)
    print(f"Dataset: {meta['name']}")
    print(f"Description: {meta.get('description', 'N/A')}")
    print("\nColumns:")
    for col in meta["columns"]:
        desc = col.get("description", "No description")
        print(f"  {col['fieldName']} ({col['dataTypeName']}): {desc[:60]}...")


# ============================================================
# Example 6: Paginate through large results
# ============================================================
def example_paginate_permits():
    """Get all building permits for 2024 using pagination."""
    all_permits = get_all_results(
        "ydr8-5enu",
        {
            "$where": "issue_date >= '2024-01-01'",
            "$order": "issue_date DESC",
        },
        page_size=2000,
    )
    print(f"Total permits: {len(all_permits)}")
    return all_permits


# ============================================================
# Example 7: Food inspections analysis
# ============================================================
def example_food_inspections():
    """Analyze food inspection results."""
    inspections = query_dataset(
        "4ijn-s7e5",
        {
            "$select": "results, count(*) as total",
            "$where": "inspection_date >= '2024-01-01'",
            "$group": "results",
            "$order": "total DESC",
        },
    )
    print("Food inspection results:")
    print(inspections)
    return inspections


if __name__ == "__main__":
    # Run examples
    print("=" * 60)
    print("Example 1: Recent crimes")
    print("=" * 60)
    example_recent_crimes()

    print("\n" + "=" * 60)
    print("Example 2: 311 by type")
    print("=" * 60)
    example_311_by_type()

    print("\n" + "=" * 60)
    print("Example 3: Crimes near Willis Tower")
    print("=" * 60)
    example_crimes_near_location(41.8789, -87.6359, 500)

    print("\n" + "=" * 60)
    print("Example 4: Monthly crime counts")
    print("=" * 60)
    example_monthly_crime_counts()

    print("\n" + "=" * 60)
    print("Example 5: Inspect crimes dataset")
    print("=" * 60)
    example_inspect_dataset("ijzp-q8t2")
