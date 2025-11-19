---
inclusion: always
---

# File Size and Refactoring Guidelines

## Size Limits

**250 lines is the threshold for refactoring.** When any file exceeds 250 lines, it must be refactored into smaller, focused units.

## Refactoring Strategies

### Python Files

Split large Python files into modules:

- **Views** - Group related views into separate files (e.g., `views/student.py`, `views/teacher.py`)
- **Models** - Separate models by domain (e.g., `models/user.py`, `models/content.py`)
- **Services** - Extract business logic into service modules
- **Utils** - Move helper functions to focused utility modules

Use `__init__.py` to maintain clean imports:

```python
# models/__init__.py
from .user import Student, Teacher
from .content import Topic, Quiz
```

### HTML Templates

Split large templates using Cotton components:

- **Extract repeated patterns** - Convert duplicated markup into reusable components
- **Break down complex pages** - Split sections into focused components
- **Follow naming conventions** - Use hyphens in component names (e.g., `quiz-card.html`)

Example refactoring:

```html
<!-- Before: 300-line template -->
<!-- After: Main template + components -->
<c-quiz-header :quiz="quiz" />
<c-quiz-questions :questions="questions" />
<c-quiz-results :score="score" />
```

## When to Refactor

- **Immediately** when a file reaches 250 lines during development
- **Before adding features** to files approaching the limit
- **During code review** if size violations are discovered

## Benefits

- Improved readability and maintainability
- Easier testing of isolated components
- Better code organization and discoverability
- Reduced merge conflicts in team environments
