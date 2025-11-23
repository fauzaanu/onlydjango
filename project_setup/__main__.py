"""Entry point for running project_setup as a module."""

from .manager import ProjectSetupManager


def main() -> None:
    """Main entry point for project setup."""
    setup_manager = ProjectSetupManager()
    setup_manager.run_setup()


if __name__ == "__main__":
    main()
