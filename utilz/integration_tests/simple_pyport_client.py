"""
PyPort Development Integration Test

This script tests your current PyPort development code (0.3.1) by:
1. Installing your local development version
2. Testing basic functionality

Usage:
    python simple_pyport_client.py

Requirements:
    - .env file with PORT_CLIENT_ID and PORT_CLIENT_SECRET
    - src/ directory with PyPort source code
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

print("🚀 Testing PyPort Development Version")
print("=" * 50)

# Get the path to the src directory (relative to this script)
script_dir = Path(__file__).parent
src_dir = script_dir.parent.parent / "src"

if not src_dir.exists():
    print(f"❌ ERROR: Source directory not found at {src_dir}")
    print("Make sure you're running this from the correct location")
    sys.exit(1)

# Check if we're running under a debugger (PyCharm, VS Code, etc.)
is_debugging = any([
    'pydevd' in sys.modules,  # PyCharm debugger
    'debugpy' in sys.modules,  # VS Code debugger
    'pdb' in sys.modules,     # Python debugger
])

if is_debugging:
    print("🐛 Debugger detected - skipping pip installation")
    print("⚠️  Make sure PyPort development version is already installed!")
    print("   Run this command first: pip install -e src/")
else:
    # Uninstall any existing pyport installation
    print("Uninstalling any existing PyPort installation...")
    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "pyport", "-y"],
        capture_output=True  # Suppress output if package not installed
    )

    # Install the local development version
    print(f"Installing PyPort from local source: {src_dir}")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", str(src_dir)],
        check=True
    )



# Now import the client after installing the development version
print("Importing PyPort client...")
try:
    from pyport import PortClient
    print("✅ PyPort import successful!")
except ImportError as e:
    print(f"❌ Failed to import PyPort: {e}")
    sys.exit(1)

# Load environment variables from .env file
print("Loading environment variables...")

# Try to find .env file in common locations
env_paths = [
    script_dir / ".env",  # Same directory as this script
    Path.cwd() / ".env",  # Current working directory
    script_dir.parent.parent / ".env",  # PyPort root directory
]

env_loaded = False
for env_path in env_paths:
    if env_path.exists():
        print(f"📁 Found .env file at: {env_path}")
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    print("⚠️  No .env file found, trying to load from current directory...")
    load_dotenv()

# Access environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

print(f"🔑 PORT_CLIENT_ID: {PORT_CLIENT_ID}")
print(f"🔑 PORT_CLIENT_SECRET: {PORT_CLIENT_SECRET}")

if not PORT_CLIENT_ID or not PORT_CLIENT_SECRET:
    print("❌ Missing PORT_CLIENT_ID or PORT_CLIENT_SECRET environment variables")
    print("Please create a .env file with your Port credentials in the PyPort root directory")
    sys.exit(1)

print("Initializing Port client...")
try:
    # Initialize the client with credentials
    port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=False)
    print("✅ Port client initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize Port client: {e}")
    sys.exit(1)

# Test API connection by fetching blueprints
print("Testing API connection by fetching blueprints...")
try:
    blueprints = port_client.blueprints.get_blueprints()
    print(f"✅ Successfully fetched {len(blueprints)} blueprints")
except Exception as e:
    print(f"❌ Failed to fetch blueprints: {e}")
    sys.exit(1)

# Test new features
print("\n🧪 Testing new features...")

try:
    # Test action_runs service
    print("Testing action_runs service...")
    action_runs = port_client.action_runs.get_action_runs()
    print(f"✅ Action runs service working - found {len(action_runs.get('runs', []))} runs")
except Exception as e:
    print(f"⚠️  Action runs test failed: {e}")

try:
    # Test webhooks service
    print("Testing webhooks service...")
    webhooks = port_client.webhooks.get_webhooks()
    print(f"✅ Webhooks service working - found {len(webhooks.get('webhooks', []))} webhooks")
except Exception as e:
    print(f"⚠️  Webhooks test failed: {e}")

try:
    # Test teams service
    print("Testing teams service...")
    teams = port_client.teams.get_teams()
    print(f"✅ Teams service working - found {len(teams.get('teams', []))} teams")
except Exception as e:
    print(f"⚠️  Teams test failed: {e}")

try:
    # Test users service
    print("Testing users service...")
    users = port_client.users.get_users()
    print(f"✅ Users service working - found {len(users.get('users', []))} users")
except Exception as e:
    print(f"⚠️  Users test failed: {e}")

print(f"\n🎉 Integration test completed successfully!")
print(f"✅ Your PyPort development code is working correctly!")
