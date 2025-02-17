import os
import unittest
import coverage
import inspect

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.badger_svc import Badger
from utilz.local_cicd.svc.scanner_svc import CodeScanner


def list_test_files(suite: unittest.TestSuite) -> list[str]:
    """
    Recursively walk a TestSuite to collect the file paths of all test cases.
    """
    test_files = set()
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            # Recursively process nested TestSuites.
            test_files.update(list_test_files(test))
        else:
            try:
                # Get the file where the test case class is defined.
                file_path = inspect.getfile(test.__class__)
                test_files.add(file_path)
            except TypeError:
                pass
    return list(test_files)

def run_tests(cicd_cfg: CicdConfig):
    """Run tests with coverage and Code Climate test reporter integration."""
    print("Running tests with coverage and Code Climate test reporter...")

    # Determine the project root (assumes this file is in a subfolder, e.g. 'scripts')
    os.chdir(cicd_cfg.project_root)

    # Initialize coverage measurement.
    cov = coverage.Coverage(config_file=cicd_cfg.coverage_config_file)
    cov.start()

    # Discover and run tests using unittest.
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    # files = list_test_files(test_suite)
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    cov.stop()
    print("\nDetailed Coverage Report:")
    cov.report(show_missing=True)
    cov.save()

    # badge_url = self.badger.generate_coverage_badge(cov)
    badger = Badger(cicd_cfg)
    scanner = CodeScanner(cicd_cfg)
    scanner.scan_coverage_badge()
    badger.update_readme_badge(badge_url, "coverage")
    # badger.update_readme_badge(badge_url, "coverage")

    # Determine exit code based on test success (0 if all passed, non-zero otherwise)
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
