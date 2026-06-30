#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OPENAPI_URL="${BACKEND_OPENAPI_URL:-http://backend:8000/openapi.json}"
GENERATOR_OUTPUT_DIR="$SCRIPT_DIR/lib/src/api"
APP_LINK_DIR="${1:-$REPO_ROOT/frontend/lib/generated_api}"
SPEC_PATH="$SCRIPT_DIR/openapi/api.yaml"
TMP_SPEC="$(mktemp)"

cleanup() {
  rm -f "$TMP_SPEC"
}
trap cleanup EXIT

printf '==> Fetching latest OpenAPI spec from %s...\n' "$OPENAPI_URL"
curl --fail --location --show-error --silent --output "$TMP_SPEC" "$OPENAPI_URL"

python3 - "$TMP_SPEC" <<'PY'
from pathlib import Path
import json
import sys

spec_path = Path(sys.argv[1])
raw = spec_path.read_text(encoding="utf-8").strip()
if not raw:
    raise SystemExit("Downloaded OpenAPI spec is empty")
try:
    spec = json.loads(raw)
except json.JSONDecodeError as exc:
    raise SystemExit(f"Downloaded OpenAPI spec is not valid JSON: {exc}") from exc
if not isinstance(spec, dict):
    raise SystemExit("Downloaded OpenAPI spec must be a JSON object")
if not spec.get("openapi"):
    raise SystemExit("Downloaded OpenAPI spec is missing the 'openapi' version")
paths = spec.get("paths")
if not isinstance(paths, dict) or not paths:
    raise SystemExit("Downloaded OpenAPI spec has no paths; generator would create no client APIs")
methods = {"get", "put", "post", "delete", "patch", "options", "head", "trace"}
operation_count = sum(
    1
    for path_item in paths.values()
    if isinstance(path_item, dict)
    for method in path_item
    if method.lower() in methods
)
if operation_count == 0:
    raise SystemExit("Downloaded OpenAPI spec contains paths but no operations")
print(f"✓ OpenAPI {spec['openapi']} with {len(paths)} paths and {operation_count} operations")
PY

mkdir -p "$(dirname "$SPEC_PATH")"
cp "$TMP_SPEC" "$SPEC_PATH"

if ! command -v dart >/dev/null 2>&1; then
  echo "ERROR: dart is required to run the OpenAPI generator. Run this script in the frontend devcontainer." >&2
  exit 127
fi

cd "$SCRIPT_DIR"
printf '==> Resolving generator dependencies...\n'
dart pub get

printf '==> Generating Dart client into %s...\n' "$GENERATOR_OUTPUT_DIR"
rm -rf "$GENERATOR_OUTPUT_DIR"
dart run build_runner build --delete-conflicting-outputs --verbose

if ! find "$GENERATOR_OUTPUT_DIR" -type f -print -quit | grep -q .; then
  echo "ERROR: OpenAPI generator completed without creating files in $GENERATOR_OUTPUT_DIR" >&2
  exit 1
fi

printf '==> Linking generated client into %s...\n' "$APP_LINK_DIR"
rm -rf "$APP_LINK_DIR"
mkdir -p "$(dirname "$APP_LINK_DIR")"
REL_GENERATOR_OUTPUT_DIR="$(python3 - "$GENERATOR_OUTPUT_DIR" "$(dirname "$APP_LINK_DIR")" <<'PY'
from pathlib import Path
import os
import sys

print(os.path.relpath(Path(sys.argv[1]), Path(sys.argv[2])))
PY
)"
ln -sfn "$REL_GENERATOR_OUTPUT_DIR" "$APP_LINK_DIR"

GENERATED_COUNT="$(find "$GENERATOR_OUTPUT_DIR" -type f | wc -l | tr -d ' ')"
printf '✓ Done. Generated %s files in %s and linked them at %s.\n' "$GENERATED_COUNT" "$GENERATOR_OUTPUT_DIR" "$APP_LINK_DIR"