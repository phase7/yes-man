# GEMINI.md - yes-man Context

## Project Overview
**yes-man** is a simple Python-based web application built with **FastAPI**. Its primary function is to act as a positive, always-affirming server (a "yes man"). It features a custom logging middleware that intercepts all HTTP requests, logs the request method and path to a local CSV file (`yes.log.csv`), and always responds with an "OK" (except for `favicon.ico` requests, which it also handles). 

**Key Technologies:**
*   **Python >=3.12**
*   **FastAPI** (Web framework)
*   **uv** (Dependency management and packaging)

## Building and Running

The project uses `uv` for dependency management.

### Setup
To install dependencies:
```bash
uv sync
```

### Running the Application
Since FastAPI is installed with the `all` extras (which includes `uvicorn`), you can run the server using:
```bash
uv run uvicorn main:app --reload
```

### Testing
Testing is configured using `pytest`. To run tests:
```bash
uv run pytest
```

## Development Conventions

Based on the `pyproject.toml` file, the following development tools and conventions are used in this project:

*   **Testing:** **Pytest** (`pytest`) is the test runner.
*   **Pre-commit Hooks:** **pre-commit** (`pre-commit`) is used to manage and maintain pre-commit hooks, likely enforcing formatting and other checks before commits.
*   **Logging:** The application logs directly to a CSV file (`yes.log.csv`) using Python's built-in `logging` module.

## Git strategy
make sure all new branches you are creating are based on latest main. switch to main and pull latest changes. then create a branch with properly descriptive name.

before committing check all changed files. try to do small atomic commits where you group related files. describe the changes in the commit message, very briefly but make sure all changes are represented by the commit message. askuserinput before pushing.
