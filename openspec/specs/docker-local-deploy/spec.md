# docker-local-deploy

## Requirements

### Requirement: Dockerfile for Application Containerization
The project SHALL include a Dockerfile that builds a container image for the FastAPI application using Python 3.12-slim as the base image.

#### Scenario: Building the Docker image
- **WHEN** a developer runs `docker build -t yes-man .` from the project root
- **THEN** the image builds successfully with all Poetry-managed dependencies installed

#### Scenario: Multi-stage build excludes build tools
- **WHEN** the Docker image is built
- **THEN** the final image does NOT contain Poetry or other build-time-only tooling

### Requirement: Non-Root Container Execution
The Dockerfile SHALL configure a non-root user (`appuser`) to run the application inside the container.

#### Scenario: Application runs as non-root
- **WHEN** the container starts
- **THEN** the application process runs as `appuser`, not as `root`

### Requirement: Docker Compose for Local Orchestration
The project SHALL include a `docker-compose.yml` that defines the application service with port mapping and volume mounts.

#### Scenario: Service starts with port mapping
- **WHEN** a developer runs `docker compose up`
- **THEN** the application is accessible at `http://localhost:8000`

#### Scenario: Log file is persisted via volume mount
- **WHEN** the container writes to `yes.log.csv`
- **THEN** the log data is persisted to the host filesystem via a bind mount

### Requirement: Docker Ignore Configuration
The project SHALL include a `.dockerignore` file that excludes unnecessary files from the Docker build context.

#### Scenario: Build context excludes non-essential files
- **WHEN** the Docker image is built
- **THEN** directories such as `.venv`, `.git`, `__pycache__`, and `tests` are excluded from the build context

### Requirement: Production Uvicorn Configuration
The container SHALL run uvicorn bound to `0.0.0.0:8000` without the `--reload` flag.

#### Scenario: Uvicorn starts in production mode
- **WHEN** the container starts
- **THEN** uvicorn serves the application on `0.0.0.0:8000` without hot-reload enabled
