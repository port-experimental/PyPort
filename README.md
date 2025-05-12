![PyPort Logo](./assets/port.png)

# PyPort 🚀

[![port-experimental - pyport](https://img.shields.io/static/v1?label=port-experimental&message=pyport&color=blue&logo=github)](https://github.com/port-experimental/pyport)
[![stars - pyport](https://img.shields.io/github/stars/port-experimental/pyport?style=social)](https://github.com/port-experimental/pyport)
[![forks - pyport](https://img.shields.io/github/forks/port-experimental/pyport?style=social)](https://github.com/port-experimental/pyport)


_Repo metadata_

![Coverage](https://img.shields.io/badge/coverage-72.00%25-yellowgreen)
![Maintainability](https://img.shields.io/badge/maintainability-100.0_A-brightgreen)
![Security](https://img.shields.io/badge/security-A-brightgreen)
![Dependencies](https://img.shields.io/badge/dependencies-Passed-brightgreen)

![GitHub issues](https://img.shields.io/github/issues/port-experimental/pyport)
[![GitHub tag](https://img.shields.io/github/tag/port-experimental/pyport?include_prereleases=&sort=semver&color=blue)](https://github.com/port-experimental/pyport/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![Documentation](https://img.shields.io/badge/docs-api.getport.io-blue?style=flat)](https://docs.port.io/api-reference/port-api/)

_Package info_

[![PyPI version](https://badge.fury.io/py/pyport.svg)](https://badge.fury.io/py/pyport)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyport)](https://pypi.org/project/pyport)


> **Simplify Your REST Interactions**
> _A Python SDK for the Port IDP REST API that handles authentication, error handling, and logging so you can focus on building your solutions._


---

## 🔍 Overview

Modern REST APIs can be powerful—but they aren’t always intuitive to work with. **PyPort** abstracts away the repetitive tasks of authentication, error handling, and logging, providing you with a clean, Pythonic client interface to interact with the Port IDP REST API.

Whether you're writing custom Python scripts or building larger applications, PyPort is designed to speed up your development process by simplifying REST operations.

## Documentation & Support

For detailed information about the data model and code implementation, please refer to our comprehensive documentation at [PyPort Documentation](https://deepwiki.com/port-experimental/PyPort).

---

## ✨ Key Features

- **Intuitive Client Interface**
  Interact with the Port IDP REST API effortlessly.

- **Automated Authentication**
  Manage API tokens and credentials automatically.

- **Robust Error Handling**
  Receive clear, actionable error messages for smooth debugging.

- **Integrated Logging**
  Built-in logging to help you trace and monitor API interactions.

- **Data Management Utilities**
  Easily create backups with snapshots and perform bulk operations like clearing all entities.

> **Note:** Additional features and improvements are planned for future releases!

---

##  🔒 Security Scan Report

We've run a security scan on our code using Bandit. Check out the [Security Scan Report](SECURITYSCAN.md) for the details on what was found.

---


## Installation

Install PyPort using pip:

```bash
pip install pyport
```

## Usage
Below is a boilerplate example to help you get started with PyPort:

```python
import os
from pyport import PortClient

PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)
blueprints = port_client.blueprints.get_blueprints()
```

### High-Level Utilities

PyPort includes high-level utility functions for common operations:

```python
from pyport import PortClient
from pyport.utils import clear_blueprint, save_snapshot, restore_snapshot, list_snapshots

# Initialize the client
client = PortClient(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Clear all entities in a blueprint
result = clear_blueprint(client, "service")
print(f"Deleted {result['deleted_entities']} entities")

# Save a snapshot of your Port data
snapshot = save_snapshot(
    client,
    prefix="my-backup",
    include_blueprints=True,
    include_entities=True,
    include_actions=True
)
print(f"Snapshot saved: {snapshot['snapshot_id']}")

# List available snapshots
snapshots = list_snapshots()
for snapshot in snapshots:
    print(f"{snapshot['snapshot_id']} ({snapshot['timestamp']})")

# Restore a snapshot
restore_result = restore_snapshot(
    client,
    "my-backup_20230101_120000",
    restore_blueprints=True,
    restore_entities=True
)
print(f"Restored {restore_result['restored_blueprints']} blueprints and {restore_result['restored_entities']} entities")
```

See the `examples` directory for more detailed examples.

## 🆕 New Features

### Snapshot Management

The new snapshot functionality allows you to create complete backups of your Port data, including blueprints, entities, actions, pages, and scorecards. This is particularly useful for:

- Creating backups before making significant changes
- Migrating data between environments
- Setting up test environments with production-like data
- Implementing disaster recovery procedures

Snapshots are stored locally in a structured directory format, making them easy to manage and transfer.

### Blueprint Utilities

The new blueprint utilities provide powerful operations for managing your Port data:

- **Clear Blueprint**: Easily delete all entities in a blueprint with a single function call
- **Save Snapshot**: Create comprehensive backups of your Port data
- **Restore Snapshot**: Restore your Port data from a previous backup
- **List Snapshots**: View all available snapshots with their timestamps and contents

These utilities make it simple to perform bulk operations that would otherwise require multiple API calls and complex logic.

Happy Coding!


