"""Main project setup orchestrator."""

import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from .port_manager import PortManager
from .config_manager import ConfigManager
from .npm_manager import NpmManager

console = Console()


class ProjectSetupManager:
    """Orchestrates the entire project setup process."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.config_manager = ConfigManager(self.project_root)
        self.port_manager = PortManager()
        self.npm_manager = NpmManager()

    def run_setup(self, project_name: str = None) -> None:
        """Run the complete project setup."""
        console.print(Panel.fit(
            "[bold cyan]Django Project Setup[/bold cyan]",
            border_style="cyan"
        ))

        # Get project name
        if not project_name:
            project_name = Prompt.ask(
                "\n[cyan]Enter your project name[/cyan]",
                default="onlydjango"
            )

        console.print(f"\n[bold green]Setting up:[/bold green] {project_name}\n")

        # Display current Docker ports
        if Confirm.ask("[cyan]Check Docker ports?[/cyan]", default=True):
            self.port_manager.display_docker_ports()

        # Update project name
        console.print("\n[bold cyan]Step 1/5:[/bold cyan] Update project name")
        if Confirm.ask(f"  Update project name to '{project_name}'?", default=True):
            self.config_manager.update_pyproject_name(project_name)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Create .env
        console.print("\n[bold cyan]Step 2/5:[/bold cyan] Create .env file")
        if Confirm.ask("  Create .env from env.sample?", default=True):
            if not self.config_manager.create_env_from_sample():
                return
        else:
            console.print("[dim]  Skipped[/dim]")

        # Find and update ports
        console.print("\n[bold cyan]Step 3/5:[/bold cyan] Configure ports")
        if Confirm.ask("  Find free ports and update configuration?", default=True):
            redis_port = self.port_manager.find_free_port(6379)
            postgres_port = self.port_manager.find_free_port(5432)
            
            console.print(f"  [green]✓[/green] Redis: [yellow]{redis_port}[/yellow] | PostgreSQL: [yellow]{postgres_port}[/yellow]")
            
            self.config_manager.update_env_ports(redis_port, postgres_port)
            self.config_manager.update_docker_compose_ports(redis_port, postgres_port)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Add docker-compose project name
        console.print("\n[bold cyan]Step 4/5:[/bold cyan] Configure docker-compose")
        if Confirm.ask("  Add project name to docker-compose?", default=True):
            self.config_manager.add_docker_compose_project_name(project_name)
        else:
            console.print("[dim]  Skipped[/dim]")

        # Install npm dependencies
        console.print("\n[bold cyan]Step 5/5:[/bold cyan] Install npm dependencies")
        if Confirm.ask("  Run npm install?", default=True):
            self.npm_manager.install_dependencies()
        else:
            console.print("[dim]  Skipped[/dim]")

        # Post-setup actions
        self._run_post_setup_actions()

    def _run_post_setup_actions(self) -> None:
        """Run post-setup actions like starting Docker, migrations, etc."""
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]Setup Completed![/bold green]",
            border_style="green"
        ))

        # Start Docker Compose
        console.print("\n[bold cyan]Post-Setup Actions[/bold cyan]")
        if Confirm.ask("\n[cyan]Start Docker Compose services?[/cyan]", default=False):
            self._start_docker_compose()

        # Run migrations
        if Confirm.ask("\n[cyan]Run database migrations?[/cyan]", default=False):
            self._run_migrations()

        # Start development server
        if Confirm.ask("\n[cyan]Start development server?[/cyan]", default=False):
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
