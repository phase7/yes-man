## Context

The yes-man application is a FastAPI server that responds "OK" to all requests and logs them to a CSV file. It currently runs directly on the host via `poetry run uvicorn main:app --reload`. The project already uses mise for task orchestration (`test`, `run`) and Poetry for dependency management. There is no containerization or deployment mechanism.

## Goals / Non-Goals

**Goals:**
- Containerize the application with Docker so it runs identically across environments
- Provide a single `mise deploy:docker-local` command to build and run the container
- Persist the log file (`yes.log.csv`) outside the container via a volume mount
- Keep the Docker setup minimal and production-oriented (small image, non-root user)

**Non-Goals:**
- CI/CD pipeline or remote deployment (cloud, registry push)
- Multi-stage build optimization beyond reasonable defaults
- Kubernetes or orchestration beyond docker-compose
- HTTPS/TLS termination inside the container

## Decisions

### Decision 1: Use a multi-stage Dockerfile with `python:3.12-slim`

Use `python:3.12-slim` as the base image with a two-stage build: one stage to install Poetry and export dependencies, a second stage for the runtime. This keeps the final image small by excluding Poetry and build tools.

**Alternative considered**: Single-stage with Poetry installed at runtime — rejected because it bloats the image with unnecessary tooling.

### Decision 2: Export Poetry dependencies to `requirements.txt`

Use `poetry export -f requirements.txt` in the build stage and `pip install -r requirements.txt` in the runtime stage. This avoids needing Poetry in the final image entirely.

**Alternative considered**: Install Poetry in the runtime image and use `poetry install --no-dev` — rejected for image size reasons.

### Decision 3: Use docker-compose for local orchestration

A `docker-compose.yml` defines the service with port mapping (8000:8000) and a bind mount for `yes.log.csv`. The mise task wraps `docker compose up --build`.

**Alternative considered**: Raw `docker build` + `docker run` commands in the mise task — rejected because compose handles port mapping, volumes, and rebuild in a cleaner declarative way.

### Decision 4: Run as non-root user inside the container

Create a dedicated `appuser` in the Dockerfile and run the application as that user. This follows container security best practices.

### Decision 5: Uvicorn runs without `--reload` in Docker

The container runs `uvicorn main:app --host 0.0.0.0 --port 8000` without `--reload` since hot-reload is a development concern and adds unnecessary overhead in a container.

## Risks / Trade-offs

- [Log file volume mount] The bind mount for `yes.log.csv` requires the host path to exist. → Mitigation: docker-compose creates the file automatically if it doesn't exist.
- [Poetry lock drift] If `poetry.lock` changes without rebuilding the image, the container runs stale dependencies. → Mitigation: `--build` flag in the mise task forces rebuild each time.
- [Port conflict] Port 8000 on the host may already be in use. → Mitigation: Document the port mapping; user can override in docker-compose.
