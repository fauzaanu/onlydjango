# onlydjango

Template repository for building Django apps with a modern, component-first
front-end workflow and batteries-included infrastructure. It ships with:

- Django 5.2, Django Allauth (Telegram provider), and Django Cotton
- PostgreSQL + Redis + Huey background tasks
- Tailwind CSS build pipeline
- HTMX + Alpine.js
- S3-ready storage backends and deployment scaffolding
- Custom management commands for app scaffolding and component validation

This README documents the template and everything it implements.

## Quick start

1) Create a local environment file.

```bash
cp env.sample .env
```

2) Install Python dependencies with uv.

```bash
uv sync
```

3) Install front-end dependencies.

```bash
npm install
```

4) Start local services (Postgres + Redis).

```bash
docker compose -f onlydjango/dev_helpers/dev.docker-compose.yml up -d
```

5) Run migrations and build CSS.

```bash
DJANGO_SETTINGS_MODULE=onlydjango.settings.dev uv run python manage.py migrate
npm run build:css
```

6) Start the dev server.

```bash
DJANGO_SETTINGS_MODULE=onlydjango.settings.dev uv run python manage.py runserver
```

Optional: start Huey workers in another shell.

```bash
DJANGO_SETTINGS_MODULE=onlydjango.settings.dev uv run python manage.py run_huey
```

Notes:
- `manage.py` defaults to `onlydjango.settings.prod`. Set
  `DJANGO_SETTINGS_MODULE=onlydjango.settings.dev` for local development.
- `setupdev.py` can bring up docker services and run migrations in one step.

## Project setup module

The `project_setup` module can bootstrap a new project by:

- Renaming the project in `pyproject.toml`
- Finding free ports for Redis and PostgreSQL
- Creating and configuring `.env`
- Updating docker-compose with project name and ports
- Installing npm dependencies for Tailwind CSS

Run it with:

```bash
uv run python -m project_setup
```

## Environment variables

Start with `env.sample` and adjust as needed.

Core:
- DJANGO_SETTINGS_MODULE (default in manage.py is onlydjango.settings.prod)
- DJANGO_SECRET_KEY (required for production)
- SITE_NAME (used in templates and OpenGraph tags)

Database (PostgreSQL):
- PGDATABASE, PGUSER, PGPASSWORD, PGHOST, PGPORT
- DB_POOL_MIN_SIZE, DB_POOL_MAX_SIZE, DB_POOL_TIMEOUT (prod)

Redis / Huey:
- REDIS_URL
- REDIS_PORT (dev uses this directly)

Storage (S3-compatible):
- AWS_STORAGE_BUCKET_NAME
- AWS_S3_ENDPOINT_URL
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_S3_CUSTOM_DOMAIN
- DEV_STORAGE (dev only; set to "local" or "S3")

Email (prod):
- ADMIN_EMAIL
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

Telegram logging:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Site metadata (used by `onlydjango_globals` context processor):
- SITE_AUTHOR, SITE_KEYWORDS, SITE_DESCRIPTION
- OG_TYPE, OG_TITLE, OG_DESCRIPTION, OG_IMAGE
- TWITTER_CARD, TWITTER_TITLE, TWITTER_DESCRIPTION, TWITTER_IMAGE

## Project structure

Key directories and their roles:

- apps/                        App modules created by the custom startapp
- onlydjango/                  Django project + shared templates/static assets
  - settings/                  base.py, dev.py, prod.py
  - templates/cotton/          Base Cotton components (layout, navbar, footer)
  - static/                    Alpine, HTMX, Font Awesome, etc
  - storage/                   S3 storage backends
  - management/commands/       Custom management commands
- project_setup/               One-time project bootstrapping module
- guard_rails/                 Utility scripts for linting and repo hygiene
- onlydjango/dev_helpers/      Local docker compose and Tailwind watcher
- onlydjango/deployment/       Railway configs and Caddyfile for VPS

## Django settings overview

`onlydjango/settings/base.py`:
- Configures installed apps (Django, Allauth, Cotton, Huey, Debug Toolbar).
- Adds `onlydjango.helpers.onlydjango_globals.global_settings` as a context
  processor for consistent site metadata.
- Defines S3 storage backends and static file locations.

`onlydjango/settings/dev.py`:
- DEBUG enabled, local filesystem storage by default.
- Dummy cache backend (Redis still used for Huey).
- Postgres settings loaded from environment.

`onlydjango/settings/prod.py`:
- Enforces HTTPS/host settings and cookie domains.
- Redis cache enabled.
- Email + Telegram logging configured.
- Postgres pool parameters available via env vars.

## Front-end tooling and Cotton components

Tailwind:
- Input: `onlydjango/input.css`
- Output: `onlydjango/static/css/style.css`
- Build command: `npm run build:css`
- Content scanning configured in `tailwind.config.js`

Cotton components:
- Base layout: `onlydjango/templates/cotton/layout.html`
- Default components: navbar, footer, section
- Naming convention:
  - File paths use underscores (example: `podcast_status.html`)
  - Tags use hyphens (example: `<c-app.podcast-status />`)

## Custom management commands

`startapp`:
```bash
uv run python manage.py startapp myapp
```
Creates apps under `apps/`, updates `FIRST_PARTY_APPS`, and scaffolds:
templates, templatetags, tests/, and signals.py.

`create_cotton_component`:
```bash
uv run python manage.py create_cotton_component app component-name
```
Creates a component file with correct underscore naming and prints tag usage.

`validate_components`:
```bash
uv run python manage.py validate_components --verbose
```
Validates Cotton component references, flags dynamic component names, and
reports unresolved or unused components.

`model_schema`:
```bash
uv run python manage.py model_schema "app_label.ModelName"
```
Prints model fields and custom methods with file/line references.

`sms` (smart collectstatic):
```bash
uv run python manage.py sms --base-ref HEAD~1
```
Runs collectstatic only when static/template assets have changed.

`sync`:
```bash
uv run python manage.py sync .kiro --repo https://github.com/fauzaanu/onlydjango
```
Downloads a folder from a GitHub repo to a local directory.

## Storage

Storage backends are defined in `onlydjango/storage/`:

- `PrivateMediaStorage` for private media (S3, signed URLs)
- `PublicMediaStorage` for public media

Development defaults to local filesystem storage unless `DEV_STORAGE=S3`.

## Background tasks (Huey)

Huey is configured with Redis (`huey.contrib.djhuey`). Run workers with:

```bash
uv run python manage.py run_huey
```

## Deployment scaffolding

Docker:
- `Dockerfile` uses uv to install dependencies and exposes port 8000.

Railway:
- `onlydjango/deployment/railway/railway.json` starts with migrate,
  collectstatic, and Gunicorn.
- Optional Huey config in `railway_huey.json`.

VPS:
- `onlydjango/deployment/vps/Caddyfile` reverse-proxy configuration example.

## Guard rails utilities

`guard_rails/health_check.py`:
- Scans Python files and reports large-file health scores.

`guard_rails/django_comments.py`:
- Converts HTML comments to Django `{% comment %}` blocks.

`guard_rails/move_md.py`:
- Moves markdown files into `.kiro/docs` with timestamp folders.

## Quality checks (optional)

Common validation commands:

```bash
uv run pyright
uv run ruff check --fix
uv run python manage.py check
uv run python manage.py validate_templates
uv run python manage.py test --noinput
```