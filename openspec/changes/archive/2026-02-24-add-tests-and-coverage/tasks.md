## 1. Setup

- [x] 1.1 Add `pytest` and `pytest-cov` to `pyproject.toml` as development dependencies (via `poetry add --group dev pytest pytest-cov`).
- [x] 1.2 Configure `pytest` settings in `pyproject.toml` (e.g., testpaths).
- [x] 1.3 Create a `tests/` directory at the project root with a `__init__.py` file.

## 2. Core Implementation

- [x] 2.1 Write initial tests in `tests/test_main.py` covering core non-side-effecting logic in `main.py`.
- [x] 2.2 Run `poetry run pytest --cov=main` to generate coverage report.
- [x] 2.3 Refactor small pieces of `main.py` if needed to increase testability of isolated components.
- [x] 2.4 Verify all tests pass successfully.
