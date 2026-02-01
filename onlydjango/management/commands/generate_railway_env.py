"""Generate Railway environment variables with proper reference syntax."""

import secrets
from django.core.management.base import BaseCommand
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


class Command(BaseCommand):
    help = "Generate Railway environment variables with service reference syntax"

    def add_arguments(self, parser):
        parser.add_argument(
            "--non-interactive",
            action="store_true",
            help="Run without prompts, requires all options to be provided",
        )
        parser.add_argument(
            "--postgres-service",
            type=str,
            help="Railway PostgreSQL service name (e.g., 'myapp-db')",
        )
        parser.add_argument(
            "--redis-service",
            type=str,
            help="Railway Redis service name (e.g., 'myapp-cache')",
        )
        parser.add_argument(
            "--allowed-hosts",
            type=str,
            help="Comma-separated list of allowed hosts",
        )
        parser.add_argument(
            "--s3-bucket",
            type=str,
            help="S3 bucket name",
        )
        parser.add_argument(
            "--s3-endpoint",
            type=str,
            help="S3 endpoint URL",
        )
        parser.add_argument(
            "--s3-access-key",
            type=str,
            help="S3 access key ID",
        )
        parser.add_argument(
            "--s3-secret-key",
            type=str,
            help="S3 secret access key",
        )
        parser.add_argument(
            "--s3-custom-domain",
            type=str,
            default="",
            help="S3 custom domain (CDN)",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="Output file path (default: print to console)",
        )

    def handle(self, *args, **options):
        interactive = not options["non_interactive"]

        if interactive:
            console.print(Panel.fit(
                "[bold cyan]Railway Environment Generator[/bold cyan]",
                border_style="cyan"
            ))
            console.print()

        # Gather inputs
        postgres_service = self._get_value(
            options, "postgres_service",
            "PostgreSQL service name on Railway",
            "myapp-db",
            interactive
        )

        redis_service = self._get_value(
            options, "redis_service",
            "Redis service name on Railway",
            "myapp-cache",
            interactive
        )

        allowed_hosts = self._get_value(
            options, "allowed_hosts",
            "Allowed hosts (comma-separated)",
            "myapp.up.railway.app",
            interactive
        )

        s3_bucket = self._get_value(
            options, "s3_bucket",
            "S3 bucket name",
            "",
            interactive
        )

        s3_endpoint = self._get_value(
            options, "s3_endpoint",
            "S3 endpoint URL",
            "",
            interactive
        )

        s3_access_key = self._get_value(
            options, "s3_access_key",
            "S3 access key ID",
            "",
            interactive
        )

        s3_secret_key = self._get_value(
            options, "s3_secret_key",
            "S3 secret access key",
            "",
            interactive
        )

        s3_custom_domain = self._get_value(
            options, "s3_custom_domain",
            "S3 custom domain (CDN, optional)",
            "",
            interactive
        )

        # Generate secret key
        secret_key = secrets.token_urlsafe(50)

        # Build environment variables
        env_vars = self._build_env_vars(
            postgres_service=postgres_service,
            redis_service=redis_service,
            allowed_hosts=allowed_hosts,
            secret_key=secret_key,
            s3_bucket=s3_bucket,
            s3_endpoint=s3_endpoint,
            s3_access_key=s3_access_key,
            s3_secret_key=s3_secret_key,
            s3_custom_domain=s3_custom_domain,
        )

        # Output
        output_file = options.get("output")
        if output_file:
            with open(output_file, "w") as f:
                f.write(env_vars)
            console.print(f"\n[green]✓[/green] Written to {output_file}")
        else:
            console.print("\n[bold cyan]Generated Railway Environment Variables:[/bold cyan]\n")
            console.print(Panel(env_vars, border_style="green"))
            console.print("\n[dim]Copy these to your Railway service variables[/dim]")

    def _get_value(self, options, key, prompt_text, default, interactive):
        """Get value from options or prompt user."""
        value = options.get(key)
        if value:
            return value
        if interactive:
            return Prompt.ask(f"[cyan]{prompt_text}[/cyan]", default=default)
        return default

    def _build_env_vars(
        self,
        postgres_service: str,
        redis_service: str,
        allowed_hosts: str,
        secret_key: str,
        s3_bucket: str,
        s3_endpoint: str,
        s3_access_key: str,
        s3_secret_key: str,
        s3_custom_domain: str,
    ) -> str:
        """Build the environment variables string."""
        lines = [
            "# Django",
            "DJANGO_SETTINGS_MODULE=onlydjango.settings.prod",
            f"DJANGO_SECRET_KEY={secret_key}",
            f"ALLOWED_HOSTS={allowed_hosts}",
            "PORT=8000",
            "",
            "# PostgreSQL (Railway private network)",
            f'PGDATABASE="${{{{{postgres_service}.PGDATABASE}}}}"',
            f'PGHOST="${{{{{postgres_service}.PGHOST}}}}"',
            f'PGPASSWORD="${{{{{postgres_service}.PGPASSWORD}}}}"',
            f'PGPORT="${{{{{postgres_service}.PGPORT}}}}"',
            f'PGUSER="${{{{{postgres_service}.PGUSER}}}}"',
            "",
            "# Redis (Railway private network)",
            f'REDIS_URL="${{{{{redis_service}.REDIS_URL}}}}"',
        ]

        if s3_bucket:
            lines.extend([
                "",
                "# AWS S3",
                f"AWS_STORAGE_BUCKET_NAME={s3_bucket}",
                f"AWS_S3_ENDPOINT_URL={s3_endpoint}",
                f"AWS_ACCESS_KEY_ID={s3_access_key}",
                f"AWS_SECRET_ACCESS_KEY={s3_secret_key}",
            ])
            if s3_custom_domain:
                lines.append(f"AWS_S3_CUSTOM_DOMAIN={s3_custom_domain}")

        return "\n".join(lines)
