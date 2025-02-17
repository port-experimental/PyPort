import glob
import os
import shutil
import sys

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def cleanup(cicd_cfg: CicdConfig):
    """Clean up build artifacts."""
    print("Running cleanup...")

    try:
        os.chdir(cicd_cfg.src_folder)

        dist_path = os.path.join(cicd_cfg.src_folder, 'dist')
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
            print("Removed dist directory.")

        for item in glob.glob('*.egg-info'):
            shutil.rmtree(item)
            print(f"Removed {item}.")

        print("Cleanup completed.")
    except Exception as e:
        print(f"Cleanup failed: {e}", file=sys.stderr)
