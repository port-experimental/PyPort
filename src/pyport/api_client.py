import json
import logging
import os
import threading
import time

import requests

from pyport.actions.actions_api_svc import Actions
from pyport.entities.entities_api_svc import Entities
from pyport.pages.pages_api_svc import Pages
from pyport.blueprints.blueprint_api_svc import Blueprints
from pyport.constants import PORT_API_US_URL, PORT_API_URL, GENERIC_HEADERS


class PortClient:
    def __init__(self, client_id: str = "", client_secret: str = "", us_region: bool = False,
                 auto_refresh: bool = True, refresh_interval: int = 900):
        """
        Initialize the PortClient.

        :param client_id: API client ID.
        :param client_secret: API client secret.
        :param us_region: Whether to use the US region API URL.
        :param auto_refresh: If True, a background thread will refresh the token periodically.
        :param refresh_interval: Token refresh interval in seconds (default 900 sec = 15 minutes).
        """
        self.api_url = PORT_API_US_URL if us_region else PORT_API_URL
        self._logger = logging.getLogger(__name__)
        self._lock = threading.Lock()

        # Obtain the initial token.
        self.token = self._get_access_token(client_id, client_secret)
        # Initialize the session and sub-clients.
        self._init_session()
        self._init_sub_clients()

        # Start a background thread to auto-refresh the token if enabled.
        self._auto_refresh = auto_refresh
        self._refresh_interval = refresh_interval
        if self._auto_refresh:
            self._start_token_refresh_thread()

    def _init_session(self):
        """Initializes the persistent session and default headers."""
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })

    def _init_sub_clients(self):
        """Initializes the API sub-clients."""
        self.blueprints = Blueprints(self)
        self.entities = Entities(self)
        self.actions = Actions(self)
        self.pages = Pages(self)

    def _start_token_refresh_thread(self):
        refresh_thread = threading.Thread(target=self._token_refresh_loop, daemon=True)
        refresh_thread.start()
        self._logger.info("Token refresh thread started.")

    def _token_refresh_loop(self):
        while True:
            time.sleep(self._refresh_interval)
            try:
                self._logger.debug("Refreshing access token...")
                new_token = self._get_access_token()
                with self._lock:
                    self.token = new_token
                    self._session.headers.update({"Authorization": f"Bearer {self.token}"})
                self._logger.info("Access token refreshed successfully.")
            except Exception as e:
                self._logger.error(f"Failed to refresh token: {str(e)}")

    def _get_access_token(self, client_id: str = "", client_secret: str = "") -> str:
        try:
            headers = GENERIC_HEADERS
            if not client_id or not client_secret:
                client_id, client_secret = self._get_local_env_cred()

            credentials = {'clientId': client_id, 'clientSecret': client_secret}
            payload = json.dumps(credentials)
            self._logger.debug("Sending authentication request to obtain access token...")

            token_response = requests.post(f'{self.api_url}/auth/access_token', headers=headers,
                                           data=payload, timeout=10)
            if token_response.status_code != 200:
                self._logger.error(
                    f"Failed to obtain access token. Status code: {token_response.status_code}. "
                    f"Response: {token_response.text}"
                )
                token_response.raise_for_status()

            token = token_response.json().get('accessToken')
            if not token:
                self._logger.error("Access token not found in the response.")
                raise ValueError("Access token not present in the API response.")

            return token

        except Exception as e:
            self._logger.error(f"An unexpected error occurred while obtaining access token: {str(e)}")
            raise

    def _get_local_env_cred(self):
        PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
        PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
        if not PORT_CLIENT_ID or not PORT_CLIENT_SECRET:
            self._logger.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET.")
            raise ValueError("Environment variables PORT_CLIENT_ID or PORT_CLIENT_SECRET are not set")
        return PORT_CLIENT_ID, PORT_CLIENT_SECRET

    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: API endpoint appended to the base URL.
        :param kwargs: Additional parameters passed to requests.request.
        :return: A requests.Response object.
        """
        url = f"{self.api_url}/{endpoint}"
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
