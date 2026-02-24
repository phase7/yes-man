## Context

The project uses Poetry for dependency management, but has experienced repeated installation failures (3 error log files present). The `Dockerfile` uses a two-stage build where Poetry exports a `requirements.txt` in the builder stage, then `pip install` in the runtime stage. `mise.toml` has tasks that call `poetry run`. The `pyproject.toml` uses Poetry-specific `[tool.poetry]` format rather than the standard PEP 621 `[project]` block. The project has `package-mode = false` (it's an app, not a library).

## Goals / Non-Goals

**Goals:**
- Convert `pyproject.toml` to PEP 621 standard format compatible with `uv`
- Replace `poetry.lock` with `uv.lock`
- Update `Dockerfile` to use `uv` natively (no `requirements.txt` export needed)
- Update `mise.toml` tasks to use `uv run` instead of `poetry run`
- Update `AGENTS.md` developer documentation

**Non-Goals:**
- Changing any runtime application behavior
- Modifying `main.py` or test files
- Switching the Python version (stays on 3.12)
- Adding new dependencies

## Decisions

### 1. Use `uvx migrate-to-uv` for initial conversion
**Decision**: Run the migration tool to convert `pyproject.toml` automatically, then manually verify and clean up.  
**Rationale**: Less error-prone than manually rewriting. The tool handles version constraint syntax differences.  
**Alternative considered**: Hand-editing — higher risk of subtle mistakes in constraint syntax.

### 2. Dockerfile: use `uv sync --no-dev` directly, no `requirements.txt` export
**Decision**: Replace the two-stage Poetry+pip pattern with a single-stage build using `uv sync`.  
**Rationale**: `uv` installs directly into a venv much faster than `pip`. No need for an intermediate `requirements.txt`. The official `ghcr.io/astral-sh/uv` image or `COPY --from=ghcr.io/astral-sh/uv /uv /usr/local/bin/uv` is the recommended pattern.  
**Alternative considered**: Keep exporting `requirements.txt` via `uv export` — adds a step without benefit.  
**Approach**: Use `COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv` to inject `uv` binary into the `python:3.12-slim` base image, then `uv sync --frozen --no-dev`.

### 3. Build system backend: use `hatchling`
**Decision**: Replace `poetry-core` with `hatchling` as the build backend.  
**Rationale**: `hatchling` is the most commonly recommended PEP 517 backend for `uv` projects that don't need poetry-specific features. Since `package-mode = false`, the build backend is largely ceremonial but required by PEP 517 tools.  
**Alternative considered**: `setuptools` — works but more verbose config required.

### 4. Dev dependencies: use `[dependency-groups]` (PEP 735)
**Decision**: Move `[tool.poetry.group.dev.dependencies]` to `[dependency-groups] dev = [...]`.  
**Rationale**: This is the PEP 735 standard that `uv` natively supports for grouped dev dependencies, replacing Poetry's custom group syntax.

## Risks / Trade-offs

- **`uv.lock` format** → Not human-readable like `poetry.lock`; this is expected and fine for this project.
- **Docker layer caching** → The new Dockerfile approach copies both `pyproject.toml` and `uv.lock` before `uv sync`, preserving layer cache efficiency.
- **`mise.toml` venv** → `mise` already manages the `.venv` path (`_.python.venv = { path = ".venv", create = true }`); `uv sync` will respect and populate this venv.
- **Pre-commit hooks** → `pre-commit` is a dev dependency; it will be available via `uv run pre-commit` after migration.
