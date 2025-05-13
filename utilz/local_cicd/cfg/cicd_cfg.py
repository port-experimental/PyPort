import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

from utilz.local_cicd.cfg.config_factory import ConfigFactory
from utilz.local_cicd.cfg.config_manager import ConfigManager


class CicdConfig(object):
    """
    Configuration for local CI/CD utilities.

    This class provides a backward-compatible interface to the new configuration system.
    It delegates to a ConfigManager instance for most operations.
    """

    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize the configuration.

        Args:
            config_file: Path to the configuration file. If None, it will be
                         automatically detected.
        """
        # Find the configuration file if not provided
        if config_file is None:
            config_file = ConfigFactory.find_config_file()

        # Create a configuration manager with all sources
        self._config = ConfigFactory.create_with_all_sources(
            file_path=config_file,
            env_prefix='CICD_',
            args=self._parse_args(),
            validate=False  # Skip validation for backward compatibility
        )

        # For backward compatibility, set attributes directly
        self._dir_depth = 3
        self.project_root = self._config.project_root
        self.src_folder = self._config.src_folder
        self.config_folder = Path(__file__).resolve().parent
        self.coverage_config_file = self._config.coverage_config_file
        self.coverage_data_file = self._config.coverage_data_file
        self.qchecks_config_file = self.config_folder / 'quality_checks.ini'
        self.coverage_badge_pattern = self._config.coverage_badge_pattern
        self.maintainability_badge_pattern = self._config.maintainability_badge_pattern
        self.security_badge_pattern = self._config.security_badge_pattern
        self.dependencies_badge_pattern = self._config.dependencies_badge_pattern
        self.doc_coverage_badge_pattern = self._config.doc_coverage_badge_pattern
        self.pypi_repo_config_file = self._config.pypi_config_file
        self.min_doc_coverage = self._config.get('project.min_doc_coverage', 80.0)

    def _parse_args(self) -> Dict[str, Any]:
        """
        Parse command-line arguments.

        Returns:
            Dictionary of command-line arguments.
        """
        # Simple argument parsing for backward compatibility
        args = {}
        for i, arg in enumerate(sys.argv[1:]):
            if arg.startswith('--'):
                key = arg[2:]
                if i + 1 < len(sys.argv[1:]) and not sys.argv[i + 2].startswith('--'):
                    args[key] = sys.argv[i + 2]
                else:
                    args[key] = True
        return args

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Dot-separated path to the configuration value.
            default: Default value to return if the key is not found.

        Returns:
            The configuration value, or the default if not found.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Dot-separated path to the configuration value.
            value: Value to set.
        """
        self._config.set(key, value)

        # Update attributes for backward compatibility
        if key == 'project.root':
            self.project_root = Path(value)
        elif key == 'project.src_folder':
            self.src_folder = Path(value)
        elif key == 'tools.coverage.config_file':
            self.coverage_config_file = Path(value)
        elif key == 'tools.coverage.data_file':
            self.coverage_data_file = Path(value)
        elif key == 'tools.coverage.badge_pattern':
            self.coverage_badge_pattern = value
        elif key == 'tools.maintainability.badge_pattern':
            self.maintainability_badge_pattern = value
        elif key == 'tools.security.badge_pattern':
            self.security_badge_pattern = value
        elif key == 'tools.dependencies.badge_pattern':
            self.dependencies_badge_pattern = value
        elif key == 'build.pypi_config':
            self.pypi_repo_config_file = Path(value)

    def as_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.

        Returns:
            A copy of the configuration dictionary.
        """
        return self._config.as_dict()
