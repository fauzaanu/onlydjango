"""Main project setup orchestrator."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from .port_manager import PortManager
from .config_manager import ConfigManager
from .npm_manager import NpmManager

console = Console()


@dataclass
class SetupOptions:
    """Configuration options for project setup."""

    project_name: str | None = None
    check_docker_ports: bool | None = None
    update_project_name: bool | None = None
    create_env: bool | None = None
    configure_ports: bool | None = None
    redis_port: int | None = None
    postgres_port: int | None = None
    configure_docker_compose: bool | None = None
    install_npm: bool | None = None
    start_docker_compose: bool | None = None
    run_migrations: bool | None = None
    start_dev_server: bool | None = None


class ProjectSetupManager:
    """Orchestrates the entire project setup process."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config_manager = ConfigManager(self.project_root)
        self.port_manager = PortManager()
        self.npm_manager = NpmManager()

    def run_setup(
        self,
        project_name: str | None = None,
        options: SetupOptions | None = None,
        interactive: bool = True,
    ) -> None:
        """Run the complete project setup."""
        if options is None:
            options = SetupOptions()
        if project_name and options.project_name is None:
            options.project_name = project_name

        console.print(Panel.fit(
            "[bold cyan]Django Project Setup[/bold cyan]",
            border_style="cyan"
        ))

        project_name = self._resolve_project_name(options, interactive)

        console.print(f"\n[bold green]Setting up:[/bold green] {project_name}\n")

        # Display current Docker ports
        check_docker_ports = self._resolve_confirm(
            options.check_docker_ports,
            prompt="[cyan]Check Docker ports?[/cyan]",
            default=True,
            interactive=interactive,
        )
        if check_docker_ports:
            self.port_manager.display_docker_ports()

        # Update project name
        console.print("\n[bold cyan]Step 1/5:[/bold cyan] Update project name")
        update_project_name = self._resolve_confirm(
            options.update_project_name,
            prompt=f"  Update project name to '{project_name}'?",
            default=True,
            interactive=interactive,
        )
        if update_project_name:
            self.config_manager.update_pyproject_name(project_name)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Create .env
        console.print("\n[bold cyan]Step 2/5:[/bold cyan] Create .env file")
        create_env = self._resolve_confirm(
            options.create_env,
            prompt="  Create .env from env.sample?",
            default=True,
            interactive=interactive,
        )
        if create_env:
            if not self.config_manager.create_env_from_sample():
                return
        else:
            console.print("[dim]  Skipped[/dim]")

        # Find and update ports
        console.print("\n[bold cyan]Step 3/5:[/bold cyan] Configure ports")
        configure_ports = self._resolve_confirm(
            options.configure_ports,
            prompt="  Find free ports and update configuration?",
            default=True,
            interactive=interactive,
        )
        if configure_ports:
            redis_port, postgres_port = self._resolve_ports(options)
            console.print(
                "  [green]✓[/green] Redis: [yellow]"
                f"{redis_port}[/yellow] | PostgreSQL: [yellow]{postgres_port}[/yellow]"
            )

            self.config_manager.update_env_ports(redis_port, postgres_port)
            self.config_manager.update_docker_compose_ports(redis_port, postgres_port)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Add docker-compose project name
        console.print("\n[bold cyan]Step 4/5:[/bold cyan] Configure docker-compose")
        configure_compose = self._resolve_confirm(
            options.configure_docker_compose,
            prompt="  Add project name to docker-compose?",
            default=True,
            interactive=interactive,
        )
        if configure_compose:
            self.config_manager.add_docker_compose_project_name(project_name)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Install npm dependencies
        console.print("\n[bold cyan]Step 5/5:[/bold cyan] Install npm dependencies")
        install_npm = self._resolve_confirm(
            options.install_npm,
            prompt="  Run npm install?",
            default=True,
            interactive=interactive,
        )
        if install_npm:
            self.npm_manager.install_dependencies()
        else:
            console.print("[dim]  Skipped[/dim]")

        # Post-setup actions
        self._run_post_setup_actions(options, interactive=interactive)

    def _resolve_project_name(self, options: SetupOptions, interactive: bool) -> str:
        """Resolve the project name from options or prompt."""
        if options.project_name:
            return options.project_name
        if interactive:
            return Prompt.ask(
                "\n[cyan]Enter your project name[/cyan]",
                default="onlydjango",
            )
        return "onlydjango"

    def _resolve_confirm(
        self,
        value: bool | None,
        *,
        prompt: str,
        default: bool,
        interactive: bool,
    ) -> bool:
        """Resolve a yes/no choice from options or prompt."""
        if value is not None:
            return value
        if interactive:
            return Confirm.ask(prompt, default=default)
        return default

    def _resolve_ports(self, options: SetupOptions) -> tuple[int, int]:
        """Resolve Redis and Postgres ports."""
        redis_port = options.redis_port or self.port_manager.find_free_port(6379)
        postgres_port = options.postgres_port or self.port_manager.find_free_port(5432)

        if redis_port == postgres_port:
            console.print(
                "[yellow]⚠[/yellow] Redis and PostgreSQL ports are the same; "
                "searching for a new PostgreSQL port."
            )
            postgres_port = self.port_manager.find_free_port(postgres_port + 1)

        return redis_port, postgres_port

    def _run_post_setup_actions(self, options: SetupOptions, *, interactive: bool) -> None:
        """Run post-setup actions like starting Docker, migrations, etc."""
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]Setup Completed![/bold green]",
            border_style="green"
        ))

        # Start Docker Compose
        console.print("\n[bold cyan]Post-Setup Actions[/bold cyan]")
        start_docker = self._resolve_confirm(
            options.start_docker_compose,
            prompt="\n[cyan]Start Docker Compose services?[/cyan]",
            default=False,
            interactive=interactive,
        )
        if start_docker:
            self._start_docker_compose()

        # Run migrations
        run_migrations = self._resolve_confirm(
            options.run_migrations,
            prompt="\n[cyan]Run database migrations?[/cyan]",
            default=False,
            interactive=interactive,
        )
        if run_migrations:
            self._run_migrations()

        # Start development server
        start_server = self._resolve_confirm(
            options.start_dev_server,
            prompt="\n[cyan]Start development server?[/cyan]",
            default=False,
            interactive=interactive,
        )
        if start_server:
            console.print("\n[yellow]Starting server...[/yellow]")
            console.print("[dim]Press Ctrl+C to stop[/dim]\n")
            self._start_dev_server()
        else:
            self._print_manual_steps()

    def _start_docker_compose(self) -> None:
        """Start Docker Compose services."""
        try:
            console.print("\n[yellow]Starting Docker Compose...[/yellow]")
            result = subprocess.run(
                ["docker", "compose", "-f", "onlydjango/dev_helpers/dev.docker-compose.yml", "up", "-d"],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print("[green]✓[/green] Docker services started")
            if result.stdout:
                console.print(f"[dim]{result.stdout}[/dim]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗[/red] Failed to start Docker services")
            if e.stderr:
                console.print(f"[dim]{e.stderr}[/dim]")
        except FileNotFoundError:
            console.print("[red]✗[/red] Docker not found in PATH")

    def _run_migrations(self) -> None:
        """Run Django migrations."""
        try:
            console.print("\n[yellow]Running migrations...[/yellow]")
            result = subprocess.run(
                ["uv", "run", "python", "manage.py", "migrate"],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print("[green]✓[/green] Migrations completed")
            if result.stdout:
                console.print(f"[dim]{result.stdout}[/dim]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗[/red] Migration failed")
            if e.stderr:
                console.print(f"[dim]{e.stderr}[/dim]")

    def _start_dev_server(self) -> None:
        """Start Django development server."""
        try:
            subprocess.run(
                ["uv", "run", "python", "manage.py", "runserver"],
                check=True,
            )
        except subprocess.CalledProcessError:
            console.print("\n[red]✗[/red] Server stopped")
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Server stopped by user[/yellow]")

    def _print_manual_steps(self) -> None:
        """Print manual steps for the user."""
        console.print("\n")
        console.print(Panel(
            "[cyan]Manual Steps:[/cyan]\n\n"
            "  [yellow]1.[/yellow] Start services:\n"
            "     [dim]docker compose -f onlydjango/dev_helpers/dev.docker-compose.yml up -d[/dim]\n\n"
            "  [yellow]2.[/yellow] Run migrations:\n"
            "     [dim]uv run python manage.py migrate[/dim]\n\n"
            "  [yellow]3.[/yellow] Start development server:\n"
            "     [dim]uv run python manage.py runserver[/dim]",
            border_style="cyan",
            title="Next Steps"
        ))
