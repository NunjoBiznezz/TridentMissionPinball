#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

find_godot() {
    for candidate in /opt/homebrew/bin/godot /usr/local/bin/godot; do
        [[ -x "$candidate" ]] && { echo "$candidate"; return 0; }
    done
    command -v godot &>/dev/null && { echo "godot"; return 0; }
    return 1
}

GODOT=$(find_godot) || {
    echo "Error: Godot not found. Install with: brew install godot" >&2
    exit 1
}

exec "$GODOT" --path gmc/ "$@"
