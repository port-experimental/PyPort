import os
from typing import Dict, Iterable, Tuple

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

class SecurityAssessor:
    def __init__(self, project_root: str,metrics_items: Iterable[Tuple[str, Dict]]) -> None:
        self.project_root = project_root
        self.metrics_items = metrics_items
        self.total_loc: int = 0
        self.total_high: int = 0
        self.total_medium: int = 0
        self.total_low: int = 0
        self.weighted_overall: int = 0
        self.overall_grade: str = ""
        self.badge_color: str = ""
        self.vulnerability_density: float = 0.0
        self.report_rows: list = []

    def compute_assessment(self) -> None:
        """
        Generate an HTML report from per‑file security metrics.

        For each file, the metrics dictionary is expected to include keys such as:
            - 'SEVERITY.HIGH'
            - 'SEVERITY.MEDIUM'
            - 'SEVERITY.LOW'
            - 'loc'
            (and optionally, other keys like 'CONFIDENCE.*', etc.)

        The function aggregates these metrics, computes a weighted vulnerability density,
        assigns an overall grade, and writes a detailed report to 'security_report.html'.
        """
        # Prepare per-file report rows and aggregate totals.
        aggregated: Dict[str, int] = {}
        self.report_rows = []

        for filepath, metrics in self.metrics_items.items():
            # Extract per-file values.
            loc = metrics.get("loc", 0)
            high = metrics.get("SEVERITY.HIGH", 0)
            medium = metrics.get("SEVERITY.MEDIUM", 0)
            low = metrics.get("SEVERITY.LOW", 0)
            # Define weights: high counts more, then medium, then low.
            weighted = 3 * high + 2 * medium + low

            # Decide on a note for the file.
            note = "OK" if weighted == 0 else "Fix Required"
            self.report_rows.append((filepath, loc, high, medium, low, weighted, note))

            # Aggregate metrics across files.
            for key, value in metrics.items():
                aggregated[key] = aggregated.get(key, 0) + value

        # Compute overall aggregated values.
        self.total_loc = aggregated.get("loc", 0)
        self.total_high = aggregated.get("SEVERITY.HIGH", 0)
        self.total_medium = aggregated.get("SEVERITY.MEDIUM", 0)
        self.total_low = aggregated.get("SEVERITY.LOW", 0)
        self.weighted_overall = 3 * self.total_high + 2 * self.total_medium + self.total_low

        # Calculate vulnerability density as weighted score per line of code.
        self.vulnerability_density = self.weighted_overall / self.total_loc if self.total_loc > 0 \
            else self.weighted_overall

        # Determine an overall grade based on thresholds.
        if self.vulnerability_density < 0.01:
            self.overall_grade = "A"
            self.badge_color = "brightgreen"
        elif self.vulnerability_density < 0.02:
            self.overall_grade = "B"
            self.badge_color = "green"
        elif self.vulnerability_density < 0.05:
            self.overall_grade = "C"
            self.badge_color = "yellow"
        elif self.vulnerability_density < 0.1:
            self.overall_grade = "D"
            self.badge_color = "orange"
        else:
            self.overall_grade = "F"
            self.badge_color = "red"

    def generate_markdown_report(self) -> None:
        """
        Builds a Markdown report with aggregated metrics and per-file details,
        and saves it to SECURITYSCAN.md in the project root.
        """
        # Header: include an image (logo) and some basic info.
        logo_md = "![Bandit Logo](assets/blogo.png)"
        header_info = (
            f"{logo_md}\n\n"
            f"**Security Scan Report**\n\n"
            f"Security scan performed using: Bandit v{self.get_bandit_version()}\n\n"
            "This report summarizes the results of our automated security scan.\n\n"
        )

        # Aggregated Metrics section.
        aggregated_info = (
            f"**Aggregated Metrics**\n\n"
            f"- Total LOC: {self.total_loc}\n"
            f"- Weighted Vulnerability Score: {self.weighted_overall}\n"
            f"- Vulnerability Density: {self.vulnerability_density:.4f}\n\n"
            f"**Overall Grade:** {self.overall_grade}\n\n"
        )

        # Per-File Report as a Markdown table.
        table_header = (
            "| File | LOC | High | Medium | Low | Weighted Score | Notes |\n"
            "| --- | ---:| ---:| ---:| ---:| ---:| --- |\n"
        )

        # Base URL conversion: convert local file path to GitHub URL.
        base_repo_url = "https://github.com/port-experimental/PyPort/"
        local_base = str(self.project_root).rstrip(os.sep) + os.sep
        table_rows = ""
        for row in self.report_rows:
            filepath, loc, high, medium, low, weighted, note = row
            # Calculate relative path and normalize to forward slashes.
            relative_path = filepath[len(local_base):].replace("\\", "/")
            github_path = f"{base_repo_url}blob/main/{relative_path}"
            table_rows += (
                f"| [{github_path}]({github_path}) | {loc} | {high} | {medium} | {low} | {weighted} | {note} |\n"
            )

        md_content = header_info + aggregated_info + table_header + table_rows

        report_path = os.path.join(str(self.project_root), "SECURITYSCAN.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Markdown security report generated and saved to '{report_path}'.")


    # Helper method to get Bandit version (to keep our code DRY)
    def get_bandit_version(self) -> str:
        try:
            from importlib.metadata import version, PackageNotFoundError
        except ImportError:
            from importlib_metadata import version, PackageNotFoundError
        try:
            return version("bandit")
        except PackageNotFoundError:
            return "unknown"
