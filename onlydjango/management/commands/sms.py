"""Smart collectstatic - only runs if static files changed in the current deployment.

Checks git diff between HEAD and the previous commit for changes to:
- HTML templates
- CSS files
- JavaScript files
- Static assets

Usage:
    python manage.py smart_collectstatic

Exit codes:
    0 - Success (either ran collectstatic or skipped because no changes)
    1 - Error occurred
"""

import subprocess
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run collectstatic only if static files changed since last commit"

    STATIC_PATTERNS = [
        "*.html",
        "*.css",
        "*.js",
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.svg",
        "*.ico",
        "*.woff",
        "*.woff2",
        "*.ttf",
        "*.eot",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force collectstatic regardless of changes",
        )
        parser.add_argument(
            "--base-ref",
            type=str,
            default="HEAD~1",
            help="Git ref to compare against (default: HEAD~1)",
        )

    def handle(self, *args, **options):
        if options["force"]:
            self.stdout.write("Force flag set, running collectstatic...")
            return self.run_collectstatic()

        base_ref = options["base_ref"]

        if self.static_files_changed(base_ref):
            self.stdout.write(self.style.WARNING("Static files changed, running collectstatic..."))
            return self.run_collectstatic()

        self.stdout.write(self.style.SUCCESS("No static file changes detected, skipping collectstatic"))

    def static_files_changed(self, base_ref: str) -> bool:
        """Check if any static files changed between base_ref and HEAD."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", base_ref, "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            changed_files = result.stdout.strip().split("\n")
            changed_files = [f for f in changed_files if f]

            for filepath in changed_files:
                if self.is_static_file(filepath):
                    self.stdout.write(f"  Changed: {filepath}")
                    return True

            return False

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Git command failed: {e.stderr}"))
            return True
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Git not found, running collectstatic to be safe"))
            return True

    def is_static_file(self, filepath: str) -> bool:
        """Check if a file path matches static file patterns."""
        filepath_lower = filepath.lower()

        for pattern in self.STATIC_PATTERNS:
            ext = pattern.replace("*", "")
            if filepath_lower.endswith(ext):
                return True

        static_dirs = ["static/", "assets/", "templates/"]
        for static_dir in static_dirs:
            if static_dir in filepath_lower:
                return True

        return False

    def run_collectstatic(self):
        """Run the actual collectstatic command."""
        try:
            subprocess.run(
                ["/bin/uv", "run", "python", "manage.py", "collectstatic", "--noinput"],
                check=True,
            )
            self.stdout.write(self.style.SUCCESS("collectstatic completed"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"collectstatic failed with exit code {e.returncode}"))
            sys.exit(1)
        except FileNotFoundError:
            self.stdout.write("Falling back to call_command for local dev...")
            call_command("collectstatic", "--noinput", verbosity=1)
            self.stdout.write(self.style.SUCCESS("collectstatic completed"))
