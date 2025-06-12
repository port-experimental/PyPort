"""Constants and configuration values for PyPort.

This module contains all the constant values used throughout the PyPort library,
including API URLs, default headers, and configuration settings.
"""

#: Default Port API URL for EU region
PORT_API_URL = 'https://api.getport.io/v1'

#: Port API URL for US region
PORT_API_US_URL = 'https://api.us.getport.io/v1'

#: Default logging level for the library
LOG_LEVEL = "DEBUG"

#: Standard HTTP headers used for all API requests
GENERIC_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
