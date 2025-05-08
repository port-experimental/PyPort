"""
Configuration schema for local CI/CD utilities.

This module defines the schema for validating configuration values.
"""
from typing import Any, Dict, List, Optional, Union


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    pass


class ConfigSchema:
    """
    Schema for validating configuration values.
    
    Provides methods for validating configuration values against a schema.
    """
    
    @staticmethod
    def validate(config: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """
        Validate configuration against a schema.
        
        Args:
            config: Configuration dictionary to validate.
            schema: Schema dictionary to validate against.
            
        Raises:
            ConfigValidationError: If validation fails.
        """
        for key, schema_value in schema.items():
            if key not in config:
                if schema_value.get('required', False):
                    raise ConfigValidationError(f"Missing required configuration key: {key}")
                continue
            
            config_value = config[key]
            
            # Validate type
            expected_type = schema_value.get('type')
            if expected_type and not ConfigSchema._check_type(config_value, expected_type):
                raise ConfigValidationError(
                    f"Invalid type for {key}: expected {expected_type}, got {type(config_value).__name__}"
                )
            
            # Validate nested schema
            nested_schema = schema_value.get('schema')
            if nested_schema and isinstance(config_value, dict):
                ConfigSchema.validate(config_value, nested_schema)
            
            # Validate enum
            enum_values = schema_value.get('enum')
            if enum_values and config_value not in enum_values:
                raise ConfigValidationError(
                    f"Invalid value for {key}: expected one of {enum_values}, got {config_value}"
                )
            
            # Validate pattern
            pattern = schema_value.get('pattern')
            if pattern and isinstance(config_value, str):
                import re
                if not re.match(pattern, config_value):
                    raise ConfigValidationError(
                        f"Invalid value for {key}: does not match pattern {pattern}"
                    )
    
    @staticmethod
    def _check_type(value: Any, expected_type: Union[str, List[str]]) -> bool:
        """
        Check if a value matches the expected type.
        
        Args:
            value: Value to check.
            expected_type: Expected type or list of types.
            
        Returns:
            True if the value matches the expected type, False otherwise.
        """
        if isinstance(expected_type, list):
            return any(ConfigSchema._check_type(value, t) for t in expected_type)
        
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'number':
            return isinstance(value, (int, float))
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'object':
            return isinstance(value, dict)
        elif expected_type == 'null':
            return value is None
        else:
            return False


# Define the schema for the local CI/CD configuration
CICD_CONFIG_SCHEMA = {
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
            'tests_folder': {
                'type': 'string',
                'required': True,
            },
        },
    },
    'tools': {
        'type': 'object',
        'required': True,
        'schema': {
            'coverage': {
                'type': 'object',
                'required': True,
                'schema': {
                    'config_file': {
                        'type': 'string',
                        'required': True,
                    },
                    'data_file': {
                        'type': 'string',
                        'required': True,
                    },
                    'badge_pattern': {
                        'type': 'string',
                        'required': True,
                    },
                },
            },
            'maintainability': {
                'type': 'object',
                'required': True,
                'schema': {
                    'badge_pattern': {
                        'type': 'string',
                        'required': True,
                    },
                },
            },
            'security': {
                'type': 'object',
                'required': True,
                'schema': {
                    'badge_pattern': {
                        'type': 'string',
                        'required': True,
                    },
                },
            },
            'dependencies': {
                'type': 'object',
                'required': True,
                'schema': {
                    'badge_pattern': {
                        'type': 'string',
                        'required': True,
                    },
                },
            },
        },
    },
    'build': {
        'type': 'object',
        'required': True,
        'schema': {
            'pypi_config': {
                'type': 'string',
                'required': True,
            },
        },
    },
}
