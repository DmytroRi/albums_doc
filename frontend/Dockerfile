# syntax=docker/dockerfile:1.7

# frontend/Dockerfile
# Flutter frontend with OpenAPI client generation from your backend.

FROM ghcr.io/cirruslabs/flutter:stable AS base

ENV FLUTTER_WEB=true \
    CHROME_EXECUTABLE=/usr/bin/chromium

WORKDIR /workspace

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    chromium \
    curl \
    git \
    ca-certificates \
    powershell \
    && rm -rf /var/lib/apt/lists/*

RUN flutter channel stable \
    && flutter config --enable-web \
    && flutter doctor

# Development stage used by docker-compose: target: development
FROM base AS development

EXPOSE 3000 9222

# docker-compose overrides this with: command: sleep infinity
CMD ["sleep", "infinity"]

# OpenAPI generation stage for your backend.
# This requires a named build context called "backend" in docker-compose.
FROM python:3.13-slim AS openapi_generator_backend

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend . /backend
WORKDIR /backend

RUN pip install --upgrade pip setuptools wheel \
    && pip install -e .[dev] \
    && python generate_openapi.py

# Build dependencies and generated OpenAPI client.
FROM base AS build_pre

COPY . .

# Shared packages directory.
# This requires a named build context called "packages" in docker-compose.
COPY --from=packages / /workspace/packages

RUN mkdir -p /workspace/packages/unified_backend_client/tmp
COPY --from=openapi_generator_backend /backend/openapi.json /workspace/packages/unified_backend_client/tmp/backend_api.json

RUN flutter clean

ENV CI=true
RUN pwsh -File /workspace/packages/unified_backend_client/utils/build.ps1

RUN flutter pub get

# Test stage
FROM build_pre AS test

RUN flutter packages pub run build_runner build --delete-conflicting-outputs || echo "No code generation needed"

ENV FLUTTER_TEST=true \
    CI=true

CMD ["flutter", "test"]

# Production build stage
FROM build_pre AS build

ARG BASE_HREF=/
ARG APP_VERSION=dev
ARG APP_GIT_HASH=unknown

RUN flutter build web --release \
    --dart-define=APP_CONFIG_SRC="${BASE_HREF}config.json" \
    --dart-define=APP_VERSION="${APP_VERSION}" \
    --dart-define=APP_GIT_HASH="${APP_GIT_HASH}" \
    --base-href="${BASE_HREF}"

# Production runtime stage
FROM nginx:alpine AS production

COPY --from=build /workspace/build/web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]