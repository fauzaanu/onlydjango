
import os
import re
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Validates all Cotton component references in HTML templates'

    def __init__(self):
        super().__init__()
        self.unresolved_components = []
        self.dynamic_components = []
        self.unused_components = []
        self.processed_files = 0
        self.total_components_found = 0
        self.referenced_components = set()  # Track which components are actually used

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output including resolved components',
        )

    def handle(self, *args, **options):
        self.verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS('Starting Cotton component validation...\n')
        )

        # Define directories to scan
        scan_directories = [
            Path('apps'),
            Path('onlydjango/templates'),
        ]

        # Find all HTML files
        html_files = []
        for directory in scan_directories:
            if directory.exists():
                html_files.extend(self.find_html_files(directory))

        if not html_files:
            self.stdout.write(
                self.style.WARNING('No HTML files found to validate.')
            )
            return

        self.stdout.write(f'Found {len(html_files)} HTML files to validate\n')

        # Process each HTML file
        for html_file in html_files:
            self.process_html_file(html_file)

        # Find unused components
        self.find_unused_components()

        # Report results
        self.report_results()

    def find_html_files(self, directory):
        """Recursively find all HTML files in a directory"""
        html_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(Path(root) / file)
        return html_files

    def process_html_file(self, html_file):
        """Process a single HTML file to find Cotton components"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.processed_files += 1
            
            # Find all Cotton component tags using regex
            # Pattern matches: <c-component-name> and stops at space, closing bracket, or template variables
            cotton_pattern = r'<c-([a-zA-Z0-9._-]+)'
            matches = re.findall(cotton_pattern, content)
            
            # Also check for dynamic component usage (contains template variables)
            dynamic_pattern = r'<c-([a-zA-Z0-9._-]*\{\{[^}]+\}\}[a-zA-Z0-9._-]*)'
            dynamic_matches = re.findall(dynamic_pattern, content)
            
            # Remove duplicates while preserving order
            matches = list(dict.fromkeys(matches))
            dynamic_matches = list(dict.fromkeys(dynamic_matches))
            
            # Report dynamic component usage as violations
            for dynamic_match in dynamic_matches:
                self.dynamic_components.append({
                    'component': dynamic_match,
                    'source_file': html_file
                })
            
            # Filter out components that end with a dot (incomplete dynamic patterns)
            # and components that contain template variables
            clean_matches = []
            for match in matches:
                if not match.endswith('.') and '{{' not in match:
                    clean_matches.append(match)
            
            matches = clean_matches
            
            if not matches:
                return
                
            self.total_components_found += len(matches)
            
            if self.verbose:
                self.stdout.write(f'\nProcessing: {html_file}')
                
            for component_name in matches:
                # Track that this component is referenced
                self.referenced_components.add(component_name)
                self.validate_component(component_name, html_file)
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing {html_file}: {str(e)}')
            )

    def validate_component(self, component_name, source_file):
        """Validate if a Cotton component exists"""
        # Convert component name to file path
        component_paths = self.get_component_paths(component_name)
        
        component_found = False
        for path in component_paths:
            if path.exists():
                component_found = True
                if self.verbose:
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ {component_name} -> {path}')
                    )
                break
        
        if not component_found:
            self.unresolved_components.append({
                'component': component_name,
                'source_file': source_file,
                'expected_paths': component_paths
            })
            
            if self.verbose:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ {component_name} (not found)')
                )

    def get_component_paths(self, component_name):
        """
        Convert Cotton component name to possible file paths
        
        Cotton naming conventions:
        - <c-component> -> cotton/component.html
        - <c-app.component> -> cotton/app/component.html  
        - <c-component.variant> -> cotton/component/variant.html
        - <c-component> can also be -> cotton/component/index.html
        """
        paths = []
        
        # Special handling for built-in Cotton tags that don't need files
        builtin_tags = ['vars', 'slot', 'component']
        if component_name in builtin_tags:
            return []  # These are built-in Cotton tags, not file components
        
        # Handle dot notation (app.component or component.variant)
        if '.' in component_name:
            parts = component_name.split('.')
            
            # For app.component pattern
            if len(parts) == 2:
                app_name, comp_name = parts
                
                # Convert hyphens to underscores for file names
                comp_file = comp_name.replace('-', '_')
                
                # Try cotton/app/component.html in main templates
                paths.append(Path(f'onlydjango/templates/cotton/{app_name}/{comp_file}.html'))
                paths.append(Path(f'onlydjango/templates/cotton/{app_name}/{comp_file}/index.html'))
                
                # Try in components subdirectory
                paths.append(Path(f'onlydjango/templates/cotton/components/{app_name}/{comp_file}.html'))
                paths.append(Path(f'onlydjango/templates/cotton/components/{app_name}/{comp_file}/index.html'))
                
                # Try in all app directories
                for app_dir in Path('apps').glob('*/templates/cotton'):
                    app_dir_name = app_dir.parent.parent.name
                    paths.append(app_dir / app_dir_name / f'{comp_file}.html')
                    paths.append(app_dir / app_dir_name / comp_file / 'index.html')
                    paths.append(app_dir / app_dir_name / 'components' / f'{comp_file}.html')
                    paths.append(app_dir / app_dir_name / 'components' / comp_file / 'index.html')
            
            # For deeper nesting like app.folder.component
            elif len(parts) > 2:
                # Join all but last as folder path, last as filename
                folder_path = '/'.join(parts[:-1])
                filename = parts[-1].replace('-', '_')
                
                paths.append(Path(f'onlydjango/templates/cotton/{folder_path}/{filename}.html'))
                paths.append(Path(f'onlydjango/templates/cotton/{folder_path}/{filename}/index.html'))
                paths.append(Path(f'onlydjango/templates/cotton/components/{folder_path}/{filename}.html'))
                paths.append(Path(f'onlydjango/templates/cotton/components/{folder_path}/{filename}/index.html'))
                
                # Try in all app directories
                for app_dir in Path('apps').glob('*/templates/cotton'):
                    paths.append(app_dir / folder_path / f'{filename}.html')
                    paths.append(app_dir / folder_path / filename / 'index.html')
        
        else:
            # Simple component name without dots
            # Convert hyphens to underscores for file names
            file_name = component_name.replace('-', '_')
            
            # Try cotton/component.html in main templates
            paths.append(Path(f'onlydjango/templates/cotton/{file_name}.html'))
            paths.append(Path(f'onlydjango/templates/cotton/{file_name}/index.html'))
            
            # Try in components subdirectory
            paths.append(Path(f'onlydjango/templates/cotton/components/{file_name}.html'))
            paths.append(Path(f'onlydjango/templates/cotton/components/{file_name}/index.html'))
            
            # Try in all app directories
            for app_dir in Path('apps').glob('*/templates/cotton'):
                app_name = app_dir.parent.parent.name
                paths.append(app_dir / app_name / f'{file_name}.html')
                paths.append(app_dir / app_name / file_name / 'index.html')
                paths.append(app_dir / app_name / 'components' / f'{file_name}.html')
                paths.append(app_dir / app_name / 'components' / file_name / 'index.html')
        
        return paths

    def find_unused_components(self):
        """Find Cotton component files that are not referenced anywhere"""
        # Find all Cotton component files
        cotton_directories = [
            Path('onlydjango/templates/cotton'),
            *Path('apps').glob('*/templates/cotton')
        ]
        
        all_component_files = []
        for cotton_dir in cotton_directories:
            if cotton_dir.exists():
                all_component_files.extend(self.find_html_files(cotton_dir))
        
        # Convert file paths to component names and check if they're referenced
        for component_file in all_component_files:
            component_names = self.file_path_to_component_names(component_file)
            
            # Check if any of the possible component names for this file are referenced
            is_referenced = False
            for comp_name in component_names:
                if comp_name in self.referenced_components:
                    is_referenced = True
                    break
            
            if not is_referenced and component_names:
                self.unused_components.append({
                    'file_path': component_file,
                    'component_names': component_names
                })

    def file_path_to_component_names(self, file_path):
        """Convert a Cotton component file path to possible component names"""
        component_names = []
        
        # Convert Path to string for easier manipulation and normalize separators
        path_str = str(file_path).replace('\\', '/')
        
        # Find the cotton directory part
        if '/cotton/' in path_str:
            # Extract the part after /cotton/
            cotton_part = path_str.split('/cotton/', 1)[1]
            
            # Remove .html extension
            if cotton_part.endswith('.html'):
                cotton_part = cotton_part[:-5]
            
            # Handle index.html files (they represent the parent directory)
            if cotton_part.endswith('/index'):
                cotton_part = cotton_part[:-6]
            
            # Convert underscores to hyphens in file names (Cotton convention)
            cotton_part = cotton_part.replace('_', '-')
            
            # Handle different component directory structures
            if cotton_part.startswith('components/'):
                # Remove 'components/' prefix and convert to ui. prefix
                ui_part = cotton_part[11:]  # Remove 'components/'
                component_name = f'ui.{ui_part.replace("/", ".")}'
                component_names.append(component_name)
            else:
                # Direct cotton component (like layout.html, nav.html, etc.)
                component_name = cotton_part.replace('/', '.')
                component_names.append(component_name)
        
        return component_names

    def report_results(self):
        """Report validation results"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('COTTON COMPONENT VALIDATION RESULTS')
        self.stdout.write('='*60)
        
        self.stdout.write(f'Files processed: {self.processed_files}')
        self.stdout.write(f'Components found: {self.total_components_found}')
        self.stdout.write(f'Unresolved components: {len(self.unresolved_components)}')
        self.stdout.write(f'Dynamic component violations: {len(self.dynamic_components)}')
        self.stdout.write(f'Unused component files: {len(self.unused_components)}')
        
        # Report dynamic component violations first (more critical)
        if self.dynamic_components:
            self.stdout.write('\n' + self.style.ERROR('DYNAMIC COMPONENT VIOLATIONS:'))
            self.stdout.write(self.style.ERROR('Dynamic component names are NOT allowed in our development philosophy!'))
            self.stdout.write('-'*60)
            
            # Group by component pattern for cleaner output
            dynamic_groups = {}
            for item in self.dynamic_components:
                comp_name = item['component']
                if comp_name not in dynamic_groups:
                    dynamic_groups[comp_name] = []
                dynamic_groups[comp_name].append(item)
            
            for comp_name, items in dynamic_groups.items():
                self.stdout.write(
                    self.style.ERROR(f'\n⚠ Dynamic Component: {comp_name}')
                )
                self.stdout.write(f'  Found in {len(items)} file(s):')
                for item in items[:5]:  # Show first 5 files
                    self.stdout.write(f'    - {item["source_file"]}')
                if len(items) > 5:
                    self.stdout.write(f'    ... and {len(items) - 5} more files')
                self.stdout.write('  ⚠ FIX: Replace with static component names')

        if self.unresolved_components:
            self.stdout.write('\n' + self.style.ERROR('UNRESOLVED COMPONENTS:'))
            self.stdout.write('-'*60)
            
            # Group by component name for cleaner output
            component_groups = {}
            for item in self.unresolved_components:
                comp_name = item['component']
                if comp_name not in component_groups:
                    component_groups[comp_name] = []
                component_groups[comp_name].append(item)
            
            for comp_name, items in component_groups.items():
                self.stdout.write(
                    self.style.ERROR(f'\n✗ Component: {comp_name}')
                )
                self.stdout.write(f'  Used in {len(items)} file(s):')
                for item in items[:5]:  # Show first 5 files
                    self.stdout.write(f'    - {item["source_file"]}')
                if len(items) > 5:
                    self.stdout.write(f'    ... and {len(items) - 5} more files')
                
                # Show expected paths for first item
                if items:
                    self.stdout.write('  Expected paths:')
                    for path in items[0]['expected_paths'][:3]:  # Show first 3 paths
                        self.stdout.write(f'    - {path}')
                    if len(items[0]['expected_paths']) > 3:
                        self.stdout.write(f'    ... and {len(items[0]["expected_paths"]) - 3} more')

        if self.unused_components:
            self.stdout.write('\n' + self.style.WARNING('UNUSED COMPONENT FILES:'))
            self.stdout.write('These Cotton component files exist but are not referenced anywhere.')
            self.stdout.write('Consider removing them to keep the codebase clean.')
            self.stdout.write('-'*60)
            
            for item in self.unused_components:
                self.stdout.write(
                    self.style.WARNING(f'\n📁 File: {item["file_path"]}')
                )
                self.stdout.write(f'  Possible component names: {", ".join(item["component_names"])}')
                self.stdout.write('  💡 ACTION: Review and consider removing if truly unused')
        
        if not self.unresolved_components and not self.dynamic_components and not self.unused_components:
            self.stdout.write(
                self.style.SUCCESS('\n✓ All Cotton components are properly resolved and used!')
            )
        
        self.stdout.write('\n' + '='*60)