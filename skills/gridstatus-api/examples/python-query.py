#!/usr/bin/env python3
"""
GridStatus API - Python Examples

Prerequisites:
    pip install gridstatusio pandas

Authentication:
    export GRIDSTATUS_API_KEY=your_api_key
    # Or pass api_key parameter to GridStatusClient()
"""

import os
from datetime import datetime, timedelta

# Ensure API key is set
if not os.environ.get("GRIDSTATUS_API_KEY"):
    print("Error: Set GRIDSTATUS_API_KEY environment variable")
    print("  export GRIDSTATUS_API_KEY=your_api_key")
    exit(1)

from gridstatusio import GridStatusClient

# Initialize client
client = GridStatusClient()


# =============================================================================
# Example 1: List Available Datasets
# =============================================================================
def list_datasets_example():
    """Discover available datasets."""
    print("\n=== List Datasets ===")

    # List all datasets (prints to console)
    # client.list_datasets()

    # Search for specific datasets
    print("\nSearching for 'ercot' datasets:")
    client.list_datasets(filter_term="ercot")

    # Get list for programmatic use
    print("\nGetting fuel_mix datasets as list:")
    datasets = client.list_datasets(filter_term="fuel_mix", return_list=True)
    for d in datasets[:5]:
        print(f"  {d.id}: {d.name}")


# =============================================================================
# Example 2: Basic Load Query
# =============================================================================
def load_query_example():
    """Get system load data."""
    print("\n=== Load Query Example ===")

    # Get ERCOT load for a specific day
    df = client.get_dataset(
        dataset="ercot_load",
        start="2024-01-01",
        end="2024-01-02",
        timezone="US/Central",
        limit=100
    )

    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
    print("\nFirst 5 rows:")
    print(df.head())

    return df


# =============================================================================
# Example 3: Price Query with Filtering
# =============================================================================
def price_query_example():
    """Get electricity prices filtered by location."""
    print("\n=== Price Query Example ===")

    # ERCOT Houston hub prices
    df = client.get_dataset(
        dataset="ercot_spp_real_time_15_min",
        start="2024-01-01",
        end="2024-01-02",
        filter_column="location",
        filter_value="HB_HOUSTON",
        filter_operator="=",
        timezone="US/Central",
        limit=100
    )

    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
    print("\nFirst 5 rows:")
    print(df.head())

    return df


# =============================================================================
# Example 4: Multiple Location Filter
# =============================================================================
def multiple_locations_example():
    """Get prices for multiple locations."""
    print("\n=== Multiple Locations Example ===")

    # All ERCOT hubs
    df = client.get_dataset(
        dataset="ercot_spp_real_time_15_min",
        start="2024-01-01",
        end="2024-01-02",
        filter_column="location",
        filter_value=["HB_HOUSTON", "HB_NORTH", "HB_SOUTH", "HB_WEST"],
        filter_operator="in",
        limit=500
    )

    print(f"Unique locations: {df['location'].unique().tolist()}")
    print(f"Total rows: {len(df)}")

    return df


# =============================================================================
# Example 5: Resampling (Aggregation)
# =============================================================================
def resampling_example():
    """Aggregate data to different time intervals."""
    print("\n=== Resampling Example ===")

    # Daily average load
    df = client.get_dataset(
        dataset="caiso_load",
        start="2024-01-01",
        end="2024-01-07",
        resample="1 day",
        resample_function="mean"
    )

    print("Daily average CAISO load:")
    print(df)

    # Hourly max prices by location
    df_hourly = client.get_dataset(
        dataset="ercot_spp_real_time_15_min",
        start="2024-01-01",
        end="2024-01-02",
        filter_column="location",
        filter_value="HB_HOUSTON",
        resample="1 hour",
        resample_function="max"
    )

    print("\nHourly max ERCOT Houston prices:")
    print(df_hourly.head())

    return df


# =============================================================================
# Example 6: Fuel Mix
# =============================================================================
def fuel_mix_example():
    """Get generation by fuel type."""
    print("\n=== Fuel Mix Example ===")

    df = client.get_dataset(
        dataset="ercot_fuel_mix",
        start="2024-01-01",
        end="2024-01-02",
        limit=100
    )

    print(f"Columns: {list(df.columns)}")
    print("\nSample fuel mix data:")
    print(df.head())

    return df


# =============================================================================
# Example 7: Day-Ahead vs Real-Time Comparison
# =============================================================================
def dart_comparison_example():
    """Compare day-ahead and real-time prices."""
    print("\n=== DA-RT Comparison Example ===")

    # Get DART (day-ahead minus real-time) directly
    df = client.get_dataset(
        dataset="pjm_lmp_dart_5_min",
        start="2024-01-01",
        end="2024-01-02",
        filter_column="location",
        filter_value="WESTERN HUB",
        limit=100
    )

    print("PJM Western Hub DA-RT spread:")
    print(df.head())

    return df


# =============================================================================
# Example 8: Check API Usage
# =============================================================================
def check_usage_example():
    """Monitor API usage against limits."""
    print("\n=== API Usage Example ===")

    usage = client.get_api_usage()
    print(f"API Usage: {usage}")

    if usage.get("limit", -1) != -1:
        remaining = usage["limit"] - usage.get("usage", 0)
        print(f"Remaining rows: {remaining:,}")


# =============================================================================
# Example 9: Cross-ISO Standardized Data
# =============================================================================
def cross_iso_example():
    """Compare data across ISOs using standardized datasets."""
    print("\n=== Cross-ISO Comparison Example ===")

    # Standardized hourly data from multiple ISOs
    isos = ["ercot", "caiso", "pjm"]

    for iso in isos:
        df = client.get_dataset(
            dataset=f"{iso}_standardized_hourly",
            start="2024-01-01",
            end="2024-01-02",
            limit=24  # One day of hourly data
        )
        print(f"\n{iso.upper()} standardized columns: {list(df.columns)[:5]}...")


# =============================================================================
# Example 10: Forecasts
# =============================================================================
def forecast_example():
    """Get load and renewable forecasts."""
    print("\n=== Forecast Example ===")

    # ERCOT load forecast
    df = client.get_dataset(
        dataset="ercot_load_forecast",
        start="2024-01-01",
        end="2024-01-03",
        limit=100
    )

    print("ERCOT Load Forecast:")
    print(f"Columns: {list(df.columns)}")
    print(df.head())

    return df


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    print("GridStatus API Python Examples")
    print("=" * 50)

    # Run examples (uncomment as needed)

    # Dataset discovery
    list_datasets_example()

    # Basic queries
    # load_query_example()
    # price_query_example()

    # Filtering
    # multiple_locations_example()

    # Aggregation
    # resampling_example()

    # Generation
    # fuel_mix_example()

    # Price analysis
    # dart_comparison_example()

    # Usage monitoring
    check_usage_example()

    # Cross-ISO
    # cross_iso_example()

    # Forecasts
    # forecast_example()

    print("\n" + "=" * 50)
    print("Examples complete!")
