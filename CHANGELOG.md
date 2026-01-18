# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
