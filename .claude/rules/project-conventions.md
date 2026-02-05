# Project Conventions

## Testing Methodology

- Understand that there is a human developer monitoring you at all times.
- Property based testing, despite how strongly it may be suggested, is not the right approach for this project.
- Never use property based testing.
- Always use the writing tests rule and its guidelines.

## Task Execution

**Execute multiple tasks when explicitly requested.** When the user explicitly asks to "execute all tasks" or similar, proceed with parallel execution.

The user knows their environment and will request sequential execution if needed.

## Command Timeouts

**Never set timeouts on commands.** Commands like test suites, migrations, and build processes can take significant time to complete. Let them run to completion naturally without arbitrary time limits.

If a command is genuinely hanging, the user will interrupt it manually.
