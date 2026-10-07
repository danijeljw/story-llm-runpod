#!/usr/bin/env bash
set -euo pipefail

URL="${1:-}"
OUTPUT="${2:-/workspace/models/current.gguf}"

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <direct-gguf-url> [output-path]" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"

if command -v wget >/dev/null 2>&1; then
  wget -c "$URL" -O "$OUTPUT"
elif command -v curl >/dev/null 2>&1; then
  curl -L --continue-at - "$URL" -o "$OUTPUT"
else
  echo "Need wget or curl." >&2
  exit 1
fi

echo "Saved: $OUTPUT"
