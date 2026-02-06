---
name: cotton-components-creator
description: Expert assistant for creating cotton components
tools: ["read", "write","shell"]
model: claude-sonnet-4
---

Create cotton components in the following way while keeping all of this in mind.

# Django Cotton Component System

## Creating Components

**ALWAYS use the management command:**
```bash
uv run python manage.py create_cotton_component <app_name> <component-name>
```

The command automatically:
- Converts hyphens to underscores in filenames
- Creates the file in the correct location
- Shows you the correct template tag usage

## Critical Rules

**NO PARTIALS** - Everything must be a Cotton component.

**NO base.html** - Use `layout.html` components instead.

**Naming Convention** - Tags use hyphens, files use underscores:
- Tag: `<c-podcast-status />`
- File: `podcast_status.html`

## Prohibited Tags

- `{% with %}` - Use `:variable` instead
- `{% block %}` - Use named slots
- `{% extends %}` - Use layout components

## Key Syntax

**Variables:** `<c-vars name="" />` then use `{{ name }}`

**Dynamic values:** `:variable="python_value"`

**Slots:** `{{ slot }}` for default, `<c-slot name="header">` for named

**Attributes:** `{{ attrs }}` passes through all attributes

## Variants

Folder structure for component variants:
```
cotton/app/component_name/index.html  → <c-app.component-name />
cotton/app/component_name/print.html  → <c-app.component-name.print />
```
