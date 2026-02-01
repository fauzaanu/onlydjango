"""Custom runserver command that reads port from DJANGO_DEV_PORT env variable."""

import os

from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticFilesRunserverCommand,
)


class Command(StaticFilesRunserverCommand):
    """Runserver with configurable default port via DJANGO_DEV_PORT env variable."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        port = os.environ.get("DJANGO_DEV_PORT")
        if port:
            self.default_port = port
