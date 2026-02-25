## Why

The application currently only supports local Docker deployment via `docker compose up`. To make it accessible on the internet and support production use cases, it needs a cloud deployment target. Azure Cloud provides managed container hosting with minimal operational overhead, making it a natural next step for this already-containerized FastAPI application.

## What Changes

- Add Azure Container Apps as a cloud deployment target using Terraform for Infrastructure-as-Code
- Add a GitHub Actions CI/CD pipeline that builds, pushes to ghcr.io, and deploys to Azure Container Apps on push to `main`
- Add Azure CLI helper scripts for initial resource provisioning and teardown
- Add environment-aware logging: auto-detect Azure via `CONTAINER_APP_NAME` env var, log to stdout (→ Log Analytics) in Azure, keep CSV file logging locally

## Capabilities

### New Capabilities
- `azure-infrastructure`: Terraform configuration defining Container Apps Environment, Container App, and Log Analytics Workspace resources with appropriate networking and scaling configuration
- `azure-ci-cd`: GitHub Actions workflow that builds the Docker image, pushes to ghcr.io, and deploys to Azure Container Apps on pushes to `main`
- `azure-provisioning`: CLI scripts and documentation for initial Azure resource group and service principal setup, plus teardown

### Modified Capabilities
- `docker-local-deploy`: The Dockerfile may need a health check endpoint addition to support Azure Container Apps health probes. The existing local Docker Compose workflow remains unchanged.

## Impact

- **New files**: Terraform configuration (`infra/`), GitHub Actions workflow (`.github/workflows/`), provisioning scripts (`scripts/`)
- **Dependencies**: Terraform, Azure CLI, GitHub Actions, GitHub Container Registry (ghcr.io), Azure Container Apps
- **Code changes**: Addition of a `/health` endpoint in `main.py` for container health probes; refactor logger setup to auto-detect environment and switch between FileHandler (local) and StreamHandler (Azure)
- **Secrets management**: GitHub repository secrets needed for Azure credentials (service principal or OIDC)
- **Cost**: $0/month — all resources within Azure free tiers (Container Apps consumption plan, Log Analytics 5GB free). Terraform runs locally, images stored on ghcr.io (free)
- **Existing workflows**: Local `docker compose` and `mise` workflows remain fully functional and unchanged
