# syntax=docker/dockerfile:1.7

FROM ghcr.io/cirruslabs/flutter:3.24.3 AS base

ENV FLUTTER_WEB=true \
    CHROME_EXECUTABLE=/usr/bin/chromium

WORKDIR /workspace

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        chromium \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN flutter config --enable-web \
    && flutter doctor

FROM base AS development

EXPOSE 3000 9222
CMD ["sleep", "infinity"]

FROM base AS build

COPY pubspec.yaml pubspec.lock ./
RUN flutter pub get

COPY . .

ARG API_BASE_URL=http://localhost:8000
RUN flutter build web --release \
    --dart-define=API_BASE_URL=${API_BASE_URL}

FROM nginx:alpine AS production

COPY --from=build /workspace/build/web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
