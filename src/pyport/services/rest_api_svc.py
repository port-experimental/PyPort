from typing import Dict, Optional, Union, Any
import logging
import requests


def post_request(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Union[str, int, float]]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None
) -> Optional[requests.Response]:
    """
    Helper function to send POST requests and handle errors.
    """
    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
