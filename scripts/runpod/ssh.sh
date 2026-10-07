#!/usr/bin/env bash
set -euo pipefail

POD_ID="${1:-}"

if [[ -z "$POD_ID" ]]; then
  echo "Usage: $0 <pod-id>" >&2
  echo "Find it with: runpodctl pod list --all" >&2
  exit 1
fi

runpodctl pod get "$POD_ID"
echo
echo "Use the SSH command shown above by RunPod."
