"""Port API utility functions."""


def get_requests_headers(token: str):
    """Get HTTP headers for API requests.

    Args:
        token: The authentication token.

    Returns:
        Dictionary containing HTTP headers.
    """
    return {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
