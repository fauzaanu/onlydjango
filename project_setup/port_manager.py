"""Port management utilities for Docker and localhost."""

import socket
import subprocess
import json
from rich.console import Console
from rich.table import Table

console = Console()


class PortManager:
    """Manages port detection and allocation."""

    @staticmethod
    def get_docker_ports(include_stopped: bool = True) -> set[int]:
        """Get all ports currently used by Docker containers.
        
        Args:
            include_stopped: If True, includes ports from stopped containers
        """
        try:
            cmd = ['docker', 'ps', '--format', '{{json .}}']
            if include_stopped:
                cmd.insert(2, '-a')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            used_ports = set()
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                container = json.loads(line)
                ports_str = container.get('Ports', '')
                
                if not ports_str or ports_str == '-':
                    continue
                
                # Parse ports like "0.0.0.0:6379->6379/tcp, 0.0.0.0:5432->5432/tcp"
                for port_mapping in ports_str.split(','):
                    port_mapping = port_mapping.strip()
                    if '->' in port_mapping and ':' in port_mapping:
                        # Extract host port from "0.0.0.0:6379->6379/tcp"
                        host_part = port_mapping.split('->')[0].strip()
                        if ':' in host_part:
                            port_str = host_part.split(':')[-1]
                            try:
                                used_ports.add(int(port_str))
                            except ValueError:
                                pass
            
            return used_ports
            
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return set()

    @staticmethod
    def is_port_in_use(port: int) -> bool:
        """Check if a port is in use on localhost."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return False
        except OSError:
            return True

    @classmethod
    def find_free_port(cls, start_port: int = 5432) -> int:
        """Find an available port starting from the given port number."""
        docker_ports = cls.get_docker_ports()
        port = start_port
        
        while port < 65535:
            # Check if port is used by Docker
            if port in docker_ports:
                port += 1
                continue
            
            # Check if port is available on localhost
            if not cls.is_port_in_use(port):
                return port
            
            port += 1
        
        raise RuntimeError(f"No free port found starting from {start_port}")

    @classmethod
    def display_docker_ports(cls) -> None:
        """Display all Docker container ports (including stopped containers)."""
        try:
            result = subprocess.run(
                ['docker', 'ps', '-a', '--format', '{{json .}}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            table = Table(title="Docker Containers", show_header=True, header_style="bold cyan")
            table.add_column("Container", style="white", width=25)
            table.add_column("State", width=10)
            table.add_column("Image", style="dim", width=25)
            table.add_column("Ports", style="yellow", width=30)
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                container = json.loads(line)
                name = container.get('Names', '-')[:24]
                state = container.get('State', '-')
                image = container.get('Image', '-')[:24]
                ports = container.get('Ports', '-')[:29]
                
                # Color code by state
                if state == 'running':
                    state_display = "[green]● running[/green]"
                else:
                    state_display = f"[red]○ {state}[/red]"
                
                table.add_row(name, state_display, image, ports)
            
            console.print(table)
            
            docker_ports = cls.get_docker_ports(include_stopped=True)
            if docker_ports:
                console.print(f"\n[cyan]Ports in use:[/cyan] [yellow]{sorted(docker_ports)}[/yellow]")
                
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            console.print(f"[red]Error accessing Docker:[/red] {e}")
