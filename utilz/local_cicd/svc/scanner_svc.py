import json
import os
import re
import subprocess

from typing import List, Tuple, Callable, Union

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.security_assesment_svc import SecurityAssessor


class CodeScanner(object):
    def __init__(self, cicd_cfg: CicdConfig):
        self.cicd_cfg = cicd_cfg

    def scan_maintainability(self) -> list[tuple[float, str]]:
        """
        Run Radon to compute maintainability and build the maintainability badge.
        """
        radon_result = None
        print("Running Radon to compute maintainability...")
        try:
            radon_result = subprocess.run(
                ["radon", "mi", self.cicd_cfg.src_folder],
                capture_output=True, text=True, check=True
            )
            print(radon_result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running radon:", e)

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
        req_path = os.path.join(self.cicd_cfg.src_folder, "requirements.txt")
        if not os.path.exists(req_path):
            print("Requirements file not found.")
            return
        print("Running pip-audit to check dependencies...")
        try:
            result = subprocess.run(
                ["pip-audit", "--requirement", req_path, "--format", "json"],
                capture_output=True, text=True, check=False
            )
        except Exception as e:
            print("Error running pip-audit:", e)
            return
        vulnerability_count = 0
        try:
            data = json.loads(result.stdout)
            # Assume data is a dictionary with a "dependencies" key, which is a list of dependency items.
            vulnerability_count = sum(len(dep.get("vulns", [])) for dep in data.get("dependencies", []))
            print(f"Found {vulnerability_count} vulnerabilities.")
        except json.JSONDecodeError:
            print("Failed to parse pip-audit output.")

    def scan_security(self) -> None:
        """
        Run Bandit to scan for security issues and build the security badge.
        """
        print("Running Bandit to scan for security issues...")
        try:
            result = subprocess.run(
                ["bandit", "-r", self.cicd_cfg.src_folder, "-f", "json"],
                capture_output=True, text=True, check=False
            )
        except subprocess.CalledProcessError as e:
            print("Error running bandit:", e)
            return

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Failed to parse bandit output.")
            return
        sa = SecurityAssessor(self.cicd_cfg.project_root, data["metrics"])
        sa.compute_assessment()
        sa.generate_markdown_report()
        return

    def run_all_scans(self) -> None:
        """
        Runs all badge scans and updates the README accordingly.
        """
        badge_scanners: dict[str, Callable[[], Union[str, List[Tuple[float, str]], None]]] = {
            "maintainability": self.scan_maintainability,
            "dependencies": self.scan_dependencies,
            "security": self.scan_security,
        }
        print("Running all badge related scans...")
        for badge_type, scan_method in badge_scanners.items():
            scan_method()  # This executes the function


if __name__ == "__main__":
    cicd_cfg1 = CicdConfig()
    code_scanner = CodeScanner(cicd_cfg1)
    code_scanner.run_all_scans()
    print("\\m/")