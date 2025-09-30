import os
import requests
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class Command(BaseCommand):
    help = 'Download files from a GitHub repository .kiro folder to local .kiro directory'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_lock = threading.Lock()

    def add_arguments(self, parser):
        parser.add_argument(
            'repo_url',
            type=str,
            nargs='?',
            default='https://github.com/fauzaanu/onlydjango',
            help='GitHub repository URL (default: https://github.com/fauzaanu/onlydjango)'
        )
        parser.add_argument(
            '--branch',
            type=str,
            default='main',
            help='Branch to download from (default: main)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing files without confirmation'
        )
        parser.add_argument(
            '--max-workers',
            type=int,
            default=10,
            help='Maximum number of concurrent downloads (default: 10)'
        )

    def handle(self, *args, **options):
        repo_url = options['repo_url']
        branch = options['branch']
        force = options['force']
        max_workers = options['max_workers']
        
        # Parse GitHub URL to get owner and repo name
        try:
            if repo_url.startswith('https://github.com/'):
                repo_path = repo_url.replace('https://github.com/', '').rstrip('/')
                owner, repo = repo_path.split('/')
            else:
                raise ValueError("Invalid GitHub URL format")
        except ValueError:
            raise CommandError(
                'Invalid GitHub URL. Expected format: https://github.com/owner/repo'
            )

        self.stdout.write(f'Syncing .kiro files from {owner}/{repo} (branch: {branch})')
        
        # GitHub API URL for the .kiro folder
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/.kiro'
        
        try:
            # Get KIRO folder contents
            response = requests.get(f'{api_url}?ref={branch}')
            response.raise_for_status()
            
            if response.status_code == 404:
                raise CommandError(f'.kiro folder not found in {owner}/{repo} on branch {branch}')
            
            files_data = response.json()
            
            if not isinstance(files_data, list):
                raise CommandError('.kiro is not a directory or is empty')
            
            # Create .kiro directory if it doesn't exist
            kiro_dir = Path('.kiro')
            kiro_dir.mkdir(exist_ok=True)
            
            # Collect all files to download
            all_files = []
            self._collect_files(files_data, kiro_dir, owner, repo, branch, all_files)
            
            # Download files concurrently
            downloaded_count = self._download_files_concurrent(all_files, force, max_workers)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully downloaded {downloaded_count} files to .kiro directory'
                )
            )
            
        except requests.RequestException as e:
            raise CommandError(f'Failed to fetch repository data: {e}')
        except json.JSONDecodeError:
            raise CommandError('Invalid response from GitHub API')

    def _collect_files(self, files_data, base_dir, owner, repo, branch, all_files, parent_path=''):
        """Recursively collect all files to download"""
        for file_info in files_data:
            if file_info['type'] == 'file':
                local_path = base_dir / file_info['name'] if not parent_path else base_dir / parent_path / file_info['name']
                all_files.append({
                    'file_info': file_info,
                    'local_path': local_path,
                    'download_url': file_info['download_url']
                })
            elif file_info['type'] == 'dir':
                # Get directory contents and collect files recursively
                dir_name = file_info['name']
                current_path = f'.kiro/{parent_path}/{dir_name}' if parent_path else f'.kiro/{dir_name}'
                api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{current_path}'
                
                try:
                    response = requests.get(f'{api_url}?ref={branch}')
                    response.raise_for_status()
                    dir_contents = response.json()
                    
                    # Create local directory
                    local_dir = base_dir / parent_path / dir_name if parent_path else base_dir / dir_name
                    local_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Recursively collect files from subdirectory
                    new_parent_path = f'{parent_path}/{dir_name}' if parent_path else dir_name
                    self._collect_files(dir_contents, base_dir, owner, repo, branch, all_files, new_parent_path)
                    
                except requests.RequestException as e:
                    with self.print_lock:
                        self.stdout.write(
                            self.style.ERROR(f'Failed to fetch directory {dir_name}: {e}')
                        )

    def _download_files_concurrent(self, all_files, force, max_workers):
        """Download all files concurrently using ThreadPoolExecutor"""
        downloaded_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all download tasks
            future_to_file = {
                executor.submit(self._download_single_file, file_data, force): file_data 
                for file_data in all_files
            }
            
            # Process completed downloads
            for future in as_completed(future_to_file):
                file_data = future_to_file[future]
                try:
                    result = future.result()
                    downloaded_count += result
                except Exception as e:
                    with self.print_lock:
                        self.stdout.write(
                            self.style.ERROR(f'Failed to download {file_data["local_path"]}: {e}')
                        )
        
        return downloaded_count

    def _download_single_file(self, file_data, force):
        """Download a single file (thread-safe)"""
        file_info = file_data['file_info']
        local_path = file_data['local_path']
        download_url = file_data['download_url']
        file_name = file_info['name']
        
        # Ensure parent directory exists
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and show info
        if local_path.exists():
            with self.print_lock:
                self.stdout.write(
                    self.style.WARNING(f'Overwriting existing file: {local_path}')
                )
        
        try:
            # Download file content
            response = requests.get(download_url)
            response.raise_for_status()
            
            # Write file to local directory
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            with self.print_lock:
                self.stdout.write(f'Downloaded: {local_path}')
            return 1
            
        except requests.RequestException as e:
            with self.print_lock:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download {local_path}: {e}')
                )
            return 0

