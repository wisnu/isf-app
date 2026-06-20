#!/usr/bin/env bash
# E2E Test: Penerimaan Amil (CI - Cash In Amil)
# Flow: login → lookups → save-and-submit → list → detail → verify discriminators
# Prereqs:
#   - isf-app zakat running: bff-api :7000, api-python :8000
#   - seed applied: seed-menu-amil-income.sql (isf_auth_zakat) + seed-entity-config-amil-income.sql (mziss_laz)
#   - ACC dev user RAIS / test1234 (branch 001) in isf_auth_zakat
# Date: 2026-06-20

set -euo pipefail

BFF_API="${BFF_API:-http://localhost:7000}"
API_PYTHON="${API_PYTHON:-http://localhost:8000}"
USERNAME="${USERNAME:-RAIS}"
PASSWORD="${PASSWORD:-test1234}"
JAR="$(mktemp)"
trap 'rm -f "$JAR"' EXIT

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${YELLOW}[..]${NC} $1"; }
die()  { echo -e "${RED}[ERR]${NC} $1"; exit 1; }

# === 1. Health ===
info "health check"
curl -sf "$BFF_API/health" >/dev/null || die "BFF not reachable at $BFF_API"
curl -sf "$API_PYTHON/health" >/dev/null || die "api-python not reachable at $API_PYTHON"
ok "services reachable"

# === 2. Login (cookie session) ===
info "login as $USERNAME"
curl -sf -c "$JAR" -X POST "$BFF_API/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" >/dev/null \
  || die "login failed for $USERNAME"
ok "logged in"

# === 3. Lookup: amil cash/bank accounts (isamilaccount='T') ===
info "lookup kas-account"
KAS=$(curl -sf -b "$JAR" "$BFF_API/api/amil-income/lookup/kas-account")
echo "$KAS" | grep -q '"account_no"' || die "kas-account lookup empty/invalid: $KAS"
DEST_ACC=$(echo "$KAS" | grep -o '"account_no":"[^"]*"' | head -1 | cut -d'"' -f4)
ok "kas-account ok (dest=$DEST_ACC)"

# === 4. Lookup: amil revenue GL accounts (430xxx) ===
info "lookup gl-account"
GL=$(curl -sf -b "$JAR" "$BFF_API/api/amil-income/lookup/gl-account?search=amil")
echo "$GL" | grep -q '"account_code"' || die "gl-account lookup empty/invalid: $GL"
GL_ACC=$(echo "$GL" | grep -o '"account_code":"43[^"]*"' | head -1 | cut -d'"' -f4)
[ -n "$GL_ACC" ] || die "no 430xxx amil revenue account returned"
ok "gl-account ok (income=$GL_ACC)"

# === 5. Create via save-and-submit ===
info "POST save-and-submit"
CREATE=$(curl -sf -b "$JAR" -X POST "$BFF_API/api/amil-income/save-and-submit" \
  -H 'Content-Type: application/json' \
  -d "{
    \"actual_date\": \"2026-06-20\",
    \"payment_type\": \"B\",
    \"bank_account_no\": \"$DEST_ACC\",
    \"reference_no\": \"E2E-AMIL-001\",
    \"paid_to\": \"$USERNAME\",
    \"received_from\": \"E2E TEST\",
    \"description\": \"E2E penerimaan amil\",
    \"rate\": 1.0,
    \"items\": [
      { \"account_code\": \"$GL_ACC\", \"account_name\": \"E2E\", \"amount\": 100000, \"description\": \"ujroh e2e\" }
    ]
  }")
echo "$CREATE" | grep -qE '"status":"(PENDING|AUTHORIZED)"' || die "create did not return PENDING/AUTHORIZED: $CREATE"
STATUS=$(echo "$CREATE" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
TXID=$(echo "$CREATE" | grep -o '"transaction_id":[0-9]*' | head -1 | cut -d: -f2)
ok "submitted (status=$STATUS, transaction_id=${TXID:-none})"

# === 6. List ===
info "GET list"
LIST=$(curl -sf -b "$JAR" "$BFF_API/api/amil-income/?page=1&limit=25&date_from=2026-06-20&date_to=2026-06-20")
echo "$LIST" | grep -q '"pagination"' || die "list missing pagination: $LIST"
ok "list ok"

# === 7. Detail + discriminator check (only if auto-authorized into transaction table) ===
if [ -n "${TXID:-}" ] && [ "$TXID" != "null" ]; then
  info "GET detail $TXID"
  DETAIL=$(curl -sf -b "$JAR" "$BFF_API/api/amil-income/$TXID")
  echo "$DETAIL" | grep -q "$GL_ACC" || die "detail missing income account $GL_ACC: $DETAIL"
  ok "detail ok (income account present)"
else
  info "status=$STATUS (PENDING) — approve di halaman Otorisasi untuk uji dispatcher 3-leg"
fi

echo -e "${GREEN}=== E2E amil-income PASSED ===${NC}"
