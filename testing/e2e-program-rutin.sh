#!/usr/bin/env bash
# E2E smoke test: Program Rutin (Regular Distribution Program)
# Target: api-python :8000 via bff-api :7000
# Usage: bash testing/e2e-program-rutin.sh [BFF_BASE]
set -euo pipefail

BFF="${1:-http://localhost:7000}"
API="${2:-http://localhost:8000}"
COOKIE_JAR=$(mktemp)
trap "rm -f $COOKIE_JAR" EXIT

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
PASS=0; FAIL=0

check() {
  local label="$1" status="$2" body="$3" expect_key="${4:-}"
  if [[ "$status" -ge 200 && "$status" -lt 300 ]]; then
    if [[ -n "$expect_key" ]] && ! echo "$body" | grep -q "$expect_key"; then
      echo -e "${RED}FAIL${NC} $label — missing '$expect_key' in response"
      echo "  body: $body" | head -c 300
      FAIL=$((FAIL+1))
    else
      echo -e "${GREEN}PASS${NC} $label (HTTP $status)"
      PASS=$((PASS+1))
    fi
  else
    echo -e "${RED}FAIL${NC} $label — HTTP $status"
    echo "  body: $body" | head -c 300
    FAIL=$((FAIL+1))
  fi
}

# ── Login (get session cookie) ─────────────────────────────────────────────

echo -e "\n${YELLOW}=== Auth ===${NC}"
LOGIN=$(curl -s -w "\n%{http_code}" -c "$COOKIE_JAR" -X POST "$BFF/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}')
LOGIN_BODY=$(echo "$LOGIN" | head -n -1)
LOGIN_STATUS=$(echo "$LOGIN" | tail -1)
check "Login HADI" "$LOGIN_STATUS" "$LOGIN_BODY" "access_token"

# ── Direct api-python tests (no auth required at this layer) ───────────────

echo -e "\n${YELLOW}=== api-python: Lookups ===${NC}"

PROD_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program/lookup/products")
PROD_BODY=$(echo "$PROD_RES" | head -n -1)
PROD_STATUS=$(echo "$PROD_RES" | tail -1)
check "GET /api/distribution/regular-program/lookup/products" "$PROD_STATUS" "$PROD_BODY" '"data"'

MUST_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program/lookup/mustahiq?search=yayasan")
MUST_BODY=$(echo "$MUST_RES" | head -n -1)
MUST_STATUS=$(echo "$MUST_RES" | tail -1)
check "GET /api/distribution/regular-program/lookup/mustahiq?search=yayasan" "$MUST_STATUS" "$MUST_BODY" '"data"'

echo -e "\n${YELLOW}=== api-python: List ===${NC}"

LIST_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program?page=1&page_size=5")
LIST_BODY=$(echo "$LIST_RES" | head -n -1)
LIST_STATUS=$(echo "$LIST_RES" | tail -1)
check "GET /api/distribution/regular-program (list)" "$LIST_STATUS" "$LIST_BODY" '"rows"'
check "List has pagination" "$LIST_STATUS" "$LIST_BODY" '"pagination"'

echo -e "\n${YELLOW}=== api-python: List with filters ===${NC}"

FILT_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program?page=1&page_size=5&date_from=2025-01-01&date_to=2026-12-31")
FILT_BODY=$(echo "$FILT_RES" | head -n -1)
FILT_STATUS=$(echo "$FILT_RES" | tail -1)
check "GET regular-program with date filter" "$FILT_STATUS" "$FILT_BODY" '"rows"'

# ── Get an existing record for CRUD test ──────────────────────────────────

PROG_ID=$(echo "$LIST_BODY" | grep -o '"program_id":[0-9]*' | head -1 | grep -o '[0-9]*' || echo "")
MUST_ID=$(echo "$LIST_BODY" | grep -o '"mustahiq_id":[0-9]*' | head -1 | grep -o '[0-9]*' || echo "")
PROD_ID=$(echo "$LIST_BODY" | grep -o '"product_id":[0-9]*' | head -1 | grep -o '[0-9]*' || echo "")

if [[ -n "$PROG_ID" ]]; then
  echo -e "\n${YELLOW}=== api-python: Detail ===${NC}"
  DET_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program/$PROG_ID")
  DET_BODY=$(echo "$DET_RES" | head -n -1)
  DET_STATUS=$(echo "$DET_RES" | tail -1)
  check "GET /api/distribution/regular-program/$PROG_ID" "$DET_STATUS" "$DET_BODY" '"program_id"'
fi

echo -e "\n${YELLOW}=== api-python: Create → Detail → Update → Delete ===${NC}"

if [[ -n "$MUST_ID" && -n "$PROD_ID" ]]; then
  # Create
  CREATE_RES=$(curl -s -w "\n%{http_code}" -X POST "$API/api/distribution/regular-program" \
    -H "Content-Type: application/json" \
    -d "{\"mustahiq_id\":$MUST_ID,\"product_id\":$PROD_ID,\"program_detail_name\":\"E2E Test Program Rutin\",\"distribution_amount\":1200000,\"date_start\":\"2026-01-01\",\"date_end\":\"2026-12-31\"}")
  CREATE_BODY=$(echo "$CREATE_RES" | head -n -1)
  CREATE_STATUS=$(echo "$CREATE_RES" | tail -1)
  check "POST /api/distribution/regular-program (create)" "$CREATE_STATUS" "$CREATE_BODY" '"program_id"'

  NEW_ID=$(echo "$CREATE_BODY" | grep -o '"program_id":[0-9]*' | grep -o '[0-9]*' || echo "")

  if [[ -n "$NEW_ID" ]]; then
    # Detail
    DET2_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program/$NEW_ID")
    DET2_BODY=$(echo "$DET2_RES" | head -n -1)
    DET2_STATUS=$(echo "$DET2_RES" | tail -1)
    check "GET created program detail" "$DET2_STATUS" "$DET2_BODY" '"E2E Test Program Rutin"'

    # Update
    UPD_RES=$(curl -s -w "\n%{http_code}" -X PUT "$API/api/distribution/regular-program/$NEW_ID" \
      -H "Content-Type: application/json" \
      -d "{\"mustahiq_id\":$MUST_ID,\"product_id\":$PROD_ID,\"program_detail_name\":\"E2E Test Updated\",\"distribution_amount\":1500000,\"date_start\":\"2026-01-01\",\"date_end\":\"2026-12-31\"}")
    UPD_BODY=$(echo "$UPD_RES" | head -n -1)
    UPD_STATUS=$(echo "$UPD_RES" | tail -1)
    check "PUT /api/distribution/regular-program/$NEW_ID (update)" "$UPD_STATUS" "$UPD_BODY" '"program_id"'

    # Delete
    DEL_RES=$(curl -s -w "\n%{http_code}" -X DELETE "$API/api/distribution/regular-program/$NEW_ID")
    DEL_BODY=$(echo "$DEL_RES" | head -n -1)
    DEL_STATUS=$(echo "$DEL_RES" | tail -1)
    check "DELETE /api/distribution/regular-program/$NEW_ID" "$DEL_STATUS" "$DEL_BODY" '"program_id"'

    # Verify gone (expect 404)
    GONE_RES=$(curl -s -w "\n%{http_code}" "$API/api/distribution/regular-program/$NEW_ID")
    GONE_STATUS=$(echo "$GONE_RES" | tail -1)
    if [[ "$GONE_STATUS" == "404" ]]; then
      echo -e "${GREEN}PASS${NC} GET deleted record returns 404"
      PASS=$((PASS+1))
    else
      echo -e "${RED}FAIL${NC} Expected 404 after delete, got $GONE_STATUS"
      FAIL=$((FAIL+1))
    fi
  fi
else
  echo -e "${YELLOW}SKIP${NC} CRUD tests — no existing mustahiq_id / product_id found in list"
fi

# ── BFF via session cookie ─────────────────────────────────────────────────

if [[ "$LOGIN_STATUS" == "200" ]]; then
  echo -e "\n${YELLOW}=== BFF: List via session ===${NC}"
  BFF_LIST=$(curl -s -w "\n%{http_code}" -b "$COOKIE_JAR" \
    "$BFF/api/distribution/regular-program?page=1&page_size=5")
  BFF_BODY=$(echo "$BFF_LIST" | head -n -1)
  BFF_STATUS=$(echo "$BFF_LIST" | tail -1)
  check "BFF GET /api/distribution/regular-program" "$BFF_STATUS" "$BFF_BODY" '"rows"'

  echo -e "\n${YELLOW}=== BFF: Lookup products ===${NC}"
  BFF_PROD=$(curl -s -w "\n%{http_code}" -b "$COOKIE_JAR" \
    "$BFF/api/distribution/regular-program/lookup/products")
  BFF_PROD_BODY=$(echo "$BFF_PROD" | head -n -1)
  BFF_PROD_STATUS=$(echo "$BFF_PROD" | tail -1)
  check "BFF GET /api/distribution/regular-program/lookup/products" "$BFF_PROD_STATUS" "$BFF_PROD_BODY" '"data"'
fi

# ── Summary ────────────────────────────────────────────────────────────────

echo -e "\n${YELLOW}=== Summary ===${NC}"
echo -e "  ${GREEN}PASS: $PASS${NC}  ${RED}FAIL: $FAIL${NC}"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
