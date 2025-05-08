"""
Logging service for local CI/CD utilities.

This module provides a flexible logging system with support for different
log levels, formats, and outputs.
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Define log levels
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_LEVEL_INFO = logging.INFO
LOG_LEVEL_WARNING = logging.WARNING
LOG_LEVEL_ERROR = logging.ERROR
LOG_LEVEL_CRITICAL = logging.CRITICAL

# Define log formats
LOG_FORMAT_SIMPLE = '%(levelname)s - %(message)s'
LOG_FORMAT_STANDARD = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT_DETAILED = '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
LOG_FORMAT_JSON = '{"timestamp": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'

# Define log outputs
LOG_OUTPUT_CONSOLE = 'console'
LOG_OUTPUT_FILE = 'file'
LOG_OUTPUT_BOTH = 'both'


class LoggingService:
    """
    Logging service for local CI/CD utilities.
    
    Provides methods for configuring and using a logger with different
    levels, formats, and outputs.
    """
    
    def __init__(self, name: str = 'cicd',
                level: int = LOG_LEVEL_INFO,
                format_str: str = LOG_FORMAT_STANDARD,
                output: str = LOG_OUTPUT_CONSOLE,
                log_file: Optional[Union[str, Path]] = None):
        """
        Initialize the logging service.
        
        Args:
            name: Name of the logger.
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            format_str: Log format string.
            output: Log output (console, file, both).
            log_file: Path to the log file (required if output is file or both).
        """
        self.name = name
        self.level = level
        self.format_str = format_str
        self.output = output
        self.log_file = log_file
        
        # Create the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(format_str)
        
        # Create handlers
        if output in [LOG_OUTPUT_CONSOLE, LOG_OUTPUT_BOTH]:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        if output in [LOG_OUTPUT_FILE, LOG_OUTPUT_BOTH]:
            if log_file is None:
                raise ValueError("Log file path is required for file output.")
            
            # Create the directory if it doesn't exist
            log_file_path = Path(log_file)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """
        Log a debug message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """
        Log an info message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """
        Log a warning message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """
        Log an error message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Log a critical message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        """
        Log an exception message.
        
        Args:
            message: Message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.logger.exception(message, *args, **kwargs)
    
    def set_level(self, level: int) -> None:
        """
        Set the log level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        self.level = level
        self.logger.setLevel(level)
    
    def add_file_handler(self, log_file: Union[str, Path],
                        level: Optional[int] = None,
                        format_str: Optional[str] = None) -> None:
        """
        Add a file handler to the logger.
        
        Args:
            log_file: Path to the log file.
            level: Log level for the handler (defaults to the logger's level).
            format_str: Log format string for the handler (defaults to the logger's format).
        """
        # Create the directory if it doesn't exist
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create formatter
        formatter = logging.Formatter(format_str or self.format_str)
        
        # Create handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        
        if level is not None:
            file_handler.setLevel(level)
        
        self.logger.addHandler(file_handler)
    
    def add_console_handler(self, level: Optional[int] = None,
                           format_str: Optional[str] = None) -> None:
        """
        Add a console handler to the logger.
        
        Args:
            level: Log level for the handler (defaults to the logger's level).
            format_str: Log format string for the handler (defaults to the logger's format).
        """
        # Create formatter
        formatter = logging.Formatter(format_str or self.format_str)
        
        # Create handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        if level is not None:
            console_handler.setLevel(level)
        
        self.logger.addHandler(console_handler)


# Create a default logger
default_logger = LoggingService(
    name='cicd',
    level=LOG_LEVEL_INFO,
    format_str=LOG_FORMAT_STANDARD,
    output=LOG_OUTPUT_CONSOLE
)


def get_logger(name: str = 'cicd') -> LoggingService:
    """
    Get a logger with the specified name.
    
    If a logger with the specified name already exists, it will be returned.
    Otherwise, a new logger will be created.
    
    Args:
        name: Name of the logger.
        
    Returns:
        A logging service instance.
    """
    if name == 'cicd':
        return default_logger
    
    return LoggingService(name=name)


def configure_logging(config: Dict[str, Any]) -> None:
    """
    Configure logging based on the provided configuration.
    
    Args:
        config: Configuration dictionary with the following keys:
            - level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            - format: Log format string.
            - output: Log output (console, file, both).
            - log_file: Path to the log file (required if output is file or both).
    """
    global default_logger
    
    level = config.get('level', LOG_LEVEL_INFO)
    format_str = config.get('format', LOG_FORMAT_STANDARD)
    output = config.get('output', LOG_OUTPUT_CONSOLE)
    log_file = config.get('log_file')
    
    default_logger = LoggingService(
        name='cicd',
        level=level,
        format_str=format_str,
        output=output,
        log_file=log_file
    )


def get_log_file_path(config_folder: Union[str, Path], prefix: str = 'cicd') -> Path:
    """
    Get a log file path with a timestamp.
    
    Args:
        config_folder: Path to the configuration folder.
        prefix: Prefix for the log file name.
        
    Returns:
        Path to the log file.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"{prefix}_{timestamp}.log"
    return Path(config_folder) / 'logs' / log_file
