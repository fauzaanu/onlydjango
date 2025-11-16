---
inclusion: always
---

# Model Schema Verification

## Critical Rule

**Never assume model field names, types, or relationships.** Always verify the actual model definition before writing ORM code.

## Verification Command

```bash
uv run python manage.py model_schema "ModelName"
```

This command outputs the complete model definition including:
- All field names and types
- Foreign key relationships
- Many-to-many relationships
- Custom methods and properties
- Related name configurations

## When to Verify

Verify model schema before:
- Writing queries with `filter()`, `get()`, or `create()`
- Accessing model fields in views or templates
- Creating or modifying forms
- Writing model methods that reference other fields
- Setting up `select_related()` or `prefetch_related()`

## Common Mistakes to Avoid

- Assuming field names (e.g., `user` vs `student` vs `owner`)
- Guessing relationship types (ForeignKey vs OneToOne vs ManyToMany)
- Using incorrect `related_name` in reverse lookups
- Accessing fields that don't exist or have been renamed

## Example Usage

```bash
# Check Student model fields
uv run python manage.py model_schema "Student"

# Check CustomTopic relationships
uv run python manage.py model_schema "CustomTopic"
```

Always verify first, code second.
