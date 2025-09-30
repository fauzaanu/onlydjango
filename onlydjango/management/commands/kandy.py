import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from pathlib import Path
import re


class Command(BaseCommand):
    help = 'Generate Cotton components with Kandy loading system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='App name (skip interactive selection)',
        )
        parser.add_argument(
            '--component',
            type=str,
            help='Component name (skip interactive input)',
        )
        parser.add_argument(
            '--htmx',
            action='store_true',
            help='Include HTMX functionality',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🍭 Kandy Component Generator')
        )
        self.stdout.write('Creating Cotton components with Kandy loading system\n')

        # Get app selection
        app_name = options.get('app') or self.select_app()
        
        # Get component name
        component_name = options.get('component') or self.get_component_name()
        
        # Ask about HTMX if not specified
        include_htmx = options.get('htmx') or self.ask_htmx()
        
        # Get HTML tag and HTTP method if HTMX is enabled
        html_tag = None
        http_method = None
        if include_htmx:
            html_tag = self.get_html_tag()
            http_method = self.get_http_method(html_tag)
        
        # Generate the component
        self.generate_component(app_name, component_name, include_htmx, html_tag, http_method)
        
        # Show usage instructions
        self.show_usage_instructions(app_name, component_name, include_htmx)

    def select_app(self):
        """Interactive app selection"""
        # Get all Django apps with templates/cotton directories
        available_apps = []
        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path)
            cotton_path = app_path / 'templates' / 'cotton'
            if cotton_path.exists() or app_config.name.startswith('apps.'):
                available_apps.append(app_config.name.split('.')[-1])
        
        if not available_apps:
            raise CommandError("No apps found with Cotton template structure")
        
        self.stdout.write("📱 Available apps:")
        for i, app in enumerate(available_apps, 1):
            self.stdout.write(f"  {i}. {app}")
        
        while True:
            try:
                choice = input("\nSelect app (number): ").strip()
                index = int(choice) - 1
                if 0 <= index < len(available_apps):
                    return available_apps[index]
                else:
                    self.stdout.write(self.style.ERROR("Invalid selection"))
            except (ValueError, KeyboardInterrupt):
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def get_component_name(self):
        """Get component name with validation"""
        while True:
            try:
                name = input("🏷️  Component name (snake_case): ").strip()
                if not name:
                    self.stdout.write(self.style.ERROR("Component name cannot be empty"))
                    continue
                
                # Validate snake_case
                if not re.match(r'^[a-z][a-z0-9_]*$', name):
                    self.stdout.write(self.style.ERROR("Use snake_case (lowercase, underscores only)"))
                    continue
                
                return name
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def ask_htmx(self):
        """Ask if component should include HTMX functionality"""
        while True:
            try:
                response = input("🔄 Include HTMX functionality? (y/N): ").strip().lower()
                return response in ['y', 'yes']
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def get_html_tag(self):
        """Get HTML tag for interactive element"""
        while True:
            try:
                tag = input("🏷️  HTML tag for interactive element (form/button/div): ").strip().lower()
                if not tag:
                    self.stdout.write(self.style.ERROR("HTML tag cannot be empty"))
                    continue
                
                # Validate common tags
                if tag not in ['form', 'button', 'div', 'a', 'span', 'input']:
                    confirm = input(f"⚠️  '{tag}' is uncommon. Continue? (y/N): ").strip().lower()
                    if confirm not in ['y', 'yes']:
                        continue
                
                return tag
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def get_http_method(self, html_tag):
        """Get HTTP method for HTMX requests"""
        # Default based on HTML tag
        default_method = 'post' if html_tag == 'form' else 'get'
        
        while True:
            try:
                method = input(f"🌐 HTTP method (get/post) [{default_method}]: ").strip().lower()
                if not method:
                    return default_method
                
                if method in ['get', 'post']:
                    return method
                else:
                    self.stdout.write(self.style.ERROR("Please enter 'get' or 'post'"))
                    continue
                    
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def generate_component(self, app_name, component_name, include_htmx, html_tag, http_method):
        """Generate the complete component structure"""
        # Create directory structure
        base_path = Path(f"apps/{app_name}/templates/cotton/{app_name}/{component_name}")
        base_path.mkdir(parents=True, exist_ok=True)
        
        state_path = base_path / "state"
        state_path.mkdir(exist_ok=True)
        
        # Generate files
        self.create_layout_file(base_path, app_name, component_name)
        self.create_index_file(base_path, app_name, component_name, include_htmx, html_tag)
        self.create_loading_file(state_path, component_name)
        
        # Create view if HTMX is enabled
        if include_htmx:
            auto_create = self.ask_auto_create_files()
            if auto_create:
                self.create_view_and_url(app_name, component_name)
            else:
                self.suggest_view_code(app_name, component_name)
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Component '{component_name}' created successfully!")
        )
        self.stdout.write(f"📁 Location: {base_path}")

    def create_layout_file(self, base_path, app_name, component_name):
        """Create layout.html file"""
        container_id = f"{component_name.replace('_', '-')}-container"
        
        content = f'''<c-vars heading="{component_name.replace('_', ' ').title()}" />

<div id="{container_id}">
    <c-ui.components.form-card :heading="heading">
        <div kandy-loading>
            <c-{app_name}.{component_name}.state.loading/>
        </div>
        
        <div kandy-content class="w-full">
            {{{{ slot }}}}
        </div>
    </c-ui.components.form-card>
</div>'''
        
        layout_file = base_path / "layout.html"
        layout_file.write_text(content)
        self.stdout.write(f"📄 Created: {layout_file}")

    def create_index_file(self, base_path, app_name, component_name, include_htmx, html_tag):
        """Create index.html file"""
        container_id = f"{component_name.replace('_', '-')}-container"
        
        if include_htmx and html_tag:
            # Generate HTMX-enabled component
            htmx_method = 'post' if html_tag == 'form' else 'post'
            htmx_trigger = 'submit' if html_tag == 'form' else 'click'
            
            if html_tag == 'form':
                content = f'''<c-{app_name}.{component_name}.layout>
    <{html_tag} hx-{htmx_method}="{{%% url '{app_name}:{component_name}' %%}}" 
          hx-trigger="{htmx_trigger}" 
          hx-target="#{container_id}"
          class="space-y-4">
        
        {{%% csrf_token %%}}
        
        <!-- Add your form fields here -->
        <div class="flex flex-col space-y-1.5">
            <label class="text-sm font-medium text-gray-300">
                Field Label
            </label>
            <input type="text" 
                   name="field_name"
                   class="input_dark_design"
                   placeholder="Enter value...">
        </div>
        
        <!-- Submit button with inline loading -->
        <button type="submit" 
                class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center space-x-2 transition-colors">
            <span>Submit</span>
            <i kandy-loading class="fas fa-spinner fa-spin text-sm"></i>
        </button>
    </{html_tag}>
</c-{app_name}.{component_name}.layout>'''
            else:
                content = f'''<c-{app_name}.{component_name}.layout>
    <{html_tag} hx-{htmx_method}="{{%% url '{app_name}:{component_name}' %%}}" 
            hx-trigger="{htmx_trigger}" 
            hx-target="#{container_id}"
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center space-x-2 transition-colors">
        
        <span>{component_name.replace('_', ' ').title()}</span>
        <i kandy-loading class="fas fa-spinner fa-spin text-sm"></i>
    </{html_tag}>
</c-{app_name}.{component_name}.layout>'''
        else:
            # Generate static component
            content = f'''<c-{app_name}.{component_name}.layout>
    <!-- Component content -->
    <div class="space-y-4">
        <div class="text-gray-300">
            <h3 class="text-lg font-medium mb-2">{component_name.replace('_', ' ').title()}</h3>
            <p>Add your component content here.</p>
        </div>
    </div>
</c-{app_name}.{component_name}.layout>'''
        
        index_file = base_path / "index.html"
        index_file.write_text(content)
        self.stdout.write(f"📄 Created: {index_file}")

    def create_loading_file(self, state_path, component_name):
        """Create loading.html file"""
        loading_text = f"Processing {component_name.replace('_', ' ')}..."
        
        content = f'''<c-vars loading_text="{loading_text}" />

<div class="flex items-center justify-center">
    <div class="flex items-center space-x-3 text-gray-300">
        <i class="fas fa-spinner fa-spin text-lg"></i>
        <span class="text-sm">{{{{ loading_text }}}}</span>
    </div>
</div>'''
        
        loading_file = state_path / "loading.html"
        loading_file.write_text(content)
        self.stdout.write(f"📄 Created: {loading_file}")

    def ask_auto_create_files(self):
        """Ask if user wants to auto-create view and URL files"""
        while True:
            try:
                response = input("📝 Auto-create view and URL code? (y/N): ").strip().lower()
                return response in ['y', 'yes']
            except KeyboardInterrupt:
                self.stdout.write(self.style.ERROR("\nOperation cancelled"))
                exit(1)

    def create_view_and_url(self, app_name, component_name):
        """Create view and URL code in the actual files"""
        try:
            self.append_view_code(app_name, component_name)
            self.append_url_code(app_name, component_name)
            self.stdout.write(self.style.SUCCESS("✅ View and URL code added successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating files: {str(e)}"))
            self.suggest_view_code(app_name, component_name)

    def append_view_code(self, app_name, component_name):
        """Append view code to views.py"""
        view_name = ''.join(word.capitalize() for word in component_name.split('_')) + 'View'
        views_file = Path(f"apps/{app_name}/views.py")
        
        if not views_file.exists():
            raise FileNotFoundError(f"views.py not found at {views_file}")
        
        view_code = f'''

class {view_name}(LessonPlannerLoginRequiredMixin, View):
    """
    {component_name.replace('_', ' ').title()} component view
    """
    
    def post(self, request):
        # Process the request
        # Add your logic here
        
        return render(request, "cotton/{app_name}/{component_name}/index.html", {{
            # Add context data here
        }})
'''
        
        # Read current content
        current_content = views_file.read_text()
        
        # Check if view already exists
        if view_name in current_content:
            self.stdout.write(self.style.WARNING(f"⚠️  View '{view_name}' already exists, skipping"))
            return
        
        # Append the view code
        with open(views_file, 'a', encoding='utf-8') as f:
            f.write(view_code)
        
        self.stdout.write(f"📄 Added view to: {views_file}")

    def append_url_code(self, app_name, component_name):
        """Append URL pattern to urls.py"""
        view_name = ''.join(word.capitalize() for word in component_name.split('_')) + 'View'
        urls_file = Path(f"apps/{app_name}/urls.py")
        
        if not urls_file.exists():
            raise FileNotFoundError(f"urls.py not found at {urls_file}")
        
        url_pattern = f'    path("{component_name.replace("_", "-")}/", views.{view_name}.as_view(), name="{component_name}"),'
        
        # Read current content
        current_content = urls_file.read_text()
        
        # Check if URL pattern already exists
        if component_name in current_content:
            self.stdout.write(self.style.WARNING(f"⚠️  URL pattern for '{component_name}' already exists, skipping"))
            return
        
        # Find the urlpatterns list and insert before the closing bracket
        lines = current_content.split('\n')
        insert_index = -1
        
        # Look for the closing bracket of urlpatterns
        in_urlpatterns = False
        for i, line in enumerate(lines):
            if 'urlpatterns' in line and '[' in line:
                in_urlpatterns = True
                continue
            
            if in_urlpatterns:
                # Look for closing bracket (could be on same line as last path or standalone)
                if ']' in line:
                    insert_index = i
                    break
        
        if insert_index == -1:
            raise ValueError("Could not find urlpatterns closing bracket in urls.py")
        
        # Check if the closing bracket is on the same line as content
        closing_line = lines[insert_index]
        if closing_line.strip() == ']':
            # Standalone closing bracket - insert before it
            lines.insert(insert_index, url_pattern)
        else:
            # Closing bracket on same line as last path - insert before this line
            lines.insert(insert_index, url_pattern)
        
        # Write back to file
        urls_file.write_text('\n'.join(lines))
        
        self.stdout.write(f"📄 Added URL to: {urls_file}")

    def suggest_view_code(self, app_name, component_name):
        """Suggest view code for HTMX components"""
        view_name = ''.join(word.capitalize() for word in component_name.split('_')) + 'View'
        
        self.stdout.write(f"\n💡 Suggested view code for views.py:")
        self.stdout.write(self.style.WARNING(f'''
class {view_name}(LessonPlannerLoginRequiredMixin, View):
    """
    {component_name.replace('_', ' ').title()} component view
    """
    
    def post(self, request):
        # Process the request
        # Add your logic here
        
        return render(request, "cotton/{app_name}/{component_name}/index.html", {{
            # Add context data here
        }})
'''))
        
        self.stdout.write(f"\n💡 Add to urls.py:")
        self.stdout.write(self.style.WARNING(f'''
    path("{component_name.replace('_', '-')}/", views.{view_name}.as_view(), name="{component_name}"),
'''))

    def show_usage_instructions(self, app_name, component_name, include_htmx):
        """Show usage instructions"""
        self.stdout.write(f"\n📖 Usage Instructions:")
        self.stdout.write(f"   In templates: <c-{app_name}.{component_name} />")
        self.stdout.write(f"   With props:   <c-{app_name}.{component_name} :data=\"data\" />")
        
        self.stdout.write(f"\n📁 Component structure:")
        self.stdout.write(f"   📄 layout.html  - Component wrapper with Kandy loading")
        self.stdout.write(f"   📄 index.html   - Main component content")
        self.stdout.write(f"   📁 state/       - Component states")
        self.stdout.write(f"      📄 loading.html - Loading state UI")
        
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Happy coding!"))