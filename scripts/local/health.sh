#!/usr/bin/env bash
set -euo pipefail

BASE="${LLM_BASE_URL:-http://127.0.0.1:8080}"
curl --fail --silent --show-error "$BASE/health"
echo
