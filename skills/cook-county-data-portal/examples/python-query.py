"""Cook County Data Portal query examples using requests + pandas."""

import requests
import pandas as pd

# Optional: Set your app token for higher rate limits
APP_TOKEN = None  # or "your-token-here"
HEADERS = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

BASE_URL = "https://datacatalog.cookcountyil.gov/resource"


def query_dataset(dataset_id: str, params: dict) -> pd.DataFrame:
    """Query a Cook County dataset and return as DataFrame."""
    url = f"{BASE_URL}/{dataset_id}.json"
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def get_metadata(dataset_id: str) -> dict:
    """Fetch dataset metadata including columns."""
    url = f"https://datacatalog.cookcountyil.gov/api/views/{dataset_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def main():
    """Run example queries to demonstrate the API."""

    # Example 1: Get assessed values for a township
    assessed_values = query_dataset("uzyt-m557", {
        "$select": "pin, year, class, mailed_tot, certified_tot",
        "$where": "year = 2024 AND township_code = '70'",
        "$order": "mailed_tot DESC",
        "$limit": 100
    })
    print(f"Assessed values: {len(assessed_values)} rows")

    # Example 2: Recent parcel sales
    sales = query_dataset("wvhk-k5uv", {
        "$select": "pin, sale_date, sale_price, class, township_code",
        "$where": "sale_date >= '2024-01-01' AND sale_price > 500000",
        "$order": "sale_date DESC",
        "$limit": 100
    })
    print(f"Sales: {len(sales)} rows")

    # Example 3: Medical examiner homicides
    homicides = query_dataset("cjeq-bs86", {
        "$select": "casenumber, death_date, age, gender, race, manner, primarycause",
        "$where": "manner = 'Homicide' AND death_date >= '2024-01-01'",
        "$order": "death_date DESC",
        "$limit": 100
    })
    print(f"Homicides: {len(homicides)} rows")

    # Example 4: Deaths aggregated by manner
    deaths_by_manner = query_dataset("cjeq-bs86", {
        "$select": "manner, count(*) as count",
        "$where": "death_date >= '2024-01-01'",
        "$group": "manner",
        "$order": "count DESC"
    })
    print(deaths_by_manner)

    # Example 5: Employee payroll by bureau
    payroll_by_bureau = query_dataset("xu6t-uvny", {
        "$select": "bureau, sum(base_pay) as total_pay, count(*) as employees",
        "$where": "fiscal_year = 2024",
        "$group": "bureau",
        "$order": "total_pay DESC",
        "$limit": 20
    })
    print(f"Payroll by bureau: {len(payroll_by_bureau)} bureaus")

    # Example 6: Sentencing data
    sentences = query_dataset("tg8v-tm6u", {
        "$select": "offense_category, sentence_type, commitment_term, commitment_unit",
        "$where": "disposition_date >= '2024-01-01' AND primary_charge = true",
        "$order": "disposition_date DESC",
        "$limit": 100
    })
    print(f"Sentences: {len(sentences)} rows")

def get_all_pages(dataset_id: str, base_params: dict, page_size: int = 1000):
    """Fetch all rows with pagination."""
    all_data = []
    offset = 0

    # Ensure stable ordering for pagination
    if "$order" not in base_params:
        raise ValueError("Pagination requires $order parameter for stability")

    while True:
        params = {**base_params, "$limit": page_size, "$offset": offset}
        df = query_dataset(dataset_id, params)
        if df.empty:
            break
        all_data.append(df)
        offset += page_size
        print(f"Fetched {offset} rows...")

        # Safety limit
        if offset > 100000:
            print("Reached 100k row limit. Use CSV export for larger datasets.")
            break

    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


def search_datasets(query: str, limit: int = 10) -> list:
    """Search Cook County datasets by keyword."""
    url = "https://api.us.socrata.com/api/catalog/v1"
    params = {
        "domains": "datacatalog.cookcountyil.gov",
        "q": query,
        "limit": limit
    }
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()

    results = []
    for item in resp.json().get("results", []):
        resource = item.get("resource", {})
        results.append({
            "name": resource.get("name"),
            "id": resource.get("id"),
            "description": resource.get("description", "")[:200]
        })
    return results


if __name__ == "__main__":
    main()

    # Example 7: Paginate through large results
    print("\nPagination example (commented out to avoid long runtime):")
    # all_2024_sales = get_all_pages("wvhk-k5uv", {
    #     "$where": "sale_date >= '2024-01-01' AND sale_date < '2025-01-01'",
    #     "$order": "sale_date, pin"
    # })

    # Example 8: Using sodapy library (if installed)
    try:
        from sodapy import Socrata

        client = Socrata("datacatalog.cookcountyil.gov", None)
        results = client.get("uzyt-m557", where="year = 2024", limit=10)
        print(f"\nSodapy results: {len(results)} rows")
    except ImportError:
        print("\nsodapy not installed. Using requests instead.")

    # Example 9: Search for datasets
    print("\nSearching for property datasets:")
    property_datasets = search_datasets("property assessment")
    for ds in property_datasets[:5]:
        print(f"  {ds['name']} ({ds['id']})")
