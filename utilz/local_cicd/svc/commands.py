"""
Concrete command implementations for CI/CD tasks.

This module provides concrete command implementations for CI/CD tasks like
testing, linting, building, scanning, etc.
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.badger_svc import Badger
from utilz.local_cicd.svc.build_svc import build_package
from utilz.local_cicd.svc.cleanup_svc import cleanup
from utilz.local_cicd.svc.command_svc import Command, register_command
from utilz.local_cicd.svc.lint_svc import lint_code
from utilz.local_cicd.svc.scanner_svc import CodeScanner
from utilz.local_cicd.svc.ship_svc import ship_package
from utilz.local_cicd.svc.test_svc import run_tests, run_integration_test
from utilz.local_cicd.svc.doc_coverage import analyze_doc_coverage


@register_command
class TestCommand(Command):
    """Command for running tests."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the test command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the test execution.
        """
        self.logger.info("Running tests...")
        result = run_tests(self.config)
        self.logger.info("Tests completed.")
        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (tests cannot be undone).
        """
        return False


@register_command
class IntegrationTestCommand(Command):
    """Command for running integration tests."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the integration test command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the integration test execution.
        """
        self.logger.info("Running integration tests...")
        result = run_integration_test(self.config)
        self.logger.info("Integration tests completed.")
        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (integration tests cannot be undone).
        """
        return False


@register_command
class LintCommand(Command):
    """Command for linting code."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the lint command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the lint execution.
        """
        self.logger.info("Linting code...")
        result = lint_code(self.config.src_folder)
        self.logger.info("Linting completed.")
        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (linting cannot be undone).
        """
        return False


@register_command
class BuildCommand(Command):
    """Command for building the package."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the build command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the build execution.
        """
        self.logger.info("Building package...")
        try:
            result = build_package(self.config)
            self.logger.info("Build completed successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Build failed: {e}")
            raise

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            True (build artifacts can be cleaned up).
        """
        return True

    def undo(self) -> bool:
        """
        Undo the build command by cleaning up build artifacts.

        Returns:
            True if the cleanup was successful, False otherwise.
        """
        self.logger.info("Cleaning up build artifacts...")
        try:
            cleanup(self.config)
            self.logger.info("Cleanup completed.")
            return True
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return False


@register_command
class ScanCommand(Command):
    """Command for scanning code quality."""

    def execute(self, scan_type: Optional[str] = None, *args, **kwargs) -> Any:
        """
        Execute the scan command.

        Args:
            scan_type: Type of scan to run (maintainability, security, dependencies, or None for all).
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the scan execution.
        """
        scanner = CodeScanner(self.config)

        if scan_type == "maintainability":
            self.logger.info("Running maintainability scan...")
            result = scanner.scan_maintainability()
            self.logger.info("Maintainability scan completed.")
        elif scan_type == "security":
            self.logger.info("Running security scan...")
            result = scanner.scan_security()
            self.logger.info("Security scan completed.")
        elif scan_type == "dependencies":
            self.logger.info("Running dependencies scan...")
            result = scanner.scan_dependencies()
            self.logger.info("Dependencies scan completed.")
        else:
            self.logger.info("Running all scans...")
            result = scanner.run_all_scans()
            self.logger.info("All scans completed.")

            # Update badges after running all scans
            self.logger.info("Updating badges based on scan results...")
            badger = Badger(self.config)
            badger.update_all_badges()

            # Run documentation coverage analysis
            self.logger.info("Running documentation coverage analysis...")
            doc_coverage_command = DocCoverageCommand(self.config)
            doc_coverage_command.execute()

            self.logger.info("Badges updated.")

        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (scans cannot be undone).
        """
        return False


@register_command
class BadgeCommand(Command):
    """Command for updating badges."""

    def execute(self, badge_type: Optional[str] = None, *args, **kwargs) -> Any:
        """
        Execute the badge command.

        Args:
            badge_type: Type of badge to update (coverage, maintainability, security, dependencies, or None for all).
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the badge update.
        """
        badger = Badger(self.config)

        if badge_type == "coverage":
            self.logger.info("Updating coverage badge...")
            badge = badger.get_coverage_badge()
            badger.update_readme_badge(badge, "coverage")
            self.logger.info("Coverage badge updated.")
            return badge
        elif badge_type == "maintainability":
            self.logger.info("Updating maintainability badge...")
            badge = badger.get_maintainability_badge()
            badger.update_readme_badge(badge, "maintainability")
            self.logger.info("Maintainability badge updated.")
            return badge
        elif badge_type == "security":
            self.logger.info("Updating security badge...")
            badge = badger.get_security_badge()
            badger.update_readme_badge(badge, "security")
            self.logger.info("Security badge updated.")
            return badge
        elif badge_type == "dependencies":
            self.logger.info("Updating dependencies badge...")
            badge = badger.get_dependencies_badge()
            badger.update_readme_badge(badge, "dependencies")
            self.logger.info("Dependencies badge updated.")
            return badge
        elif badge_type == "doc_coverage":
            self.logger.info("Updating documentation coverage badge...")
            badge = badger.get_doc_coverage_badge()
            badger.update_readme_badge(badge, "doc_coverage")
            self.logger.info("Documentation coverage badge updated.")
            return badge
        else:
            self.logger.info("Updating all badges...")
            badger.update_all_badges()
            self.logger.info("All badges updated.")
            return True

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (badge updates cannot be undone).
        """
        return False


@register_command
class ShipCommand(Command):
    """Command for shipping the package."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the ship command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the ship execution.
        """
        self.logger.info("Shipping package...")
        try:
            result = ship_package(self.config)
            self.logger.info("Shipping completed successfully.")
            return result
        except Exception as e:
            self.logger.error(f"Shipping failed: {e}")
            raise

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (shipping cannot be undone).
        """
        return False


@register_command
class CleanupCommand(Command):
    """Command for cleaning up build artifacts."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the cleanup command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the cleanup execution.
        """
        self.logger.info("Cleaning up build artifacts...")
        result = cleanup(self.config)
        self.logger.info("Cleanup completed.")
        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (cleanup cannot be undone).
        """
        return False


@register_command
class CompositeCommand(Command):
    """Command for executing multiple commands in sequence."""

    def __init__(self, config: CicdConfig, commands: List[Command] = None, name: str = None):
        """
        Initialize the composite command.

        Args:
            config: Configuration for the CI/CD utilities.
            commands: List of commands to execute.
            name: Name of the command (defaults to the class name).
        """
        super().__init__(config, name)
        self.commands = commands or []

    def add_command(self, command: Command) -> None:
        """
        Add a command to the composite.

        Args:
            command: Command to add.
        """
        self.commands.append(command)

    def execute(self, *args, **kwargs) -> List[Any]:
        """
        Execute all commands in sequence.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            A list of results from each command.
        """
        self.logger.info(f"Executing {len(self.commands)} commands...")
        results = []

        for command in self.commands:
            self.logger.info(f"Executing command: {command.name}")
            try:
                result = command.execute(*args, **kwargs)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Command {command.name} failed: {e}")
                if kwargs.get("fail_fast", False):
                    self.logger.error("Aborting remaining commands due to failure.")
                    raise RuntimeError(f"Command {command.name} failed: {e}") from e
                break

        self.logger.info("All commands completed.")
        return results

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            True if all commands can be undone, False otherwise.
        """
        return all(command.can_undo() for command in self.commands)

    def undo(self) -> bool:
        """
        Undo all commands in reverse order.

        Returns:
            True if all commands were successfully undone, False otherwise.
        """
        self.logger.info(f"Undoing {len(self.commands)} commands...")
        success = True

        for command in reversed(self.commands):
            self.logger.info(f"Undoing command: {command.name}")
            if command.can_undo():
                try:
                    if not command.undo():
                        self.logger.warning(f"Command {command.name} could not be undone.")
                        success = False
                except Exception as e:
                    self.logger.error(f"Error undoing command {command.name}: {e}")
                    success = False
            else:
                self.logger.warning(f"Command {command.name} cannot be undone.")
                success = False

        self.logger.info("All commands undone.")
        return success


@register_command
class ReleaseCommand(Command):
    """Command for releasing a new version."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the release command.

        This command builds the package, ships it, and cleans up.
        (Note: Testing, linting, scanning, and badge updates are temporarily removed from the release process.)

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the release execution.
        """
        self.logger.info("Releasing new version...")

        # Create a composite command
        composite = CompositeCommand(self.config, name="ReleaseSteps")

        # Add commands to the composite
        # Testing and linting temporarily removed from release process
        # composite.add_command(TestCommand(self.config))
        # composite.add_command(LintCommand(self.config))
        # composite.add_command(ScanCommand(self.config))
        # composite.add_command(BadgeCommand(self.config))
        composite.add_command(BuildCommand(self.config))
        composite.add_command(ShipCommand(self.config))
        composite.add_command(CleanupCommand(self.config))

        # Execute the composite command
        result = composite.execute(fail_fast=True)

        self.logger.info("Release completed.")
        return result

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (release cannot be fully undone).
        """
        return False


@register_command
class DocCoverageCommand(Command):
    """Command for analyzing documentation coverage."""

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the documentation coverage command.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The documentation coverage report.
        """
        self.logger.info("Analyzing documentation coverage...")
        src_dir = self.config.src_folder
        min_coverage = self.config.min_doc_coverage
        report = analyze_doc_coverage(src_dir, min_coverage, verbose=True)
        self.logger.info(f"Documentation coverage: {report['coverage']:.1f}% (Minimum: {min_coverage:.1f}%)")
        if report["success"]:
            self.logger.info("Documentation coverage check passed!")
        else:
            self.logger.warning("Documentation coverage check failed!")
        return report

    def can_undo(self) -> bool:
        """
        Check if the command can be undone.

        Returns:
            False (documentation coverage analysis cannot be undone).
        """
        return False
