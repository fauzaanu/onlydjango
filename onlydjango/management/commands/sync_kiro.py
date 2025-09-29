import os
import requests
import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Download files from a GitHub repository KIRO folder to local .kiro directory'

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

    def handle(self, *args, **options):
        repo_url = options['repo_url']
        branch = options['branch']
        force = options['force']
        
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

        self.stdout.write(f'Syncing KIRO files from {owner}/{repo} (branch: {branch})')
        
        # GitHub API URL for the KIRO folder
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/KIRO'
        
        try:
            # Get KIRO folder contents
            response = requests.get(f'{api_url}?ref={branch}')
            response.raise_for_status()
            
            if response.status_code == 404:
                raise CommandError(f'KIRO folder not found in {owner}/{repo} on branch {branch}')
            
            files_data = response.json()
            
            if not isinstance(files_data, list):
                raise CommandError('KIRO is not a directory or is empty')
            
            # Create .kiro directory if it doesn't exist
            kiro_dir = Path('.kiro')
            kiro_dir.mkdir(exist_ok=True)
            
            # Process each file in the KIRO folder
            downloaded_count = 0
            skipped_count = 0
            
            for file_info in files_data:
                if file_info['type'] == 'file':
                    downloaded_count += self._download_file(
                        file_info, kiro_dir, force
                    )
                elif file_info['type'] == 'dir':
                    # Recursively download directory contents
                    downloaded_count += self._download_directory(
                        file_info, kiro_dir, owner, repo, branch, force
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully downloaded {downloaded_count} files to .kiro directory'
                )
            )
            
        except requests.RequestException as e:
            raise CommandError(f'Failed to fetch repository data: {e}')
        except json.JSONDecodeError:
            raise CommandError('Invalid response from GitHub API')

    def _download_file(self, file_info, base_dir, force):
        """Download a single file"""
        file_name = file_info['name']
        download_url = file_info['download_url']
        local_path = base_dir / file_name
        
        # Check if file exists and handle confirmation
        if local_path.exists() and not force:
            self.stdout.write(
                self.style.WARNING(f'File {local_path} already exists.')
            )
            confirm = input('Overwrite? (y/N): ').lower().strip()
            if confirm != 'y':
                self.stdout.write(f'Skipped {file_name}')
                return 0
        
        try:
            # Download file content
            response = requests.get(download_url)
            response.raise_for_status()
            
            # Write file to local directory
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            self.stdout.write(f'Downloaded: {file_name}')
            return 1
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to download {file_name}: {e}')
            )
            return 0

    def _download_directory(self, dir_info, base_dir, owner, repo, branch, force):
        """Recursively download directory contents"""
        dir_name = dir_info['name']
        local_dir = base_dir / dir_name
        local_dir.mkdir(exist_ok=True)
        
        # Get directory contents
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/KIRO/{dir_name}'
        
        try:
            response = requests.get(f'{api_url}?ref={branch}')
            response.raise_for_status()
            dir_contents = response.json()
            
            downloaded_count = 0
            
            for item in dir_contents:
                if item['type'] == 'file':
                    # Update the item to have the correct local path
                    item_copy = item.copy()
                    downloaded_count += self._download_file_to_subdir(
                        item_copy, local_dir, force
                    )
                elif item['type'] == 'dir':
                    # Recursively handle subdirectories
                    downloaded_count += self._download_subdirectory(
                        item, local_dir, owner, repo, branch, force, f'KIRO/{dir_name}'
                    )
            
            return downloaded_count
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to download directory {dir_name}: {e}')
            )
            return 0

    def _download_file_to_subdir(self, file_info, target_dir, force):
        """Download a file to a specific subdirectory"""
        file_name = file_info['name']
        download_url = file_info['download_url']
        local_path = target_dir / file_name
        
        # Check if file exists and handle confirmation
        if local_path.exists() and not force:
            self.stdout.write(
                self.style.WARNING(f'File {local_path} already exists.')
            )
            confirm = input('Overwrite? (y/N): ').lower().strip()
            if confirm != 'y':
                self.stdout.write(f'Skipped {local_path}')
                return 0
        
        try:
            # Download file content
            response = requests.get(download_url)
            response.raise_for_status()
            
            # Write file to local directory
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            self.stdout.write(f'Downloaded: {local_path}')
            return 1
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to download {local_path}: {e}')
            )
            return 0

    def _download_subdirectory(self, dir_info, base_dir, owner, repo, branch, force, parent_path):
        """Recursively download subdirectory contents"""
        dir_name = dir_info['name']
        local_dir = base_dir / dir_name
        local_dir.mkdir(exist_ok=True)
        
        # Get subdirectory contents
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{parent_path}/{dir_name}'
        
        try:
            response = requests.get(f'{api_url}?ref={branch}')
            response.raise_for_status()
            dir_contents = response.json()
            
            downloaded_count = 0
            
            for item in dir_contents:
                if item['type'] == 'file':
                    downloaded_count += self._download_file_to_subdir(
                        item, local_dir, force
                    )
                elif item['type'] == 'dir':
                    downloaded_count += self._download_subdirectory(
                        item, local_dir, owner, repo, branch, force, f'{parent_path}/{dir_name}'
                    )
            
            return downloaded_count
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to download subdirectory {dir_name}: {e}')
            )
            return 0