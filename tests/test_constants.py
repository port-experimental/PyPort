import unittest

from pyport.constants import PORT_API_URL, PORT_API_US_URL, LOG_LEVEL, GENERIC_HEADERS


class TestConstants(unittest.TestCase):
    def test_port_api_url(self):
        self.assertEqual(PORT_API_URL, 'https://api.getport.io/v1')
        self.assertIsInstance(PORT_API_URL, str)

    def test_port_api_us_url(self):
        self.assertEqual(PORT_API_US_URL, 'https://api.us.getport.io/v1')
        self.assertIsInstance(PORT_API_US_URL, str)

    def test_log_level(self):
        self.assertEqual(LOG_LEVEL, 'DEBUG')
        self.assertIsInstance(LOG_LEVEL, str)

    def test_generic_headers(self):
        expected_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.assertEqual(GENERIC_HEADERS, expected_headers)
        self.assertIsInstance(GENERIC_HEADERS, dict)
        self.assertIn('Content-Type', GENERIC_HEADERS)
        self.assertIn('Accept', GENERIC_HEADERS)


if __name__ == "__main__":
    unittest.main()
