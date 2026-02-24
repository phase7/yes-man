## ADDED Requirements

### Requirement: Docker Local Deploy Task
The mise configuration SHALL include a `deploy:docker-local` task that builds and runs the application in a local Docker container.

#### Scenario: Developer deploys locally with mise
- **WHEN** a developer runs `mise run deploy:docker-local`
- **THEN** the system executes `docker compose up --build` to build the image and start the container

#### Scenario: Deploy task rebuilds on each run
- **WHEN** a developer runs `mise run deploy:docker-local` after changing application code
- **THEN** the Docker image is rebuilt with the latest code changes before starting the container
