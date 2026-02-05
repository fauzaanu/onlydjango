# Environment Variables

All environment variables are centralized in `onlydjango/settings/constants/`.

## Rule

**Never use `os.environ` or `os.getenv` outside of the constants module.**

All environment variable access must go through:
- `onlydjango/settings/constants/dev.py` - Development variables
- `onlydjango/settings/constants/prod.py` - Production variables

## Usage in Settings

```python
# In dev.py or prod.py
from .constants import dev as env  # or prod as env

DATABASES = {
    "default": {
        "NAME": env.PGDATABASE,
        "USER": env.PGUSER,
        ...
    }
}
```

## Usage in Application Code

```python
from django.conf import settings

# Access via Django settings (preferred)
bucket = settings.AWS_STORAGE_BUCKET_NAME

# Or import constants directly
from onlydjango.settings.constants import env
redis_url = env.REDIS_URL
```

## Adding New Variables

1. Add to `constants/dev.py` with sensible defaults
2. Add to `constants/prod.py` (required variables use `os.environ["VAR"]`)
3. Use in settings via `env.VARIABLE_NAME`

## Benefits

- Single source of truth for all environment variables
- Easy to audit what variables the project needs
- Clear separation between dev defaults and prod requirements
- Type hints and documentation in one place
