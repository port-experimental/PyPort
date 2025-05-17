# PyPort API Usage Examples

This directory contains comprehensive examples demonstrating how to use the PyPort library for various API operations.

## Available Examples

1. **[01_basic_usage.py](01_basic_usage.py)**: Basic usage of the PyPort library
   - Initializing the client
   - Getting blueprints
   - Getting entities
   - Getting actions
   - Getting organization details

2. **[02_blueprint_management.py](02_blueprint_management.py)**: Blueprint management operations
   - Creating blueprints
   - Getting blueprints
   - Updating blueprints
   - Getting blueprint system structure
   - Deleting blueprints

3. **[03_entity_management.py](03_entity_management.py)**: Entity management operations
   - Creating entities
   - Getting entities
   - Updating entities
   - Searching for entities
   - Deleting entities

4. **[04_action_management.py](04_action_management.py)**: Action management operations
   - Creating actions
   - Getting actions
   - Updating actions
   - Running actions
   - Getting action runs
   - Deleting actions

5. **[05_error_handling_and_retry.py](05_error_handling_and_retry.py)**: Error handling and retry configuration
   - Basic error handling
   - Custom retry configuration
   - Creating RetryConfig objects
   - Handling different types of errors
   - Using try/except with specific error handling

6. **[06_advanced_search_and_filtering.py](06_advanced_search_and_filtering.py)**: Advanced search and filtering
   - Basic search by property value
   - Search with multiple criteria
   - Search with array contains
   - Search with logical operators
   - Search with complex queries
   - Text search

7. **[07_utility_functions.py](07_utility_functions.py)**: Utility functions
   - Saving snapshots
   - Listing snapshots
   - Clearing blueprints
   - Restoring snapshots
   - Deleting snapshots

## Running the Examples

To run any example, make sure you have set the required environment variables:

```bash
# Set your Port API credentials
export PORT_CLIENT_ID=your-client-id
export PORT_CLIENT_SECRET=your-client-secret
```

Then run the example script:

```bash
python examples/api_usage/01_basic_usage.py
```

## Notes

- These examples are designed to be run from the project root directory
- They automatically add the `src` directory to the Python path
- Most examples create test resources and clean them up afterward
- Be careful when running examples in a production environment, as they may modify your Port data
