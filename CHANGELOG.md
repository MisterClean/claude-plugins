# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2026-01-13

### Changed

- **gridstatus-api** skill (v1.0.0 → v1.1.0): Updated based on real-world API testing
  - **CRITICAL FIX**: Corrected API parameter names - use `start_time`/`end_time` for curl, `start`/`end` for Python SDK
  - Added documentation for standardized datasets (`pjm_standardized_hourly`, `pjm_standardized_5_min`)
  - Clarified zone-specific data access via columns (e.g., `load.comed`) not filters
  - Added energy calculation formulas for hourly and 5-minute data
  - Enhanced troubleshooting section with common errors and fixes
  - Added timezone parameter guidance (`timezone="market"` for local time)
  - Documented curl as fallback when Python SDK has dependency issues
  - Added zone-specific load query examples for PJM

## [1.0.3] - 2026-01-13

### Added

- **gridstatus-api** skill: Query electricity grid data from US ISOs via GridStatus.io API
  - SKILL.md with workflow for load, pricing (LMP/SPP), fuel mix, forecasts, and ancillary services
  - Support for all major US ISOs: ERCOT, CAISO, PJM, MISO, NYISO, ISO-NE, SPP
  - Support for Canadian markets: IESO (Ontario), AESO (Alberta)
  - EIA national/regional data
  - `references/datasets-by-iso.md`: Complete catalog of 454 datasets organized by ISO
  - `references/api-reference.md`: Full API parameter documentation (filtering, resampling, pagination)
  - `references/common-queries.md`: Ready-to-use query patterns for common analysis tasks
  - `examples/python-query.py`: Python SDK examples using gridstatusio library
  - `examples/curl-examples.sh`: curl command templates for direct API access
  - API key management via GRIDSTATUS_API_KEY in .env file
  - Rate limit guidance (500K rows/month free tier)

## [1.0.2] - 2026-01-13

### Added

- **us-census-data** skill: Query demographic, economic, and housing data from the US Census Bureau API
  - SKILL.md with complete workflow for dataset selection, variable discovery, and query building
  - Support for ACS 5-Year, ACS 1-Year, Decennial Census, and Population Estimates
  - All geography levels (state, county, tract, block group, ZCTA, congressional district, etc.)
  - `references/datasets.md`: Complete dataset documentation with selection guide
  - `references/popular-variables.md`: 100+ curated variables by topic (demographics, income, housing, education, etc.)
  - `references/geographies.md`: Geography hierarchy, FIPS codes, query syntax
  - `references/tigerweb.md`: TIGERweb API guide for boundary geometry retrieval
  - `examples/python-query.py`: Python code using requests + pandas with .env API key loading
  - `examples/curl-examples.sh`: curl command templates for all query scenarios
  - API key management via CENSUS_API_KEY in .env file
  - Margin of error handling guidance for ACS estimates
  - Inspired by tidycensus R package but language-agnostic

## [1.0.1] - 2026-01-13

### Added

- **cook-county-data-portal** skill: Query and download datasets from Cook County Open Data Portal
  - SKILL.md with complete workflow for dataset discovery, querying, and output formatting
  - Progressive disclosure architecture with category-specific reference files
  - `references/datasets-property.md`: Property & Taxation datasets (Assessor, Treasurer)
  - `references/datasets-courts.md`: Courts & Legal datasets (State's Attorney, sentencing)
  - `references/datasets-health.md`: Health & Medical Examiner datasets
  - `references/datasets-finance.md`: Finance & Administration datasets (payroll, procurement)
  - `references/soql-quick-ref.md`: Complete SoQL function reference
  - `examples/python-query.py`: Python code using requests + pandas
  - `examples/curl-examples.sh`: Ready-to-run curl commands
  - Cook County-specific documentation (PINs, townships, fiscal quarters)

### Changed

- Reorganized project structure: skills now live in `skills/` directory
- Added `skills/README.md` as skills index
- Updated all documentation to reflect new structure

## [1.0.0] - 2026-01-13

### Added

- **chicago-data-portal** plugin: Query and download datasets from the City of Chicago Data Portal
  - SKILL.md with complete workflow for dataset discovery, querying, and output formatting
  - Support for both legacy GET and SODA3 POST query patterns
  - Geospatial query support (within_circle, within_box, within_polygon)
  - `references/popular-datasets.md`: 8 verified popular datasets with IDs
  - `references/soql-quick-ref.md`: Complete SoQL function reference
  - `examples/python-query.py`: Python code using requests + pandas
  - `examples/curl-examples.sh`: Ready-to-run curl commands
- Project README with installation and contribution guidelines
- MIT License
- This changelog

[1.0.2]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.2
[1.0.1]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.1
[1.0.0]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.0
