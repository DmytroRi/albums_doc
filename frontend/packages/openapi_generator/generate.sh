#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

OPENAPI_URL="${BACKEND_OPENAPI_URL:-http://backend:8000/openapi.json}"

printf '==> Fetching latest OpenAPI spec from %s...\n' "$OPENAPI_URL"
curl --fail --location --show-error --output openapi/api.yaml "$OPENAPI_URL"
echo "✓ Done. Generated files are in lib/src/api/"