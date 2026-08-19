#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ ! -d .venv ]; then
    PYTHON="$(command -v python3.11 || command -v python3.12 || command -v python3)"
    "$PYTHON" -m venv .venv
    .venv/bin/pip install -q -e ".[dev]"
fi

exec .venv/bin/mcp-hub
