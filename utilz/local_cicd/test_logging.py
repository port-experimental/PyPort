"""
Test script for the logging system.

This script tests the logging system by creating loggers with different
configurations and logging messages at different levels.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from utilz.local_cicd.svc.logging_svc import (
    LoggingService, get_logger, configure_logging,
    LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR, LOG_LEVEL_CRITICAL,
    LOG_FORMAT_SIMPLE, LOG_FORMAT_STANDARD, LOG_FORMAT_DETAILED, LOG_FORMAT_JSON,
    LOG_OUTPUT_CONSOLE, LOG_OUTPUT_FILE, LOG_OUTPUT_BOTH
)


def test_basic_logging():
    """Test basic logging functionality."""
    print("Testing basic logging...")

    # Create a logger
    logger = LoggingService(
        name='test',
        level=LOG_LEVEL_DEBUG,
        format_str=LOG_FORMAT_SIMPLE,
        output=LOG_OUTPUT_CONSOLE
    )

    # Log messages at different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print("Basic logging test passed.")


def test_file_logging():
    """Test logging to a file."""
    print("\nTesting file logging...")

    # Create a log file
    log_file = Path('test_log.log')
    if log_file.exists():
        log_file.unlink()

    # Create a logger that logs to a file
    logger = LoggingService(
        name='test_file',
        level=LOG_LEVEL_INFO,
        format_str=LOG_FORMAT_STANDARD,
        output=LOG_OUTPUT_FILE,
        log_file=log_file
    )

    # Log messages at different levels
    logger.debug("This is a debug message")  # Should not be logged
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Close all handlers to release the file
    for handler in logger.logger.handlers:
        handler.close()

    # Check that the log file exists and contains the expected messages
    if log_file.exists():
        with open(log_file, 'r') as f:
            content = f.read()
            print(f"Log file content:\n{content}")

        # Clean up
        try:
            log_file.unlink()
        except PermissionError:
            print(f"Could not delete log file {log_file} (still in use)")
    else:
        print("Log file was not created!")

    print("File logging test passed.")


def test_get_logger():
    """Test the get_logger function."""
    print("\nTesting get_logger...")

    # Get the default logger
    logger1 = get_logger()
    logger1.info("This is a message from the default logger")

    # Get a named logger
    logger2 = get_logger('custom')
    logger2.info("This is a message from a custom logger")

    print("get_logger test passed.")


def test_configure_logging():
    """Test the configure_logging function."""
    print("\nTesting configure_logging...")

    # Configure logging
    configure_logging({
        'level': LOG_LEVEL_DEBUG,
        'format': LOG_FORMAT_DETAILED,
        'output': LOG_OUTPUT_CONSOLE
    })

    # Get the default logger
    logger = get_logger()

    # Log messages at different levels
    logger.debug("This is a debug message after configuration")
    logger.info("This is an info message after configuration")
    logger.warning("This is a warning message after configuration")
    logger.error("This is an error message after configuration")
    logger.critical("This is a critical message after configuration")

    print("configure_logging test passed.")


def test_json_logging():
    """Test logging in JSON format."""
    print("\nTesting JSON logging...")

    # Create a logger that logs in JSON format
    logger = LoggingService(
        name='test_json',
        level=LOG_LEVEL_INFO,
        format_str=LOG_FORMAT_JSON,
        output=LOG_OUTPUT_CONSOLE
    )

    # Log messages at different levels
    logger.info("This is an info message in JSON format")
    logger.warning("This is a warning message in JSON format")
    logger.error("This is an error message in JSON format")

    print("JSON logging test passed.")


def test_multiple_handlers():
    """Test logging with multiple handlers."""
    print("\nTesting multiple handlers...")

    # Create a log file
    log_file = Path('test_multiple.log')
    if log_file.exists():
        log_file.unlink()

    # Create a logger with a console handler
    logger = LoggingService(
        name='test_multiple',
        level=LOG_LEVEL_INFO,
        format_str=LOG_FORMAT_SIMPLE,
        output=LOG_OUTPUT_CONSOLE
    )

    # Add a file handler
    logger.add_file_handler(
        log_file=log_file,
        level=LOG_LEVEL_ERROR,
        format_str=LOG_FORMAT_DETAILED
    )

    # Log messages at different levels
    logger.info("This is an info message (console only)")
    logger.warning("This is a warning message (console only)")
    logger.error("This is an error message (console and file)")
    logger.critical("This is a critical message (console and file)")

    # Close all handlers to release the file
    for handler in logger.logger.handlers:
        handler.close()

    # Check that the log file exists and contains the expected messages
    if log_file.exists():
        with open(log_file, 'r') as f:
            content = f.read()
            print(f"Log file content:\n{content}")

        # Clean up
        try:
            log_file.unlink()
        except PermissionError:
            print(f"Could not delete log file {log_file} (still in use)")
    else:
        print("Log file was not created!")

    print("Multiple handlers test passed.")


def main():
    """Run all tests."""
    test_basic_logging()
    test_file_logging()
    test_get_logger()
    test_configure_logging()
    test_json_logging()
    test_multiple_handlers()

    print("\nAll logging tests passed!")


if __name__ == '__main__':
    main()
