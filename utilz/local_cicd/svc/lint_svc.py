import os
import sys

from flake8.api import legacy as flake8_api

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


def lint_code(path: str):
    """Run linting on the source code."""
    print(f"Running lint...for {path}")

    try:
        if not os.path.exists(path):
            raise Exception(f"Path '{path}' does not exist")

        os.chdir(path)

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


if __name__ == "__main__":
    cicd_cfg1 = CicdConfig()
    lint_code(cicd_cfg1.src_folder)
    lint_code(os.path.join(cicd_cfg1.project_root, "utilz"))
    pass
