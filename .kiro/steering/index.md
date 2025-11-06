---
inclusion: always
---

# Steering Guide Index

This project uses specific conventions and patterns. Reference the appropriate steering files based on your task:

## Templates & UI

**Working with HTML templates?** → Read `cotton docs summarized.md`
- Cotton component syntax and architecture
- Naming conventions (hyphens vs underscores)
- Kandy pattern for stateful components
- Prohibited template tags (no `{% extends %}`, `{% block %}`, `{% with %}`)
- No partials, no base.html

**Designing UI components?** → Read `Keep UI code lean.md`
- Use custom template tags and filters to reduce template code
- Keep components minimal and reusable

## Views & Business Logic

**Writing views?** → Read `Writing views.md` and `fat models and thin views.md`
- Use class-based views inheriting from `View` (no generic views)
- Keep views thin, move logic to model classmethods
- Move complex context to services if over 50 lines

**Working with forms?** → Read `using django forms.md`
- Use Django forms for POST validation only
- Don't pass forms to templates on GET requests
- Build custom form HTML with Tailwind
- Remember CSRF tokens and exact field names

**Dealing with database queries?** → Read `avoiding n+1.md`
- Use `select_related` and `prefetch_related`
- Optimize queries in model classmethods

**Adding pagination?** → Read `paginate.md`
- Add pagination only when necessary (blogs yes, team members no)

## Background Tasks & Events

**Using signals or background tasks?** → Read `signals tasks commands.md`
- Use signals appropriately
- Create Huey tasks for heavy operations
- Make tasks triggerable via management commands
- Use Django messages framework for user notifications

## Testing

**Writing tests?** → Read `writing tests.md`
- Create a test class for each view
- Test both GET and POST methods
- Use base TestCase for shared login logic

## Database & Models

**Modifying models?** → Read `dont create migrations.md`
- Never manually create migrations
- Generate with `uv run python manage.py makemigrations`
- Don't delete migrations unless explicitly instructed

**Working with admin.py?** → Read `dont bother with admin.md`
- Skip admin.py unless explicitly requested

## Code Quality & Workflow

**Before committing code** → Read `checks.md`
- Run validation commands based on scope of changes
- `uv run pyright`, `uv run ruff check --fix`, etc.

**Managing your workflow** → Read `managing focus.md`
- Write production-quality code following conventions
- No ad-hoc test files at repository root
- No markdown progress tracking files
- Trust the dev environment is configured

**Facing complex tasks?** → Read `harder tasks.md`
- Delegate directory deletion to humans
- Stop and ask for clarification when stuck
- Recognize when tasks need human judgment
