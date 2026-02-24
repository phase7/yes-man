## ADDED Requirements

### Requirement: PEP 621 project metadata
The project `pyproject.toml` SHALL use the standard `[project]` table (PEP 621) for all metadata including name, version, description, authors, license, requires-python, and dependencies. The `[tool.poetry]` table SHALL NOT be present.

#### Scenario: Standard project table present
- **WHEN** a developer opens `pyproject.toml`
- **THEN** a `[project]` table exists with `name`, `version`, `requires-python`, and `dependencies` fields

#### Scenario: Poetry table absent
- **WHEN** a developer opens `pyproject.toml`
- **THEN** no `[tool.poetry]` table is present

### Requirement: uv-compatible lockfile
The project SHALL use `uv.lock` as the canonical lockfile. The `poetry.lock` file SHALL NOT be present in the repository.

#### Scenario: uv.lock exists after sync
- **WHEN** a developer runs `uv lock` in the project root
- **THEN** a `uv.lock` file is generated and reflects all resolved dependencies

#### Scenario: poetry.lock is absent
- **WHEN** a developer inspects the repository root
- **THEN** no `poetry.lock` file is present

### Requirement: uv-based developer workflow
All developer workflow commands documented in `AGENTS.md` and `mise.toml` SHALL use `uv run` instead of `poetry run`. Dependency installation SHALL use `uv sync`.

#### Scenario: Install dependencies with uv sync
- **WHEN** a developer sets up the project for the first time
- **THEN** running `uv sync` installs all production and dev dependencies into `.venv`

#### Scenario: Run tests via uv
- **WHEN** a developer runs `uv run pytest`
- **THEN** pytest executes and all tests pass

#### Scenario: Run server via uv
- **WHEN** a developer runs `uv run uvicorn main:app --reload`
- **THEN** the FastAPI server starts successfully

#### Scenario: mise task uses uv
- **WHEN** a developer runs `mise run test`
- **THEN** the task executes `uv run pytest` (not `poetry run pytest`)

### Requirement: uv-based Docker build
The `Dockerfile` SHALL use `uv` for dependency installation instead of Poetry. The build SHALL NOT require a `requirements.txt` export step.

#### Scenario: Docker image builds without Poetry
- **WHEN** `docker compose up --build` is run
- **THEN** the image builds successfully using `uv sync --frozen --no-dev` without installing Poetry

#### Scenario: Runtime container is functional
- **WHEN** the built Docker container starts
- **THEN** the FastAPI application responds to HTTP requests with "OK"

### Requirement: hatchling build backend
The `[build-system]` table in `pyproject.toml` SHALL use `hatchling` as the build backend. `poetry-core` SHALL NOT be referenced.

#### Scenario: Build system uses hatchling
- **WHEN** a developer inspects `pyproject.toml`
- **THEN** `build-backend = "hatchling.build"` is present and `requires = ["hatchling"]`

### Requirement: Dev dependencies in dependency-groups
Development dependencies SHALL be declared in a `[dependency-groups]` table under a `dev` group (PEP 735), replacing the `[tool.poetry.group.dev.dependencies]` table.

#### Scenario: Dev group declared correctly
- **WHEN** a developer inspects `pyproject.toml`
- **THEN** a `[dependency-groups]` table exists with a `dev` key listing pytest, pre-commit, ipython, and pytest-cov
