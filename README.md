# onlydjango

A batteries-included Django template for building modern web apps fast. Ships with:

- Django 5.2, Django Allauth, Django Cotton components
- PostgreSQL + Redis + Huey background tasks
- Tailwind CSS + HTMX + Alpine.js
- S3-ready storage backends
- Auto port detection (no conflicts with other projects)
- Railway deployment ready

## Quick Start

### One Command Setup

```bash
uv run python -m project_setup \
  --non-interactive \
  --project-name myproject \
  --start-docker-compose \
  --run-migrations
```

That's it. This command:
1. Creates `.env` from template
2. Finds free ports for Redis, PostgreSQL, and dev server
3. Configures docker-compose with your project name
4. Installs npm dependencies
5. Starts Docker services
6. Runs migrations

### Start Development

```bash
uv run python manage.py runserver
```

The dev server automatically uses the port configured during setup.

### Interactive Setup

If you prefer prompts:

```bash
uv run python -m project_setup
```

## LLM-Friendly Setup

For AI assistants bootstrapping projects:

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

All flags documented in `.kiro/steering/project-setup.md`.

## Project Structure

```
apps/                          Your Django apps go here
onlydjango/
  settings/
    base.py                    Shared settings
    dev.py                     Development (DEBUG=True)
    prod.py                    Production
    tests.py                   Fast SQLite test runner
    constants/
      dev.py                   Dev environment variables
      prod.py                  Prod environment variables
  templates/cotton/            Base components (layout, navbar, footer)
  static/                      Alpine, HTMX, Font Awesome
  management/commands/         Custom commands
project_setup/                 Project bootstrapping module
```

## Creating Apps

```bash
uv run python manage.py startapp myapp
```

Apps are created in `apps/` and auto-registered in settings.

## Running Tests

Tests use SQLite for speed:

```bash
uv run python manage.py test --settings=onlydjango.settings.tests --noinput
```

## Environment Variables

All environment variables are centralized in `onlydjango/settings/constants/`. Never use `os.environ` directly elsewhere.

Key variables:
- `DJANGO_SECRET_KEY` - Required for production
- `SITE_NAME` - Used in templates
- `REDIS_URL` - Redis connection
- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT` - PostgreSQL
- `DEV_STORAGE` - Set to `local` or `S3` for development

## Railway Deployment

Generate Railway environment variables:

```bash
uv run python manage.py generate_railway_env \
  --non-interactive \
  --postgres-service myapp-db \
  --redis-service myapp-cache \
  --allowed-hosts myapp.up.railway.app
```

This generates Railway's `${{service.VARIABLE}}` syntax for private network connections.

## Custom Commands

| Command | Description |
|---------|-------------|
| `startapp` | Create app in `apps/` with full scaffolding |
| `create_cotton_component` | Create a Cotton component |
| `validate_components` | Check Cotton component references |
| `model_schema` | Print model fields and methods |
| `generate_railway_env` | Generate Railway env vars |
| `runserver` | Dev server (auto-detects port from .env) |

## Background Tasks

Huey workers:

```bash
uv run python manage.py run_huey
```

In development, tasks run synchronously when `DEBUG=True`.

## Quality Checks

```bash
uv run pyright                 # Type checking
uv run ruff check --fix        # Linting
uv run python manage.py check  # Django checks
npm run build:css              # Build Tailwind
```

## Cotton Components

Components use hyphens in tags, underscores in filenames:

```html
<!-- Tag -->
<c-app.my-component />

<!-- File: apps/myapp/templates/cotton/my_component.html -->
```

Base layout: `onlydjango/templates/cotton/layout.html`
