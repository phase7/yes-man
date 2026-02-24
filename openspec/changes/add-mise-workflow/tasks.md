## 1. Setup `mise.toml`

- [ ] 1.1 Create a `mise.toml` file at the root of the project.
- [ ] 1.2 Define the pinned Python version inside `mise.toml` under the `[tools]` section.

## 2. Configure Environment and Tasks

- [ ] 2.1 Configure `mise` to use Poetry for virtual environments if necessary.
- [ ] 2.2 Define common task commands (e.g., `test = "poetry run pytest"`) in the `[tasks]` section.
- [ ] 2.3 Verify `mise install` installs correct tool versions.
- [ ] 2.4 Verify `mise run test` executes pytest successfully.
