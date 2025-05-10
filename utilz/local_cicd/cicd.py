import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.command_svc import CommandInvoker, CommandFactory
from utilz.local_cicd.svc.commands import (
    TestCommand, LintCommand, BuildCommand, ScanCommand,
    BadgeCommand, ShipCommand, CleanupCommand, CompositeCommand, ReleaseCommand
)
from utilz.local_cicd.svc.logging_svc import (
    get_logger, configure_logging, LOG_LEVEL_INFO, LOG_FORMAT_STANDARD, LOG_OUTPUT_CONSOLE
)


# Configure logging
configure_logging({
    'level': LOG_LEVEL_INFO,
    'format': LOG_FORMAT_STANDARD,
    'output': LOG_OUTPUT_CONSOLE
})

# Create a logger
logger = get_logger('cicd')

# Create a command invoker
invoker = CommandInvoker()


def execute_choice(choice, config):
    """Executes the command associated with the given choice.

    Args:
        choice: The choice to execute (1-7).
        config: The CI/CD configuration.

    Returns:
        True if the program should continue, False if it should exit.
    """
    try:
        if choice == '1':
            # Test
            command = TestCommand(config)
            invoker.execute(command)
        elif choice == '2':
            # Lint
            command = LintCommand(config)
            invoker.execute(command)
        elif choice == '3':
            # Build
            command = BuildCommand(config)
            invoker.execute(command)
        elif choice == '4':
            # Scan all
            command = ScanCommand(config)
            invoker.execute(command)
        elif choice == '5':
            # Release (update badges, build, ship, cleanup)
            command = ReleaseCommand(config)
            invoker.execute(command)
        elif choice == '6':
            # Cleanup
            command = CleanupCommand(config)
            invoker.execute(command)
        elif choice == '7':
            logger.info("Exiting...")
            return False
        else:
            logger.warning(f"Invalid option: {choice}. Please try again.")
    except Exception as e:
        logger.error(f"Error executing command: {e}")

    return True


def interactive_mode(config):
    """Interactive mode using standard input().

    Args:
        config: The CI/CD configuration.
    """
    logger.info("Starting interactive mode...")

    while True:
        print("\nCI/CD Menu:")
        print("1) Test")
        print("2) Lint")
        print("3) Build")
        print("4) Scan-all (maintainability, security, etc.)")
        print("5) Release (Update Badges + Build + Ship + Cleanup)")
        print("6) Cleanup only")
        print("7) Exit")

        try:
            choice = input("Enter your choice (1-7): ").strip()
            if not execute_choice(choice, config):
                break
        except KeyboardInterrupt:
            logger.warning("Operation cancelled by user.")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    # Show command history
    history = invoker.get_history()
    if history:
        logger.info("Command history:")
        for i, (name, result) in enumerate(history, 1):
            logger.info(f"{i}. {name}")


def main():
    """Main entry point for the CI/CD utility."""
    # Create a configuration
    config = CicdConfig()

    # If command-line arguments are provided, process them as a comma-separated list
    if len(sys.argv) > 1:
        logger.info("Running in command-line mode...")
        input_str = " ".join(sys.argv[1:])
        options = [opt.strip() for opt in input_str.split(',') if opt.strip()]

        for opt in options:
            logger.info(f"Executing option: {opt}")
            if not execute_choice(opt, config):
                break
    else:
        # No command-line arguments, run in interactive mode
        interactive_mode(config)

    logger.info("CI/CD utility completed.")


if __name__ == '__main__':
    main()
