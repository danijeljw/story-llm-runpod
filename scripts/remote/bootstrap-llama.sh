#!/usr/bin/env bash
set -euo pipefail

MODEL="${LLAMA_MODEL:-/workspace/models/current.gguf}"
PORT="${LLAMA_PORT:-8080}"
CTX="${LLAMA_CONTEXT:-32768}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-999}"

if [[ ! -f "$MODEL" ]]; then
  echo "Model not found: $MODEL" >&2
  exit 1
fi

mkdir -p /workspace/runtime

if command -v llama-server >/dev/null 2>&1; then
  LLAMA_SERVER="$(command -v llama-server)"
else
  echo "llama-server is not installed." >&2
  echo "Install/build llama.cpp CUDA on the Pod image, or use a custom image containing it." >&2
  exit 1
fi

echo "Starting llama-server"
echo "Model:   $MODEL"
echo "Context: $CTX"
echo "Port:    $PORT"

exec "$LLAMA_SERVER" \
  --model "$MODEL" \
  --host 127.0.0.1 \
  --port "$PORT" \
  --ctx-size "$CTX" \
  --n-gpu-layers "$GPU_LAYERS"
