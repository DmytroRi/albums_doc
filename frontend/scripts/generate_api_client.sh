#!/usr/bin/env bash
set -euo pipefail

BACKEND_OPENAPI_URL="${BACKEND_OPENAPI_URL:-http://backend:8000/openapi.json}"
OUTPUT_SPEC="${OUTPUT_SPEC:-/tmp/albums-openapi.json}"

curl -sS "${BACKEND_OPENAPI_URL}" -o "${OUTPUT_SPEC}"
openapi-generator-cli generate \
  -i "${OUTPUT_SPEC}" \
  -g dart-dio \
  -o lib/generated_api \
  --additional-properties=pubName=albums_api_client,pubVersion=1.0.0,useEnumExtension=true
