import unittest
import logging
import os

# Import the function and map from your module (adjust the path if needed)
from src.pyport.logging import init_logging, LOG_LEVEL_MAP, logger


class TestInitLogging(unittest.TestCase):
    def setUp(self):
        # Remove any existing handlers from the root logger.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Reset the logger level.
        logging.root.setLevel(logging.NOTSET)

    def test_init_logging_valid(self):
        # Call init_logging with a valid level (e.g., "INFO").
        init_logging("INFO")
        logger = logging.getLogger()
        # Verify the logger's level is set correctly.
        self.assertEqual(logger.level, logging.INFO)

        # Check that a FileHandler writing to "app.log" exists.
        file_handler_found = any(
            isinstance(h, logging.FileHandler) and os.path.basename(getattr(h, 'baseFilename', '')) == "app.log"
            for h in logger.handlers
        )
        # Check that a StreamHandler exists.
        stream_handler_found = any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        )
        self.assertTrue(file_handler_found, "FileHandler for app.log not found")
        self.assertTrue(stream_handler_found, "StreamHandler not found")

    def test_init_logging_invalid(self):
        # Calling init_logging with an invalid level should use the default level (INFO).
        # Get the root logger level before the test
        root_logger = logging.getLogger()
        original_level = root_logger.level

        try:
            # Run the test
            init_logging("INVALID")
            # Check that the root logger level is set to INFO
            self.assertEqual(root_logger.level, logging.INFO)
        finally:
            # Restore the original level
            root_logger.setLevel(original_level)


if __name__ == "__main__":
    unittest.main()
