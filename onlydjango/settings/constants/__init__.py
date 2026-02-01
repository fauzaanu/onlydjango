"""Environment-specific constants.

Usage in settings:
    from onlydjango.settings.constants import env

    # Access variables
    env.REDIS_URL
    env.PGDATABASE
"""

import os

# Import the appropriate constants based on DJANGO_SETTINGS_MODULE
_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "onlydjango.settings.dev")

if "prod" in _settings_module:
    from .prod import *  # noqa: F401, F403
    from . import prod as env
else:
    from .dev import *  # noqa: F401, F403
    from . import dev as env

__all__ = ["env"]
