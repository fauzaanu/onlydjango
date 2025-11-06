---
inclusion: fileMatch
fileMatchPattern: "**/models.py"
---

# Models and Views File Structure

Use modular file structures for views and models. Single-file `views.py` and `models.py` are only acceptable for trivial apps with 1-2 views and 1-2 models.

## Views Structure

Create a `views/` module with separate files per view:

```
views/
  __init__.py
  home_view.py
  profile_view.py
  settings_view.py
```

## Models Structure

Create a `models/` module with subdirectories per model, separating database schema from business logic:

```
models/
  __init__.py
  user/
    models.py    # Database fields only
    methods.py   # Model methods and business logic
  post/
    models.py
    methods.py
```

### Rationale

Separating `models.py` (schema) from `methods.py` (logic) keeps the database structure file small and fast to read. Model methods can grow arbitrarily large without cluttering the schema definition. This follows the fat models philosophy while maintaining readability.

However even methods can be modularized if nessesary!