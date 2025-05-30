import os
import subprocess
import sys
from dotenv import load_dotenv

# Set default version to test
VERSION = "0.2.7"

# Get version from command line argument if provided
if len(sys.argv) > 1:
    VERSION = sys.argv[1]

print(f"Testing PyPort version: {VERSION}")

# Install the specified version
print(f"Installing PyPort version {VERSION}...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", f"pyport=={VERSION}"],
    check=True
)

# Now import the client after installing the specified version
from pyport import PortClient

# Load environment variables from .env file
load_dotenv()

# Access environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

# Initialize the client with credentials
port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)

# Test API connection by fetching blueprints
blueprints = port_client.blueprints.get_blueprints()

# Get installed version using pip
result = subprocess.run(
    [sys.executable, "-m", "pip", "show", "pyport"],
    capture_output=True,
    text=True,
    check=True
)

# Extract version from pip show output
for line in result.stdout.split('\n'):
    if line.startswith('Version:'):
        installed_version = line.split(':', 1)[1].strip()
        break
else:
    installed_version = "unknown"

print(f"Using PyPort version: {installed_version}")
print(f"Successfully fetched {len(blueprints)} blueprints")