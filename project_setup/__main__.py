"""Entry point for running project_setup as a module."""

import argparse

from .manager import ProjectSetupManager, SetupOptions


def main() -> None:
    """Main entry point for project setup."""
    parser = argparse.ArgumentParser(
        description="Run the OnlyDjango project setup.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name to set (default: onlydjango).",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without prompts; use defaults or CLI flags.",
    )

    bool_opt = {"action": argparse.BooleanOptionalAction, "default": None}
    parser.add_argument(
        "--check-docker-ports",
        **bool_opt,
        help="Display Docker ports before setup (default: true).",
    )
    parser.add_argument(
        "--update-project-name",
        **bool_opt,
        help="Update pyproject.toml with the project name (default: true).",
    )
    parser.add_argument(
        "--create-env",
        **bool_opt,
        help="Create .env from env.sample (default: true).",
    )
    parser.add_argument(
        "--configure-ports",
        **bool_opt,
        help="Find/update Redis/PostgreSQL ports (default: true).",
    )
    parser.add_argument(
        "--redis-port",
        type=int,
        help="Redis port to write into .env and docker-compose.",
    )
    parser.add_argument(
        "--postgres-port",
        type=int,
        help="PostgreSQL port to write into .env and docker-compose.",
    )
    parser.add_argument(
        "--dev-server-port",
        type=int,
        help="Django dev server port to write into .env.",
    )
    parser.add_argument(
        "--configure-docker-compose",
        **bool_opt,
        help="Add project name to docker-compose file (default: true).",
    )
    parser.add_argument(
        "--install-npm",
        **bool_opt,
        help="Run npm install (default: true).",
    )
    parser.add_argument(
        "--start-docker-compose",
        **bool_opt,
        help="Start Docker Compose services (default: false).",
    )
    parser.add_argument(
        "--run-migrations",
        **bool_opt,
        help="Run database migrations (default: false).",
    )
    parser.add_argument(
        "--start-dev-server",
        **bool_opt,
        help="Start Django development server (default: false).",
    )

    args = parser.parse_args()
    options = SetupOptions(
        project_name=args.project_name,
        check_docker_ports=args.check_docker_ports,
        update_project_name=args.update_project_name,
        create_env=args.create_env,
        configure_ports=args.configure_ports,
        redis_port=args.redis_port,
        postgres_port=args.postgres_port,
        dev_server_port=args.dev_server_port,
        configure_docker_compose=args.configure_docker_compose,
        install_npm=args.install_npm,
        start_docker_compose=args.start_docker_compose,
        run_migrations=args.run_migrations,
        start_dev_server=args.start_dev_server,
    )

    setup_manager = ProjectSetupManager()
    setup_manager.run_setup(options=options, interactive=not args.non_interactive)


if __name__ == "__main__":
    main()
