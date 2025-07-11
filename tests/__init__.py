"""Initialize the tests package.

This module adds the src directory to the Python path so that the tests can import
the package modules.
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_dir))