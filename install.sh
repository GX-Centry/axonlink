#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="${1:-$HOME/.claude/skills/axonlink}"

mkdir -p "$(dirname "$DEST_DIR")"
rm -rf "$DEST_DIR"
cp -R "$SRC_DIR" "$DEST_DIR"

echo "Installed AxonLink skill to: $DEST_DIR"
echo "Invoke with: /axonlink <user@target> <workflow-goal>"
