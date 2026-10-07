#!/usr/bin/env bash
set -euo pipefail

BASE="${LLM_BASE_URL:-http://127.0.0.1:8080}"

curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  "$BASE/v1/chat/completions" \
  -d '{
    "messages": [
      {"role": "user", "content": "Reply with exactly: MODEL READY"}
    ],
    "temperature": 0
  }' | jq .
