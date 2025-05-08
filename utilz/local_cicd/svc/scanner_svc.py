import json
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple, Callable, Union, Optional, Dict, Any

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.logging_svc import get_logger
from utilz.local_cicd.svc.security_assesment_svc import SecurityAssessor


class CodeScanner(object):
    """
    Scanner for code quality metrics.

    This class provides methods for scanning code quality metrics like
    maintainability, security, and dependencies.
    """

    def __init__(self, cicd_cfg: CicdConfig):
        """
        Initialize the code scanner.

        Args:
            cicd_cfg: Configuration for the CI/CD utilities.
        """
        self.cicd_cfg = cicd_cfg
        self.logger = get_logger('scanner')

    def scan_maintainability(self) -> list[tuple[float, str]]:
        """
        Run Radon to compute maintainability and build the maintainability badge.
        """
        radon_result = None
        self.logger.info("Running Radon to compute maintainability...")
        try:
            radon_result = subprocess.run(
                ["radon", "mi", self.cicd_cfg.src_folder],
                capture_output=True, text=True, check=True
            )
            self.logger.debug(f"Radon output:\n{radon_result.stdout}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running radon: {e}")

        scores: List[Tuple[float, str]] = []
        for line in radon_result.stdout.splitlines():
            # Try to match the full pattern with a numeric score first.
            match = re.search(r"MI:\s*([\d\.]+)\s+\(([A-F])\)", line)
            if not match:
                # Fallback: match lines like '... - A' that only capture the grade.
                match = re.search(r".* - ([A-F])$", line)
            if match:
                if len(match.groups()) == 2:
                    score = float(match.group(1))
                    grade = match.group(2)
                else:
                    # Only the grade was captured; assign a default score based on the grade.
                    grade = match.group(1)
                    default_scores = {"A": 100.0, "B": 80.0, "C": 60.0, "D": 40.0, "F": 20.0}
                    score = default_scores.get(grade, 0)
                scores.append((score, grade))

        return scores

    def scan_dependencies(self) -> None:
        """
        Run pip-audit to check dependencies and build the dependencies badge.
        """
        req_path = Path(self.cicd_cfg.src_folder) / "requirements.txt"
        if not req_path.exists():
            self.logger.warning(f"Requirements file not found at {req_path}")
            return

        self.logger.info("Running pip-audit to check dependencies...")
        try:
            result = subprocess.run(
                ["pip-audit", "--requirement", str(req_path), "--format", "json"],
                capture_output=True, text=True, check=False
            )
        except Exception as e:
            self.logger.error(f"Error running pip-audit: {e}")
            return

        vulnerability_count = 0
        try:
            data = json.loads(result.stdout)
            # Assume data is a dictionary with a "dependencies" key, which is a list of dependency items.
            vulnerability_count = sum(len(dep.get("vulns", [])) for dep in data.get("dependencies", []))
            self.logger.info(f"Found {vulnerability_count} vulnerabilities.")
        except json.JSONDecodeError:
            self.logger.error("Failed to parse pip-audit output.")
            self.logger.debug(f"pip-audit output: {result.stdout[:500]}...")

    def scan_security(self) -> None:
        """
        Run Bandit to scan for security issues and build the security badge.
        """
        self.logger.info("Running Bandit to scan for security issues...")
        try:
            result = subprocess.run(
                ["bandit", "-r", str(self.cicd_cfg.src_folder), "-f", "json"],
                capture_output=True, text=True, check=False
            )
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running bandit: {e}")
            return

        # Process the output to handle potential non-JSON content at the beginning
        output = result.stdout

        # Check if the first character is '{' and if not, remove the first line
        if output and output.strip() and output.strip()[0] != '{':
            self.logger.warning("First character is not '{', removing first line...")
            output = '\n'.join(output.splitlines()[1:])

        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            self.logger.error("Failed to parse bandit output.")
            self.logger.debug(f"Output starts with: {output[:100]}...")
            return

        self.logger.info("Processing security assessment...")
        sa = SecurityAssessor(self.cicd_cfg.project_root, data["metrics"])
        sa.compute_assessment()
        sa.generate_markdown_report()
        self.logger.info(f"Security assessment complete with grade: {sa.overall_grade}")
        return

    def run_all_scans(self) -> None:
        """
        Runs all badge scans and updates the README accordingly.
        """
        badge_scanners: Dict[str, Callable[[], Union[str, List[Tuple[float, str]], None]]] = {
            "maintainability": self.scan_maintainability,
            "dependencies": self.scan_dependencies,
            "security": self.scan_security,
        }
        self.logger.info("Running all badge related scans...")
        for badge_type, scan_method in badge_scanners.items():
            self.logger.info(f"Running {badge_type} scan...")
            scan_method()  # This executes the function
            self.logger.info(f"{badge_type.capitalize()} scan complete.")


if __name__ == "__main__":
    from utilz.local_cicd.svc.logging_svc import configure_logging, LOG_LEVEL_DEBUG, LOG_FORMAT_DETAILED

    # Configure logging for debugging
    configure_logging({
        'level': LOG_LEVEL_DEBUG,
        'format': LOG_FORMAT_DETAILED,
        'output': 'both',
        'log_file': 'scanner.log'
    })

    # Create scanner and run scans
    cicd_cfg1 = CicdConfig()
    code_scanner = CodeScanner(cicd_cfg1)
    code_scanner.run_all_scans()
    code_scanner.logger.info("All scans completed successfully!")
