# Backend Tests

This directory contains the backend test suite for the FastAPI/SQLModel service.

## Layout

- `models/` contains unit tests for SQLModel data models, validation rules, link tables, and relationships.
- `endpoints/` contains API tests for FastAPI routes, status codes, payload validation, happy paths, and not-found/error behavior.
- `conftest.py` builds an isolated in-memory SQLite database per test and overrides the FastAPI `get_session` dependency so tests do not require PostgreSQL or any external service.

## Run tests

From the repository root:

```bash
PYTHONPATH=backend pytest backend/tests -v --tb=short
```

From inside the backend devcontainer, the workspace is mounted at `/workspace`, so run:

```bash
pytest tests -v --tb=short
```

You can also use the VS Code task **Run Tests** to execute the same command in the container.

## Debug tests in VS Code

1. Open the backend devcontainer.
2. Install the recommended Python extension if prompted.
3. Use the Testing panel to discover pytest tests under `tests/`.
4. Select a test and choose **Debug Test**, or run the **Run Tests** task from **Terminal > Run Task...**.

## Adding tests

- Add model-focused tests under `models/`.
- Add route/API tests under `endpoints/`.
- Prefer the `client` fixture for endpoint tests and the `session` fixture for direct database/model tests.
- Keep tests isolated: create all required records inside each test, and mock or dependency-override external services instead of calling real infrastructure.
