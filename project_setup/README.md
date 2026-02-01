# Project Setup Module

This module handles the initial setup of a Django project, including:

- Renaming the project in `pyproject.toml`
- Finding free ports for Redis and PostgreSQL (avoiding Docker conflicts)
- Creating and configuring `.env` file
- Configuring docker-compose with project name and ports
- Installing npm dependencies for Tailwind CSS

## Usage

Run the setup as a module:

```bash
python -m project_setup
```

Or with uv:

```bash
uv run python -m project_setup
```

### Non-interactive usage

Run without prompts and pass all options up front:

```bash
uv run python -m project_setup \
  --non-interactive \
  --project-name myproject \
  --check-docker-ports \
  --update-project-name \
  --create-env \
  --configure-ports \
  --redis-port 6380 \
  --postgres-port 5433 \
  --configure-docker-compose \
  --install-npm \
  --no-start-docker-compose \
  --no-run-migrations \
  --no-start-dev-server
```

If you omit flags in non-interactive mode, the defaults match the
interactive prompts (yes for setup steps, no for post-setup actions).

## Testing

Test Docker port detection:

```bash
python project_setup/test_ports.py
```

## Module Structure

- `__init__.py` - Module initialization and exports
- `__main__.py` - Entry point for running as a module
- `manager.py` - Main orchestrator for the setup process
- `config_manager.py` - Configuration file management
- `port_manager.py` - Docker and localhost port detection
- `npm_manager.py` - NPM dependency installation
- `test_ports.py` - Standalone test script for port detection
