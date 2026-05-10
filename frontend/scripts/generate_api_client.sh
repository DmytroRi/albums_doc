#!/usr/bin/env bash
set -euo pipefail
curl -sS ${BACKEND_OPENAPI_URL:-http://localhost:8000/openapi.json} -o ../backend/openapi.json
openapi-generator-cli generate -c openapi-generator-config.yaml
