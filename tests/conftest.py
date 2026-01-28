"""Shared pytest fixtures and configuration for skill tests."""

import os

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "live: marks tests as requiring live API access")
    config.addinivalue_line("markers", "slow: marks tests as slow-running")


@pytest.fixture
def chicago_app_token():
    """Get Chicago Data Portal app token from environment if available."""
    return os.getenv("CHICAGO_DATA_PORTAL_TOKEN")


@pytest.fixture
def cook_county_app_token():
    """Get Cook County Data Portal app token from environment if available."""
    return os.getenv("COOK_COUNTY_DATA_PORTAL_TOKEN") or os.getenv(
        "CHICAGO_DATA_PORTAL_TOKEN"
    )


@pytest.fixture
def census_api_key():
    """Get Census API key from environment if available."""
    return os.getenv("CENSUS_API_KEY")
