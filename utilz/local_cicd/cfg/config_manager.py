"""
Configuration management for local CI/CD utilities.

This module provides a flexible configuration system that supports multiple
sources (environment variables, config files, CLI arguments) and validation.
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union


class ConfigManager:
    """
    Manages configuration for local CI/CD utilities.
    
    Supports loading configuration from multiple sources with priority:
    1. CLI arguments (highest priority)
    2. Environment variables
    3. Config files
    4. Default values (lowest priority)
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            project_root: The root directory of the project. If None, it will be
                          automatically detected.
        """
        self._config: Dict[str, Any] = {}
        self._project_root = project_root or self._detect_project_root()
        self._load_defaults()
    
    def _detect_project_root(self) -> Path:
        """
        Detect the project root directory.
        
        The project root is determined by looking for common project files
        (like pyproject.toml, setup.py, etc.) in parent directories.
        
        Returns:
            The detected project root directory.
        """
        current_dir = Path(__file__).resolve().parent
        
        # Go up to 5 levels to find the project root
        for _ in range(5):
            current_dir = current_dir.parent
            
            # Check for common project files
            if any((current_dir / marker).exists() for marker in 
                   ['pyproject.toml', 'setup.py', '.git', 'README.md']):
                return current_dir
        
        # If no project root is found, use the parent directory of the config module
        return Path(__file__).resolve().parents[2]
    
    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            'project': {
                'root': str(self._project_root),
                'src_folder': str(self._project_root / 'src'),
                'tests_folder': str(self._project_root / 'tests'),
            },
            'tools': {
                'coverage': {
                    'config_file': str(Path(__file__).parent / '.coveragerc'),
                    'data_file': str(self._project_root / '.coverage'),
                    'badge_pattern': r'!\[Coverage\]\(.*\)',
                },
                'maintainability': {
                    'badge_pattern': r'!\[Maintainability\]\(.*\)',
                },
                'security': {
                    'badge_pattern': r'!\[Security\]\(.*\)',
                },
                'dependencies': {
                    'badge_pattern': r'!\[Dependencies\]\(.*\)',
                },
            },
            'build': {
                'pypi_config': str(Path(__file__).parent / '.pypirc'),
            }
        }
    
    def load_from_file(self, file_path: Union[str, Path]) -> None:
        """
        Load configuration from a file.
        
        Args:
            file_path: Path to the configuration file (JSON or TOML).
        """
        file_path = Path(file_path)
        if not file_path.exists():
            return
        
        if file_path.suffix.lower() == '.json':
            with open(file_path, 'r') as f:
                file_config = json.load(f)
        elif file_path.suffix.lower() == '.toml':
            try:
                import toml
                with open(file_path, 'r') as f:
                    file_config = toml.load(f)
            except ImportError:
                print("TOML support requires the 'toml' package. Please install it.")
                return
        else:
            print(f"Unsupported configuration file format: {file_path.suffix}")
            return
        
        # Update configuration with values from file
        self._update_config(file_config)
    
    def load_from_env(self, prefix: str = 'CICD_') -> None:
        """
        Load configuration from environment variables.
        
        Environment variables should be prefixed with the specified prefix
        and use double underscores to indicate nesting.
        
        Example:
            CICD_PROJECT__SRC_FOLDER=/path/to/src
            
        Args:
            prefix: Prefix for environment variables.
        """
        env_config = {}
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Remove prefix and split by double underscore
                key_parts = key[len(prefix):].lower().split('__')
                
                # Build nested dictionary
                current = env_config
                for part in key_parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Set the value
                current[key_parts[-1]] = value
        
        # Update configuration with values from environment
        self._update_config(env_config)
    
    def load_from_args(self, args: Dict[str, Any]) -> None:
        """
        Load configuration from command-line arguments.
        
        Args:
            args: Dictionary of command-line arguments.
        """
        # Convert flat arguments to nested dictionary
        args_config = {}
        
        for key, value in args.items():
            if value is None:
                continue
                
            # Split by double underscore to indicate nesting
            key_parts = key.lower().split('__')
            
            # Build nested dictionary
            current = args_config
            for part in key_parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Set the value
            current[key_parts[-1]] = value
        
        # Update configuration with values from arguments
        self._update_config(args_config)
    
    def _update_config(self, new_config: Dict[str, Any], target: Optional[Dict[str, Any]] = None, 
                      path: Optional[str] = None) -> None:
        """
        Recursively update configuration dictionary.
        
        Args:
            new_config: New configuration values.
            target: Target dictionary to update (defaults to self._config).
            path: Current path in the configuration (for error reporting).
        """
        if target is None:
            target = self._config
        
        if path is None:
            path = ''
        
        for key, value in new_config.items():
            current_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                # Recursively update nested dictionaries
                self._update_config(value, target[key], current_path)
            else:
                # Update or add the value
                target[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Dot-separated path to the configuration value.
            default: Default value to return if the key is not found.
            
        Returns:
            The configuration value, or the default if not found.
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Dot-separated path to the configuration value.
            value: Value to set.
        """
        keys = key.split('.')
        target = self._config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            elif not isinstance(target[k], dict):
                target[k] = {}
            
            target = target[k]
        
        # Set the value
        target[keys[-1]] = value
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            A copy of the configuration dictionary.
        """
        return self._config.copy()
    
    @property
    def project_root(self) -> Path:
        """Get the project root directory."""
        return Path(self.get('project.root'))
    
    @property
    def src_folder(self) -> Path:
        """Get the source folder."""
        return Path(self.get('project.src_folder'))
    
    @property
    def tests_folder(self) -> Path:
        """Get the tests folder."""
        return Path(self.get('project.tests_folder'))
    
    @property
    def coverage_config_file(self) -> Path:
        """Get the coverage configuration file."""
        return Path(self.get('tools.coverage.config_file'))
    
    @property
    def coverage_data_file(self) -> Path:
        """Get the coverage data file."""
        return Path(self.get('tools.coverage.data_file'))
    
    @property
    def coverage_badge_pattern(self) -> str:
        """Get the coverage badge pattern."""
        return self.get('tools.coverage.badge_pattern')
    
    @property
    def maintainability_badge_pattern(self) -> str:
        """Get the maintainability badge pattern."""
        return self.get('tools.maintainability.badge_pattern')
    
    @property
    def security_badge_pattern(self) -> str:
        """Get the security badge pattern."""
        return self.get('tools.security.badge_pattern')
    
    @property
    def dependencies_badge_pattern(self) -> str:
        """Get the dependencies badge pattern."""
        return self.get('tools.dependencies.badge_pattern')
    
    @property
    def pypi_config_file(self) -> Path:
        """Get the PyPI configuration file."""
        return Path(self.get('build.pypi_config'))
