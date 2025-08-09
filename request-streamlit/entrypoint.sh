#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] starting…"
SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
SRC_DIR="${SRC_DIR:-${SCRIPT_DIR}/src}"

HEALTH_PATH="${HEALTH_PATH:-${SRC_DIR}/health.py}"
HEALTH_PORT="${HEALTH_PORT:-8080}"

# Resolve Streamlit target (arg or default)
if [[ $# -ge 1 ]]; then
  if [[ -f "$1" ]]; then
    TARGET="$1"
  elif [[ -f "${SRC_DIR}/$1" ]]; then
    TARGET="${SRC_DIR}/$1"
  else
    echo "[entrypoint] ERROR: cannot find Streamlit target: $1"
    exit 2
  fi
else
  TARGET="${SRC_DIR}/app.py"
fi

echo "[entrypoint] health: python ${HEALTH_PATH} (HEALTH_PORT=${HEALTH_PORT})"
python "${HEALTH_PATH}" &

STREAMLIT_ADDR="${STREAMLIT_ADDR:-0.0.0.0}"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"
echo "[entrypoint] streamlit: ${TARGET} on ${STREAMLIT_ADDR}:${STREAMLIT_PORT}"

exec streamlit run "${TARGET}" --server.address="${STREAMLIT_ADDR}" --server.port="${STREAMLIT_PORT}"
