## 1. Docker Configuration

- [x] 1.1 Create `.dockerignore` to exclude `.venv`, `.git`, `__pycache__`, `tests`, `*.log.csv`, and other non-essential files from the build context
- [x] 1.2 Create multi-stage `Dockerfile` with `python:3.12-slim` base — build stage exports Poetry deps to `requirements.txt`, runtime stage installs them with pip, creates `appuser`, and runs uvicorn on `0.0.0.0:8000`

## 2. Docker Compose

- [x] 2.1 Create `docker-compose.yml` defining the app service with build context, port mapping `8000:8000`, and a bind mount for `yes.log.csv`

## 3. Mise Task

- [x] 3.1 Add `deploy:docker-local` task to `mise.toml` that runs `docker compose up --build`

## 4. Verification

- [x] 4.1 Run `mise run deploy:docker-local` and confirm the container starts, responds at `http://localhost:8000`, and logs are written to `yes.log.csv` on the host
