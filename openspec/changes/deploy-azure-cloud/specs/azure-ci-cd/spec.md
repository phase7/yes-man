## ADDED Requirements

### Requirement: GitHub Actions Workflow File
The project SHALL include a GitHub Actions workflow at `.github/workflows/deploy.yml` that triggers on pushes to the `main` branch.

#### Scenario: Workflow triggers on push to main
- **WHEN** a commit is pushed to the `main` branch
- **THEN** the deploy workflow is triggered automatically

#### Scenario: Workflow does not trigger on other branches
- **WHEN** a commit is pushed to a branch other than `main`
- **THEN** the deploy workflow is NOT triggered

### Requirement: Docker Build and Push to ghcr.io
The workflow SHALL include a `build` job that builds the Docker image and pushes it to GitHub Container Registry (ghcr.io) tagged with the commit SHA.

#### Scenario: Image is built and pushed
- **WHEN** the `build` job runs
- **THEN** the Docker image is built from the project's Dockerfile and pushed to `ghcr.io/<owner>/yes-man:<commit-sha>`

#### Scenario: Build uses GITHUB_TOKEN for authentication
- **WHEN** the `build` job authenticates to ghcr.io
- **THEN** it uses the built-in `GITHUB_TOKEN` secret (no additional credentials needed)

#### Scenario: Image is also tagged as latest
- **WHEN** the `build` job completes
- **THEN** the image is tagged with both the commit SHA and `latest`

### Requirement: Azure Deployment via OIDC
The workflow SHALL include a `deploy` job that authenticates to Azure using OIDC federation and updates the Container App with the newly built image.

#### Scenario: Deploy job authenticates via OIDC
- **WHEN** the `deploy` job runs
- **THEN** it authenticates to Azure using the `azure/login` action with OIDC (federated credentials), reading client ID, tenant ID, and subscription ID from GitHub repository variables

#### Scenario: Container App is updated with new image
- **WHEN** the `deploy` job completes
- **THEN** the Azure Container App is updated to use the new image tag (`ghcr.io/<owner>/yes-man:<commit-sha>`)

#### Scenario: Deploy job depends on build job
- **WHEN** the workflow runs
- **THEN** the `deploy` job only starts after the `build` job completes successfully

### Requirement: Workflow Permissions
The workflow SHALL declare minimum required permissions for OIDC authentication and package publishing.

#### Scenario: OIDC token permission is declared
- **WHEN** the workflow file is read
- **THEN** it declares `id-token: write` permission (required for OIDC federation with Azure)

#### Scenario: Package write permission is declared
- **WHEN** the workflow file is read
- **THEN** it declares `packages: write` permission (required for pushing to ghcr.io)

#### Scenario: Contents read permission is declared
- **WHEN** the workflow file is read
- **THEN** it declares `contents: read` permission (required for checkout)
