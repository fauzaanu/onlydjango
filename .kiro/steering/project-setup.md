---
inclusion: manual
---

# Project Setup

This repository includes a `project_setup` module that automates initial configuration. Use it to get started immediately.

## CRITICAL: Project Naming

**"onlydjango" is the template name - NEVER use it as the actual project name.**

When setting up a new project, you MUST invent an appropriate project name based on what you're building. Derive the name from:
- The spec/feature being implemented
- The business domain (e.g., "msh-invoices" for Maldives Software House invoices)
- Keep it short, lowercase, with hyphens

Do NOT ask the user what the project name should be - decide it yourself based on context.

## Quick Start (Non-Interactive)

Run this command to set up everything automatically:

```bash
uv run python -m project_setup \
  --non-interactive \
  --project-name myproject \
  --check-docker-ports \
  --update-project-name \
  --create-env \
  --configure-ports \
  --configure-docker-compose \
  --install-npm \
  --start-docker-compose \
  --run-migrations
```

## What It Does

1. Updates `pyproject.toml` with your project name
2. Creates `.env` from `env.sample`
3. Finds free ports for Redis, PostgreSQL, and Django dev server (avoids conflicts)
4. Configures `docker-compose.yml` with project name and ports
5. Runs `npm install` for Tailwind CSS

## Available Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--project-name NAME` | Set the project name | onlydjango |
| `--non-interactive` | Skip all prompts | false |
| `--check-docker-ports` / `--no-check-docker-ports` | Display Docker ports | true |
| `--update-project-name` / `--no-update-project-name` | Update pyproject.toml | true |
| `--create-env` / `--no-create-env` | Create .env file | true |
| `--configure-ports` / `--no-configure-ports` | Auto-configure ports | true |
| `--redis-port PORT` | Specific Redis port | auto-detected |
| `--postgres-port PORT` | Specific PostgreSQL port | auto-detected |
| `--dev-server-port PORT` | Specific Django dev server port | auto-detected |
| `--configure-docker-compose` / `--no-configure-docker-compose` | Update docker-compose | true |
| `--install-npm` / `--no-install-npm` | Run npm install | true |
| `--start-docker-compose` / `--no-start-docker-compose` | Start Docker services | false |
| `--run-migrations` / `--no-run-migrations` | Run Django migrations | false |
| `--start-dev-server` / `--no-start-dev-server` | Start runserver | false |

## Post-Setup Commands

After setup, start development:

```bash
# Start Docker services
docker compose -f onlydjango/dev_helpers/dev.docker-compose.yml up -d

# Run migrations
uv run python manage.py migrate

# Start dev server (uses DJANGO_DEV_PORT from .env)
uv run python manage.py runserver
```

## Creating New Django Apps

```bash
uv run python manage.py startapp appname
```

Apps are created in `apps/` directory and auto-registered in settings.

## Environment Constants

Environment variables are organized in `onlydjango/settings/constants/`:
- `dev.py` - Development variables (localhost, Docker)
- `prod.py` - Production variables (Railway, S3)

Usage in code:
```python
from onlydjango.settings.constants import env
print(env.REDIS_URL)
```

## Railway Deployment

Generate Railway environment variables with proper service reference syntax:

### Interactive Mode
```bash
uv run python manage.py generate_railway_env
```

### Non-Interactive Mode (LLM-friendly)
```bash
uv run python manage.py generate_railway_env \
  --non-interactive \
  --postgres-service myapp-db \
  --redis-service myapp-cache \
  --allowed-hosts myapp.up.railway.app \
  --s3-bucket mybucket \
  --s3-endpoint https://s3.amazonaws.com \
  --s3-access-key AKIAXXXXXXXX \
  --s3-secret-key secretkey \
  --output railway.env
```

This generates Railway's `${{service.VARIABLE}}` syntax for database and Redis connections over the private network.
