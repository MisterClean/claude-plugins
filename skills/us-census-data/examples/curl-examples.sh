#!/bin/bash
# US Census API curl examples
# Requires: CENSUS_API_KEY environment variable or replace $CENSUS_API_KEY with your key
# Get a key at: https://api.census.gov/data/key_signup.html

# Note: Queries work without a key but are rate-limited (~500/day)
# With a key, there are no published rate limits

# ============================================================
# DISCOVERY - Find datasets, variables, and geographies
# ============================================================

# List all available datasets
curl "https://api.census.gov/data.json" | jq '.dataset[] | {title, c_vintage, c_dataset}'

# List variables for ACS 5-Year 2022
curl "https://api.census.gov/data/2022/acs/acs5/variables.json" | jq '.variables | keys[:20]'

# Search for specific variable by name
curl "https://api.census.gov/data/2022/acs/acs5/variables.json" | jq '.variables | to_entries | map(select(.key | contains("B19013"))) | from_entries'

# Get all variables in a table (group)
curl "https://api.census.gov/data/2022/acs/acs5/groups/B19013.json" | jq '.variables'

# List available tables/groups
curl "https://api.census.gov/data/2022/acs/acs5/groups.json" | jq '.groups[:20]'

# List available geographies
curl "https://api.census.gov/data/2022/acs/acs5/geography.json" | jq '.fips[:20]'


# ============================================================
# STATE-LEVEL QUERIES
# ============================================================

# Total population by state
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:*&key=$CENSUS_API_KEY"

# Median household income by state
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=state:*&key=$CENSUS_API_KEY"

# Multiple variables - population, income, housing units
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E,B25001_001E&for=state:*&key=$CENSUS_API_KEY"

# Specific state (Illinois = 17)
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E&for=state:17&key=$CENSUS_API_KEY"


# ============================================================
# COUNTY-LEVEL QUERIES
# ============================================================

# All counties in a state (Illinois)
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY"

# Specific county (Cook County, IL = 031)
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E&for=county:031&in=state:17&key=$CENSUS_API_KEY"

# Multiple counties in a state
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=county:031,043,089&in=state:17&key=$CENSUS_API_KEY"

# Include margin of error
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E,B19013_001M&for=county:*&in=state:17&key=$CENSUS_API_KEY"


# ============================================================
# TRACT-LEVEL QUERIES (requires state AND county)
# ============================================================

# All tracts in Cook County, IL
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=tract:*&in=state:17&in=county:031&key=$CENSUS_API_KEY"

# Specific tract
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E&for=tract:010100&in=state:17&in=county:031&key=$CENSUS_API_KEY"


# ============================================================
# BLOCK GROUP QUERIES (requires state, county, AND tract)
# ============================================================

# All block groups in a tract
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=block%20group:*&in=state:17&in=county:031&in=tract:010100&key=$CENSUS_API_KEY"


# ============================================================
# ZIP CODE TABULATION AREAS (ZCTA)
# ============================================================

# All ZCTAs (warning: large response)
# curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=zip%20code%20tabulation%20area:*&key=$CENSUS_API_KEY"

# Specific ZCTA
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E,B19013_001E&for=zip%20code%20tabulation%20area:60601&key=$CENSUS_API_KEY"


# ============================================================
# METROPOLITAN STATISTICAL AREAS
# ============================================================

# Chicago-Naperville-Elgin MSA (code 16980)
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=metropolitan%20statistical%20area/micropolitan%20statistical%20area:16980&key=$CENSUS_API_KEY"


# ============================================================
# CONGRESSIONAL DISTRICTS
# ============================================================

# All congressional districts in Illinois
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=congressional%20district:*&in=state:17&key=$CENSUS_API_KEY"


# ============================================================
# DECENNIAL CENSUS (2020)
# ============================================================

# 2020 Decennial - Total population by state
curl "https://api.census.gov/data/2020/dec/dhc?get=NAME,P1_001N&for=state:*&key=$CENSUS_API_KEY"

# 2020 Decennial - Race by county
curl "https://api.census.gov/data/2020/dec/dhc?get=NAME,P1_001N,P3_003N,P3_004N&for=county:*&in=state:17&key=$CENSUS_API_KEY"

# 2020 Decennial - Block level (only available in Decennial)
curl "https://api.census.gov/data/2020/dec/dhc?get=NAME,P1_001N&for=block:*&in=state:17&in=county:031&in=tract:010100&in=block%20group:1&key=$CENSUS_API_KEY"


# ============================================================
# POPULATION ESTIMATES
# ============================================================

# Population estimates by state (2021)
curl "https://api.census.gov/data/2021/pep/population?get=NAME,POP_2021&for=state:*&key=$CENSUS_API_KEY"


# ============================================================
# ACS 1-YEAR (only large geographies 65k+ population)
# ============================================================

# ACS 1-Year - States
curl "https://api.census.gov/data/2023/acs/acs1?get=NAME,B01001_001E&for=state:*&key=$CENSUS_API_KEY"

# ACS 1-Year - Large counties only
curl "https://api.census.gov/data/2023/acs/acs1?get=NAME,B01001_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY"


# ============================================================
# SUBJECT TABLES (pre-calculated percentages)
# ============================================================

# Poverty rate by state
curl "https://api.census.gov/data/2022/acs/acs5/subject?get=NAME,S1701_C03_001E&for=state:*&key=$CENSUS_API_KEY"

# Education attainment percentage
curl "https://api.census.gov/data/2022/acs/acs5/subject?get=NAME,S1501_C02_015E&for=state:*&key=$CENSUS_API_KEY"


# ============================================================
# SAVING OUTPUT
# ============================================================

# Save as JSON
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY" > illinois_income.json

# Convert to CSV with jq
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY" | jq -r '.[] | @csv' > illinois_income.csv

# Pretty print JSON
curl "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:17&key=$CENSUS_API_KEY" | jq '.'
