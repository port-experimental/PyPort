import os
import sys
from pathlib import Path

from flake8.api import legacy as flake8_api

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def lint_code(cicd_cfg: CicdConfig):
    """Run linting on the source code."""
    print("Running lint...")

    try:
        os.chdir(cicd_cfg.src_folder)

        style_guide = flake8_api.get_style_guide(
            max_line_length=120,
            ignore=['E203', 'W503', 'E501'],
        )
        report = style_guide.check_files(['.'])

        if report.get_statistics('E') or report.get_statistics('W'):
            raise Exception("Linting errors found")

        print("Linting passed.")
    except Exception as e:
        print(f"Linting failed: {e}", file=sys.stderr)
