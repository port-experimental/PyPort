import sys
from pathlib import Path

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig

from utilz.local_cicd.svc.badger_svc import Badger
from utilz.local_cicd.svc.build_svc import build_package
from utilz.local_cicd.svc.cleanup_svc import cleanup
from utilz.local_cicd.svc.lint_svc import lint_code
from utilz.local_cicd.svc.scanner_svc import CodeScanner
from utilz.local_cicd.svc.ship_svc import ship_package
from utilz.local_cicd.svc.test_svc import run_tests

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main():
    """Main menu-driven CI/CD script."""
    cicd_cfg = CicdConfig()
    scanner = CodeScanner(cicd_cfg)
    badger = Badger(cicd_cfg)
    while True:
        print("\nCI/CD Menu:")
        print("1) Test")
        print("2) Lint")
        print("3) Build")
        print("4) Scan-all")
        print("5) Build + Ship + Cleanup")
        print("6) Cleanup only")
        print("7) Exit")

        try:
            choice = input("Enter your choice (0-5): ").strip()

            if choice == '1':
                run_tests(cicd_cfg)
            elif choice == '2':
                lint_code(cicd_cfg)
            elif choice == '3':
                build_package(cicd_cfg)
            elif choice == '4':
                scanner.run_all_scans()
            elif choice == '5':
                badger.update_all_badges()
                build_package(cicd_cfg)
                ship_package(cicd_cfg)
                cleanup(cicd_cfg)
            elif choice == '6':
                cleanup(cicd_cfg)
            elif choice == '7':
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
