import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

try:
    from coverage import Coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False
    print("Warning: coverage module not available. Coverage badge will show an error.")

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.scanner_svc import CodeScanner
from utilz.local_cicd.svc.security_assesment_svc import SecurityAssessor


def get_score_color(coverage_percentage):
    if coverage_percentage >= 90:
        color = 'brightgreen'
    elif coverage_percentage >= 75:
        color = 'green'
    elif coverage_percentage >= 60:
        color = 'yellowgreen'
    elif coverage_percentage >= 40:
        color = 'yellow'
    else:
        color = 'red'
    return color


def get_maintainability_badge_scoring(scores: List[Tuple[float, str]]) -> Tuple[float, str, str]:
    """Compute average maintainability and choose badge color and overall grade."""
    if not scores:
        return 0.0, "lightgrey", "N/A"
    avg_score = sum(score for score, _ in scores) / len(scores)
    badge_color = get_score_color(avg_score)
    if avg_score >= 90:
        return avg_score, badge_color, "A"
    elif avg_score >= 70:
        return avg_score, badge_color, "B"
    else:
        return avg_score, badge_color, "C"


class Badger(object):
    def __init__(self, cicd_cfg: CicdConfig):
        self.cicd_cfg = cicd_cfg
        self.scanner = CodeScanner(cicd_cfg)

    def update_readme_badge(self, new_badge: str, badge_type: str) -> None:
        """
        Update each README.md file with a new badge based on badge_type.

        Parameters:
            new_badge (str): The new badge Markdown string to insert.
            badge_type (str): The type of badge (e.g., "coverage", "maintainability", "security").
                              The function will look for a corresponding config attribute
                              named '{badge_type}_badge_pattern' to locate an existing badge.
        """
        # Build the attribute name to get the regex pattern from your config.
        pattern_attr = f"{badge_type}_badge_pattern"
        badge_pattern = getattr(self.cicd_cfg, pattern_attr, None)
        if badge_pattern is None:
            raise ValueError(f"Badge pattern for '{badge_type}' not configured.")

        # Define the two paths separately.
        readme_paths = [
            os.path.join(self.cicd_cfg.src_folder, 'README.md'),
            os.path.join(self.cicd_cfg.project_root, 'README.md')
        ]

        for readme_path in readme_paths:
            if os.path.exists(readme_path):
                # Read existing content from this file.
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # If the badge already exists, replace it; otherwise, prepend the new badge.
                match = re.search(badge_pattern, content)
                if match:
                    updated_content = re.sub(badge_pattern, new_badge, content)
                else:
                    updated_content = new_badge + '\n\n' + content

                # Write updated content back to this file.
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            else:
                print(f"File {readme_path} does not exist. Skipping update.")
        print(f"Badge updated in README files for '{badge_type}'.")

    def get_maintainability_badge(self) -> str:
        """
        Run Radon to compute maintainability and build the maintainability badge.
        """
        try:
            scores = self.scanner.scan_maintainability()
            if scores is None:
                return "![Maintainability](https://img.shields.io/badge/maintainability-Not%20Available-lightgrey)"

            avg_score, maint_color, overall_grade = get_maintainability_badge_scoring(scores)
            return (f"![Maintainability](https://img.shields.io/badge/maintainability-"
                    f"{avg_score:.1f}_{overall_grade}-{maint_color})")
        except Exception as e:
            print(f"Unexpected error generating maintainability badge: {e}")
            return "![Maintainability](https://img.shields.io/badge/maintainability-Error-red)"

    def get_coverage_badge(self) -> str:
        """
        Run Coverage.py to generate a coverage report,
        parse its output, and build a coverage badge.
        """
        if not COVERAGE_AVAILABLE:
            return "![Coverage](https://img.shields.io/badge/coverage-Not%20Available-lightgrey)"

        try:
            # Create a Coverage object and load existing data.
            cov = Coverage(config_file=self.cicd_cfg.coverage_config_file, data_file=self.cicd_cfg.coverage_data_file)
            cov.load()  # Assumes that coverage data has been previously generated.
            # data = cov.get_data()

            # Capture the report output.
            report_output = io.StringIO()
            original_stdout = sys.stdout
            sys.stdout = report_output
            try:
                cov.report(show_missing=False)
            finally:
                sys.stdout = original_stdout

            output_lines = report_output.getvalue().strip().split('\n')
            if not output_lines:
                coverage_percentage = 0.0
            else:
                total_line = output_lines[-1]
                try:
                    coverage_percentage = float(total_line.split()[-1].rstrip('%'))
                except (ValueError, IndexError):
                    coverage_percentage = 0.0

            color = get_score_color(coverage_percentage)
            return f"![Coverage](https://img.shields.io/badge/coverage-{coverage_percentage:.2f}%25-{color})"
        except Exception as e:
            print(f"Error generating coverage badge: {e}")
            return "![Coverage](https://img.shields.io/badge/coverage-Error-red)"

    def get_dependencies_badge(self) -> str:
        """
        Run pip-audit to check dependencies and build the dependencies badge.
        """
        try:
            req_path = Path(self.cicd_cfg.src_folder) / "requirements.txt"
            if not req_path.exists():
                return "![Dependencies](https://img.shields.io/badge/dependencies-Not%20Configured-lightgrey)"

            try:
                result = subprocess.run(
                    ["pip-audit", "--requirement", str(req_path), "--format", "json"],
                    capture_output=True, text=True, check=False
                )
            except FileNotFoundError:
                print("pip-audit command not found. Make sure pip-audit is installed.")
                return "![Dependencies](https://img.shields.io/badge/dependencies-Not%20Available-lightgrey)"
            except Exception as e:
                print(f"Error running pip-audit: {e}")
                return "![Dependencies](https://img.shields.io/badge/dependencies-Error-red)"

            vulnerability_count = 0
            try:
                data = json.loads(result.stdout)
                # Assume data is a dictionary with a "dependencies" key, which is a list of dependency items.
                vulnerability_count = sum(len(dep.get("vulns", [])) for dep in data.get("dependencies", []))
            except json.JSONDecodeError:
                print("Failed to parse pip-audit output.")
                print(f"Output starts with: {result.stdout[:100]}...")
                return "![Dependencies](https://img.shields.io/badge/dependencies-Error-red)"

            if vulnerability_count == 0:
                status = "Passed"
                color = "brightgreen"
            else:
                status = f"Issues%20{vulnerability_count}"
                color = "red"

            return f"![Dependencies](https://img.shields.io/badge/dependencies-{status}-{color})"
        except Exception as e:
            print(f"Unexpected error generating dependencies badge: {e}")
            return "![Dependencies](https://img.shields.io/badge/dependencies-Error-red)"

    def get_security_badge(self) -> str:
        """
        Run Bandit to scan for security issues and build the security badge.
        """
        try:
            # Try to run bandit
            try:
                result = subprocess.run(
                    ["bandit", "-r", str(self.cicd_cfg.src_folder), "-f", "json"],
                    capture_output=True, text=True, check=False
                )
            except subprocess.CalledProcessError as e:
                print("Error running bandit:", e)
                return "![Security](https://img.shields.io/badge/security-Error-red)"
            except FileNotFoundError:
                print("Bandit command not found. Make sure bandit is installed.")
                return "![Security](https://img.shields.io/badge/security-Not%20Available-lightgrey)"

            # Process the output to handle potential non-JSON content at the beginning
            output = result.stdout

            # Check if the first character is '{' and if not, remove the first line
            if output and output.strip() and output.strip()[0] != '{':
                print("First character is not '{', removing first line...")
                output = '\n'.join(output.splitlines()[1:])

            # Try to parse the JSON output
            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                print("Failed to parse bandit output.")
                print(f"Output starts with: {output[:100]}...")
                return "![Security](https://img.shields.io/badge/security-Error-red)"

            # Check if the metrics key exists
            if "metrics" not in data:
                print("No metrics found in bandit output.")
                return "![Security](https://img.shields.io/badge/security-Error-red)"

            # Process the security assessment
            sa = SecurityAssessor(self.cicd_cfg.project_root, data["metrics"])
            sa.compute_assessment()
            sa.generate_markdown_report()

            return f"![Security](https://img.shields.io/badge/security-{sa.overall_grade}-{sa.badge_color})"
        except Exception as e:
            print(f"Unexpected error generating security badge: {e}")
            return "![Security](https://img.shields.io/badge/security-Error-red)"

    def update_all_badges(self):
        """
        Update all badges in the README file.
        """
        badges = {
            "coverage": self.get_coverage_badge(),
            "maintainability": self.get_maintainability_badge(),
            "dependencies": self.get_dependencies_badge(),
            "security": self.get_security_badge()
        }
        for badge_type, badge in badges.items():
            self.update_readme_badge(badge, badge_type)

        print("Badges updated successfully.")


if __name__ == "__main__":
    cicd_cfg1 = CicdConfig()
    badger = Badger(cicd_cfg1)
    # cov_b = badger.get_coverage_badge()
    # badger.update_readme_badge(cov_b, "coverage")
    # cov_m = badger.get_maintainability_badge()
    # badger.update_readme_badge(cov_m, "maintainability")
    # cov_d = badger.get_dependencies_badge()
    # badger.update_readme_badge(cov_d, "dependencies")
    # cov_s = badger.get_security_badge()
    # badger.update_readme_badge(cov_s, "security")
