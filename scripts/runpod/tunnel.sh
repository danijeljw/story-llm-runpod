#!/usr/bin/env bash
set -euo pipefail

SSH_HOST="${1:-}"
SSH_PORT="${2:-22}"
SSH_USER="${3:-root}"
LOCAL_PORT="${LOCAL_PORT:-8080}"
REMOTE_PORT="${LLAMA_PORT:-8080}"

if [[ -z "$SSH_HOST" ]]; then
  echo "Usage: $0 <ssh-host> [ssh-port] [ssh-user]" >&2
  exit 1
fi

echo "Forwarding http://127.0.0.1:${LOCAL_PORT} -> Pod 127.0.0.1:${REMOTE_PORT}"
exec ssh -N \
  -p "$SSH_PORT" \
  -L "${LOCAL_PORT}:127.0.0.1:${REMOTE_PORT}" \
  "${SSH_USER}@${SSH_HOST}"
