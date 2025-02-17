import os
import platform
import re
import subprocess
import sys
from pathlib import Path

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def update_version_in_toml(cicd_cfg: CicdConfig):

    version_file_path = os.path.join(cicd_cfg.project_root, "version.txt")
    toml_file_path = os.path.join(cicd_cfg.project_root, "src" ,"pyproject.toml")

    with open(version_file_path, "r") as f:
        new_version = f.read().strip()  # Remove any extra whitespace or newlines

        # Read the pyproject.toml file
        with open(toml_file_path, "r") as f2:
            content = f2.read()

        # Regex to match lines like 'version = "0.1.2"'
        version_pattern = r'(?m)^(\s*version\s*=\s*")([^"]+)(")'

        # Use a replacement function to avoid raw-string confusion with \1, \3, etc.
        def replace_version(match):
            # match.group(1) = leading text up to first quote, e.g. 'version = "'
            # match.group(2) = current version number
            # match.group(3) = closing quote
            return f'{match.group(1)}{new_version}{match.group(3)}'

        # Replacements are now done safely via our function
        updated_content = re.sub(version_pattern, replace_version, content)

        # Write the updated content back to the TOML file
        with open(toml_file_path, "w") as f3:
            f3.write(updated_content)

def build_package(cicd_cfg: CicdConfig):
    """Build the Python package using a subprocess call to `python -m build`."""
    print("Building package...")

    # Get the path two levels up (assuming the same structure as your original code).
    project_root = cicd_cfg.project_root
    src_path = cicd_cfg.src_folder
    venv_dir = os.path.join(project_root , '.venv')
    if platform.system().lower().startswith("win"):
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(venv_dir, "bin", "python")

    try:
        os.chdir(src_path)
        update_version_in_toml()
        subprocess.run([python_executable, '-m', 'build', '--no-isolation'], cwd=src_path, check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
