## Why

The project currently runs only via `poetry run uvicorn` on the host machine, with no containerization. Dockerizing the application enables consistent, reproducible deployments and aligns with the existing mise task workflow by adding a single `mise deploy:docker-local` command to build and run the container locally.

## What Changes

- Add a `Dockerfile` to containerize the FastAPI application with Python 3.12 and Poetry-managed dependencies
- Add a `docker-compose.yml` for local orchestration (build, port mapping, volume mounts for log file)
- Add a `deploy:docker-local` task to `mise.toml` that builds the Docker image and starts the container
- Add a `.dockerignore` to keep the image lean

## Capabilities

### New Capabilities
- `docker-local-deploy`: Dockerfile, docker-compose configuration, and mise task for building and running the application in a local Docker container

### Modified Capabilities
- `mise-workflow`: Adding the `deploy:docker-local` task to the existing mise task configuration

## Impact

- **Files added**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- **Files modified**: `mise.toml` (new task)
- **Dependencies**: Requires Docker to be installed on the developer's machine
- **No breaking changes** to existing application code or workflows
