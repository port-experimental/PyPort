import os
import sys
import time
import unittest
import coverage
import inspect
from typing import Dict, Any, List, Optional, Union

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


class ProgressTextTestResult(unittest.TextTestResult):
    """Custom test result class that shows progress during test execution."""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.total_tests = 0
        self.current_test = 0
        self.current_test_class = ""
        self.last_update_time = time.time()
        self.update_interval = 0.5  # Update progress every 0.5 seconds

    def startTest(self, test):
        """Called when a test starts."""
        super().startTest(test)
        self.current_test += 1

        # Get the test class name
        test_class = test.__class__.__name__
        if test_class != self.current_test_class:
            self.current_test_class = test_class

        # Update progress at most every update_interval seconds
        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            self._update_progress()
            self.last_update_time = current_time

    def _update_progress(self):
        """Update the progress display."""
        if self.total_tests > 0:
            percent = int(100 * self.current_test / self.total_tests)
            sys.stdout.write(f"\rRunning tests: {self.current_test}/{self.total_tests} ({percent}%) - Current: {self.current_test_class}")
            sys.stdout.flush()


class ProgressTextTestRunner(unittest.TextTestRunner):
    """Custom test runner that shows progress during test execution."""

    def __init__(self, verbosity=1, stream=None, descriptions=True, **kwargs):
        super().__init__(verbosity=verbosity, stream=stream, descriptions=descriptions, **kwargs)

    def _makeResult(self):
        """Create a test result object."""
        result = ProgressTextTestResult(self.stream, self.descriptions, self.verbosity)
        return result

    def run(self, test):
        """Run the tests."""
        # Count the total number of tests
        result = self._makeResult()
        result.total_tests = test.countTestCases()

        # Print initial progress
        sys.stdout.write(f"Running tests: 0/{result.total_tests} (0%)\n")
        sys.stdout.flush()

        # Run the tests
        startTime = time.time()
        try:
            test(result)
        finally:
            stopTime = time.time()

        # Print final progress and clear the line
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()

        # Print results
        timeTaken = stopTime - startTime
        result.printErrors()

        if self.verbosity > 0:
            run = result.testsRun
            self.stream.writeln(f"Ran {run} test{'s' if run != 1 else ''} in {timeTaken:.3f}s")

        self.stream.writeln()

        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                self.stream.write(f" (failures={failed}")
            if errored:
                if failed:
                    self.stream.write(", ")
                self.stream.write(f"errors={errored}")
            if failed or errored:
                self.stream.write(")")
            self.stream.writeln()
        else:
            self.stream.writeln("OK")

        return result


def discover_test_modules(test_dir: str = "tests", exclude_dirs: list = None) -> list[str]:
    """
    Discover test modules while excluding specified directories.

    Args:
        test_dir: The root test directory
        exclude_dirs: List of directory names to exclude (e.g., ['snapshots', 'integration'])

    Returns:
        List of module names that can be imported
    """
    if exclude_dirs is None:
        exclude_dirs = ['snapshots']

    test_modules = []

    # Walk through the test directory
    for root, dirs, files in os.walk(test_dir):
        # Remove excluded directories from dirs list to prevent os.walk from entering them
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Process Python test files in current directory
        for file in files:
            if file.startswith('test_') and file.endswith('.py') and file != 'test_integration.py':
                # Convert file path to module name
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                module_name = rel_path.replace(os.sep, '.').replace('.py', '')
                test_modules.append(module_name)

    return test_modules


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


def run_integration_test(cicd_cfg: CicdConfig):
    """Run the integration test to verify package import and authentication."""
    print("Running integration test...")

    # Determine the project root
    os.chdir(cicd_cfg.project_root)

    # Run the integration test specifically
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromName('tests.test_integration')
    test_runner = ProgressTextTestRunner()
    result = test_runner.run(test_suite)

    # Determine exit code based on test success
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"Integration test completed. Exiting with code {exit_code}.")
    return exit_code


def run_tests_summary(cicd_cfg: CicdConfig):
    """Run tests with coverage and display only a summary."""
    print("Running tests with summary output...")
    print("Integration test (test_integration.py) and snapshots will be excluded from this run.")

    # Determine the project root
    os.chdir(cicd_cfg.project_root)

    # Initialize coverage measurement
    cov = coverage.Coverage(config_file=cicd_cfg.coverage_config_file)
    cov.erase()
    cov.start()

    # Discover and run tests using unittest, excluding the integration test and snapshots
    test_loader = unittest.TestLoader()

    # Discover test modules excluding snapshots directory
    test_modules = discover_test_modules("tests", exclude_dirs=['snapshots'])

    # Load all discovered test modules
    test_suite = unittest.TestSuite()
    for module_name in test_modules:
        try:
            suite = test_loader.loadTestsFromName(module_name)
            test_suite.addTest(suite)
        except Exception as e:
            print(f"Error loading tests from {module_name}: {e}")

    # Run the tests with progress updates
    test_runner = ProgressTextTestRunner(verbosity=0)  # Minimal output
    result = test_runner.run(test_suite)

    # Stop coverage
    cov.stop()

    # Print summary
    print("\nTest Summary:")
    print(f"  Total tests: {result.testsRun}")
    print(f"  Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failed: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")

    # Print coverage table
    print("\nCoverage Summary:")
    cov.report(show_missing=False)
    cov.save()

    # Determine exit code based on test success
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    return exit_code


def run_tests_full(cicd_cfg: CicdConfig):
    """Run tests with full unittest output."""
    print("Running tests with full output...")
    print("Integration test (test_integration.py) and snapshots will be excluded from this run.")

    # Determine the project root
    os.chdir(cicd_cfg.project_root)

    # Initialize coverage measurement
    cov = coverage.Coverage(config_file=cicd_cfg.coverage_config_file)
    cov.erase()
    cov.start()

    # Discover and run tests using unittest, excluding the integration test and snapshots
    test_loader = unittest.TestLoader()

    # Discover test modules excluding snapshots directory
    test_modules = discover_test_modules("tests", exclude_dirs=['snapshots'])

    # Load all discovered test modules
    test_suite = unittest.TestSuite()
    for module_name in test_modules:
        try:
            suite = test_loader.loadTestsFromName(module_name)
            test_suite.addTest(suite)
        except Exception as e:
            print(f"Error loading tests from {module_name}: {e}")

    # Run the tests with full output and progress updates
    test_runner = ProgressTextTestRunner(verbosity=2)  # Detailed output
    result = test_runner.run(test_suite)

    # Stop coverage
    cov.stop()
    print("\nDetailed Coverage Report:")
    cov.report(show_missing=True)
    cov.save()

    # Determine exit code based on test success
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    return exit_code


def run_tests(cicd_cfg: CicdConfig):
    """Run tests with coverage and Code Climate test reporter integration."""
    print("Running tests with coverage and Code Climate test reporter...")
    print("Integration test (test_integration.py) and snapshots will be excluded from this run.")

    # Determine the project root (assumes this file is in a subfolder, e.g. 'scripts')
    os.chdir(cicd_cfg.project_root)

    # Initialize coverage measurement.
    cov = coverage.Coverage(config_file=cicd_cfg.coverage_config_file)
    cov.erase()
    cov.start()

    # Discover and run tests using unittest, excluding the integration test and snapshots
    test_loader = unittest.TestLoader()

    # Discover test modules excluding snapshots directory
    test_modules = discover_test_modules("tests", exclude_dirs=['snapshots'])

    # Load all discovered test modules
    test_suite = unittest.TestSuite()
    for module_name in test_modules:
        try:
            suite = test_loader.loadTestsFromName(module_name)
            test_suite.addTest(suite)
        except Exception as e:
            print(f"Error loading tests from {module_name}: {e}")

    # Run the tests with progress updates
    test_runner = ProgressTextTestRunner()
    result = test_runner.run(test_suite)

    cov.stop()
    print("\nDetailed Coverage Report:")
    cov.report(show_missing=True)
    cov.save()

    # Determine exit code based on test success (0 if all passed, non-zero otherwise)
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    return exit_code
