# Skill Tests

Integration tests that verify the API examples in skills work against live endpoints.

## Setup

```bash
pip install -r tests/requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only Chicago data portal tests
pytest tests/test_chicago_data_portal.py -v

# Skip live API tests (useful for CI without network)
pytest tests/ -m "not live"

# Run with app token for higher rate limits
export CHICAGO_DATA_PORTAL_TOKEN="your_token"
pytest tests/test_chicago_data_portal.py -v
```

## Test Structure

Each skill has a corresponding test file:

| Skill | Test File |
|-------|-----------|
| chicago-data-portal | `test_chicago_data_portal.py` |
| cook-county-data-portal | `test_cook_county_data_portal.py` (planned) |
| us-census-data | `test_us_census_data.py` (planned) |

## What's Tested

Tests verify that the query patterns documented in skill examples actually work:

- **Basic queries**: JSON/CSV responses, column existence
- **Metadata**: Dataset schema retrieval, column info
- **Filtering**: Date ranges, category filters, IN clauses
- **Aggregation**: GROUP BY, count, date_trunc functions
- **Geospatial**: within_circle, within_box queries
- **Pagination**: Offset-based paging, no overlap
- **Error handling**: Invalid datasets, bad column names

## Markers

- `@pytest.mark.live` - Tests that hit live APIs (may be slow, need network)
- `@pytest.mark.slow` - Long-running tests

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CHICAGO_DATA_PORTAL_TOKEN` | App token for higher rate limits |
| `COOK_COUNTY_DATA_PORTAL_TOKEN` | Cook County app token |
| `CENSUS_API_KEY` | US Census API key |

Tests work without tokens but may hit rate limits on repeated runs.
