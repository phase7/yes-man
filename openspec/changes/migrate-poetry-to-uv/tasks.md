## 1. Migrate pyproject.toml

- [x] 1.1 Run `uvx migrate-to-uv` to auto-convert `pyproject.toml` from Poetry format to PEP 621
- [x] 1.2 Verify `[project]` table has correct `name`, `version`, `requires-python`, `description`, `authors`, `license`, and `dependencies`
- [x] 1.3 Verify `[dependency-groups]` `dev` group contains: `pytest`, `pre-commit`, `ipython`, `pytest-cov`
- [x] 1.4 Verify `[build-system]` uses `hatchling` (`requires = ["hatchling"]`, `build-backend = "hatchling.build"`)
- [x] 1.5 Remove any remaining `[tool.poetry*]` tables if migration tool left them behind

## 2. Generate uv lockfile and sync environment

- [x] 2.1 Delete `poetry.lock`
- [x] 2.2 Run `uv lock` to generate `uv.lock`
- [x] 2.3 Run `uv sync` to install all dependencies (prod + dev) into `.venv`
- [x] 2.4 Verify tests pass: `uv run pytest`

## 3. Update mise.toml tasks

- [x] 3.1 Replace `poetry run pytest` with `uv run pytest` in the `test` task
- [x] 3.2 Replace `poetry run uvicorn main:app --reload` with `uv run uvicorn main:app --reload` in the `run` task

## 4. Update Dockerfile

- [x] 4.1 Remove the builder stage that installs Poetry and exports `requirements.txt`
- [x] 4.2 Add `COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv` to inject the `uv` binary
- [x] 4.3 Copy `pyproject.toml` and `uv.lock` into the image
- [x] 4.4 Run `uv sync --frozen --no-dev` to install only production dependencies
- [x] 4.5 Verify Docker image builds successfully: `docker compose up --build`

## 5. Update documentation

- [x] 5.1 Update `AGENTS.md`: replace `poetry install` with `uv sync`, `poetry run pytest` with `uv run pytest`, `poetry run uvicorn ...` with `uv run uvicorn ...`
- [x] 5.2 Update any references to `poetry` in `README.md` if present

## 6. Cleanup

- [x] 6.1 Delete stale `poetry-installer-error-*.log` files from the project root
- [x] 6.2 Add `poetry.lock` to `.gitignore` (or verify it's not tracked); add `uv.lock` tracking if not already present
- [x] 6.3 Run smoke test to verify end-to-end: `mise run smoke-test`
