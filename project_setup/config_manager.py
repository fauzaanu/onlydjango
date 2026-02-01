"""Configuration file management utilities."""

import re
from pathlib import Path
from rich.console import Console

console = Console()


class ConfigManager:
    """Manages project configuration files."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()

    def update_pyproject_name(self, new_name: str) -> None:
        """Update the project name in pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        
        if not pyproject_path.exists():
            print("ERROR: pyproject.toml not found")
            return

        content = pyproject_path.read_text(encoding="utf-8")
        updated_content = content.replace('name = "onlydjango"', f'name = "{new_name}"')

        if content != updated_content:
            pyproject_path.write_text(updated_content, encoding="utf-8")
            console.print(f"[green]✓[/green] Updated project name to [yellow]{new_name}[/yellow]")
        else:
            console.print("[green]✓[/green] Project name already set")

    def create_env_from_sample(self) -> bool:
        """Copy env.sample to .env if .env doesn't exist."""
        env_path = self.project_root / ".env"
        env_sample_path = self.project_root / "env.sample"

        if not env_sample_path.exists():
            console.print("[red]✗[/red] env.sample file not found")
            return False

        if env_path.exists():
            console.print("[green]✓[/green] .env file already exists")
            return True

        content = env_sample_path.read_text(encoding="utf-8")
        env_path.write_text(content, encoding="utf-8")
        console.print("[green]✓[/green] Created .env from env.sample")
        return True

    def update_env_ports(self, redis_port: int, postgres_port: int, dev_server_port: int | None = None) -> None:
        """Update .env file with available ports."""
        env_path = self.project_root / ".env"
        
        if not env_path.exists():
            print("ERROR: .env file not found")
            return

        content = env_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        updated_lines = []
        dev_port_found = False
        for line in lines:
            if line.startswith("REDIS_URL="):
                updated_lines.append(f"REDIS_URL=redis://localhost:{redis_port}")
            elif line.startswith("REDIS_PORT="):
                updated_lines.append(f"REDIS_PORT={redis_port}")
            elif line.startswith("PGPORT="):
                updated_lines.append(f"PGPORT={postgres_port}")
            elif line.startswith("DJANGO_SETTINGS_MODULE="):
                updated_lines.append("DJANGO_SETTINGS_MODULE=onlydjango.settings.dev")
            elif line.startswith("DJANGO_DEV_PORT="):
                dev_port_found = True
                if dev_server_port:
                    updated_lines.append(f"DJANGO_DEV_PORT={dev_server_port}")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

        # Add DJANGO_DEV_PORT if not found and port is specified
        if dev_server_port and not dev_port_found:
            updated_lines.append(f"DJANGO_DEV_PORT={dev_server_port}")

        env_path.write_text("\n".join(updated_lines), encoding="utf-8")
        console.print("[green]✓[/green] Updated .env with ports")
        console.print("[green]✓[/green] Changed to dev settings")

    def update_docker_compose_ports(self, redis_port: int, postgres_port: int) -> None:
        """Update docker-compose file with the new ports."""
        docker_compose_path = self.project_root / "onlydjango/dev_helpers/dev.docker-compose.yml"
        
        if not docker_compose_path.exists():
            print("ERROR: docker-compose file not found")
            return

        content = docker_compose_path.read_text(encoding="utf-8")
        
        # Replace redis port mapping (any host port -> 6379)
        content = re.sub(r'"(\d+):6379"', f'"{redis_port}:6379"', content)
        
        # Replace postgres port mapping (any host port -> 5432)
        content = re.sub(r'"(\d+):5432"', f'"{postgres_port}:5432"', content)

        docker_compose_path.write_text(content, encoding="utf-8")
        console.print("[green]✓[/green] Updated docker-compose ports")

    def add_docker_compose_project_name(self, project_name: str) -> None:
        """Add project name to docker-compose file."""
        docker_compose_path = self.project_root / "onlydjango/dev_helpers/dev.docker-compose.yml"
        
        if not docker_compose_path.exists():
            print("ERROR: docker-compose file not found")
            return

        content = docker_compose_path.read_text(encoding="utf-8")

        if content.strip().startswith("name:"):
            console.print("[green]✓[/green] Docker compose already has project name")
            return

        updated_content = f"name: {project_name}\n\n{content}"
        docker_compose_path.write_text(updated_content, encoding="utf-8")
        console.print(f"[green]✓[/green] Added project name to docker-compose")
