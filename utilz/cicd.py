import os
import subprocess
import sys
import unittest


from pathlib import Path

import coverage
import platform

import shutil
import glob
import re

from io import StringIO

from dotenv import load_dotenv
from flake8.api import legacy as flake8_api


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_version_in_toml():

    version_file_path = os.path.join(PROJECT_ROOT, "version.txt")
    toml_file_path = os.path.join(PROJECT_ROOT, "src" ,"pyproject.toml")

    with open(version_file_path, "r") as f:
        new_version = f.read().strip()  # Remove any extra whitespace or newlines

        # Read the pyproject.toml file
        with open(toml_file_path, "r") as f2:
            content = f2.read()

        # Regex to match lines like 'version = "0.1.2"'
        version_pattern = r'(?m)^(\s*version\s*=\s*")([^"]+)(")'

        # Use a replacement function to avoid raw-string confusion with \1, \3, etc.
        def replace_version(match):
            # match.group(1) = leading text up to first quote, e.g. 'version = "'
            # match.group(2) = current version number
            # match.group(3) = closing quote
            return f'{match.group(1)}{new_version}{match.group(3)}'

        # Replacements are now done safely via our function
        updated_content = re.sub(version_pattern, replace_version, content)

        # Write the updated content back to the TOML file
        with open(toml_file_path, "w") as f3:
            f3.write(updated_content)

def update_readme_badge(new_badge):
    """Update README.md with coverage badge."""
    src_readme_path = os.path.join(PROJECT_ROOT, 'src', 'README.md')
    gh_readme_path = os.path.join(PROJECT_ROOT, 'README.md')

    # Read existing README
    with open(src_readme_path, 'r') as f:
        content = f.read()

    # Regex to replace or insert coverage badge

    badge_pattern = r'!\[Coverage\]\(.*\)'

    if re.search(badge_pattern, content):
        # Replace existing badge
        updated_content = re.sub(badge_pattern, new_badge, content)
    else:
        # Insert badge at the top of the README
        updated_content = new_badge + '\n\n' + content

    # Write updated README
    with open(src_readme_path, 'w') as file1, open(gh_readme_path, "w") as file2:
        file1.write(updated_content)
        file2.write(updated_content)

def generate_coverage_badge(cov):
    """Generate coverage badge using Coverage report."""
    # Write coverage report to console


    # Capture coverage report output
    report_output = StringIO()
    sys.stdout = report_output
    cov.report(show_missing=False)
    sys.stdout = sys.__stdout__

    # Parse the output
    output_lines = report_output.getvalue().strip().split('\n')

    # Last line typically contains the total coverage percentage
    total_line = output_lines[-1]
    coverage_percentage = float(total_line.split()[-1].rstrip('%'))

    # Determine badge color
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

    # Generate badge URL
    badge_url = f"https://img.shields.io/badge/coverage-{coverage_percentage:.2f}%25-{color}"

    return badge_url, coverage_percentage

def run_tests():
    """Run tests with coverage and Code Climate test reporter integration."""
    print("Running tests with coverage and Code Climate test reporter...")

    # Determine the project root (assumes this file is in a subfolder, e.g. 'scripts')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    # Initialize coverage measurement.
    cov = coverage.Coverage(
        omit=[
            '**/__init__.py',  # Ignore __init__.py files
            'tests/*',         # Ignore tests folder
            '*/test_*.py',     # Ignore individual test files
        ]
    )
    cov.start()

    # Discover and run tests using unittest.
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    cov.stop()
    print("\nDetailed Coverage Report:")
    cov.report(show_missing=True)

    # Generate an LCOV coverage report (requires coverage-lcov plugin)
    try:
        subprocess.run(["coverage", "lcov", "-o", "lcov.info"], check=True)
        print("LCOV report generated at lcov.info")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate LCOV report: {e}", file=sys.stderr)

    # Determine exit code based on test success (0 if all passed, non-zero otherwise)
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    # sys.exit(exit_code)

def lint_code():
    """Run linting on the source code."""
    print("Running lint...")
    src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')

    try:
        os.chdir(src_path)

        style_guide = flake8_api.get_style_guide(
            max_line_length=120,
            ignore=['E203', 'E501', 'W503']
        )
        report = style_guide.check_files(['.'])

        if report.get_statistics('E') or report.get_statistics('W'):
            raise Exception("Linting errors found")

        print("Linting passed.")
    except Exception as e:
        print(f"Linting failed: {e}", file=sys.stderr)

def build_package():
    """Build the Python package using a subprocess call to `python -m build`."""
    print("Building package...")

    # Get the path two levels up (assuming the same structure as your original code).
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(project_root, 'src')
    venv_dir = os.path.join(project_root , '.venv')
    if platform.system().lower().startswith("win"):
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(venv_dir, "bin", "python")

    try:
        os.chdir(src_path)
        update_version_in_toml()
        subprocess.run([python_executable, '-m', 'build', '--no-isolation'], cwd=src_path, check=True)
        print("Build completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)


def ship_package():
    """
    Uploads the package to PyPI using Twine.
    Assumes the .pypirc file is located in the utilz directory and the dist directory is in src.
    """
    repo_config = os.path.join("..", "utilz", ".pypirc")  # Path to .pypirc
    dist_path = os.path.join("dist", "*")  # Path to distribution files

    try:
        print("Shipping package...")
        subprocess.run(["twine", "upload", "--config-file", repo_config, dist_path], check=True)
        print("Ship completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Ship failed: {e}")


def cleanup():
    """Clean up build artifacts."""
    print("Running cleanup...")
    src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')

    try:
        os.chdir(src_path)

        dist_path = os.path.join(src_path, 'dist')
        if os.path.exists(dist_path):
            shutil.rmtree(dist_path)
            print("Removed dist directory.")

        for item in glob.glob('*.egg-info'):
            shutil.rmtree(item)
            print(f"Removed {item}.")

        print("Cleanup completed.")
    except Exception as e:
        print(f"Cleanup failed: {e}", file=sys.stderr)


def main():
    """Main menu-driven CI/CD script."""
    while True:
        print("\nCI/CD Menu:")
        print("0) Test")
        print("1) Lint")
        print("2) Build")
        print("3) Build + Ship + Cleanup")
        print("4) Cleanup only")
        print("5) Exit")

        try:
            choice = input("Enter your choice (0-5): ").strip()

            if choice == '0':
                run_tests()
            elif choice == '1':
                lint_code()
            elif choice == '2':
                build_package()
            elif choice == '3':
                build_package()
                ship_package()
                cleanup()
            elif choice == '4':
                cleanup()
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()