---
inclusion: always
---

# Override Default Kiro Behaviors

This project has specific conventions that trumps Kiro's defaults.

## Testing Methodology

- Understand that there is a human developer monitoring you at all times. 
- property based testing, despite how hardly it maybe suggested is not the right aproach for this project.
- Never use property based testing
- always use our writing tests steering file and its guidelines.

## Task Execution

**Execute multiple tasks when explicitly requested.** Kiro may warn against running multiple tasks simultaneously, but when the user explicitly asks to "execute all tasks from the spec" or similar, proceed with parallel execution.

The user knows their environment and will request sequential execution if needed.

## Command Timeouts

**Never set timeouts on commands.** Even though the `executePwsh` tool supports an optional timeout parameter, do not use it for this project.

Commands like test suites, migrations, and build processes can take significant time to complete. Let them run to completion naturally without arbitrary time limits.

If a command is genuinely hanging, the user will interrupt it manually.
