---
inclusion: fileMatch
fileMatchPattern: '**/*.html'
---

# Django Cotton Component System

## Critical Rules

**NO PARTIALS** - Everything must be a Cotton component. Delete any `partials/` folders immediately.

**NO base.html** - Use `layout.html` components instead per Cotton guidelines.

**Naming Convention** - Component tags use hyphens, file paths use underscores:
- Tag: `<c-file-name />` or `<c-app.application-card />`
- File: `cotton/file_name.html` or `cotton/app/application_card.html`

## Prohibited Django Template Tags

Do NOT use these tags - Cotton components replace their functionality:
- `{% with %}` - Pass variables directly to components with `:variable`
- `{% block %}` - Use named slots instead
- `{% extends %}` - Use layout components instead

## Dynamic Attributes

Prefix `:` to pass Python values instead of strings:
```html
<c-weather :temperature="temp_var" :today="today_obj" />
<c-mycomp :items="['a','b','c']" :count="1" :flag="None" />
<c-mycomp :data="{'key': 'value'}" />
<c-select :options="form.field.choices" />
```

## Component Variants

Convert a file to a folder with `index.html` as default:
```
cotton/report/file_name/index.html    → <c-report.file-name />
cotton/report/file_name/print.html    → <c-report.file-name.print />
```

## Core Syntax

**Default Slot**
```html
<!-- cotton/box.html -->
<div class="box">{{ slot }}</div>
<!-- usage -->
<c-box>Content here</c-box>
```

**Named Slots**
```html
<c-card>
  <c-slot name="header">Title</c-slot>
  <c-slot name="body">Content</c-slot>
</c-card>
```

**Attributes & `{{ attrs }}`**
```html
<!-- component -->
<input {{ attrs }} />
<!-- usage -->
<c-input name="email" placeholder="Enter email" required />
<c-input :attrs="form_widget_attrs" />
```

**Variables with `<c-vars />`**
```html
<c-vars type="success" size="md" />
<div class="alert-{{ type }} size-{{ size }}">{{ slot }}</div>
```

**Boolean Attributes**
```html
<c-input required />  <!-- required=True -->
```

**Dynamic Components**
```html
<c-component :is="icon_component_name" />
```

**Context Isolation**
```html
<c-component only />  <!-- Limits context to passed props -->
```

## Alpine.js Integration

- Access `x-data` via `{{ x_data }}`
- Use `::` prefix to preserve `:` in attributes: `::x-bind:value`

## Component Architecture (Kandy Pattern)

Structure for stateful components with loading states:

```
templates/cotton/{app}/{component_name}/
├── layout.html          # Static skeleton/wrapper
├── index.html          # Main component content
└── state/              # Dynamic state components
    ├── loading.html    # Loading state UI
    ├── error.html      # Error state UI (optional)
    └── success.html    # Success state UI (optional)
```

**Layout Component** - Provides container for HTMX targeting:
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

**Index Component** - Main logic, targets its own container:
```html
<c-{app}.{component}.layout>
    <form hx-post="{% url 'app:endpoint' %}" hx-target="#{component}-container">
        <!-- Component content -->
    </form>
</c-{app}.{component}.layout>
```

**Loading State** - Shows spinner with message:
```html
<c-vars loading_text="Processing your request..." />

<div class="flex items-center justify-center">
    <div class="flex items-center space-x-3 text-gray-300">
        <i class="fas fa-spinner fa-spin text-lg"></i>
        <span class="text-sm">{{ loading_text }}</span>
    </div>
</div>
```

**Kandy Attributes** for state management:
- `kandy-loading`: Elements that show during loading
- `kandy-content`: Elements that hide during loading

## Template Structure

```
templates/
├─ cotton/<app>/      # Reusable components
│   └─ component.html
└─ <app>/            # Full-page templates
    └─ page.html
```

Components use dot notation: `<c-app.component-name />`
