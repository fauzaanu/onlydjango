---
inclusion: always
---

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

# Test suite - Always use noinput

uv run python manage.py test --noinput
```

Run these checks selectively based on the scope of your changes. Not every change requires all checks.
