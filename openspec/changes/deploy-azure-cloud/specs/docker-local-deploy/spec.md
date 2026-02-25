## ADDED Requirements

### Requirement: Health Check Endpoint
The application SHALL expose a `GET /health` endpoint that returns a health status response without logging the request.

#### Scenario: Health endpoint returns healthy status
- **WHEN** an HTTP GET request is made to `/health`
- **THEN** the response body is `{"status": "healthy"}` with HTTP status 200

#### Scenario: Health endpoint does not generate log entries
- **WHEN** an HTTP GET request is made to `/health`
- **THEN** no entry is written to `yes.log.csv` and no log line is emitted to stdout

### Requirement: Environment-Aware Logging
The application SHALL auto-detect whether it is running in Azure Container Apps and configure the appropriate log handler without manual configuration.

#### Scenario: Local environment uses file logging
- **WHEN** the application starts and the `CONTAINER_APP_NAME` environment variable is NOT set
- **THEN** the logger uses a `FileHandler` writing to `yes.log.csv` (existing behavior)

#### Scenario: Azure environment uses stdout logging
- **WHEN** the application starts and the `CONTAINER_APP_NAME` environment variable IS set
- **THEN** the logger uses a `StreamHandler` writing to stdout

#### Scenario: Log format is consistent across environments
- **WHEN** a request is logged in either environment
- **THEN** the log entry uses the same CSV formatter: `%(asctime)s,%(thread)d,%(levelname)s,%(message)s`
