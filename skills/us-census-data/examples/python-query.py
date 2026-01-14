"""US Census API query examples using requests + pandas."""

import os
import requests
import pandas as pd
from typing import Optional

# Load API key from environment or .env file
def load_api_key() -> Optional[str]:
    """Load Census API key from environment or .env file."""
    key = os.environ.get("CENSUS_API_KEY")
    if key:
        return key

    # Try loading from .env file
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("CENSUS_API_KEY="):
                    return line.strip().split("=", 1)[1]

    print("Warning: No CENSUS_API_KEY found. Register at https://api.census.gov/data/key_signup.html")
    return None

API_KEY = load_api_key()
BASE_URL = "https://api.census.gov/data"


def get_census_data(
    year: int,
    dataset: str,
    variables: list[str],
    geography: str,
    filters: Optional[dict] = None
) -> pd.DataFrame:
    """
    Query Census API and return results as DataFrame.

    Args:
        year: Data year (e.g., 2022)
        dataset: Dataset path (e.g., "acs/acs5")
        variables: List of variable codes (e.g., ["NAME", "B01001_001E"])
        geography: Target geography (e.g., "county:*")
        filters: Parent geography filters (e.g., {"state": "17"})

    Returns:
        DataFrame with Census data
    """
    url = f"{BASE_URL}/{year}/{dataset}"

    params = {
        "get": ",".join(variables),
        "for": geography,
    }

    if filters:
        for geo, code in filters.items():
            params[f"in"] = params.get("in", "") + f"{geo}:{code} "
        params["in"] = params["in"].strip().replace(" ", "&in=")

    if API_KEY:
        params["key"] = API_KEY

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    return pd.DataFrame(data[1:], columns=data[0])


def search_variables(
    year: int,
    dataset: str,
    keyword: str
) -> pd.DataFrame:
    """
    Search for variables containing a keyword.

    Args:
        year: Data year
        dataset: Dataset path
        keyword: Search term (case-insensitive)

    Returns:
        DataFrame of matching variables with name, label, concept
    """
    url = f"{BASE_URL}/{year}/{dataset}/variables.json"
    response = requests.get(url)
    response.raise_for_status()

    variables = response.json()["variables"]

    results = []
    keyword_lower = keyword.lower()

    for name, info in variables.items():
        label = info.get("label", "")
        concept = info.get("concept", "")

        if keyword_lower in label.lower() or keyword_lower in concept.lower():
            results.append({
                "variable": name,
                "label": label,
                "concept": concept
            })

    return pd.DataFrame(results)


def get_table_variables(year: int, dataset: str, table: str) -> pd.DataFrame:
    """
    Get all variables in a Census table.

    Args:
        year: Data year
        dataset: Dataset path
        table: Table code (e.g., "B19013")

    Returns:
        DataFrame with variable codes and labels
    """
    url = f"{BASE_URL}/{year}/{dataset}/groups/{table}.json"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    variables = data.get("variables", {})

    results = []
    for name, info in variables.items():
        if not name.endswith("_"):  # Skip internal variables
            results.append({
                "variable": name,
                "label": info.get("label", "")
            })

    return pd.DataFrame(results).sort_values("variable")


# Example 1: State-level population
print("Example 1: Total population by state")
states = get_census_data(
    year=2022,
    dataset="acs/acs5",
    variables=["NAME", "B01001_001E"],
    geography="state:*"
)
states["B01001_001E"] = pd.to_numeric(states["B01001_001E"])
print(states.head(10))
print()


# Example 2: County-level median income in Illinois
print("Example 2: Median household income by county in Illinois")
income = get_census_data(
    year=2022,
    dataset="acs/acs5",
    variables=["NAME", "B19013_001E", "B19013_001M"],
    geography="county:*",
    filters={"state": "17"}
)
income["B19013_001E"] = pd.to_numeric(income["B19013_001E"])
income["B19013_001M"] = pd.to_numeric(income["B19013_001M"])
print(income.sort_values("B19013_001E", ascending=False).head(10))
print()


# Example 3: Tract-level data in Cook County
print("Example 3: Population and housing units by tract in Cook County, IL")
tracts = get_census_data(
    year=2022,
    dataset="acs/acs5",
    variables=["NAME", "B01001_001E", "B25001_001E"],
    geography="tract:*",
    filters={"state": "17", "county": "031"}
)
tracts["B01001_001E"] = pd.to_numeric(tracts["B01001_001E"])
tracts["B25001_001E"] = pd.to_numeric(tracts["B25001_001E"])
print(f"Found {len(tracts)} tracts")
print(tracts.head(10))
print()


# Example 4: Search for income variables
print("Example 4: Search for variables containing 'median income'")
income_vars = search_variables(2022, "acs/acs5", "median income")
print(income_vars.head(20))
print()


# Example 5: Get all variables in a table
print("Example 5: Variables in table B19013 (Median Household Income)")
table_vars = get_table_variables(2022, "acs/acs5", "B19013")
print(table_vars)
print()


# Example 6: Multiple variables with race iterations
print("Example 6: Median income by race (table iterations)")
race_income = get_census_data(
    year=2022,
    dataset="acs/acs5",
    variables=[
        "NAME",
        "B19013_001E",   # All households
        "B19013A_001E",  # White alone
        "B19013B_001E",  # Black alone
        "B19013D_001E",  # Asian alone
        "B19013I_001E",  # Hispanic/Latino
    ],
    geography="state:17"  # Illinois
)
print(race_income)
