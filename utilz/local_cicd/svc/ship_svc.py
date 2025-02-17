import os
import subprocess

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def ship_package(cicd_cfg: CicdConfig):
    """
    Uploads the package to PyPI using Twine.
    Assumes the .pypirc file is located in the utilz directory and the dist directory is in src.
    """
    repo_config_file  = cicd_cfg.pypi_repo_config_file  # Path to PyPI repository configuration file
    dist_path = os.path.join("dist", "*")  # Path to distribution files

    try:
        print("Shipping package...")
        subprocess.run(["twine", "upload", "--config-file", repo_config_file , dist_path], check=True)
        print("Ship completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Ship failed: {e}")
