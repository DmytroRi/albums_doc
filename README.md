# Albums Doc

Full-stack album documentation app with FastAPI + SQLModel backend and Flutter BLoC frontend.

## Project structure

- `backend/` FastAPI app, SQLModel models, Alembic migrations
- `frontend/` Flutter app (StatelessWidget-only UI), BLoC, generated OpenAPI client location
- `.devcontainer/backend` backend development container
- `.devcontainer/frontend` frontend development container
- `docker-compose.dev.yml` development stack
- `docker-compose.prod.yml` production/public stack

## Required tools

- Docker + Docker Compose
- (optional local) Python 3.12+
- (optional local) Flutter 3.24+
- OpenAPI Generator CLI (`openapi-generator-cli`)

## Environment variables

Use `backend/.env.example`:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `DATABASE_URL`

## OpenAPI workflow

FastAPI exposes OpenAPI at `/openapi.json` and docs at `/docs`.

Generate Dart client:
```bash
cd frontend
./scripts/generate_api_client.sh
```
Generator configuration is in `frontend/openapi-generator-config.yaml`.

## Development stack (WSL/local)

Start full stack:
```bash
docker compose -f docker-compose.dev.yml up --build
```

Start only PostgreSQL:
```bash
docker compose -f docker-compose.dev.yml up -d postgres
```

Start only backend:
```bash
docker compose -f docker-compose.dev.yml up --build backend
```

Start only frontend:
```bash
docker compose -f docker-compose.dev.yml up --build frontend
```

## Production/public stack (Ubuntu Server)

Start full stack:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Start individual services:
```bash
docker compose -f docker-compose.prod.yml up -d postgres
docker compose -f docker-compose.prod.yml up -d backend
docker compose -f docker-compose.prod.yml up -d frontend
```

## Container lifecycle commands

Stop:
```bash
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.prod.yml down
```

Rebuild:
```bash
docker compose -f docker-compose.dev.yml build --no-cache
docker compose -f docker-compose.prod.yml build --no-cache
```

## Run backend locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run frontend locally

```bash
cd frontend
flutter pub get
flutter run -d web-server --web-port 3000
```

## Devcontainers

Backend devcontainer:
- Open folder in `.devcontainer/backend`
- Run migrations, tests, and uvicorn inside container

Frontend devcontainer:
- Open folder in `.devcontainer/frontend`
- Run flutter and OpenAPI generation commands inside container

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

## Ubuntu deployment notes

1. Install Docker and Compose plugin.
2. Copy project to server.
3. Adjust `backend/.env.example` values for production secrets/hosts.
4. Run `docker compose -f docker-compose.prod.yml up -d --build`.
5. Expose frontend port (8080) and backend port through reverse proxy as needed.
