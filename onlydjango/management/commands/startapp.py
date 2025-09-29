# startapp.py
import os
import re
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = (
        "Like startapp, but always under apps/, "
        "with AppConfig.name='apps.<appname>' and auto-added to FIRST_PARTY_APPS."
    )

    def add_to_settings(self, app_name):
        base_path = os.path.join('onlydjango', 'settings', 'base.py')
        if os.path.exists(base_path):
            content = open(base_path, 'r').read().splitlines(keepends=True)
            out = []
            injected = False
            for line in content:
                if (not injected
                        and re.match(r'\s*FIRST_PARTY_APPS\s*=.*\[\s*', line)
                ):
                    out.append(line)
                    # keep app entries until closing bracket
                    continue
                if (not injected
                        and re.match(r'\s*\]', line)
                        and 'FIRST_PARTY_APPS' not in line
                ):
                    indent = re.match(r'^(\s*)\]', line).group(1)
                    out.append(f"{indent}'apps.{app_name}',\n")
                    injected = True
                out.append(line)
            if injected:
                open(base_path, 'w').write(''.join(out))
                self.stdout.write(self.style.SUCCESS(
                    f"Added 'apps.{app_name}' to FIRST_PARTY_APPS in base.py"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    "Could not find FIRST_PARTY_APPS to inject into."
                ))
        else:
            self.stdout.write(self.style.WARNING(
                f"Settings file not found at {base_path}"
            ))

    def patch_into_apps(self, app_name, target_dir):
        apps_py = os.path.join(target_dir, 'apps.py')
        text = open(apps_py, 'r').read()
        text = re.sub(
            r"name\s*=\s*['\"][\w\.]+['\"]",
            f"name = 'apps.{app_name}'",
            text
        )
        open(apps_py, 'w').write(text)

    def create_templatetags_folder(self, target_dir):
        """Create templatetags folder with __init__.py"""
        templatetags_dir = os.path.join(target_dir, 'templatetags')
        os.makedirs(templatetags_dir, exist_ok=True)
        
        init_py = os.path.join(templatetags_dir, '__init__.py')
        if not os.path.exists(init_py):
            open(init_py, 'w').close()
            self.stdout.write(self.style.SUCCESS(
                f"Created templatetags folder with __init__.py"
            ))

    def create_templates_structure(self, target_dir, app_name):
        """Create templates folder with app subfolder and cotton subfolder with layout.html"""
        templates_dir = os.path.join(target_dir, 'templates')
        app_templates_dir = os.path.join(templates_dir, app_name)
        cotton_dir = os.path.join(templates_dir, 'cotton')
        
        # Create both directories
        os.makedirs(app_templates_dir, exist_ok=True)
        os.makedirs(cotton_dir, exist_ok=True)
        
        # Create layout.html in the cotton directory
        layout_html = os.path.join(cotton_dir, 'layout.html')
        if not os.path.exists(layout_html):
            layout_content = '''
<c-layout>
    {{ slot }}
</c-layout>
'''.replace('{{ app_name }}', app_name)
            with open(layout_html, 'w') as f:
                f.write(layout_content)

    def remove_tests_py_and_create_tests_dir(self, target_dir):
        """Remove tests.py and create tests directory with required files"""
        tests_py = os.path.join(target_dir, 'tests.py')
        if os.path.exists(tests_py):
            os.remove(tests_py)
            self.stdout.write(self.style.SUCCESS("Removed tests.py"))
        
        tests_dir = os.path.join(target_dir, 'tests')
        os.makedirs(tests_dir, exist_ok=True)
        
        # Create __init__.py
        init_py = os.path.join(tests_dir, '__init__.py')
        if not os.path.exists(init_py):
            open(init_py, 'w').close()
        
        # Create test_views.py
        test_views_py = os.path.join(tests_dir, 'test_views.py')
        if not os.path.exists(test_views_py):
            test_views_content = '''from django.test import TestCase
from django.urls import reverse


class ViewTestCase(TestCase):
    """Base test case for views"""
    
    def setUp(self):
        pass
    
    # Add your view tests here
'''
            with open(test_views_py, 'w') as f:
                f.write(test_views_content)
        
        # Create test_models.py
        test_models_py = os.path.join(tests_dir, 'test_models.py')
        if not os.path.exists(test_models_py):
            test_models_content = '''from django.test import TestCase


class ModelTestCase(TestCase):
    """Base test case for models"""
    
    def setUp(self):
        pass
    
    # Add your model tests here
'''
            with open(test_models_py, 'w') as f:
                f.write(test_models_content)

    def create_signals_file(self, target_dir):
        """Create signals.py file"""
        signals_py = os.path.join(target_dir, 'signals.py')
        if not os.path.exists(signals_py):
            signals_content = '''from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from .models import YourModel


# Example signal
# @receiver(post_save, sender=YourModel)
# def your_model_post_save(sender, instance, created, **kwargs):
#     """Signal handler for YourModel post_save"""
#     if created:
#         # Handle new instance creation
#         pass
#     else:
#         # Handle instance update
#         pass
'''
            with open(signals_py, 'w') as f:
                f.write(signals_content)
            
            self.stdout.write(self.style.SUCCESS("Created signals.py"))

    def handle(self, *args, **options):
        app_name = options['name']

        os.makedirs('apps', exist_ok=True)
        init_py = os.path.join('apps', '__init__.py')
        if not os.path.exists(init_py):
            open(init_py, 'w').close()

        target_dir = os.path.join('apps', app_name)
        options['directory'] = target_dir
        os.makedirs(target_dir, exist_ok=True)
        super().handle(*args, **options)

        self.patch_into_apps(app_name, target_dir)
        self.add_to_settings(app_name)
        
        # Add the new functionality
        self.create_templatetags_folder(target_dir)
        self.create_templates_structure(target_dir, app_name)
        self.remove_tests_py_and_create_tests_dir(target_dir)
        self.create_signals_file(target_dir)
