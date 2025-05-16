# Changelog

All notable changes to the PyPort project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
