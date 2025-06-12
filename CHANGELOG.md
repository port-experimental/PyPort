# Changelog

All notable changes to the PyPort project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2024-12-19

### Fixed
- **CRITICAL**: Fixed packaging issue causing `ModuleNotFoundError: No module named 'pyport.action_runs'` when installing via pip
- Replaced manual package listing with automatic package discovery in `pyproject.toml`
- All 26 PyPort service packages now properly included in distribution (was only 7 before)
- Import errors resolved for all service modules when using installed package

### Changed
- Updated `pyproject.toml` to use `setuptools.find_packages()` for automatic package discovery
- Improved package build configuration with proper exclusions for test and utility packages
- Enhanced package maintainability - new service packages will be automatically included

### Documentation
- Added comprehensive documentation for 8 missing service APIs (actions, action_runs, integrations, teams, users, webhooks, audit, scorecards)
- Fixed outdated pagination examples in service documentation
- Corrected method signatures in entities service documentation
- Updated utility function documentation to reflect API method usage

### Utilities
- Simplified `clear_blueprint` utility to use existing `delete_all_blueprint_entities` API method
- Improved performance by using bulk operations instead of individual entity deletions
- Updated tests to reflect simplified utility implementation

## [0.3.1] - 2024-12-19

### Added
- JWT token session management with automatic refresh
- New API endpoints for action runs, teams, users, webhooks, and other services
- Comprehensive test coverage improvements
- Documentation coverage increased to 97.5%

### Fixed
- Authentication token handling and session management
- Test failures across multiple service modules
- Linting issues in service files

## [0.2.8] - 2025-05-16

### Fixed
- Authentication URL bug that was duplicating the 'v1' path segment
- Improved error messages in test mocks for better debugging

### Changed
- Enhanced test mocks to provide more realistic responses
- Fixed snapshot utility to make saving entities optional (default: False)
- Removed snapshot functionality from unit testing
- Temporarily removed testing and linting from the release process

## [0.2.7] - 2025-05-15

### Added
- Visual progress bars for wait operations in the CICD utility
- Improved feedback during command execution
- Enhanced terminal output with descriptive messages
- API usage examples
- Jupyter notebooks
- Architecture diagrams
- Snapshot testing
- Dependency analysis
- Documentation coverage
