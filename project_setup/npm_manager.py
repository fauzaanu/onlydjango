"""NPM dependency management utilities."""

import subprocess
import sys
from rich.console import Console

console = Console()


class NpmManager:
    """Manages NPM dependencies."""

    @staticmethod
    def install_dependencies() -> bool:
        """Run npm install to install tailwindcss and other dependencies."""
        # Try to find npm in PATH or nvm
        npm_cmd = NpmManager._find_npm_command()
        
        if not npm_cmd:
            console.print("[yellow]⚠[/yellow]  npm not found in PATH")
            console.print("[dim]   If using nvm, run 'nvm use' first or install manually with 'npm install'[/dim]")
            return False
        
        try:
            # Use shell=True on Windows to properly resolve npm through nvm
            result = subprocess.run(
                f"{npm_cmd} install",
                capture_output=True,
                text=True,
                check=True,
                shell=True,
            )
            console.print("[green]✓[/green] npm dependencies installed")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗[/red] Failed to install npm dependencies")
            if e.stderr:
                console.print(f"[dim]{e.stderr}[/dim]")
            return False

    @staticmethod
    def _find_npm_command() -> str:
        """Find npm command, checking for nvm on Windows."""
        # Try npm directly first
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                check=True,
                shell=True,
            )
            return "npm"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # On Windows, check if nvm is available
        if sys.platform == "win32":
            try:
                # Check if nvm is in PATH
                subprocess.run(
                    ["nvm", "version"],
                    capture_output=True,
                    check=True,
                    shell=True,
                )
                # nvm exists, but npm might not be activated
                # Try to get current node version
                result = subprocess.run(
                    ["nvm", "current"],
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return "npm"
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return None
