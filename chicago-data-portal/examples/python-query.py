"""Chicago Data Portal query examples using requests + pandas."""

import requests
import pandas as pd

# Optional: Set your app token for higher rate limits
APP_TOKEN = None  # or "your-token-here"
HEADERS = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

BASE_URL = "https://data.cityofchicago.org/resource"


def query_dataset(dataset_id: str, params: dict) -> pd.DataFrame:
    """Query a Chicago dataset and return as DataFrame."""
    url = f"{BASE_URL}/{dataset_id}.json"
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def get_metadata(dataset_id: str) -> dict:
    """Fetch dataset metadata including columns."""
    url = f"https://data.cityofchicago.org/api/views/{dataset_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


# Example 1: Recent crimes in a ward
crimes = query_dataset("ijzp-q8t2", {
    "$select": "date, primary_type, description, block",
    "$where": "date >= '2024-01-01' AND ward = '42'",
    "$order": "date DESC",
    "$limit": 100
})

# Example 2: 311 requests by type (aggregated)
requests_by_type = query_dataset("v6vf-nfxy", {
    "$select": "sr_type, count(*) as total",
    "$where": "created_date >= '2024-01-01'",
    "$group": "sr_type",
    "$order": "total DESC",
    "$limit": 20
})

# Example 3: Paginate through large results
def get_all_pages(dataset_id: str, base_params: dict, page_size: int = 1000):
    """Fetch all rows with pagination."""
    all_data = []
    offset = 0
    while True:
        params = {**base_params, "$limit": page_size, "$offset": offset}
        df = query_dataset(dataset_id, params)
        if df.empty:
            break
        all_data.append(df)
        offset += page_size
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
