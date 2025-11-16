import inspect
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    help = 'Display the schema of a Django model'

    def add_arguments(self, parser):
        parser.add_argument(
            'model',
            type=str,
            help='Model name in format "app_label.ModelName" or just "ModelName"'
        )

    def handle(self, *args, **options):
        model_name = options['model']
        
        # Try to find the model
        model = self.get_model(model_name)
        if not model:
            self.stdout.write(self.style.ERROR(f'Model "{model_name}" not found'))
            return
        
        # Get model file location
        model_file = inspect.getfile(model)
        source_lines, start_line = inspect.getsourcelines(model)
        end_line = start_line + len(source_lines) - 1
        
        # Convert to relative path from project root
        base_dir = Path(settings.BASE_DIR)
        try:
            relative_path = Path(model_file).relative_to(base_dir)
        except ValueError:
            relative_path = model_file
        
        # Display model location
        self.stdout.write(f'\nModel: {model.__name__}')
        self.stdout.write(f'{relative_path} [{start_line}:{end_line}]')
        
        # Display fields
        self.stdout.write('\nFields:')
        
        for field in model._meta.get_fields():
            field_type = field.__class__.__name__
            field_info = f'{field.name} ({field_type})'
            
            # Add additional info for specific field types
            if hasattr(field, 'max_length') and field.max_length:
                field_info += f' [max_length={field.max_length}]'
            if hasattr(field, 'null') and field.null:
                field_info += ' [null=True]'
            if hasattr(field, 'blank') and field.blank:
                field_info += ' [blank=True]'
            if hasattr(field, 'default') and field.default is not None:
                field_info += f' [default={field.default}]'
            if hasattr(field, 'related_model') and field.related_model:
                field_info += f' -> {field.related_model.__name__}'
            
            self.stdout.write(f'  {field_info}')
        
        # Display methods grouped by file
        self.stdout.write('\nMethods:')
        
        methods = self.get_model_methods(model, base_dir)
        if methods:
            # Group methods by file
            methods_by_file = {}
            for method_info in methods:
                file_path = str(method_info['file'])
                if file_path not in methods_by_file:
                    methods_by_file[file_path] = []
                methods_by_file[file_path].append(method_info)
            
            # Display grouped by file
            for file_path, file_methods in methods_by_file.items():
                self.stdout.write(f'  {file_path}')
                for method_info in file_methods:
                    lines = f'{method_info["start_line"]}:{method_info["end_line"]}'
                    self.stdout.write(f'    {method_info["name"]}() [{lines}]')
        else:
            self.stdout.write('  No custom methods found')
        
        self.stdout.write('')

    def get_model(self, model_name):
        """Find and return the model class."""
        # Try direct lookup with app_label.ModelName
        if '.' in model_name:
            try:
                return apps.get_model(model_name)
            except LookupError:
                pass
        
        # Search all apps for the model
        for app_config in apps.get_app_configs():
            try:
                return app_config.get_model(model_name)
            except LookupError:
                continue
        
        return None

    def get_model_methods(self, model, base_dir):
        """Get all custom methods defined on the model."""
        methods = []
        
        # Get instance methods and classmethods defined in the model
        for name in dir(model):
            if name.startswith('_'):
                continue
            
            try:
                attr = getattr(model, name)
                
                # Check if it's a callable
                if not callable(attr):
                    continue
                
                # Get the underlying function
                func = None
                if hasattr(attr, '__func__'):
                    func = attr.__func__
                elif inspect.isfunction(attr):
                    func = attr
                elif inspect.ismethod(attr):
                    func = attr.__func__ if hasattr(attr, '__func__') else None
                
                if func is None:
                    continue
                
                # Get source file
                source_file = inspect.getfile(func)
                
                # Only include methods defined in the project (not in site-packages)
                if 'site-packages' in source_file or '.venv' in source_file:
                    continue
                
                # Convert to relative path
                try:
                    relative_path = Path(source_file).relative_to(base_dir)
                except ValueError:
                    continue
                
                source_lines, start_line = inspect.getsourcelines(func)
                end_line = start_line + len(source_lines) - 1
                
                # Avoid duplicates
                if not any(m['name'] == name for m in methods):
                    methods.append({
                        'name': name,
                        'file': relative_path,
                        'start_line': start_line,
                        'end_line': end_line
                    })
            except (TypeError, OSError, AttributeError):
                pass
        
        return sorted(methods, key=lambda x: x['start_line'])
