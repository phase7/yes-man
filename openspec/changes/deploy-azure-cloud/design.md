## Context

yes-man is a minimal FastAPI application (~45 lines) that logs every HTTP request to a CSV file and responds with "OK". It is currently containerized (Docker + docker-compose) and deployed locally. The goal is to deploy it to Azure Cloud using Terraform for infrastructure-as-code and GitHub Actions for CI/CD.

**Current state:**
- Dockerfile builds a `python:3.12-slim` image with `uv` for dependency management
- Application runs as non-root `appuser` on port 8000
- Logs are written to a local file `yes.log.csv` via Python's `logging.FileHandler`
- No health check endpoint exists
- No CI/CD pipeline exists

## Goals / Non-Goals

**Goals:**
- Deploy the containerized app to Azure Container Apps with Terraform
- Automate build and deploy via GitHub Actions on push to `main`
- Provide scripts for first-time Azure resource provisioning
- Keep the local Docker Compose workflow fully functional
- Maintain scale-to-zero capability to minimize costs

**Non-Goals:**
- Custom domain or TLS configuration (use Azure-provided FQDN for now)
- Multi-region or high-availability setup
- Log aggregation or monitoring dashboards (Azure Container Apps provides basic log streaming out of the box)
- Database or external storage integration
- Staging/production environment separation (single environment for now)

## Decisions

### 1. Azure Container Apps over App Service or AKS

**Choice:** Azure Container Apps

**Rationale:** Container Apps is purpose-built for containerized microservices. It provides scale-to-zero (no cost when idle), built-in ingress, and managed HTTPS — all without the operational overhead of AKS. App Service can host containers but lacks native scale-to-zero on consumption tiers and requires an App Service Plan. AKS is overkill for a single-container stateless app.

**Alternatives considered:**
- Azure App Service: Higher baseline cost, no true scale-to-zero
- AKS: Excessive complexity for a single container
- Azure Container Instances: No built-in ingress or auto-scaling

### 2. Terraform with AzureRM provider, remote state in Azure Storage

**Choice:** Terraform with the `azurerm` provider, state stored remotely in an Azure Storage Account blob container.

**Rationale:** Terraform is cloud-agnostic, widely adopted, and provides explicit state management with drift detection. The AzureRM provider has mature support for Container Apps resources. Remote state in Azure Storage provides state locking (prevents concurrent modifications), encryption at rest, and eliminates the risk of losing state if a local machine is wiped. The Azure free tier includes 5 GB of LRS Blob Storage — a Terraform state file is a few KB, so this costs nothing.

**State management:**
- The provisioning script (`scripts/provision.sh`) creates a Storage Account + blob container before any `terraform init`
- `infra/backend.tf` configures the `azurerm` backend pointing to this storage account
- The storage access key is passed via the `ARM_ACCESS_KEY` environment variable (not stored in code)
- State locking is automatic via Azure Blob lease — prevents two people running `terraform apply` simultaneously

**Bootstrap order:** The storage account for state must exist before `terraform init`. The provisioning script handles this: it creates the storage account first (via `az` CLI), then Terraform can initialize with the remote backend.

**Alternatives considered:**
- Bicep: Azure-native but vendor-locked, smaller ecosystem
- Pulumi: Good but adds a programming language dependency
- ARM templates: Verbose and harder to maintain
- Local state: Simpler but risks state loss, no locking, doesn't support CI/CD-driven infra changes
- Terraform Cloud: Free tier available but adds external dependency outside Azure

### 3. GitHub Container Registry (ghcr.io) for image storage

**Choice:** ghcr.io — free for public repos, generous free tier for private repos

**Rationale:** Eliminates the ~$5/month ACR cost, keeping the entire deployment within Azure free tiers. ghcr.io is tightly integrated with GitHub Actions (same `GITHUB_TOKEN` used for push), so no extra credentials needed for the build job. Container Apps pulls the image via public URL (for public repos) or with a registry secret (for private repos).

**Container Apps authentication:** For a public ghcr.io image, no auth is needed — Container Apps pulls directly. For private repos, a registry secret with a GitHub Personal Access Token (PAT) with `read:packages` scope is configured on the Container App resource in Terraform.

**Alternatives considered:**
- ACR Basic SKU: Native Azure integration but ~$5/month minimum cost
- Docker Hub: Rate limits on free tier, separate credentials
- ACR with managed identity: Most secure Azure option but adds cost and complexity

### 4. GitHub Actions with OIDC federation for Azure auth

**Choice:** OpenID Connect (OIDC) federation between GitHub Actions and Azure AD — no stored secrets

**Rationale:** OIDC eliminates the need for long-lived service principal secrets in GitHub. The GitHub Actions workflow authenticates using a federated identity token, which Azure validates. This is the recommended approach by both Microsoft and GitHub, and avoids secret rotation concerns.

**Alternatives considered:**
- Service principal with client secret: Simpler setup but requires secret rotation
- Service principal with certificate: More secure than secrets but more complex to manage

### 5. Health check endpoint

**Choice:** Add a `GET /health` endpoint to `main.py` that returns `{"status": "healthy"}` without logging

**Rationale:** Azure Container Apps uses health probes (liveness and readiness) to manage container lifecycle. Without a health endpoint, probes would hit `/` which triggers CSV logging on every probe interval (~30s), polluting the log file. A dedicated `/health` endpoint avoids this.

**Implementation:** Add a route before the middleware catch-all, or handle it within the existing middleware similar to the favicon.ico pattern.

### 6. Environment-aware logging with Azure Log Analytics

**Choice:** Auto-detect Azure environment and switch to stdout logging; keep CSV file logging for local development. Provision a Log Analytics Workspace in Terraform so container logs are queryable in Azure Portal.

**Detection mechanism:** Check for the `CONTAINER_APP_NAME` environment variable, which Azure Container Apps sets automatically in every container. No manual `ENV=prod` flag needed.

**Behavior:**
- **Local** (`CONTAINER_APP_NAME` not set): `FileHandler` → `yes.log.csv` (existing behavior, unchanged)
- **Azure** (`CONTAINER_APP_NAME` set): `StreamHandler` → stdout → captured by Container Apps into Log Analytics

**Implementation:** Replace the hardcoded `FileHandler` setup in `main.py` (lines 10-16) with a conditional that checks `os.environ.get("CONTAINER_APP_NAME")`. If present, attach a `StreamHandler(sys.stdout)` instead of `FileHandler`. Same formatter for both.

**Viewing logs in Azure:** Container Apps automatically forwards stdout to the associated Log Analytics Workspace. Logs are queryable via Azure Portal → Container App → Log stream, or via KQL queries in Log Analytics:
```kql
ContainerAppConsoleLogs_CL
| where ContainerAppName_s == "yes-man"
| order by TimeGenerated desc
```

**Terraform:** The `container-app.tf` will include a `azurerm_log_analytics_workspace` resource linked to the Container Apps Environment. No extra cost — Log Analytics ingestion is included in the Container Apps consumption plan up to a baseline.

**Rationale:** This keeps the app self-aware of its environment with zero configuration. Local developers get the familiar CSV file. In Azure, logs flow to Log Analytics where they're searchable, filterable, and retained (default 30 days). No additional SDKs or dependencies required.

### 7. Terraform file structure

**Choice:** Flat structure under `infra/` directory

```
infra/
├── main.tf           # Provider config, resource group
├── backend.tf        # Azure Storage remote state configuration
├── log-analytics.tf  # Log Analytics Workspace
├── container-app.tf  # Container Apps Environment + Container App
├── variables.tf      # Input variables (including ghcr.io image reference)
├── outputs.tf        # Output values (FQDN)
├── .gitignore        # Ignores .terraform/, *.tfvars (state is remote now)
└── .terraform.lock.hcl  # Provider lock file (committed)
```

**Rationale:** The infrastructure is small enough that a flat structure is clear and navigable. Modules would add indirection without benefit at this scale. The `.terraform/` directory and variable overrides are gitignored; state lives remotely in Azure Storage. The provider lock file is committed for reproducible builds.

### 8. CI/CD pipeline design

**Choice:** Single GitHub Actions workflow with two jobs: `build` and `deploy`

```
push to main → build job (Docker build + push to ghcr.io) → deploy job (az containerapp update)
```

**Rationale:** Separating build and deploy into two jobs allows rerunning deploy independently if only the deployment step fails. The build job uses `docker/build-push-action` with the built-in `GITHUB_TOKEN` to push to ghcr.io — no extra secrets needed. The deploy job uses `azure/container-apps-deploy-action` to update the Container App with the new image tag.

## Risks / Trade-offs

- **[Log format difference]** → Local logs go to CSV file, Azure logs go to stdout (plain text in Log Analytics). Mitigation: Same formatter is used in both environments; KQL queries can parse the CSV-formatted stdout lines.
- **[ghcr.io availability]** → If GitHub has an outage, Container Apps can't pull new images. Mitigation: Running containers are unaffected; only new deployments are blocked. Acceptable for a non-critical app.
- **[Private repo image pull]** → Private ghcr.io images require a PAT with `read:packages` scope stored as a Container App registry secret. Mitigation: PAT can be scoped narrowly; if repo is public, no auth needed at all.
- **[OIDC setup complexity]** → Requires Azure AD app registration with federated credentials. Mitigation: Provisioning script automates this; one-time setup.
- **[Terraform state bootstrap]** → The Azure Storage Account for remote state must exist before `terraform init`. Mitigation: `scripts/provision.sh` creates it first via `az` CLI; this is a one-time setup step.
- **[Storage access key management]** → The `ARM_ACCESS_KEY` env var must be set for Terraform to access state. Mitigation: Provisioning script prints the key; developer sets it in their shell. For production, key can be stored in Azure Key Vault.
- **[Cost if left running with traffic]** → Container Apps charges per vCPU-second and request. Mitigation: Scale-to-zero means no cost at idle; consumption plan keeps costs proportional to usage.

## Migration Plan

1. Run provisioning script to create Azure resource group, Storage Account (for TF state), and AD app registration (for OIDC)
2. Set `ARM_ACCESS_KEY` env var with the storage access key (printed by provisioning script)
3. Run `terraform init` + `terraform apply` to create Log Analytics Workspace, Container Apps Environment, and Container App
3. Configure GitHub repository secrets/variables for OIDC
4. Push to `main` to trigger first automated build (push to ghcr.io) and deploy
5. Verify app responds at the Azure-provided FQDN

**Rollback:** `terraform destroy` tears down all Azure resources cleanly. GitHub Actions workflow can be disabled by removing the workflow file.

## Open Questions

- Should the Container App have a minimum replica count of 1 (always warm) or 0 (scale-to-zero with cold start latency)?
- Is the Azure-provided `*.azurecontainerapps.io` FQDN sufficient, or will a custom domain be needed soon?
