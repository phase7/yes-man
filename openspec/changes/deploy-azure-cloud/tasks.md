## 1. Application Changes

- [ ] 1.1 Add health check endpoint: handle `/health` in the middleware (similar to favicon.ico pattern), return `{"status": "healthy"}` without logging
- [ ] 1.2 Refactor logger setup to auto-detect environment: check `os.environ.get("CONTAINER_APP_NAME")`, use `StreamHandler(sys.stdout)` if set, else `FileHandler("yes.log.csv")`
- [ ] 1.3 Add `import sys, os` to main.py for the new logger setup
- [ ] 1.4 Update tests: add test for `/health` endpoint (returns 200, correct body, no log entry)
- [ ] 1.5 Add test for environment-aware logging: mock `CONTAINER_APP_NAME` env var and verify StreamHandler is used

## 2. Terraform Infrastructure

- [ ] 2.1 Create `infra/` directory with `infra/.gitignore` (exclude `.terraform/`, `*.tfvars` — state is remote, no local state files to ignore)
- [ ] 2.2 Create `infra/main.tf`: configure AzureRM provider and define resource group resource with variable-driven name and location
- [ ] 2.3 Create `infra/backend.tf`: configure `azurerm` backend with resource group name, storage account name, container name, and state file key
- [ ] 2.4 Create `infra/variables.tf`: define input variables for resource group name, location (default `eastus`), app name, storage account name, and container image reference (no default)
- [ ] 2.5 Create `infra/log-analytics.tf`: define Log Analytics Workspace resource with PerGB2018 SKU and 30-day retention
- [ ] 2.6 Create `infra/container-app.tf`: define Container Apps Environment linked to Log Analytics, and Container App with external ingress on port 8000, ghcr.io image reference, scale 0-1, and health probes targeting `/health`
- [ ] 2.7 Create `infra/outputs.tf`: output the Container App FQDN
- [ ] 2.8 Validate Terraform config: set `ARM_ACCESS_KEY` env var, run `terraform init` and `terraform validate` locally

## 3. Provisioning Scripts

- [ ] 3.1 Create `scripts/provision.sh`: check for `az` CLI and active login, create resource group, create Storage Account + blob container (for TF state), create AD app registration with federated credential for the GitHub repo, print client ID / tenant ID / subscription ID / storage access key
- [ ] 3.2 Make `scripts/provision.sh` idempotent (skip existing resources)
- [ ] 3.3 Create `scripts/teardown.sh`: run `terraform destroy`, delete AD app registration, delete Storage Account, delete resource group
- [ ] 3.4 Make both scripts executable (`chmod +x`)

## 4. GitHub Actions CI/CD

- [ ] 4.1 Create `.github/workflows/deploy.yml`: trigger on push to `main`, declare permissions (`id-token: write`, `packages: write`, `contents: read`)
- [ ] 4.2 Add `build` job: checkout, login to ghcr.io with `GITHUB_TOKEN`, build and push Docker image tagged with commit SHA and `latest`
- [ ] 4.3 Add `deploy` job: depends on `build`, authenticate to Azure via `azure/login` with OIDC (read client ID, tenant ID, subscription ID from GitHub vars), update Container App with new image tag

## 5. Integration and Verification

- [ ] 5.1 Run full test suite (`uv run pytest`) to verify app changes don't break existing tests
- [ ] 5.2 Test local Docker workflow still works: `docker compose up --build`, verify `/` returns "OK" and `/health` returns healthy status
- [ ] 5.3 Run `scripts/provision.sh` against a real Azure subscription
- [ ] 5.4 Set `ARM_ACCESS_KEY` env var, run `terraform init` + `terraform apply` to provision infrastructure
- [ ] 5.5 Verify Terraform state is stored in Azure Storage blob (check via Azure Portal or `az storage blob list`)
- [ ] 5.6 Push to `main` and verify GitHub Actions workflow builds, pushes to ghcr.io, and deploys to Azure
- [ ] 5.7 Verify app responds at the Azure-provided FQDN
- [ ] 5.8 Verify logs appear in Azure Portal → Container App → Log stream
