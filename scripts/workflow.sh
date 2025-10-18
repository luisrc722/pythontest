#!/usr/bin/env bash
set -euo pipefail

# Move to repo root (one level above this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo "[workflow] Repo: ${REPO_ROOT}"

if command -v make >/dev/null 2>&1; then
  echo "[workflow] 'make' found. Running: make workflow"
  exec make workflow
fi

echo "[workflow] 'make' not found. Running fallback steps..."

# Create venv if missing
if [[ ! -d .venv ]]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 -m venv .venv
  else
    python -m venv .venv
  fi
fi

PY=".venv/bin/python"
PIP=".venv/bin/pip"

echo "[workflow] Upgrading pip..."
"${PY}" -m pip install --upgrade pip

echo "[workflow] Installing dependencies..."
if [[ -f requirements.txt ]]; then
  "${PIP}" install -r requirements.txt
else
  # Minimal set per project docs
  "${PIP}" install numpy pytest pytest-cov ipywidgets jupyterlab rich black isort flake8 pydantic click toml inquirer streamlit fastapi uvicorn pandas matplotlib
fi

echo "[workflow] Validating question bank (strict coverage)..."
"${PY}" scripts/validate_questions.py --strict-coverage

echo "[workflow] Running tests with coverage..."
"${PY}" -m pytest --cov=src --cov-report=term-missing --cov-report=html

echo "[workflow] Done. Coverage report in ./htmlcov/index.html"

