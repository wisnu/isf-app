#!/usr/bin/env bash
# E2E smoke test — Program Non Rutin (distribution domain)
# Portal: Zakat | BFF: http://localhost:7000 | API: http://localhost:8000
# Auth : session cookie required (use HADI/test1234 — DIST/SPVDIST)
# Usage: COOKIE="session=<value>" bash testing/e2e-program-non-rutin.sh

set -euo pipefail

BFF="http://localhost:7000"
API="http://localhost:8000"
COOKIE="${COOKIE:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

# ── Helpers ────────────────────────────────────────────────────────────────────

bff_get() {
  local path="$1"; shift
  curl -s -b "$COOKIE" "$BFF$path" "$@"
}

bff_post() {
  local path="$1"; local body="$2"
  curl -s -b "$COOKIE" -X POST -H 'Content-Type: application/json' -d "$body" "$BFF$path"
}

bff_put() {
  local path="$1"; local body="$2"
  curl -s -b "$COOKIE" -X PUT -H 'Content-Type: application/json' -d "$body" "$BFF$path"
}

bff_delete() {
  local path="$1"
  curl -s -b "$COOKIE" -X DELETE "$BFF$path"
}

api_get() {
  local path="$1"
  curl -s "$API$path"
}

assert_ok() {
  local label="$1"; local resp="$2"
  if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'error' not in d else 1)" 2>/dev/null; then
    pass "$label"
  else
    fail "$label — response: $resp"
  fi
}

assert_field() {
  local label="$1"; local resp="$2"; local field="$3"
  if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if '$field' in str(d) else 1)" 2>/dev/null; then
    pass "$label"
  else
    fail "$label — missing field '$field' in: $resp"
  fi
}

# ── Tests ──────────────────────────────────────────────────────────────────────

info "=== Program Non Rutin E2E Smoke Test ==="
echo ""

# 1. API direct — health
info "1. API Python — lookup products"
resp=$(api_get "/api/distribution/non-regular-program/lookup/products")
assert_ok "API lookup/products" "$resp"

info "2. API Python — lookup mustahiq"
resp=$(api_get "/api/distribution/non-regular-program/lookup/mustahiq")
assert_ok "API lookup/mustahiq" "$resp"

info "3. API Python — list (page 1)"
resp=$(api_get "/api/distribution/non-regular-program?page=1&page_size=5")
assert_ok "API list" "$resp"
assert_field "API list has pagination" "$resp" "pagination"

# 4. BFF routes (need auth cookie)
if [ -z "$COOKIE" ]; then
  info "Skipping BFF tests — no COOKIE set. Run: COOKIE='session=...' bash $0"
else
  info "4. BFF — list non-regular programs"
  resp=$(bff_get "/api/distribution/non-regular-program?page=1&page_size=5")
  assert_ok "BFF list" "$resp"

  info "5. BFF — lookup products"
  resp=$(bff_get "/api/distribution/non-regular-program/lookup/products")
  assert_ok "BFF lookup/products" "$resp"

  info "6. BFF — lookup mustahiq (search: 'a')"
  resp=$(bff_get "/api/distribution/non-regular-program/lookup/mustahiq?search=a")
  assert_ok "BFF lookup/mustahiq" "$resp"

  # Get first product_id and mustahiq_id from lookup
  PRODUCT_ID=$(curl -s "$API/api/distribution/non-regular-program/lookup/products" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['product_id'] if d.get('data') else 1)")
  MUSTAHIQ_ID=$(curl -s "$API/api/distribution/non-regular-program/lookup/mustahiq" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['mustahiq_id'] if d.get('data') else 1)")

  info "7. BFF — create program (product=$PRODUCT_ID, mustahiq=$MUSTAHIQ_ID)"
  CREATE_BODY=$(python3 -c "import json; print(json.dumps({
    'mustahiq_id': $MUSTAHIQ_ID,
    'product_id': $PRODUCT_ID,
    'program_detail_name': 'TEST Non Rutin E2E',
    'distribution_amount': 500000,
    'date_start': '2026-06-22',
    'date_end': None,
    'proposal_id': None
  }))")
  resp=$(bff_post "/api/distribution/non-regular-program" "$CREATE_BODY")
  assert_ok "BFF create" "$resp"
  PROGRAM_ID=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['program_id'])" 2>/dev/null || echo "")

  if [ -n "$PROGRAM_ID" ]; then
    info "8. BFF — get detail (id=$PROGRAM_ID)"
    resp=$(bff_get "/api/distribution/non-regular-program/$PROGRAM_ID")
    assert_ok "BFF get detail" "$resp"
    assert_field "detail has program_id" "$resp" "program_id"

    info "9. BFF — update program"
    UPDATE_BODY=$(python3 -c "import json; print(json.dumps({
      'mustahiq_id': $MUSTAHIQ_ID,
      'product_id': $PRODUCT_ID,
      'program_detail_name': 'TEST Non Rutin E2E UPDATED',
      'distribution_amount': 750000,
      'date_start': '2026-06-22',
      'date_end': None
    }))")
    resp=$(bff_put "/api/distribution/non-regular-program/$PROGRAM_ID" "$UPDATE_BODY")
    assert_ok "BFF update" "$resp"

    info "10. BFF — filter by date"
    resp=$(bff_get "/api/distribution/non-regular-program?date_from=2026-06-01&date_to=2026-06-30")
    assert_ok "BFF filter by date" "$resp"

    info "11. BFF — filter by search"
    resp=$(bff_get "/api/distribution/non-regular-program?search=TEST")
    assert_ok "BFF filter by search" "$resp"

    info "12. BFF — delete program"
    resp=$(bff_delete "/api/distribution/non-regular-program/$PROGRAM_ID")
    assert_ok "BFF delete" "$resp"

    info "13. BFF — verify deleted (expect 404)"
    resp=$(bff_get "/api/distribution/non-regular-program/$PROGRAM_ID")
    if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'error' in d else 1)" 2>/dev/null; then
      pass "BFF get deleted returns error"
    else
      fail "BFF get deleted should return error"
    fi
  else
    info "Skipping detail/update/delete — could not extract program_id from create response"
  fi
fi

echo ""
info "=== Test complete ==="
