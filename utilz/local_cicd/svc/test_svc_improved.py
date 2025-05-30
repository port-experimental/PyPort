import os
import unittest
import coverage
import inspect
from typing import Dict, Any, List, Optional, Union

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig


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
    test_runner = unittest.TextTestRunner()
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

    # Load all test modules except test_integration.py and tests in snapshots folder
    test_suite = unittest.TestSuite()
    for test_file in os.listdir('tests'):
        if (test_file.startswith('test_') and 
            test_file.endswith('.py') and 
            test_file != 'test_integration.py' and
            'snapshots' not in test_file):
            module_name = f'tests.{test_file[:-3]}'
            try:
                suite = test_loader.loadTestsFromName(module_name)
                test_suite.addTest(suite)
            except Exception as e:
                print(f"Error loading tests from {module_name}: {e}")

    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=0)  # Minimal output
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

    # Discover and run tests using unittest, excluding the integration test and snapshots
    test_loader = unittest.TestLoader()

    # Load all test modules except test_integration.py and tests in snapshots folder
    test_suite = unittest.TestSuite()
    for test_file in os.listdir('tests'):
        if (test_file.startswith('test_') and 
            test_file.endswith('.py') and 
            test_file != 'test_integration.py' and
            'snapshots' not in test_file):
            module_name = f'tests.{test_file[:-3]}'
            try:
                suite = test_loader.loadTestsFromName(module_name)
                test_suite.addTest(suite)
            except Exception as e:
                print(f"Error loading tests from {module_name}: {e}")

    # Run the tests with full output
    test_runner = unittest.TextTestRunner(verbosity=2)  # Detailed output
    result = test_runner.run(test_suite)

    # Determine exit code based on test success
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    return exit_code


def run_tests(cicd_cfg: CicdConfig):
    """Run tests with coverage and Code Climate test reporter integration."""
    print("Running tests with coverage and Code Climate test reporter...")
    print("Integration test (test_integration.py) will be excluded from this run.")

    # Determine the project root (assumes this file is in a subfolder, e.g. 'scripts')
    os.chdir(cicd_cfg.project_root)

    # Initialize coverage measurement.
    cov = coverage.Coverage(config_file=cicd_cfg.coverage_config_file)
    cov.erase()
    cov.start()

    # Discover and run tests using unittest, excluding the integration test
    test_loader = unittest.TestLoader()

    # Load all test modules except test_integration.py
    test_suite = unittest.TestSuite()
    for test_file in os.listdir('tests'):
        if test_file.startswith('test_') and test_file.endswith('.py') and test_file != 'test_integration.py':
            module_name = f'tests.{test_file[:-3]}'
            try:
                suite = test_loader.loadTestsFromName(module_name)
                test_suite.addTest(suite)
            except Exception as e:
                print(f"Error loading tests from {module_name}: {e}")

    # Run the tests
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    cov.stop()
    print("\nDetailed Coverage Report:")
    cov.report(show_missing=True)
    cov.save()

    # Determine exit code based on test success (0 if all passed, non-zero otherwise)
    exit_code = 0 if result.wasSuccessful() else 1

    print(f"All tests completed. Exiting with code {exit_code}.")
    return exit_code
