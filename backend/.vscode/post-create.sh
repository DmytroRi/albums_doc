set -e
echo "Setting git configurations"
get config --global --unset-all safe.directory || true
get config --global --add safe.directory '*' || true

chmod +x scripts/*.sh 2>/dev/null || true

echo "Installing Python dependencies"
cd /workspace
source .venv/bin/activate
pip install -e ".[dev]"
echo "Dependencies installed"