#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Fetching latest OpenAPI spec..."
curl -o openapi/api.yaml http://albums_doc-backend:8000/openapi.json
echo "✓ Done. Generated files are in lib/src/api/"