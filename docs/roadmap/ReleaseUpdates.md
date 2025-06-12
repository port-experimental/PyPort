# PyPort Release Updates

This document tracks the changes and improvements made in each version of the PyPort client library.

## Version 0.3.2 (Latest) - 2024-12-19

### 🚨 Critical Packaging Fix
- ✅ **RESOLVED**: Fixed `ModuleNotFoundError: No module named 'pyport.action_runs'` when installing via pip
- ✅ **ROOT CAUSE**: Only 7 out of 26 packages were being included in the distribution due to incomplete `pyproject.toml` configuration
- ✅ **SOLUTION**: Replaced manual package listing with automatic package discovery using `setuptools.find_packages()`
- ✅ **IMPACT**: All 26 PyPort service packages now properly included in pip installations

### Package Distribution Improvements
- ✅ Updated `pyproject.toml` to use automatic package discovery
- ✅ Proper exclusion of test and utility packages from distribution
- ✅ Future-proof configuration - new service packages automatically included
- ✅ Verified wheel contents include all required modules

### Documentation Enhancements
- ✅ **NEW**: Complete documentation for 8 missing service APIs:
  - ✅ Actions service (`docs/api_reference/services/actions.md`)
  - ✅ Action Runs service (`docs/api_reference/services/action_runs.md`)
  - ✅ Integrations service (`docs/api_reference/services/integrations.md`)
  - ✅ Teams service (`docs/api_reference/services/teams.md`)
  - ✅ Users service (`docs/api_reference/services/users.md`)
  - ✅ Webhooks service (`docs/api_reference/services/webhooks.md`)
  - ✅ Audit service (`docs/api_reference/services/audit.md`)
  - ✅ Scorecards service (`docs/api_reference/services/scorecards.md`)
- ✅ **FIXED**: Corrected outdated pagination examples in service documentation
- ✅ **FIXED**: Updated method signatures in entities service documentation
- ✅ **ENHANCED**: Added comprehensive examples, error handling, and best practices

### Utility Function Improvements
- ✅ **SIMPLIFIED**: `clear_blueprint` utility now uses existing `delete_all_blueprint_entities` API method
- ✅ **PERFORMANCE**: Replaced individual entity deletions with bulk API operation
- ✅ **RELIABILITY**: Leverages official Port API endpoint instead of custom implementation
- ✅ **MAINTAINABILITY**: Reduced code complexity and improved error handling

### Testing and Quality
- ✅ Updated tests to reflect simplified utility implementations
- ✅ Verified import functionality after packaging fix
- ✅ Enhanced test coverage for packaging scenarios
- ✅ Documentation coverage increased to 97.5%

### Build and Release Process
- ✅ Improved package build configuration with automatic discovery
- ✅ Enhanced wheel verification process
- ✅ Added comprehensive packaging fix documentation
- ✅ **FIXED**: Updated license configuration to modern SPDX format (`license = "MIT"`)
- ✅ **FIXED**: Removed deprecated license classifier to eliminate build warnings
- ✅ **ENHANCED**: Clean build process with no deprecation warnings

## Version 0.3.1 - 2024-12-19

### 🆕 New API Services and Endpoints
- ✅ **Action Runs service** - Complete action execution lifecycle management
- ✅ **Teams service** - Team management and permissions
- ✅ **Users service** - User management and invitations
- ✅ **Webhooks service** - Event notifications and webhook management
- ✅ **Audit service** - Activity logging and compliance tracking
- ✅ **Scorecards service** - Quality and compliance measurement
- ✅ **Integrations service** - External system connections
- ✅ **Apps service** - Custom application management
- ✅ **Migrations service** - Data migration operations

### 🔧 Enhanced Blueprint Operations
- ✅ **NEW**: `get_blueprint_entities()` - Retrieve all entities for a specific blueprint
- ✅ **NEW**: `delete_all_blueprint_entities()` - Bulk delete all entities in a blueprint
- ✅ **NEW**: Blueprint permissions management (`get_blueprint_permissions`, `update_blueprint_permissions`)
- ✅ **NEW**: Blueprint system structure operations
- ✅ **ENHANCED**: Pagination support for `get_blueprints()` with `page` and `per_page` parameters

### 📊 Enhanced Entity Operations
- ✅ **NEW**: `create_entities_bulk()` - Bulk entity creation for improved performance
- ✅ **NEW**: `get_all_entities()` - Retrieve all entities including related entities
- ✅ **NEW**: `search_blueprint_entities()` - Advanced entity search within blueprints
- ✅ **ENHANCED**: Pagination support for `get_entities()` with `page` and `per_page` parameters
- ✅ **ENHANCED**: Advanced filtering options (include/exclude fields, calculated properties)

### 🔍 Search and Filtering Capabilities
- ✅ **NEW**: Entity search with query, filter, and sort parameters
- ✅ **NEW**: Blueprint-specific entity search
- ✅ **NEW**: Field inclusion/exclusion for optimized responses
- ✅ **NEW**: Calculated properties control
- ✅ **NEW**: Compact response format options

### 🛠 Service Method Implementations
- ✅ **Action Runs**: Lifecycle management (get, update, approve, logs, approvers)
- ✅ **Teams**: Membership and permission management
- ✅ **Users**: Invitation and role management with email-based identification
- ✅ **Webhooks**: Creation, configuration, and event handling
- ✅ **Audit**: Log retrieval with filtering and pagination
- ✅ **Scorecards**: Creation, rule management, and blueprint-specific operations
- ✅ **Integrations**: Configuration, synchronization, and resync operations

### 📋 Pagination and Performance
- ✅ **NEW**: Standardized pagination support across services
- ✅ **NEW**: `page` and `per_page` parameters for list operations
- ✅ **NEW**: Bulk operations for improved performance
- ✅ **NEW**: Optimized response formats with field selection

### 🧪 Testing and Quality Improvements
- ✅ Fixed test failures across all service modules
- ✅ Comprehensive test coverage for new services and methods
- ✅ Enhanced mock testing capabilities with proper API response simulation
- ✅ Updated test assertions to match actual API implementations
- ✅ Added integration tests for new functionality

### 📝 Code Quality and Standards
- ✅ Fixed linting issues across all service files
- ✅ Improved code formatting and consistency
- ✅ Enhanced error handling patterns with specific exception types
- ✅ Standardized method signatures and parameter handling
- ✅ Comprehensive docstring documentation for all new methods

### 🔧 Advanced Client Features
- ✅ **NEW**: Comprehensive retry logic with exponential backoff
- ✅ **NEW**: Circuit breaker pattern for API resilience
- ✅ **NEW**: Configurable retry strategies (`exponential`, `linear`, `fixed`)
- ✅ **NEW**: Retry jitter for distributed system stability
- ✅ **NEW**: Custom retry status codes and exception handling
- ✅ **NEW**: Request correlation IDs for debugging and tracing

### 🛠 Utility Functions and Helpers
- ✅ **NEW**: `clear_blueprint()` utility for bulk entity deletion
- ✅ **NEW**: Snapshot utilities (`save_snapshot`, `restore_snapshot`, `list_snapshots`)
- ✅ **NEW**: Blueprint backup and restore capabilities
- ✅ **NEW**: Data migration helpers
- ✅ **ENHANCED**: Utility functions now use official API endpoints for better performance

### 🔐 Error Handling and Resilience
- ✅ **NEW**: Comprehensive exception hierarchy with specific error types
- ✅ **NEW**: `PortAuthError`, `PortResourceNotFoundError`, `PortValidationError`
- ✅ **NEW**: `PortServerError`, `PortNetworkError`, `PortTimeoutError`
- ✅ **NEW**: Detailed error information with correlation IDs
- ✅ **NEW**: Automatic error logging and debugging support
- ✅ **NEW**: Custom error handling patterns and examples

## Version 0.3.0 - 2024-12-19

### 🔐 Authentication and Session Management
- ✅ **MAJOR**: JWT token session management with automatic refresh
- ✅ **FIXED**: Authentication token handling bug that was causing session failures
- ✅ Enhanced session management reliability and error recovery
- ✅ Improved token lifecycle management with proper expiration handling
- ✅ Added automatic token refresh before expiration (configurable interval)
- ✅ Enhanced authentication error handling and retry logic
- ✅ **NEW**: `auto_refresh` and `refresh_interval` configuration options
- ✅ **NEW**: `skip_auth` option for testing environments

## Version 0.2.8

### Bug Fixes
- ✅ Fixed authentication URL bug that was duplicating the 'v1' path segment
- ✅ Improved error messages in test mocks for better debugging

### Testing Improvements
- ✅ Enhanced test mocks to provide more realistic responses
- ✅ Fixed snapshot utility to make saving entities optional (default: False)
- ✅ Removed snapshot functionality from unit testing
- ✅ Added real integration testing with environment-based credentials
- ✅ Created simple client for testing specific PyPort versions

### Build Process
- ✅ Temporarily removed testing and linting from the release process

### Documentation
- ✅ Added integration testing documentation

## Version 0.2.7

### Documentation Improvements
- ✅ API usage examples
- ✅ Jupyter notebooks
- ✅ Architecture diagrams

### Testing Enhancements
- ✅ Snapshot testing

### Code Quality
- ✅ Dependency analysis
- ✅ Documentation coverage

## Version 0.2.6

### IDE Support Improvements
- ✅ Added property decorators with explicit return types for all service attributes
- ✅ Added type annotations in `__init__` with proper types
- ✅ Enhanced docstrings with detailed information about each service
- ✅ Created type stub files (.pyi) for key modules:
  - ✅ Client module (PortClient class)
  - ✅ Blueprints module
  - ✅ Entities module
  - ✅ BaseAPIService class
  - ✅ Types module
- ✅ Added dedicated IDE support documentation
- ✅ Updated README with IDE support information

### Testing Improvements
- ✅ Increased test coverage for BaseAPIService class
- ✅ Added tests for client properties and type annotations
- ✅ Added tests for type stubs
- ✅ Implemented mock server for API testing
- ✅ Enhanced integration tests for real-world scenarios
- ✅ Added edge case tests for error conditions
- ✅ Implemented property-based testing framework

### Documentation Enhancements
- ✅ Created comprehensive API reference documentation
- ✅ Added more usage examples for common operations
- ✅ Created step-by-step tutorials for complex operations
- ✅ Improved inline documentation and docstrings
- ✅ Added architecture documentation for contributors

## Version 0.2.4

### API Enhancements
- Added API wrapper functions for common operations
- Implemented clear_blueprint functionality
- Added save_snapshot capability
- Fixed GitHub Actions workflow

### Bug Fixes
- Fixed import error when used in external projects
- Improved error handling for API responses
- Enhanced retry logic for transient errors

## Version 0.2.1 - 0.2.3

### Testing Improvements
- ✅ Implemented comprehensive test suite
- ✅ Added unit and integration tests
- ✅ Created mock client for testing
- ✅ Added test fixtures and utilities

### Retry Logic Enhancements
- ✅ Implemented exponential backoff with jitter
- ✅ Added configurable retry settings
- ✅ Improved handling of transient errors

## Version 0.2.0

### Error Handling
- ✅ Added custom exception classes for different error types
- ✅ Implemented centralized error handling mechanism
- ✅ Enhanced error messages with context

### Type Hints and Documentation
- ✅ Added specific type definitions for API responses
- ✅ Improved docstrings with examples
- ✅ Enhanced parameter and return value documentation

### Logging
- ✅ Implemented structured logging with correlation IDs
- ✅ Added sensitive data masking
- ✅ Added configurable log levels and formats

## Version 0.2.5

### Code Structure and Organization
- ✅ Created a BaseAPIService class with common functionality for all API services
- ✅ Extracted common patterns from existing API service classes
- ✅ Standardized method signatures across all API services
- ✅ Improved type hints for complex data structures and API responses
- ✅ Reduced code duplication in API service classes
- ✅ Ensured consistent parameter naming across all methods

### Error Handling and Logging
- ✅ Consolidated error handling approaches across all API services
- ✅ Enhanced logging with more context about API requests and responses
- ✅ Optimized retry logic for better handling of transient errors
- ✅ Improved error messages to be more actionable for users
- ✅ Added more detailed logging for debugging purposes
- ✅ Ensured consistent error handling patterns across the codebase

### Code Quality
- ✅ Fixed all linting issues across the codebase
- ✅ Improved code formatting and consistency
- ✅ Enhanced docstrings with better descriptions and examples

## Upcoming Features

### Version 0.2.9 (In Progress)
- Performance Optimizations
  - Connection pooling for better performance
  - Caching for frequently accessed resources
  - Request batching for improved efficiency
  - Optimized sensitive data masking
  - More efficient JSON parsing

### Future Versions
- Feature Enhancements
  - Context manager support for the client (with statement)
  - Resource pooling for efficient client usage
  - Batch operations for bulk API calls
  - Automatic request throttling to prevent rate limiting
  - Support for custom serializers/deserializers

- Developer Experience
  - Pre-commit hooks
  - VS Code devcontainer
  - Makefile for common tasks
  - CLI tool for CICD

- Testing Enhancements
  - Fuzzing tests
  - Performance benchmarks

- Packaging Improvements
  - Conditional dependencies
  - Type stub package
  - Binary wheels

- Monitoring and Telemetry
  - Usage statistics
  - Enhanced error reporting
  - Performance metrics

- Code Quality
  - Code complexity metrics

- Compatibility and Interoperability
  - Compatibility layer for API version differences

- User Experience
  - Progress bars
  - Interactive CLI
  - Configuration wizard

- Build and Release Process
  - Semantic release
  - Changelog generation
  - Release notes

- Performance Optimizations
  - Connection pooling for better performance
  - Caching for frequently accessed resources
  - Request batching for improved efficiency
  - Optimized sensitive data masking
  - More efficient JSON parsing

### Long-term Roadmap
- Configuration Management (environment variables, config files, etc.)
- API Versioning Support (version parameter, adapters for different versions)
- Async Support (AsyncPortClient, async methods, etc.)
- CLI Tool for common operations
- Framework Integrations (FastAPI, Django, etc.)
