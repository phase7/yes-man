## ADDED Requirements

### Requirement: Terraform Provider and Resource Group Configuration
The project SHALL include a Terraform configuration (`infra/main.tf`) that configures the AzureRM provider and defines a resource group for all Azure resources.

#### Scenario: Terraform initializes successfully
- **WHEN** a developer runs `terraform init` from the `infra/` directory
- **THEN** the AzureRM provider is downloaded and initialized without errors

#### Scenario: Resource group is created
- **WHEN** a developer runs `terraform apply`
- **THEN** an Azure resource group is created with a configurable name and location

### Requirement: Log Analytics Workspace
The project SHALL include a Terraform resource (`infra/log-analytics.tf`) that provisions an Azure Log Analytics Workspace linked to the Container Apps Environment.

#### Scenario: Workspace is created with free-tier retention
- **WHEN** `terraform apply` completes
- **THEN** a Log Analytics Workspace is created with the free tier (PerGB2018 SKU) and 30-day retention

#### Scenario: Container app stdout is queryable in Log Analytics
- **WHEN** the Container App writes to stdout
- **THEN** the log entries are available in the Log Analytics Workspace via KQL queries on the `ContainerAppConsoleLogs_CL` table

### Requirement: Container Apps Environment
The project SHALL include a Terraform resource (`infra/container-app.tf`) that provisions an Azure Container Apps Environment linked to the Log Analytics Workspace.

#### Scenario: Environment is created with consumption plan
- **WHEN** `terraform apply` completes
- **THEN** a Container Apps Environment is created using the consumption workload profile (scale-to-zero capable)

#### Scenario: Environment is linked to Log Analytics
- **WHEN** the Container Apps Environment is provisioned
- **THEN** it is configured to send logs to the Log Analytics Workspace

### Requirement: Container App Resource
The project SHALL define a Container App resource that runs the yes-man Docker image from ghcr.io with external ingress on port 8000.

#### Scenario: Container App is created with correct image
- **WHEN** `terraform apply` completes
- **THEN** a Container App is created referencing the ghcr.io image specified in the `image` input variable

#### Scenario: External ingress is enabled
- **WHEN** the Container App is provisioned
- **THEN** external ingress is enabled on target port 8000 with an Azure-provided FQDN

#### Scenario: Scale-to-zero is configured
- **WHEN** the Container App is provisioned
- **THEN** the minimum replica count is set to 0 and maximum replica count is configurable (default 1)

#### Scenario: Health probes target the health endpoint
- **WHEN** the Container App is provisioned
- **THEN** liveness and readiness probes are configured to target `GET /health` on port 8000

### Requirement: Terraform Input Variables
The project SHALL define input variables (`infra/variables.tf`) for configurable values including resource group name, location, container image reference, and app name.

#### Scenario: Variables have sensible defaults
- **WHEN** a developer runs `terraform apply` without a `*.tfvars` file
- **THEN** default values are used for resource group name, location (e.g., `eastus`), and app name

#### Scenario: Image reference is required
- **WHEN** a developer runs `terraform apply` without specifying the `image` variable
- **THEN** Terraform prompts for the ghcr.io image reference (no default — must be explicit)

### Requirement: Terraform Outputs
The project SHALL define outputs (`infra/outputs.tf`) that expose the Container App FQDN after deployment.

#### Scenario: FQDN is output after apply
- **WHEN** `terraform apply` completes
- **THEN** the Container App's public FQDN is printed as a Terraform output

### Requirement: Remote State in Azure Storage
The project SHALL include a Terraform backend configuration (`infra/backend.tf`) that stores state in an Azure Storage Account blob container, authenticated via the `ARM_ACCESS_KEY` environment variable.

#### Scenario: State is stored remotely
- **WHEN** a developer runs `terraform init` with `ARM_ACCESS_KEY` set
- **THEN** Terraform initializes with the Azure Storage backend and state is stored in the configured blob container

#### Scenario: State locking prevents concurrent modifications
- **WHEN** two processes attempt `terraform apply` simultaneously
- **THEN** the second process is blocked until the first releases the Azure Blob lease lock

### Requirement: Gitignore for Terraform Working Directory
The project SHALL include an `infra/.gitignore` that excludes the `.terraform/` directory and `*.tfvars` files from version control.

#### Scenario: Working directory is gitignored
- **WHEN** a developer runs `terraform init` in the `infra/` directory
- **THEN** the `.terraform/` directory and `*.tfvars` files are NOT tracked by git

#### Scenario: Provider lock file is committed
- **WHEN** a developer runs `terraform init`
- **THEN** the `.terraform.lock.hcl` file is generated and IS tracked by git for reproducible provider versions
