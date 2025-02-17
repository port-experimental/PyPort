import unittest

# Import the function from your module.
from src.pyport.services.port_api_svc import get_requests_headers

class TestGetRequestsHeaders(unittest.TestCase):
    def test_with_valid_token(self):
        token = "abc123"
        expected_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer abc123'
        }
        self.assertEqual(get_requests_headers(token), expected_headers)

    def test_with_empty_token(self):
        token = ""
        expected_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '
        }
        self.assertEqual(get_requests_headers(token), expected_headers)

if __name__ == '__main__':
    unittest.main()
