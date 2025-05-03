![PyPort Logo](./assets/port.png)

# PyPort 🚀

[![dan-amzulescu-port - pyport](https://img.shields.io/static/v1?label=port-experimental&message=pyport&color=blue&logo=github)](https://github.com/dan-amzulescu-port/pyport)
[![stars - pyport](https://img.shields.io/github/stars/dan-amzulescu-port/pyport?style=social)](https://github.com/dan-amzulescu-port/pyport)
[![forks - pyport](https://img.shields.io/github/forks/dan-amzulescu-port/pyport?style=social)](https://github.com/dan-amzulescu-port/pyport)


_Repo metadata_

![Coverage](https://img.shields.io/badge/coverage-87.00%25-green)
![Maintainability](https://img.shields.io/badge/maintainability-100.0_A-brightgreen)
![Security](https://img.shields.io/badge/security-A-brightgreen)
![Dependencies](https://img.shields.io/badge/dependencies-Passed-brightgreen)

![GitHub issues](https://img.shields.io/github/issues/dan-amzulescu-port/pyport)
[![GitHub tag](https://img.shields.io/github/tag/dan-amzulescu-port/pyport?include_prereleases=&sort=semver&color=blue)](https://github.com/dan-amzulescu-port/pyport/releases/)
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

If you have questions or need clarification on any aspect of this project, the documentation provides in-depth explanations, code examples, and best practices to help you get started quickly.
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
from pyport import PortClient

PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")

port_client = PortClient(client_id=PORT_CLIENT_ID, client_secret=PORT_CLIENT_SECRET, us_region=True)
blueprints = port_client.blueprints.get_blueprints()
```    

Happy Coding!


