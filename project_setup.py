"""
Meant to be run just once when starting the project

1. We should rename project name in pyproject
2. Use .env to manage redis and postgres ports dynamically : find existing ports and get a random unoccupied port setup
3. give a name to docker compose file so it doesnt get a generic one
4. run npm i so that tailwindcss is installed and available
"""

import socket
import subprocess
import sys
from pathlib import Path


def find_free_port(start_port: int = 5432) -> int:
    """Find an available port starting from the given port number."""
    port = start_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            port += 1
    raise RuntimeError(f"No free port found starting from {start_port}")


def update_pyproject_name(new_name: str) -> None:
    """Update the project name in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("ERROR: pyproject.toml not found")
        return

    content = pyproject_path.read_text(encoding="utf-8")
    updated_content = content.replace('name = "onlydjango"', f'name = "{new_name}"')

    if content != updated_content:
        pyproject_path.write_text(updated_content, encoding="utf-8")
        print(f"Updated project name to '{new_name}' in pyproject.toml")
    else:
        print("Project name already set or not found in pyproject.toml")


def create_env_from_sample() -> None:
    """Copy env.sample to .env if .env doesn't exist."""
    env_path = Path(".env")
    env_sample_path = Path("env.sample")

    if not env_sample_path.exists():
        print("ERROR: env.sample file not found")
        sys.exit(1)

    if env_path.exists():
        print(".env file already exists, skipping copy")
        return

    # Copy env.sample to .env
    content = env_sample_path.read_text(encoding="utf-8")
    env_path.write_text(content, encoding="utf-8")
    print("Created .env from env.sample")


def update_env_ports() -> None:
    """Update .env file with available ports for Redis and PostgreSQL, and change to dev settings."""
    env_path = Path(".env")
    if not env_path.exists():
        print("ERROR: .env file not found")
        return

    # Find free ports
    redis_port = find_free_port(6379)
    postgres_port = find_free_port(5432)

    print(f"Found free ports - Redis: {redis_port}, PostgreSQL: {postgres_port}")

    # Read current .env content
    content = env_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Update ports and settings in .env
    updated_lines = []
    for line in lines:
        if line.startswith("REDIS_URL="):
            updated_lines.append(f"REDIS_URL=redis://localhost:{redis_port}")
        elif line.startswith("PGPORT="):
            updated_lines.append(f"PGPORT={postgres_port}")
        elif line.startswith("DJANGO_SETTINGS_MODULE="):
            updated_lines.append("DJANGO_SETTINGS_MODULE=onlydjango.settings.dev")
        else:
            updated_lines.append(line)

    env_path.write_text("\n".join(updated_lines), encoding="utf-8")
    print(f"Updated .env with Redis port {redis_port} and PostgreSQL port {postgres_port}")
    print("Changed DJANGO_SETTINGS_MODULE to dev")

    # Update docker-compose file
    update_docker_compose_ports(redis_port, postgres_port)


def update_docker_compose_ports(redis_port: int, postgres_port: int) -> None:
    """Update docker-compose file with the new ports."""
    docker_compose_path = Path("onlydjango/dev_helpers/dev.docker-compose.yml")
    if not docker_compose_path.exists():
        print("ERROR: docker-compose file not found")
        return

    content = docker_compose_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    updated_lines = []
    for line in lines:
        if '"6379:6379"' in line:
            updated_lines.append(line.replace('"6379:6379"', f'"{redis_port}:6379"'))
        elif '"5432:5432"' in line:
            updated_lines.append(line.replace('"5432:5432"', f'"{postgres_port}:5432"'))
        else:
            updated_lines.append(line)

    docker_compose_path.write_text("\n".join(updated_lines), encoding="utf-8")
    print("Updated docker-compose with new ports")


def add_docker_compose_project_name(project_name: str) -> None:
    """Add project name to docker-compose file."""
    docker_compose_path = Path("onlydjango/dev_helpers/dev.docker-compose.yml")
    if not docker_compose_path.exists():
        print("ERROR: docker-compose file not found")
        return

    content = docker_compose_path.read_text(encoding="utf-8")

    # Check if name already exists
    if content.strip().startswith("name:"):
        print("Docker compose already has a project name")
        return

    # Add name at the beginning
    updated_content = f"name: {project_name}\n\n{content}"
    docker_compose_path.write_text(updated_content, encoding="utf-8")
    print(f"Added project name '{project_name}' to docker-compose")


def install_npm_dependencies() -> None:
    """Run npm install to install tailwindcss and other dependencies."""
    print("Installing npm dependencies...")
    try:
        result = subprocess.run(
            ["npm", "install"],
            capture_output=True,
            text=True,
            check=True,
        )
        print("npm dependencies installed successfully")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install npm dependencies: {e}")
        if e.stderr:
            print(e.stderr)
    except FileNotFoundError:
        print("ERROR: npm not found. Please install Node.js and npm first.")


def main() -> None:
    """Main setup function."""
    print("Starting project setup...\n")

    # Get project name from user
    project_name = input("Enter your project name (default: onlydjango): ").strip()
    if not project_name:
        project_name = "onlydjango"

    # 1. Update project name in pyproject.toml
    update_pyproject_name(project_name)

    # 2. Create .env from env.sample
    create_env_from_sample()

    # 3. Update .env with available ports and dev settings
    update_env_ports()

    # 4. Add project name to docker-compose
    add_docker_compose_project_name(project_name)

    # 5. Install npm dependencies
    install_npm_dependencies()

    print("\nProject setup completed!")
    print("\nNext steps:")
    print("  1. Review the updated .env file")
    print("  2. Start services: docker compose -f onlydjango/dev_helpers/dev.docker-compose.yml up -d")
    print("  3. Run migrations: uv run python manage.py migrate")
    print("  4. Start development server: uv run python manage.py runserver")


if __name__ == "__main__":
    main()
