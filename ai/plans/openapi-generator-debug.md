# OpenAPI Generator Silent Failure Troubleshooting Plan

Use this single-session runbook when `openapi-generator` can read the OpenAPI spec but creates no output and exits without an obvious error. The commands assume you are running from the repository root (`/workspace/albums_doc`) and that the Flutter/Dart generator package lives in `frontend/packages/openapi_generator`.

## Phase 1: Diagnosis & Validation

### 1. Confirm the working tree and generator package paths

```bash
pwd
git status --short
test -d frontend/packages/openapi_generator && echo "generator package exists"
test -f frontend/packages/openapi_generator/build.yaml && echo "build.yaml exists"
test -f frontend/packages/openapi_generator/openapi/api.yaml && echo "OpenAPI input exists"
```

**Success:** `pwd` prints `/workspace/albums_doc`, the three `test` commands print their confirmation messages, and `git status --short` shows only changes you expect.

### 2. Capture the exact input and output paths used by the Dart builder

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
python3 - <<'PY'
from pathlib import Path
for rel in ["build.yaml", "openapi/api.yaml", "lib/src/api"]:
    p = Path(rel)
    print(f"{rel}: exists={p.exists()} is_file={p.is_file()} is_dir={p.is_dir()} absolute={p.resolve()}")
PY
```

**Success:** `build.yaml` and `openapi/api.yaml` report `exists=True`; `lib/src/api` may be absent before generation, but the absolute paths should point inside `frontend/packages/openapi_generator`.

### 3. Validate the OpenAPI document is parseable YAML/JSON

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
python3 - <<'PY'
from pathlib import Path
import json
try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is not installed; install it or use the JSON validation command below") from exc
spec_path = Path("openapi/api.yaml")
spec = yaml.safe_load(spec_path.read_text())
print("top-level type:", type(spec).__name__)
print("openapi:", spec.get("openapi"))
print("paths:", len(spec.get("paths", {})))
print("components.schemas:", len(spec.get("components", {}).get("schemas", {})))
assert isinstance(spec, dict), "spec must be a mapping/object"
assert spec.get("openapi"), "missing openapi version"
assert spec.get("paths"), "missing or empty paths"
PY
```

If your input file is JSON instead of YAML, run:

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
python3 -m json.tool openapi/openapi.json >/tmp/openapi.pretty.json
```

**Success:** The YAML command prints the OpenAPI version plus non-zero `paths`; the JSON command exits with code `0` and writes `/tmp/openapi.pretty.json`.

### 4. Validate the spec with OpenAPI Generator before generating code

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
npx --yes @openapitools/openapi-generator-cli validate -i openapi/api.yaml --recommend
```

**Success:** The command exits with code `0` and reports that the specification is valid. Warnings are acceptable only if they do not reference missing `paths`, invalid schemas, unresolved `$ref`s, or unsupported OpenAPI versions.

### 5. Confirm the output directory is writable and can be recreated

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
mkdir -p lib/src/api
printf 'write-test\n' > lib/src/api/.write-test
cat lib/src/api/.write-test
rm lib/src/api/.write-test
```

**Success:** `cat` prints `write-test`, and the temporary file is removed without permission errors.

### 6. Confirm Java, Dart, and generator entry points are available

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
java -version
dart --version
dart pub deps --style=compact | sed -n '/openapi_generator/p'
npx --yes @openapitools/openapi-generator-cli version
```

**Success:** Java prints a supported runtime version, Dart prints a Dart 3.x version compatible with `pubspec.yaml`, `dart pub deps` includes `openapi_generator`, and the `npx` command prints an OpenAPI Generator CLI version.

## Phase 2: Verbose Localization

### 1. Run the Dart builder with maximum verbosity

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
dart pub get
dart run build_runner build --delete-conflicting-outputs --verbose 2>&1 | tee /tmp/openapi_build_runner_verbose.log
```

**Success:** The log contains builder activity for `openapi_generator|openapi_generator`, exits with code `0`, and files appear under `lib/src/api`. If it exits `0` but no files appear, continue to the direct CLI commands below.

### 2. Run the Java CLI directly with generator debug flags

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
rm -rf /tmp/openapi-generator-debug-out
npx --yes @openapitools/openapi-generator-cli generate \
  -i openapi/api.yaml \
  -g dart-dio \
  -o /tmp/openapi-generator-debug-out \
  --verbose \
  --global-property debugOpenAPI=true,debugModels=true,debugOperations=true,debugSupportingFiles=true \
  --additional-properties pubName=openapi_generator,pubAuthor=art-lib,useEnumExtension=true,nullableFields=true \
  2>&1 | tee /tmp/openapi_generator_cli_verbose.log
```

**Success:** The command exits with code `0`, `/tmp/openapi-generator-debug-out` contains generated files, and the log shows parsed models, operations, and supporting files. If `/tmp` generation works but project generation fails, the issue is likely Dart builder configuration, output path resolution, or project write permissions.

### 3. Generate into the real output path with the direct CLI

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
rm -rf lib/src/api
npx --yes @openapitools/openapi-generator-cli generate \
  -i openapi/api.yaml \
  -g dart-dio \
  -o lib/src/api \
  --verbose \
  --global-property debugOpenAPI=true,debugModels=true,debugOperations=true,debugSupportingFiles=true \
  --additional-properties pubName=openapi_generator,pubAuthor=art-lib,useEnumExtension=true,nullableFields=true \
  2>&1 | tee /tmp/openapi_generator_real_output_verbose.log
```

**Success:** `lib/src/api` is recreated with Dart files, `pubspec.yaml`, and generator metadata. Failure here localizes the problem to the spec, generator version, template resolution, or filesystem path.

### 4. Inspect the verbose logs for silent skip signals

```bash
for log in /tmp/openapi_build_runner_verbose.log /tmp/openapi_generator_cli_verbose.log /tmp/openapi_generator_real_output_verbose.log; do
  echo "===== $log ====="
  test -f "$log" && rg -n "error|exception|warn|skip|ignored|no files|template|mustache|unsupported|failed|empty|invalid" "$log" || true
done
```

**Success:** No high-severity errors are present. Any matched warnings identify the next remediation target, such as template lookup, invalid schema names, unsupported generator options, or an empty operations list.

## Phase 3: Common Fixes Root Cause Analysis

### 1. Fix incorrect CLI syntax or misplaced debug flags

Use supported CLI options instead of JVM-style flags placed in the wrong position:

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
npx --yes @openapitools/openapi-generator-cli help generate | sed -n '/--verbose/,+25p'
npx --yes @openapitools/openapi-generator-cli generate \
  -i openapi/api.yaml \
  -g dart-dio \
  -o lib/src/api \
  --verbose \
  --global-property debugModels=true,debugOperations=true,debugSupportingFiles=true \
  --additional-properties pubName=openapi_generator,pubAuthor=art-lib,useEnumExtension=true,nullableFields=true
```

**Success:** Help output documents the flags being used, and generation creates files. If `-DdebugModels` is required by your installed CLI wrapper, pass it before the Java `generate` command only when invoking the JAR directly; otherwise prefer `--global-property debugModels=true`.

### 2. Fix output path confusion between the generator package and Flutter app

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
printf 'Configured outputDirectory from build.yaml:\n'
python3 - <<'PY'
import yaml
cfg = yaml.safe_load(open('build.yaml'))
opts = cfg['targets']['$default']['builders']['openapi_generator|openapi_generator']['options']
print(opts['outputDirectory'])
PY
printf 'Generated package output:\n'
find lib/src/api -maxdepth 3 -type f | sort | head -50
printf 'Flutter app generated output:\n'
find /workspace/albums_doc/frontend/lib/generated_api -maxdepth 3 -type f | sort | head -50
```

**Success:** You know which output tree the generator writes. If the app expects `frontend/lib/generated_api` but the builder writes `frontend/packages/openapi_generator/lib/src/api`, either update `outputDirectory` or add a copy step after generation.

### 3. Fix missing or stale dependencies

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
dart pub cache repair
dart pub get
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs --verbose
```

**Success:** Dependency resolution completes, the build cache is cleaned, and a verbose build generates output without stale-cache warnings.

### 4. Fix version mismatch between Dart builder and Java CLI

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
dart pub deps --style=compact | sed -n '/openapi_generator/p'
npx --yes @openapitools/openapi-generator-cli version-manager list | sed -n '1,80p'
npx --yes @openapitools/openapi-generator-cli version-manager set 7.8.0
npx --yes @openapitools/openapi-generator-cli version
```

**Success:** The selected Java CLI version is known and stable. Re-run the direct generation command after pinning. If the Dart builder wraps a different Java CLI version, align package versions in `pubspec.yaml` or bypass the builder with the direct CLI until the package is upgraded.

### 5. Fix missing custom templates or wrong template path

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
find . -maxdepth 4 -type d \( -name templates -o -name template \) -print
npx --yes @openapitools/openapi-generator-cli author template -g dart-dio -o /tmp/dart-dio-default-templates
find /tmp/dart-dio-default-templates -maxdepth 2 -type f | sort | head -50
```

If `build.yaml` or your script references a custom template directory, verify it:

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
CUSTOM_TEMPLATE_DIR="./templates"
test -d "$CUSTOM_TEMPLATE_DIR" && find "$CUSTOM_TEMPLATE_DIR" -maxdepth 2 -type f | sort || echo "custom template directory is missing"
```

**Success:** Either no custom template directory is configured, or the configured directory exists and contains the expected Mustache templates. If templates are missing, remove the custom template option or restore the template files.

### 6. Fix an empty effective API caused by filters or malformed paths

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
python3 - <<'PY'
import yaml
spec = yaml.safe_load(open('openapi/api.yaml'))
methods = {'get','put','post','delete','patch','options','head','trace'}
ops = []
for path, item in (spec.get('paths') or {}).items():
    for method, op in (item or {}).items():
        if method.lower() in methods:
            ops.append((method.upper(), path, op.get('operationId')))
print(f"operation count: {len(ops)}")
for row in ops[:50]:
    print(*row)
assert ops, "No operations found; generator has nothing to emit"
PY
```

**Success:** The operation count is greater than zero. If zero, fix the backend OpenAPI export before troubleshooting code generation.

### 7. Fix permissions or container user ownership issues

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
id
stat -c '%U:%G %a %n' . openapi openapi/api.yaml lib lib/src 2>/dev/null || true
mkdir -p lib/src/api
chmod -R u+rwX lib/src/api
```

**Success:** The current user owns or can write the output directory. If files are owned by another container user, change ownership in the container or regenerate into a clean, user-owned directory.

## Phase 4: Verification

### 1. Confirm files were generated where expected

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
find lib/src/api -type f | sort | tee /tmp/openapi_generated_files.txt
wc -l /tmp/openapi_generated_files.txt
test "$(wc -l < /tmp/openapi_generated_files.txt)" -gt 0
```

**Success:** The file list is non-empty, `wc -l` is greater than zero, and the final `test` exits with code `0`.

### 2. Confirm generated Dart sources contain expected APIs and models

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
rg -n "class .*Api|class .*Model|ApiClient|Dio" lib/src/api
```

**Success:** `rg` finds API classes, model classes, and client/Dio references in the generated output.

### 3. Run package-level static checks

```bash
cd /workspace/albums_doc/frontend/packages/openapi_generator
dart pub get
dart analyze lib/src/api
```

**Success:** `dart analyze` exits with code `0` or reports only accepted generated-code informational lints. Any syntax errors mean the generator produced invalid Dart for the current dependency versions.

### 4. If the Flutter app consumes generated files, sync and analyze the app

```bash
cd /workspace/albums_doc
rm -rf frontend/lib/generated_api
mkdir -p frontend/lib/generated_api
cp -R frontend/packages/openapi_generator/lib/src/api/. frontend/lib/generated_api/
cd frontend
flutter pub get
flutter analyze
```

**Success:** The app dependency resolution completes and `flutter analyze` exits with code `0`, proving the generated client is compatible with the consuming Flutter app.

### 5. Record the final generator command and diff

```bash
cd /workspace/albums_doc
git diff -- frontend/packages/openapi_generator frontend/lib/generated_api | sed -n '1,240p'
git status --short
```

**Success:** The diff contains only expected generated-code or configuration changes, and `git status --short` has no unexpected files. Commit only after the generated output and configuration are verified.
