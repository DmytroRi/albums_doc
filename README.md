# Albums Doc

Full-stack album documentation app with a PostgreSQL database, FastAPI + SQLModel backend, and Flutter BLoC frontend.

## Project structure

- `backend/` FastAPI app, SQLModel models, Alembic migrations, and backend Dockerfile
- `frontend/` Flutter app, generated OpenAPI client, and frontend Dockerfile
- `.devcontainer/backend` backend VS Code Devcontainer configuration
- `.devcontainer/frontend` frontend VS Code Devcontainer configuration
- `docker-compose.dev.yml` development stack
- `docker-compose.prod.yml` production/public stack

## Required tools

- Docker + Docker Compose
- VS Code Dev Containers extension for containerized development
- Optional local Python 3.12+
- Optional local Flutter 3.24+
- Optional local OpenAPI Generator CLI (`openapi-generator-cli`)

## Environment variables

Development and production containers use PostgreSQL service discovery through the Compose service name `postgres`.

`backend/.env.example` defines the backend/database defaults:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `DATABASE_URL`

For local non-container backend runs, override `DATABASE_URL` if PostgreSQL is exposed on `localhost` instead of the Compose hostname.

## Development stack

Start the full development stack:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Start only PostgreSQL:

```bash
docker compose -f docker-compose.dev.yml up -d postgres
```

Start only backend dependencies and attach to the backend devcontainer from VS Code:

```bash
docker compose -f docker-compose.dev.yml up -d postgres backend
```

Start only frontend dependencies and attach to the frontend devcontainer from VS Code:

```bash
docker compose -f docker-compose.dev.yml up -d postgres backend frontend
```

Inside the backend devcontainer, run the API server with:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Inside the frontend devcontainer, run the web app with:

```bash
flutter pub get
flutter run -d web-server --web-hostname 0.0.0.0 --web-port 3000 --dart-define=API_BASE_URL=http://localhost:8000
```

## Devcontainers

The devcontainer configs avoid remote Dev Container Features so opening containers does not need to resolve `ghcr.io/devcontainers/features/*`; required OS tools such as Git are installed by the service Dockerfiles.

Backend devcontainer:

1. Open the repository in VS Code.
2. Use **Dev Containers: Reopen in Container** with `.devcontainer/backend/devcontainer.json`.
3. Run migrations, tests, and `uvicorn` inside the container.

Frontend devcontainer:

1. Open the repository in VS Code.
2. Use **Dev Containers: Reopen in Container** with `.devcontainer/frontend/devcontainer.json`.
3. Run `flutter`, web server, and OpenAPI generation commands inside the container.

## OpenAPI workflow

FastAPI exposes OpenAPI at `/openapi.json` and docs at `/docs`.

Generate the Dart client from inside the frontend devcontainer:

```bash
cd /workspace
BACKEND_OPENAPI_URL=http://backend:8000/openapi.json ./scripts/generate_api_client.sh
```

Generate the Dart client from the host while the backend is published on localhost:

```bash
cd frontend
BACKEND_OPENAPI_URL=http://localhost:8000/openapi.json ./scripts/generate_api_client.sh
```

Generator output is written to `frontend/lib/generated_api`.

## Production/public stack

Start the full production stack:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Start individual services:

```bash
docker compose -f docker-compose.prod.yml up -d postgres
docker compose -f docker-compose.prod.yml up -d backend
docker compose -f docker-compose.prod.yml up -d frontend
```

The production stack publishes:

- Backend API: `http://localhost:8000`
- Frontend web app: `http://localhost:8080`

## Container lifecycle commands

Stop development containers while preserving named volumes:

```bash
docker compose -f docker-compose.dev.yml down
```

Stop production containers while preserving named volumes:

```bash
docker compose -f docker-compose.prod.yml down
```

Rebuild development images:

```bash
docker compose -f docker-compose.dev.yml build --no-cache
```

Rebuild production images:

```bash
docker compose -f docker-compose.prod.yml build --no-cache
```

## Run backend locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=postgresql+psycopg://albums:albums@localhost:5432/albums uvicorn app.main:app --reload
```

## Run frontend locally

```bash
cd frontend
flutter pub get
flutter run -d web-server --web-port 3000 --dart-define=API_BASE_URL=http://localhost:8000
```

## Alembic migrations

Create migration:

```bash
cd backend
alembic revision --autogenerate -m "message"
```

Apply migrations:

```bash
cd backend
alembic upgrade head
```

## Tests

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
flutter test
```

## Ubuntu deployment notes

1. Install Docker and the Compose plugin.
2. Copy the project to the server.
3. Copy `backend/.env.example` to a production env file or replace its values with production secrets.
4. Update `docker-compose.prod.yml` to reference the production env file if needed.
5. Run `docker compose -f docker-compose.prod.yml up -d --build`.
6. Put a reverse proxy in front of published frontend/backend ports as needed.