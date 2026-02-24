## Why

The project currently lacks unit testing and test coverage measurement. Adding tests ensures the reliability of the application, makes future refactoring safer, and test coverage guarantees that critical paths in the codebase are actively verified. This is an essential step for maintaining code quality as the project evolves.

## What Changes

- Introduce a testing framework (e.g., `pytest`).
- Introduce a coverage measurement tool (e.g., `pytest-cov`).
- Add basic unit tests for the existing logic in `main.py`.
- Configure `pyproject.toml` to support running tests and generating coverage reports.
- Ensure test commands are easily executable.

## Capabilities

### New Capabilities

- `unit-testing`: The ability to run automated tests against the application's components and measure code coverage.

### Modified Capabilities

- 

## Impact

- **Codebase:** A new `tests/` directory will be added containing test files.
- **Dependencies:** Development dependencies for testing (`pytest`, `pytest-cov` etc.) will be added to `pyproject.toml` and `poetry.lock`.
- **Workflows:** Developers will be able to verify their changes locally by running a test command.
