## ADDED Requirements

### Requirement: Azure Resource Group and State Storage Provisioning Script
The project SHALL include a shell script (`scripts/provision.sh`) that creates the Azure resource group, Storage Account for Terraform state, and Azure AD app registration needed before Terraform can run.

#### Scenario: Script creates resource group
- **WHEN** a developer runs `scripts/provision.sh`
- **THEN** an Azure resource group is created with a configurable name and location

#### Scenario: Script creates Storage Account and blob container for Terraform state
- **WHEN** a developer runs `scripts/provision.sh`
- **THEN** an Azure Storage Account (Standard LRS) and a blob container named `tfstate` are created within the resource group

#### Scenario: Script creates AD app registration with OIDC federation
- **WHEN** a developer runs `scripts/provision.sh`
- **THEN** an Azure AD app registration is created with a federated credential for the GitHub repository, enabling OIDC authentication from GitHub Actions

#### Scenario: Script outputs required configuration values
- **WHEN** the provisioning script completes
- **THEN** it prints the values needed for GitHub repository configuration (Azure client ID, tenant ID, subscription ID) and the Storage Account access key for `ARM_ACCESS_KEY`

#### Scenario: Script is idempotent
- **WHEN** a developer runs `scripts/provision.sh` a second time
- **THEN** existing resources are not duplicated and the script completes without errors

### Requirement: Azure Teardown Script
The project SHALL include a shell script (`scripts/teardown.sh`) that removes all Azure resources created by the provisioning script and Terraform.

#### Scenario: Script destroys Terraform-managed resources
- **WHEN** a developer runs `scripts/teardown.sh`
- **THEN** it runs `terraform destroy` in the `infra/` directory to remove all Terraform-managed Azure resources

#### Scenario: Script removes AD app registration
- **WHEN** a developer runs `scripts/teardown.sh`
- **THEN** the Azure AD app registration created by the provisioning script is deleted

#### Scenario: Script removes Storage Account
- **WHEN** a developer runs `scripts/teardown.sh`
- **THEN** the Azure Storage Account used for Terraform state is deleted

#### Scenario: Script removes resource group
- **WHEN** a developer runs `scripts/teardown.sh`
- **THEN** the Azure resource group is deleted (removing any remaining resources within it)

### Requirement: Prerequisites Documentation
The provisioning scripts SHALL include clear error messages if prerequisites (Azure CLI, Terraform, active Azure subscription) are not met.

#### Scenario: Missing Azure CLI is detected
- **WHEN** a developer runs `scripts/provision.sh` without the Azure CLI installed
- **THEN** the script exits with an error message indicating that `az` CLI is required

#### Scenario: Not logged in to Azure is detected
- **WHEN** a developer runs `scripts/provision.sh` without an active Azure CLI session
- **THEN** the script exits with an error message indicating that `az login` is required first
