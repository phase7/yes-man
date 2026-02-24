## Why

Poetry has recurring installation failures on this project (evidenced by multiple `poetry-installer-error-*.log` files) and is significantly slower than `uv`. Migrating to `uv` provides a faster, more reliable dependency resolver and environment manager with full `pyproject.toml` compatibility.

## What Changes

- **BREAKING**: Replace `poetry.lock` with `uv.lock` as the canonical lockfile.
- Replace `[tool.poetry]` and `[tool.poetry.dependencies]` / `[tool.poetry.group.*]` sections in `pyproject.toml` with PEP 621 `[project]` and `[dependency-groups]` sections.
- Replace `[build-system]` backend from `poetry-core` to `hatchling` (uv-compatible, no build needed since `package-mode = false`).
- Delete `poetry.lock`; generate `uv.lock` via `uv lock`.
- Update `Dockerfile` to install `uv` and use `uv sync` instead of `poetry install`.
- Update `AGENTS.md` to replace all `poetry run <cmd>` instructions with `uv run <cmd>`.
- Update `mise.toml` if it references poetry toolchain.
- Remove stale `poetry-installer-error-*.log` files.

## Capabilities

### New Capabilities

- `uv-project-config`: The project is configured for `uv` — `pyproject.toml` uses PEP 621 format, `uv.lock` is the lockfile, and all dev workflows use `uv run` / `uv sync`.

### Modified Capabilities

- None. No spec-level behavioral requirements of the application change; only the toolchain changes.

## Impact

- **`pyproject.toml`**: Rewritten from Poetry format to PEP 621 + `[dependency-groups]`.
- **`poetry.lock`**: Deleted.
- **`uv.lock`**: Generated (new).
- **`Dockerfile`**: Updated to use `uv` for dependency installation.
- **`AGENTS.md`**: Updated developer workflow instructions.
- **`mise.toml`**: Reviewed and updated if poetry is referenced.
- **`.venv`**: Recreated by `uv sync`.
- **No runtime code changes** — `main.py`, `tests/`, application logic untouched.
