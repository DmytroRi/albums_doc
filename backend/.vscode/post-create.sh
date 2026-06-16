#!/usr/bin/env bash
set -euo pipefail

echo "Configuring Git safe directory"
git config --global --unset-all safe.directory || true
git config --global --add safe.directory '*'

echo "Installing Python dependencies"
cd /workspace
python -m pip install -r requirements.txt

echo "Backend devcontainer ready"
