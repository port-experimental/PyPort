# Configuration System for Local CI/CD

This module provides a flexible configuration system for the local CI/CD utilities.

## Features

- **Multiple Configuration Sources**: Load configuration from files, environment variables, and command-line arguments.
- **Configuration Validation**: Validate configuration against a schema.
- **Backward Compatibility**: Maintain compatibility with the existing `CicdConfig` class.
- **Flexible API**: Simple API for getting and setting configuration values.

## Usage

### Basic Usage

```python
from utilz.local_cicd.cfg.cicd_cfg import CicdConfig

# Create a configuration object
config = CicdConfig()

# Access configuration values
project_root = config.project_root
src_folder = config.src_folder

# Get a configuration value with a default
value = config.get('some.key', 'default_value')

# Set a configuration value
config.set('some.key', 'new_value')
```

### Advanced Usage

```python
from utilz.local_cicd.cfg.config_factory import ConfigFactory

# Create a configuration manager with all sources
config = ConfigFactory.create_with_all_sources(
    file_path='.cicd.json',
    env_prefix='CICD_',
    args={'project__src_folder': 'src'},
    validate=True
)

# Access configuration values
project_root = config.project_root
src_folder = config.src_folder

# Get a configuration value with a default
value = config.get('some.key', 'default_value')

# Set a configuration value
config.set('some.key', 'new_value')

# Get the entire configuration as a dictionary
config_dict = config.as_dict()
```

## Configuration Sources

Configuration values are loaded from multiple sources in order of priority:

1. **Default Values** (lowest priority): Hardcoded default values.
2. **Configuration File**: Values from a JSON or TOML configuration file.
3. **Environment Variables**: Values from environment variables with a specified prefix.
4. **Command-Line Arguments** (highest priority): Values from command-line arguments.

### Configuration File

The configuration file can be in JSON or TOML format. The system looks for configuration files in the following locations:

1. `pyproject.toml` (with `[tool.cicd]` section)
2. `.cicd.json`
3. `.cicd.toml`
4. `cicd.json`
5. `cicd.toml`

Example `.cicd.json`:

```json
{
  "project": {
    "root": ".",
    "src_folder": "src",
    "tests_folder": "tests"
  },
  "tools": {
    "coverage": {
      "config_file": "utilz/local_cicd/cfg/.coveragerc",
      "data_file": ".coverage",
      "badge_pattern": "!\\[Coverage\\]\\(.*\\)"
    }
  }
}
```

### Environment Variables

Environment variables should be prefixed with the specified prefix (default: `CICD_`) and use double underscores to indicate nesting.

Example:

```
CICD_PROJECT__SRC_FOLDER=/path/to/src
CICD_TOOLS__COVERAGE__CONFIG_FILE=/path/to/coveragerc
```

### Command-Line Arguments

Command-line arguments should use double underscores to indicate nesting.

Example:

```
--project__src_folder /path/to/src
--tools__coverage__config_file /path/to/coveragerc
```

## Configuration Schema

The configuration schema is defined in `config_schema.py`. It specifies the expected structure and types of configuration values.

Example schema:

```python
{
    'project': {
        'type': 'object',
        'required': True,
        'schema': {
            'root': {
                'type': 'string',
                'required': True,
            },
            'src_folder': {
                'type': 'string',
                'required': True,
            },
        },
    },
}
```

## Backward Compatibility

The `CicdConfig` class provides a backward-compatible interface to the new configuration system. It delegates to a `ConfigManager` instance for most operations, but also sets attributes directly for backward compatibility.

```python
# Old code
config = CicdConfig()
root = config.project_root

# New code (still works)
config = CicdConfig()
root = config.project_root

# New code (preferred)
config = CicdConfig()
root = config.get('project.root')
```
