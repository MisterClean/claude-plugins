"""
Integration tests for Chicago Data Portal skill examples.

These tests verify that the SODA API endpoints and query patterns
documented in the skill actually work against the live API.

Run with: pytest tests/test_chicago_data_portal.py -v
Skip live tests: pytest tests/test_chicago_data_portal.py -v -m "not live"
"""

import pytest
import requests

# Base URLs
BASE_URL = "https://data.cityofchicago.org/resource"
METADATA_URL = "https://data.cityofchicago.org/api/views"
CATALOG_URL = "https://api.us.socrata.com/api/catalog/v1"

# Dataset IDs
CRIMES_ID = "ijzp-q8t2"
SERVICE_REQUESTS_ID = "v6vf-nfxy"
BUILDING_PERMITS_ID = "ydr8-5enu"
FOOD_INSPECTIONS_ID = "4ijn-s7e5"

# Test timeout
TIMEOUT = 30


def get_headers(app_token: str | None) -> dict:
    """Build request headers with optional app token."""
    if app_token:
        return {"X-App-Token": app_token}
    return {}


# ============================================================
# Basic Query Tests
# ============================================================


@pytest.mark.live
def test_basic_query_json(chicago_app_token):
    """Test basic JSON query returns data."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {"$limit": 5, "$order": "date DESC"}

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 5
    if data:
        # Verify expected columns exist
        assert "date" in data[0]
        assert "primary_type" in data[0]


@pytest.mark.live
def test_basic_query_csv(chicago_app_token):
    """Test basic CSV query returns data."""
    url = f"{BASE_URL}/{CRIMES_ID}.csv"
    params = {"$limit": 5}

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("Content-Type", "")
    # CSV should have header row + data rows
    lines = resp.text.strip().split("\n")
    assert len(lines) >= 1  # At least header


# ============================================================
# Metadata Tests
# ============================================================


@pytest.mark.live
def test_get_dataset_metadata(chicago_app_token):
    """Test fetching dataset metadata including columns."""
    url = f"{METADATA_URL}/{CRIMES_ID}"

    resp = requests.get(url, headers=get_headers(chicago_app_token), timeout=TIMEOUT)

    assert resp.status_code == 200
    meta = resp.json()

    # Verify structure
    assert "name" in meta
    assert "columns" in meta
    assert isinstance(meta["columns"], list)

    # Verify we can extract column info
    column_names = [col["fieldName"] for col in meta["columns"]]
    assert "date" in column_names
    assert "primary_type" in column_names


@pytest.mark.live
def test_catalog_search(chicago_app_token):
    """Test searching the catalog API."""
    params = {"domains": "data.cityofchicago.org", "q": "crimes"}

    resp = requests.get(
        CATALOG_URL, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()

    # Should return results
    assert "results" in data
    assert len(data["results"]) > 0


# ============================================================
# Filter Tests
# ============================================================


@pytest.mark.live
def test_where_filter_date(chicago_app_token):
    """Test date filtering with $where clause."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {
        "$where": "date >= '2024-01-01'",
        "$limit": 5,
        "$order": "date DESC",
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # All dates should be >= 2024-01-01
    for row in data:
        assert row["date"] >= "2024-01-01"


@pytest.mark.live
def test_where_filter_type(chicago_app_token):
    """Test filtering by category."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {
        "$where": "primary_type = 'THEFT'",
        "$limit": 10,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    for row in data:
        assert row["primary_type"] == "THEFT"


@pytest.mark.live
def test_where_filter_in_clause(chicago_app_token):
    """Test IN clause for multiple values."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {
        "$where": "primary_type IN ('THEFT', 'BATTERY', 'ASSAULT')",
        "$limit": 20,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    for row in data:
        assert row["primary_type"] in ("THEFT", "BATTERY", "ASSAULT")


# ============================================================
# Aggregation Tests
# ============================================================


@pytest.mark.live
def test_aggregation_count_by_type(chicago_app_token):
    """Test GROUP BY aggregation."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {
        "$select": "primary_type, count(*) as total",
        "$group": "primary_type",
        "$order": "total DESC",
        "$limit": 10,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0

    # Each row should have aggregated fields
    for row in data:
        assert "primary_type" in row
        assert "total" in row
        assert int(row["total"]) > 0


@pytest.mark.live
def test_aggregation_date_trunc(chicago_app_token):
    """Test date_trunc_ym for monthly aggregation."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {
        "$select": "date_trunc_ym(date) as month, count(*) as total",
        "$where": "date >= '2024-01-01'",
        "$group": "date_trunc_ym(date)",
        "$order": "month",
        "$limit": 12,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0

    for row in data:
        assert "month" in row
        assert "total" in row


# ============================================================
# Geospatial Tests
# ============================================================


@pytest.mark.live
def test_geospatial_within_circle(chicago_app_token):
    """Test within_circle geospatial query (downtown Chicago)."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    # Downtown Chicago: 41.8781, -87.6298, 500m radius
    params = {
        "$where": "within_circle(location, 41.8781, -87.6298, 500)",
        "$limit": 10,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    # Should find some crimes in downtown (high-traffic area)
    assert isinstance(data, list)


@pytest.mark.live
def test_geospatial_within_box(chicago_app_token):
    """Test within_box geospatial query (The Loop)."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    # The Loop bounding box
    params = {
        "$where": "within_box(location, 41.887, -87.6425, 41.875, -87.619)",
        "$limit": 10,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


# ============================================================
# Pagination Tests
# ============================================================


@pytest.mark.live
def test_pagination_offset(chicago_app_token):
    """Test pagination with limit and offset."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"

    # Get page 1
    params_p1 = {"$order": "date DESC", "$limit": 5, "$offset": 0}
    resp1 = requests.get(
        url, params=params_p1, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    # Get page 2
    params_p2 = {"$order": "date DESC", "$limit": 5, "$offset": 5}
    resp2 = requests.get(
        url, params=params_p2, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp1.status_code == 200
    assert resp2.status_code == 200

    data1 = resp1.json()
    data2 = resp2.json()

    # Pages should have different data (no overlap)
    if data1 and data2:
        ids1 = {row.get("id") for row in data1}
        ids2 = {row.get("id") for row in data2}
        # Should have no overlap
        assert ids1.isdisjoint(ids2)


# ============================================================
# Multi-Dataset Tests
# ============================================================


@pytest.mark.live
def test_311_service_requests(chicago_app_token):
    """Test 311 service requests dataset."""
    url = f"{BASE_URL}/{SERVICE_REQUESTS_ID}.json"
    params = {
        "$select": "sr_type, count(*) as total",
        "$where": "created_date >= '2024-01-01'",
        "$group": "sr_type",
        "$order": "total DESC",
        "$limit": 5,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "sr_type" in data[0]


@pytest.mark.live
def test_building_permits(chicago_app_token):
    """Test building permits dataset."""
    url = f"{BASE_URL}/{BUILDING_PERMITS_ID}.json"
    params = {
        "$order": "issue_date DESC",
        "$limit": 5,
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        assert "permit_type" in data[0] or "permit_" in data[0]


@pytest.mark.live
def test_food_inspections(chicago_app_token):
    """Test food inspections dataset."""
    url = f"{BASE_URL}/{FOOD_INSPECTIONS_ID}.json"
    params = {
        "$select": "results, count(*) as total",
        "$where": "inspection_date >= '2024-01-01'",
        "$group": "results",
        "$order": "total DESC",
    }

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0

    # Should have common results
    result_types = {row["results"] for row in data}
    assert "Pass" in result_types or "Fail" in result_types


# ============================================================
# Error Handling Tests
# ============================================================


@pytest.mark.live
def test_invalid_dataset_returns_404(chicago_app_token):
    """Test that invalid dataset ID returns 404."""
    url = f"{BASE_URL}/invalid-dataset-id.json"

    resp = requests.get(url, headers=get_headers(chicago_app_token), timeout=TIMEOUT)

    assert resp.status_code == 404


@pytest.mark.live
def test_invalid_column_returns_error(chicago_app_token):
    """Test that invalid column name returns error."""
    url = f"{BASE_URL}/{CRIMES_ID}.json"
    params = {"$where": "nonexistent_column = 'value'"}

    resp = requests.get(
        url, params=params, headers=get_headers(chicago_app_token), timeout=TIMEOUT
    )

    # Should return 400 Bad Request for invalid column
    assert resp.status_code in (400, 404)
