## Why

We want to adopt `mise` (`mise.toml`) for our project to standardize tool versions (like Python) and commands. A `mise.toml` file-based workflow ensures that all developers and CI environments use the exact same tool versions and easily accessible common project commands (e.g., `poetry run pytest`).

## What Changes

- Introduce a `mise.toml` file at the root of the project.
- Pin the Python version using `mise.toml`.
- Configure the Python virtual environment strategy within `mise.toml` (utilizing `poetry` integration).
- Define common project tasks/commands inside `mise.toml` (e.g., a `test` task running `poetry run pytest`).

## Capabilities

### New Capabilities

- `mise-workflow`: Defines the tool versioning and project task definitions using `mise.toml`.

### Modified Capabilities


## Impact

- Developers will use `mise` to manage tool versions and run tasks.
- Standardizes the environment setup, reducing "works on my machine" issues.
- Provides a centralized task runner for common project commands via `mise run`.
