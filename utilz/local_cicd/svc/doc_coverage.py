"""
Documentation coverage service for PyPort.

This module provides tools for analyzing and ensuring documentation coverage.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path


class DocCoverageAnalyzer:
    """
    Analyzer for Python package documentation coverage.
    
    This class provides methods for analyzing documentation coverage and
    generating reports.
    """
    
    def __init__(self, src_dir: str = "src/pyport", min_coverage: float = 80.0):
        """
        Initialize the documentation coverage analyzer.
        
        Args:
            src_dir: The directory containing the source code to analyze.
            min_coverage: The minimum acceptable documentation coverage percentage.
        """
        self.src_dir = src_dir
        self.min_coverage = min_coverage
        self.output_dir = Path("temp/doc_coverage")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def check_interrogate_installed(self) -> bool:
        """
        Check if the interrogate package is installed.
        
        Returns:
            True if interrogate is installed, False otherwise.
        """
        try:
            subprocess.run(
                [sys.executable, "-m", "interrogate", "--help"],
                capture_output=True,
                text=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def analyze_coverage(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Analyze documentation coverage.
        
        Args:
            verbose: Whether to include detailed information in the output.
            
        Returns:
            A dictionary with the analysis results.
        """
        if not self.check_interrogate_installed():
            print("interrogate not installed. Install with: pip install interrogate")
            return {
                "success": False,
                "error": "interrogate not installed",
                "coverage": 0.0,
                "files": []
            }
        
        # Run interrogate
        cmd = [sys.executable, "-m", "interrogate"]
        if verbose:
            cmd.append("-v")
        cmd.append(self.src_dir)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        # Parse the output
        output = result.stdout
        
        # Extract the coverage percentage
        coverage = 0.0
        if "actual: " in output:
            try:
                coverage_str = output.split("actual: ")[1].split("%")[0]
                coverage = float(coverage_str)
            except (IndexError, ValueError):
                pass
        
        # Check if the coverage meets the minimum requirement
        success = coverage >= self.min_coverage
        
        # Parse detailed file information if verbose
        files = []
        if verbose:
            lines = output.split("\n")
            in_table = False
            for line in lines:
                if "| Name " in line:
                    in_table = True
                    continue
                if in_table and "| TOTAL" in line:
                    break
                if in_table and "| " in line and " |" in line:
                    parts = line.split("|")
                    if len(parts) >= 6:
                        file_name = parts[1].strip()
                        total = parts[2].strip()
                        miss = parts[3].strip()
                        cover = parts[4].strip()
                        cover_pct = parts[5].strip()
                        
                        files.append({
                            "file": file_name,
                            "total": total,
                            "miss": miss,
                            "cover": cover,
                            "cover_pct": cover_pct
                        })
        
        # Create the report
        report = {
            "success": success,
            "coverage": coverage,
            "min_coverage": self.min_coverage,
            "files": files,
            "output": output
        }
        
        # Save the report to a file
        report_path = self.output_dir / "doc_coverage_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """
        Print a human-readable version of the documentation coverage report.
        
        Args:
            report: The documentation coverage report to print.
        """
        print("\n" + "=" * 80)
        print("DOCUMENTATION COVERAGE REPORT")
        print("=" * 80)
        
        # Print overall coverage
        print(f"\nOverall Coverage: {report['coverage']:.1f}% (Minimum: {report['min_coverage']:.1f}%)")
        if report["success"]:
            print("Status: PASSED")
        else:
            print("Status: FAILED")
        
        # Print files with low coverage
        if report["files"]:
            print("\nFiles with low coverage:")
            print("-" * 80)
            for file in report["files"]:
                if file["file"].strip() and "%" in file["cover_pct"]:
                    try:
                        cover_pct = float(file["cover_pct"].replace("%", ""))
                        if cover_pct < self.min_coverage:
                            print(f"{file['file']}: {file['cover_pct']}")
                    except ValueError:
                        pass
        
        print("\n" + "=" * 80)
        print("END OF REPORT")
        print("=" * 80 + "\n")
    
    def generate_badge(self) -> str:
        """
        Generate a documentation coverage badge.
        
        Returns:
            The path to the generated badge.
        """
        # Analyze coverage
        report = self.analyze_coverage()
        
        # Determine badge color
        if report["coverage"] >= 90:
            color = "brightgreen"
        elif report["coverage"] >= 80:
            color = "green"
        elif report["coverage"] >= 70:
            color = "yellowgreen"
        elif report["coverage"] >= 60:
            color = "yellow"
        else:
            color = "red"
        
        # Generate badge URL
        badge_url = f"https://img.shields.io/badge/doc%20coverage-{report['coverage']:.1f}%25-{color}"
        
        # Save badge URL to a file
        badge_path = self.output_dir / "doc_coverage_badge.txt"
        with open(badge_path, "w") as f:
            f.write(badge_url)
        
        return str(badge_path)


def analyze_doc_coverage(src_dir: str = "src/pyport", min_coverage: float = 80.0, verbose: bool = True) -> Dict[str, Any]:
    """
    Analyze documentation coverage for a package.
    
    Args:
        src_dir: The directory containing the source code to analyze.
        min_coverage: The minimum acceptable documentation coverage percentage.
        verbose: Whether to include detailed information in the output.
        
    Returns:
        A dictionary with the documentation coverage analysis results.
    """
    analyzer = DocCoverageAnalyzer(src_dir, min_coverage)
    report = analyzer.analyze_coverage(verbose)
    analyzer.print_report(report)
    return report


if __name__ == "__main__":
    # If run directly, analyze documentation coverage for PyPort
    analyze_doc_coverage()
