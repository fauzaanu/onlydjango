---
inclusion: fileMatch
fileMatchPattern: "{**/*.html}"
---

# Cotton Component Architecture

## Component Structure

We use django-cotton components in the following architecture.

```
templates/cotton/{app}/{component_name}/
├── layout.html          # Static skeleton/wrapper
├── index.html          # Main component content
└── state/              # Dynamic state components
    ├── loading.html    # Loading state UI
    ├── error.html      # Error state UI (optional)
    └── success.html    # Success state UI (optional)
```

## How It Works

### Layout Component (`layout.html`)
Static skeleton that wraps all dynamic content. Contains `kandy-loading` and `kandy-content` elements. **Must provide its own container** for HTMX targeting:

```html
<div id="{component}-container">
    <c-ui.components.form-card :heading="heading">
        <div kandy-loading>
            <c-{app}.{component}.state.loading/>
        </div>
        
        <div kandy-content class="w-full">
            {{ slot }}
        </div>
    </c-ui.components.form-card>
</div>
```

### Index Component (`index.html`)
Main component logic and content. Uses the layout as wrapper. **Targets its own container** provided by layout:

```html
<c-{app}.{component}.layout>
    <form hx-post="{% url 'app:endpoint' %}" hx-target="#{component}-container">
        <!-- Component content -->
    </form>
</c-{app}.{component}.layout>
```

### State Components (`state/` folder)
Handle different UI states. Loading state shows spinner with message:

```html
<c-vars loading_text="Processing your request..." />

<div class="flex items-center justify-center">
    <div class="flex items-center space-x-3 text-gray-300">
        <i class="fas fa-spinner fa-spin text-lg"></i>
        <span class="text-sm">{{ loading_text }}</span>
    </div>
</div>
```

## Loading System (Kandy)

Uses simple attributes for state management:
- `kandy-loading`: Elements that show during loading
- `kandy-content`: Elements that hide during loading