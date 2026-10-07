#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "Missing .env. Copy .env.example to .env first." >&2
  exit 1
fi

set -a
source .env
set +a

: "${RUNPOD_NETWORK_VOLUME_ID:?RUNPOD_NETWORK_VOLUME_ID is required}"
: "${RUNPOD_GPU_ID:?RUNPOD_GPU_ID is required}"
: "${RUNPOD_IMAGE:?RUNPOD_IMAGE is required}"

ARGS=(
  pod create
  --name "${RUNPOD_POD_NAME:-story-writer}"
  --image "$RUNPOD_IMAGE"
  --gpu-id "$RUNPOD_GPU_ID"
  --gpu-count 1
  --cloud-type "${RUNPOD_CLOUD_TYPE:-COMMUNITY}"
  --container-disk-in-gb "${RUNPOD_CONTAINER_DISK_GB:-20}"
  --network-volume-id "$RUNPOD_NETWORK_VOLUME_ID"
  --volume-mount-path /workspace
  --ssh
  --terminate-after "${RUNPOD_TERMINATE_AFTER:-6h}"
)

if [[ -n "${RUNPOD_COUNTRY_CODE:-}" ]]; then
  ARGS+=(--country-code "$RUNPOD_COUNTRY_CODE")
fi

if [[ -n "${RUNPOD_DATA_CENTER_IDS:-}" ]]; then
  ARGS+=(--data-center-ids "$RUNPOD_DATA_CENTER_IDS")
fi

echo "Creating disposable RunPod..."
runpodctl "${ARGS[@]}"

echo
echo "Run: ./scripts/runpod/status.sh"
echo "The Pod has a terminate-after safety limit of ${RUNPOD_TERMINATE_AFTER:-6h}."
