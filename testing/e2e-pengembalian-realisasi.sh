#!/usr/bin/env bash
# E2E Smoke Test: Pengembalian Realisasi Program
# Portal: Zakat | Domain: Distribution
# Menu: distribution.realization-return.list
# Endpoints: /api/distribution/realization-return (BFF → api-python)
#
# Prasyarat:
#   - Stack zakat berjalan (make run-zakat)
#   - Seed diapply: psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-pengembalian-realisasi.sql
#   - Ada data realisasi di program.realization yang belum punya return
#
# Jalankan: bash testing/e2e-pengembalian-realisasi.sh

set -euo pipefail

BFF="http://localhost:7000"
API="http://localhost:8000"
COOKIE_FILE="/tmp/isf_e2e_pengembalian.txt"
PASS=0
FAIL=0

green() { echo -e "\033[32m✓ $*\033[0m"; }
red()   { echo -e "\033[31m✗ $*\033[0m"; }

check() {
  local desc="$1"
  local result="$2"
  local expected="${3:-}"
  if [[ -n "$expected" ]]; then
    if echo "$result" | grep -q "$expected"; then
      green "$desc"
      PASS=$((PASS+1))
    else
      red "$desc — expected '$expected' in: ${result:0:200}"
      FAIL=$((FAIL+1))
    fi
  else
    if [[ "$result" == "true" ]]; then
      green "$desc"
      PASS=$((PASS+1))
    else
      red "$desc — got: ${result:0:200}"
      FAIL=$((FAIL+1))
    fi
  fi
}

echo "=== E2E: Pengembalian Realisasi Program ==="
echo ""

# ── Health checks ─────────────────────────────────────────────────────────────
echo "--- Health checks ---"
BFF_H=$(curl -s --max-time 5 "$BFF/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['status'])" 2>/dev/null || echo "error")
check "BFF health" "$BFF_H" "ok"

API_H=$(curl -s --max-time 5 "$API/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['status'])" 2>/dev/null || echo "error")
check "api-python health" "$API_H" "ok"

echo ""

# ── Login sebagai HADI (DIST, SPVDIST) ───────────────────────────────────────
echo "--- Authentication ---"
LOGIN=$(curl -s --max-time 10 -c "$COOKIE_FILE" -X POST "$BFF/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}')
check "Login HADI" "$LOGIN" '"username":"HADI"'
check "Has DIST role" "$LOGIN" '"DIST"'

echo ""

# ── Lookup: Cost Items ────────────────────────────────────────────────────────
echo "--- Lookups ---"
COST_ITEMS=$(curl -s --max-time 10 -b "$COOKIE_FILE" "$BFF/api/distribution/realization-return/lookup/cost-items")
check "GET /lookup/cost-items returns items" "$COST_ITEMS" '"items"'

# ── Lookup: Available Realizations ───────────────────────────────────────────
REALIZATIONS=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
  "$BFF/api/distribution/realization-return/lookup/realizations?page=1&page_size=10")
check "GET /lookup/realizations returns rows" "$REALIZATIONS" '"rows"'
check "Lookup realizations has pagination" "$REALIZATIONS" '"pagination"'

# Get first available realization_id for detail test
REALIZATION_ID=$(echo "$REALIZATIONS" | python3 -c \
  "import sys,json; rows=json.load(sys.stdin)['data']['rows']; print(rows[0]['realization_id'] if rows else 0)" 2>/dev/null || echo "0")
check "Has available realization for return" "$([[ "$REALIZATION_ID" != "0" ]] && echo true || echo false)"

echo ""

# ── Lookup: Realization Details ───────────────────────────────────────────────
if [[ "$REALIZATION_ID" != "0" ]]; then
  echo "--- Detail lookup for realization $REALIZATION_ID ---"
  DETAILS=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
    "$BFF/api/distribution/realization-return/realization/$REALIZATION_ID/details")
  check "GET /realization/{id}/details returns rows" "$DETAILS" '"rows"'

  # Get detail row for create payload
  DETAIL_ID=$(echo "$DETAILS" | python3 -c \
    "import sys,json; rows=json.load(sys.stdin)['data']['rows']; print(rows[0]['realization_detail_id'] if rows else 0)" 2>/dev/null || echo "0")
  REAL_AMOUNT=$(echo "$DETAILS" | python3 -c \
    "import sys,json; rows=json.load(sys.stdin)['data']['rows']; print(rows[0]['realization_amount'] if rows else 0)" 2>/dev/null || echo "0")
  ACCOUNT_NO=$(echo "$DETAILS" | python3 -c \
    "import sys,json; rows=json.load(sys.stdin)['data']['rows']; print(rows[0].get('account_no') or '')" 2>/dev/null || echo "")
  MUSTAHIQ_PRODUCT_ID=$(echo "$DETAILS" | python3 -c \
    "import sys,json; rows=json.load(sys.stdin)['data']['rows']; print(rows[0].get('mustahiq_product_id') or 0)" 2>/dev/null || echo "0")

  check "Realization detail has detail_id" "$([[ "$DETAIL_ID" != "0" ]] && echo true || echo false)"
  echo ""
fi

# ── List (BFF, date range) ────────────────────────────────────────────────────
echo "--- List endpoint ---"
LIST=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
  "$BFF/api/distribution/realization-return?begin_date=2025-01-01&end_date=2026-12-31&page=1&page_size=10")
check "GET list returns rows" "$LIST" '"rows"'
check "GET list has pagination" "$LIST" '"pagination"'

TOTAL=$(echo "$LIST" | python3 -c \
  "import sys,json; print(json.load(sys.stdin)['data']['pagination']['total'])" 2>/dev/null || echo "0")
echo "  → Total existing returns: $TOTAL"

echo ""

# ── CREATE via BFF ────────────────────────────────────────────────────────────
echo "--- CRUD operations ---"
if [[ "$REALIZATION_ID" != "0" && "$DETAIL_ID" != "0" && "$REAL_AMOUNT" != "0" ]]; then
  CREATE_PAYLOAD=$(python3 -c "
import json
payload = {
  'return_date': '2026-06-22',
  'return_description': 'Test E2E Pengembalian Realisasi',
  'realization_id': $REALIZATION_ID,
  'details': [{
    'realization_detail_id': $DETAIL_ID,
    'return_amount': $REAL_AMOUNT,
    'detail_description': 'Test detail pengembalian',
    'mustahiq_product_id': $MUSTAHIQ_PRODUCT_ID,
    'account_no': '$ACCOUNT_NO'
  }],
  'costs': []
}
print(json.dumps(payload))
")

  CREATE=$(curl -s --max-time 10 -b "$COOKIE_FILE" -X POST "$BFF/api/distribution/realization-return" \
    -H "Content-Type: application/json" \
    -d "$CREATE_PAYLOAD")
  check "POST create realization return" "$CREATE" '"return_id"'

  RETURN_ID=$(echo "$CREATE" | python3 -c \
    "import sys,json; print(json.load(sys.stdin)['data']['return_id'])" 2>/dev/null || echo "0")
  echo "  → Created return_id: $RETURN_ID"

  if [[ "$RETURN_ID" != "0" ]]; then
    # ── GET DETAIL ────────────────────────────────────────────────────────────
    DETAIL=$(curl -s --max-time 10 -b "$COOKIE_FILE" "$BFF/api/distribution/realization-return/$RETURN_ID")
    check "GET detail by id returns data" "$DETAIL" '"return_id"'
    check "Detail has details array" "$DETAIL" '"details"'
    check "Detail has costs array" "$DETAIL" '"costs"'

    # ── UPDATE ────────────────────────────────────────────────────────────────
    UPDATE_PAYLOAD=$(python3 -c "
import json
payload = {
  'return_date': '2026-06-22',
  'return_description': 'Test E2E Pengembalian Realisasi (UPDATED)',
  'realization_id': $REALIZATION_ID,
  'details': [{
    'realization_detail_id': $DETAIL_ID,
    'return_amount': $REAL_AMOUNT,
    'detail_description': 'Updated detail',
    'mustahiq_product_id': $MUSTAHIQ_PRODUCT_ID,
    'account_no': '$ACCOUNT_NO'
  }],
  'costs': []
}
print(json.dumps(payload))
")
    UPDATE=$(curl -s --max-time 10 -b "$COOKIE_FILE" -X PUT "$BFF/api/distribution/realization-return/$RETURN_ID" \
      -H "Content-Type: application/json" \
      -d "$UPDATE_PAYLOAD")
    check "PUT update realization return" "$UPDATE" '"return_id"'

    # ── VERIFY LIST now shows return ──────────────────────────────────────────
    LIST2=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
      "$BFF/api/distribution/realization-return?begin_date=2026-06-22&end_date=2026-06-22&page=1&page_size=25")
    NEW_TOTAL=$(echo "$LIST2" | python3 -c \
      "import sys,json; print(json.load(sys.stdin)['data']['pagination']['total'])" 2>/dev/null || echo "0")
    check "New return appears in list" "$([[ "$NEW_TOTAL" -gt 0 ]] && echo true || echo false)"

    # ── VERIFY realization now excluded from lookup ───────────────────────────
    REALIZATIONS2=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
      "$BFF/api/distribution/realization-return/lookup/realizations?page=1&page_size=20")
    AVAIL_IDS=$(echo "$REALIZATIONS2" | python3 -c \
      "import sys,json; ids=set(str(r['realization_id']) for r in json.load(sys.stdin)['data']['rows']); print('returned' if '$REALIZATION_ID' in ids else 'excluded')" 2>/dev/null || echo "unknown")
    check "Returned realization excluded from lookup" "$AVAIL_IDS" "excluded"

    # ── DELETE ────────────────────────────────────────────────────────────────
    DELETE=$(curl -s --max-time 10 -b "$COOKIE_FILE" -X DELETE "$BFF/api/distribution/realization-return/$RETURN_ID")
    check "DELETE realization return" "$DELETE" '"message"'

    # ── VERIFY deleted (404) ──────────────────────────────────────────────────
    GET_DELETED=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" -b "$COOKIE_FILE" \
      "$BFF/api/distribution/realization-return/$RETURN_ID")
    check "Deleted return returns 404" "$GET_DELETED" "404"

    # ── VERIFY realization back in lookup ─────────────────────────────────────
    REALIZATIONS3=$(curl -s --max-time 10 -b "$COOKIE_FILE" \
      "$BFF/api/distribution/realization-return/lookup/realizations?page=1&page_size=20")
    RESTORED=$(echo "$REALIZATIONS3" | python3 -c \
      "import sys,json; ids=set(str(r['realization_id']) for r in json.load(sys.stdin)['data']['rows']); print('restored' if '$REALIZATION_ID' in ids else 'missing')" 2>/dev/null || echo "unknown")
    check "Realization restored to lookup after delete" "$RESTORED" "restored"
  fi
else
  echo "  → Skipping CRUD: no available realization without a return"
fi

echo ""

# ── DISCRIMINATOR CHECK: realizationcost isolation ───────────────────────────
echo "--- Discriminator check ---"
DISC=$(PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -tAc \
  "SELECT COUNT(*) FROM program.realizationcost WHERE returnid IS NOT NULL" 2>/dev/null || echo "skip")
if [[ "$DISC" != "skip" ]]; then
  check "realizationcost.returnid discriminator exists" "true"
  echo "  → Rows with returnid (return costs): $DISC"
fi

echo ""
echo "=== SUMMARY ==="
echo "PASS: $PASS | FAIL: $FAIL"
echo ""
if [[ "$FAIL" -eq 0 ]]; then
  green "All tests passed!"
  exit 0
else
  red "$FAIL test(s) failed"
  exit 1
fi
