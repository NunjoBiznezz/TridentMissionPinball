#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Find a Python 3.11 interpreter that has MPF installed.
# Checks common venv locations, then falls back to python3.11 on PATH.
find_python() {
    for candidate in ~/mpf/venv ~/mpf-env ~/.local/share/mpf/venv ./venv; do
        py="${candidate/#\~/$HOME}/bin/python3.11"
        if [[ -x "$py" ]] && "$py" -c "import mpf" 2>/dev/null; then
            echo "$py"; return 0
        fi
    done
    if command -v python3.11 &>/dev/null && python3.11 -c "import mpf" 2>/dev/null; then
        echo "python3.11"; return 0
    fi
    return 1
}

PYTHON=$(find_python) || {
    echo "Error: Python 3.11 with MPF not found." >&2
    echo "Set up with: python3.11 -m venv ~/mpf/venv && source ~/mpf/venv/bin/activate && pip install mpf" >&2
    exit 1
}

exec "$PYTHON" -m mpf . -c config_dev.yaml -t -x "$@"
