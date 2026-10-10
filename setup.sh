#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Add OPENAI_API_KEY before running the demo."
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [ ! -d agntid-python ]; then
  git clone https://github.com/AGNTID-AI/agntid-python.git
fi
.venv/bin/python -m pip install -e "./agntid-python[openai]"

echo "Setup complete. Start services with: docker compose up -d --build"
echo "Then check readiness with: .venv/bin/python demo.py doctor"
