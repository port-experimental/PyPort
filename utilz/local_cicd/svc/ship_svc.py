import os
import subprocess

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def ship_package(cicd_cfg: CicdConfig):
    """
    Uploads the package to PyPI using Twine.
    Assumes the .pypirc file is located in the utilz directory and the dist directory is in src.
    """
    repo_config_file = cicd_cfg.pypi_repo_config_file  # Path to PyPI repository configuration file
    dist_dir = os.path.join(cicd_cfg.src_folder, "dist")
    dist_path = os.path.join(dist_dir, "*")  # Path to distribution files

    # Check if dist directory exists and contains files
    if not os.path.exists(dist_dir):
        error_msg = f"Distribution directory not found: {dist_dir}"
        print(error_msg)
        raise FileNotFoundError(error_msg)

    if not os.listdir(dist_dir):
        error_msg = f"No distribution files found in {dist_dir}"
        print(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        print("Shipping package...")
        subprocess.run(["twine", "upload", "--config-file", repo_config_file, dist_path], check=True)
        print("Ship completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        error_msg = f"Ship failed: {e}"
        print(error_msg)
        raise RuntimeError(error_msg)


if __name__ == "__main__":
    # cicd_cfg1 = CicdConfig()
    # ship_package(cicd_cfg1)
    pass
