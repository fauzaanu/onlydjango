import os
import subprocess

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = (
        "Run collectstatic only if the last git commit touched static files. "
        "Use -force to run regardless."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-force",
            "--force",
            action="store_true",
            help="Run collectstatic regardless of git changes",
        )

    def handle(self, *args, **options):
        if options["force"] or self._has_static_changes():
            self.stdout.write("Collecting static files...")
            call_command("collectstatic", "--noinput")
        else:
            self.stdout.write("No static changes detected. Skipping collectstatic.")

    def _get_changed_files(self):
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            capture_output=True,
            text=True,
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def _has_static_changes(self):
        static_exts = {
            ".css",
            ".js",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".ico",
            ".json",
            ".woff",
            ".woff2",
            ".ttf",
            ".eot",
            ".otf",
            ".scss",
            ".sass",
            ".less",
        }
        for path in self._get_changed_files():
            lower = path.lower()
            if "/static/" in lower or lower.startswith("static/"):
                return True
            if os.path.splitext(lower)[1] in static_exts:
                return True
        return False
