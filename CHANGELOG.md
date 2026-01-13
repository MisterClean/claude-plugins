# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/MisterClean/claude-plugins/releases/tag/v1.0.0
