---
inclusion: always
---

# Code-First Approach

Write production-quality code following project conventions. Minimize unnecessary command execution.

## Prohibited Actions

- Creating ad-hoc test files at repository root (e.g., `test_*.py`)
- Running the development server (assume it's already running)
- Creating markdown files for progress tracking or documentation
- Running one-off validation commands outside proper test suites

## Required Actions

- Write code following project steering conventions
- Create tests only in appropriate test directories when explicitly requested
- Prioritize code quality over command execution
- Trust the developer's environment is configured and running