"""Management command to create Cotton components with correct naming."""
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    """Create a Cotton component with proper underscore naming."""
    
    help = 'Create a Cotton component file with correct naming convention'
    
    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Django app name (e.g., selfmade)')
        parser.add_argument('component_name', type=str, help='Component name (hyphens will be converted to underscores)')
    
    def handle(self, *args, **options):
        app_name = options['app_name']
        component_name = options['component_name']
        
        # Convert hyphens to underscores for file path
        file_component_name = component_name.replace('-', '_')
        
        # Build the path
        cotton_dir = Path('apps') / app_name / 'templates' / 'cotton' / app_name
        cotton_dir.mkdir(parents=True, exist_ok=True)
        
        component_file = cotton_dir / f'{file_component_name}.html'
        
        # Create the file with basic structure
        if component_file.exists():
            self.stdout.write(self.style.WARNING(f'Component already exists: {component_file}'))
        else:
            component_file.write_text('<c-vars />\n\n{{ slot }}\n')
            self.stdout.write(self.style.SUCCESS(f'✓ Created component file: {component_file}'))
        
        # Generate the tag name (with hyphens)
        tag_component_name = file_component_name.replace('_', '-')
        tag_usage = f'<c-{app_name}.{tag_component_name} />'
        
        # Output reminder about naming convention
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('═' * 70))
        self.stdout.write(self.style.WARNING('REMINDER: Cotton component naming convention'))
        self.stdout.write(self.style.WARNING('  • File paths use UNDERSCORES: podcast_status.html'))
        self.stdout.write(self.style.WARNING('  • Template tags use HYPHENS: <c-podcast-status />'))
        self.stdout.write(self.style.WARNING('═' * 70))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Use in templates: {tag_usage}'))
        self.stdout.write('')
