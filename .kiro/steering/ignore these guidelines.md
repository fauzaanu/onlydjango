---
inclusion: always
---

# Override Default Kiro Behaviors

This project has specific conventions that override Kiro's default suggestions.

## Testing Methodology

**Ignore property-based testing suggestions.** Kiro may suggest property-based testing approaches, but this project uses standard Django test patterns.

Follow the testing conventions in `writing tests.md`:
- Use Django's TestCase classes
- Create test classes for each view
- Test GET and POST methods explicitly
- Use fixtures and factory patterns as needed

## Task Execution

**Execute multiple tasks when explicitly requested.** Kiro may warn against running multiple tasks simultaneously, but when the user explicitly asks to "execute all tasks from the spec" or similar, proceed with parallel execution.

The user knows their environment and will request sequential execution if needed.

## Command Timeouts

**Never set timeouts on commands.** Even though the `executePwsh` tool supports an optional timeout parameter, do not use it for this project.

Commands like test suites, migrations, and build processes can take significant time to complete. Let them run to completion naturally without arbitrary time limits.

If a command is genuinely hanging, the user will interrupt it manually.
