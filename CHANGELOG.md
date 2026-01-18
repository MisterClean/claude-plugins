# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **chicago-data-portal** skill (v1.2.0): Major refactor for better usability and progressive disclosure
  - **SKILL.md**: Streamlined from ~200 lines to ~110 lines focused on quick-start workflow
    - New quick reference table for common endpoints
    - Simplified auth check section
    - Essential SoQL examples inline, detailed reference moved to `references/`
    - Cleaner output template
  - **references/popular-datasets.md**: Expanded with decision tree lookup table ("If user asks about X, use Y dataset")
    - Added more datasets: Employee Salaries, Divvy Stations, Lobbyist Data
    - Richer column documentation and common values
    - Better categorization (Public Safety, City Services, Business & Permits, Transportation, Government)
  - **references/soql-quick-ref.md**: Enhanced with more practical examples
    - Added common query patterns section (pagination, time series, aggregations)
    - Better date function examples with `date_trunc_ym` for grouping
    - Added `contains()` text function
  - **references/geospatial.md**: New reference file for location-based queries
    - Coordinate ordering warning (lat/lon vs lon/lat gotcha)
    - Common Chicago landmark coordinates
    - Examples combining spatial + other filters
  - **examples/typescript-query.ts**: New TypeScript/JavaScript example
    - Async/await with fetch API
    - Typed interfaces for query params and metadata
    - AsyncGenerator for pagination
  - **examples/python-query.py**: Expanded with more practical examples
    - Added `get_all_results()` helper for pagination
    - Time series example (monthly counts)
    - Food inspections analysis example
  - **examples/curl-examples.sh**: More organized with clear sections
    - Added filtering, aggregation, and geospatial sections
    - Dataset-specific examples for permits, licenses, crashes

### Added

- **Test Infrastructure**: Integration tests for skill API examples
  - `tests/` directory with pytest-based test suite
  - `test_chicago_data_portal.py`: 17 tests covering basic queries, metadata, filtering, aggregation, geospatial, pagination, and error handling
  - Tests marked with `@pytest.mark.live` for easy skip when offline
  - Shared fixtures in `conftest.py` for app tokens across skills
  - Documentation in `tests/README.md`

- **Plugin Marketplace Support**: Repository can now be added as a Claude Code plugin marketplace
  - `.claude-plugin/marketplace.json` manifest with all plugins listed
  - Individual `plugin.json` files for each skill
  - Installation via `/plugin marketplace add MisterClean/claude-plugins`
  - Install plugins with `/plugin install <plugin-name>@misterclean-plugins`

- Individual README.md files for each skill with installation instructions, triggers, usage examples, and file contents overview
  - `skills/chicago-data-portal/README.md`
  - `skills/cook-county-data-portal/README.md`
  - `skills/housing-copywriter/README.md`
  - `skills/us-census-data/README.md`

### Changed

- **chicago-data-portal** skill (v1.1.0): Added Prerequisites section with .env API key check
  - Checks for `CHICAGO_DATA_PORTAL_TOKEN` in user's .env file
  - Provides signup instructions if token not found
  - Clarifies that queries work without token but are rate-limited

- **cook-county-data-portal** skill (v1.1.0): Added Prerequisites section with .env API key check
  - Checks for `COOK_COUNTY_DATA_PORTAL_TOKEN` in user's .env file
  - Falls back to `CHICAGO_DATA_PORTAL_TOKEN` (both use Socrata, tokens are interchangeable)
  - Provides signup instructions if neither token found

- **us-census-data** skill (v1.1.0): Standardized Prerequisites section format
  - Moved API key setup to dedicated Prerequisites section for consistency
  - Checks for `CENSUS_API_KEY` in user's .env file
  - Clarifies that API works without key but is rate-limited

### Tested

- Verified all data portal skills with smoke tests:
  - **chicago-data-portal**: Crimes, 311 requests, building permits - all APIs working
  - **cook-county-data-portal**: Assessed values, Medical Examiner, payroll - all APIs working
  - **us-census-data**: ACS state population, county median income - all APIs working

## [1.0.3] - 2026-01-17

### Added

- **housing-copywriter** skill: Write authentic, human-sounding copy that avoids AI-generated patterns
  - SKILL.md with 5 core copywriting principles (specificity, cutting ruthlessly, conversational tone, showing vs announcing, earning adjectives)
  - Self-check framework to prevent AI-sounding output
  - Tone calibration guidance for different contexts (casual, professional, luxury, startup)
  - Pro-housing advocacy messaging framework (5-step housing structure, 3-step parking structure)
  - `references/avoid-list.md`: Comprehensive banned words, phrases, and patterns with alternatives (204 items)
  - `references/pro-housing-messaging.md`: Research-backed YIMBY messaging (Welcoming Neighbors Network, Sightline Institute, Parking Reform Network)
  - Terminology guide for housing advocacy (homes vs units, housing shortage vs crisis, etc.)
  - Top-performing message examples with statistical backing
  - Before/after examples for common copywriting scenarios
  - Specialized guidance for zoning reform, parking reform, and housing affordability communications

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

[1.0.3]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.3
[1.0.2]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.2
[1.0.1]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.1
[1.0.0]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.0
