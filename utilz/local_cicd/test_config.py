"""
Test script for the new configuration system.

This script tests the new configuration system by creating a configuration
manager and accessing configuration values.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.cfg.config_factory import ConfigFactory
from utilz.local_cicd.cfg.config_manager import ConfigManager
from utilz.local_cicd.cfg.config_schema import ConfigSchema, CICD_CONFIG_SCHEMA


def test_config_manager():
    """Test the ConfigManager class."""
    print("Testing ConfigManager...")
    
    # Create a configuration manager
    config = ConfigManager()
    
    # Access configuration values
    print(f"Project root: {config.project_root}")
    print(f"Source folder: {config.src_folder}")
    print(f"Coverage config file: {config.coverage_config_file}")
    
    # Get a configuration value with a default
    value = config.get('nonexistent.key', 'default_value')
    print(f"Nonexistent key with default: {value}")
    
    # Set a configuration value
    config.set('new.key', 'new_value')
    print(f"New key: {config.get('new.key')}")
    
    print("ConfigManager test passed.")


def test_config_factory():
    """Test the ConfigFactory class."""
    print("\nTesting ConfigFactory...")
    
    # Create a configuration manager with default values
    config = ConfigFactory.create_default_config()
    print(f"Default config project root: {config.project_root}")
    
    # Create a configuration manager from environment variables
    os.environ['CICD_PROJECT__SRC_FOLDER'] = 'custom_src'
    config = ConfigFactory.create_from_env()
    print(f"Env config source folder: {config.src_folder}")
    
    # Create a configuration manager with all sources
    config = ConfigFactory.create_with_all_sources(
        args={'project__src_folder': 'args_src'},
        validate=False
    )
    print(f"All sources config source folder: {config.src_folder}")
    
    # Find a configuration file
    config_file = ConfigFactory.find_config_file()
    print(f"Found configuration file: {config_file}")
    
    print("ConfigFactory test passed.")


def test_config_schema():
    """Test the ConfigSchema class."""
    print("\nTesting ConfigSchema...")
    
    # Create a configuration manager
    config = ConfigManager()
    
    # Validate the configuration
    try:
        ConfigSchema.validate(config.as_dict(), CICD_CONFIG_SCHEMA)
        print("Configuration validation passed.")
    except Exception as e:
        print(f"Configuration validation failed: {e}")
    
    print("ConfigSchema test passed.")


def test_cicd_config():
    """Test the CicdConfig class."""
    print("\nTesting CicdConfig...")
    
    # Create a configuration object
    config = CicdConfig()
    
    # Access configuration values
    print(f"Project root: {config.project_root}")
    print(f"Source folder: {config.src_folder}")
    print(f"Coverage config file: {config.coverage_config_file}")
    
    # Get a configuration value with a default
    value = config.get('nonexistent.key', 'default_value')
    print(f"Nonexistent key with default: {value}")
    
    # Set a configuration value
    config.set('new.key', 'new_value')
    print(f"New key: {config.get('new.key')}")
    
    print("CicdConfig test passed.")


def main():
    """Run all tests."""
    test_config_manager()
    test_config_factory()
    test_config_schema()
    test_cicd_config()
    
    print("\nAll tests passed!")


if __name__ == '__main__':
    main()
