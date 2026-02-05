# Code Validation

After making code changes, run these validation commands to ensure quality:

```bash
# Type checking
uv run pyright

# Linting and auto-fix
uv run ruff check --fix

# Django system checks
uv run python manage.py check

# Template validation
uv run python manage.py validate_templates

# Test suite - Uses SQLite for speed, always use noinput

uv run python manage.py test --settings=onlydjango.settings.tests --noinput

# LLM Health check, helps you in the future if everything is modularized well with less loc per file.
uv run python llm_health_check.py

npm run build:css
```

Run these checks selectively based on the scope of your changes. Not every change requires all checks.
