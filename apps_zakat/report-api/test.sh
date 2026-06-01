#!/usr/bin/env bash
# Run pytest untuk isf-zakat-report-api service.
# Pakai: ./test.sh [pytest-args...]
# Contoh:
#   ./test.sh                                   # semua test
#   ./test.sh tests/test_identity.py -v         # satu file
#   ./test.sh tests/test_identity.py::test_x    # satu test
#   ./test.sh -k profile                        # filter via keyword
set -euo pipefail

# Detect compose runtime (prefer podman, fallback docker)
if command -v podman-compose >/dev/null 2>&1; then
    COMPOSE="podman-compose"
elif command -v podman >/dev/null 2>&1 && podman compose version >/dev/null 2>&1; then
    COMPOSE="podman compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    COMPOSE="docker compose"
else
    echo "ERROR: tidak nemu podman-compose / podman compose / docker compose" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/infra/docker-compose.zakat.yml"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "ERROR: compose file tidak ditemukan: $COMPOSE_FILE" >&2
    exit 1
fi

# Default args kalau user tidak kasih apa-apa
if [ $# -eq 0 ]; then
    set -- "tests/" "-v"
fi

exec $COMPOSE -f "$COMPOSE_FILE" exec -T report-api python -m pytest "$@"
