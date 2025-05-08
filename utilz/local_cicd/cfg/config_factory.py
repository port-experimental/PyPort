"""
Configuration factory for local CI/CD utilities.

This module provides a factory for creating configuration managers with
different sources and validation.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from utilz.local_cicd.cfg.config_manager import ConfigManager
from utilz.local_cicd.cfg.config_schema import ConfigSchema, CICD_CONFIG_SCHEMA


class ConfigFactory:
    """
    Factory for creating configuration managers.
    
    Provides methods for creating configuration managers with different
    sources and validation.
    """
    
    @staticmethod
    def create_default_config(project_root: Optional[Path] = None) -> ConfigManager:
        """
        Create a configuration manager with default values.
        
        Args:
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
                          
        Returns:
            A configuration manager with default values.
        """
        return ConfigManager(project_root)
    
    @staticmethod
    def create_from_file(file_path: Union[str, Path], 
                         project_root: Optional[Path] = None) -> ConfigManager:
        """
        Create a configuration manager from a file.
        
        Args:
            file_path: Path to the configuration file.
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
                          
        Returns:
            A configuration manager with values from the file.
        """
        config = ConfigManager(project_root)
        config.load_from_file(file_path)
        return config
    
    @staticmethod
    def create_from_env(prefix: str = 'CICD_',
                       project_root: Optional[Path] = None) -> ConfigManager:
        """
        Create a configuration manager from environment variables.
        
        Args:
            prefix: Prefix for environment variables.
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
                          
        Returns:
            A configuration manager with values from environment variables.
        """
        config = ConfigManager(project_root)
        config.load_from_env(prefix)
        return config
    
    @staticmethod
    def create_from_args(args: Dict[str, Any],
                        project_root: Optional[Path] = None) -> ConfigManager:
        """
        Create a configuration manager from command-line arguments.
        
        Args:
            args: Dictionary of command-line arguments.
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
                          
        Returns:
            A configuration manager with values from command-line arguments.
        """
        config = ConfigManager(project_root)
        config.load_from_args(args)
        return config
    
    @staticmethod
    def create_with_all_sources(file_path: Optional[Union[str, Path]] = None,
                               env_prefix: str = 'CICD_',
                               args: Optional[Dict[str, Any]] = None,
                               project_root: Optional[Path] = None,
                               validate: bool = True) -> ConfigManager:
        """
        Create a configuration manager with all sources.
        
        Sources are loaded in order of priority:
        1. Default values (lowest priority)
        2. Configuration file
        3. Environment variables
        4. Command-line arguments (highest priority)
        
        Args:
            file_path: Path to the configuration file.
            env_prefix: Prefix for environment variables.
            args: Dictionary of command-line arguments.
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
            validate: Whether to validate the configuration against the schema.
                          
        Returns:
            A configuration manager with values from all sources.
            
        Raises:
            ConfigValidationError: If validation is enabled and fails.
        """
        config = ConfigManager(project_root)
        
        # Load from file if provided
        if file_path is not None:
            config.load_from_file(file_path)
        
        # Load from environment variables
        config.load_from_env(env_prefix)
        
        # Load from command-line arguments if provided
        if args is not None:
            config.load_from_args(args)
        
        # Validate configuration if enabled
        if validate:
            ConfigSchema.validate(config.as_dict(), CICD_CONFIG_SCHEMA)
        
        return config
    
    @staticmethod
    def find_config_file(project_root: Optional[Path] = None) -> Optional[Path]:
        """
        Find a configuration file in the project.
        
        Looks for configuration files in the following locations:
        1. pyproject.toml (with [tool.cicd] section)
        2. .cicd.json
        3. .cicd.toml
        4. cicd.json
        5. cicd.toml
        
        Args:
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
                          
        Returns:
            Path to the configuration file, or None if not found.
        """
        if project_root is None:
            project_root = ConfigManager()._detect_project_root()
        
        # Check for pyproject.toml with [tool.cicd] section
        pyproject_path = project_root / 'pyproject.toml'
        if pyproject_path.exists():
            try:
                import toml
                with open(pyproject_path, 'r') as f:
                    pyproject = toml.load(f)
                if 'tool' in pyproject and 'cicd' in pyproject['tool']:
                    return pyproject_path
            except (ImportError, Exception):
                pass
        
        # Check for other configuration files
        for filename in ['.cicd.json', '.cicd.toml', 'cicd.json', 'cicd.toml']:
            file_path = project_root / filename
            if file_path.exists():
                return file_path
        
        return None
