#!/usr/bin/env bash
# E2E Smoke Test: Branch Management (Manajemen Cabang)
# Portal: zakat
# User default: YASIN (ADM role, has appadmin.branch.* menus)
# Usage: bash testing/e2e-cabang-appadmin.sh
#        BASE_URL=http://localhost:7001 bash testing/e2e-cabang-appadmin.sh  ← wakaf

set -euo pipefail

# ─── Config ──────────────────────────────────────────────────────────────────
BASE_URL="${BASE_URL:-http://localhost:7000}"
USERNAME="${TEST_USER:-YASIN}"
PASSWORD="${TEST_PASS:-test1234}"
COOKIE_JAR="/tmp/e2e-cabang-$$.jar"

# ─── Utils ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'; BOLD='\033[1m'
pass()    { echo -e "  ${GREEN}✓${NC} $1"; }
fail()    { echo -e "  ${RED}✗${NC} $1"; echo ""; exit 1; }
warn()    { echo -e "  ${YELLOW}⚠${NC} $1"; }
section() { echo -e "\n${BOLD}=== $1 ===${NC}"; }

jq_val() { python3 -c "import sys,json; print(json.load(sys.stdin)$1)" 2>/dev/null; }

# ─── Cleanup on exit ──────────────────────────────────────────────────────────
cleanup() {
  rm -f "$COOKIE_JAR"
  if [[ "${BASE_URL}" == *"7001"* ]]; then DB=mziss_wakaf; else DB=mziss_laz; fi
  PGPASSWORD=solusi psql -U transaction -h 172.200.3.15 -d "$DB" \
    -c "DELETE FROM enterprise.cabang WHERE kode_cabang='E2ETST';" 2>/dev/null || true
}
trap cleanup EXIT

# ─── Auth ─────────────────────────────────────────────────────────────────────
section "Auth"

LOGIN=$(curl -sf -c "$COOKIE_JAR" -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  || fail "BFF tidak bisa diakses di $BASE_URL")

USER_ID=$(echo "$LOGIN" | jq_val "['data']['user']['username']" || true)
[ -n "$USER_ID" ] || fail "Login gagal — cek username/password (user=$USERNAME)"
pass "Login OK: $USER_ID"

BRANCH_MENUS=$(echo "$LOGIN" | python3 -c "
import sys,json; d=json.load(sys.stdin)
menus=d.get('data',{}).get('user',{}).get('menus',[])
bm=[m for m in menus if 'branch' in m]
print(','.join(bm))" 2>/dev/null || true)
[ -n "$BRANCH_MENUS" ] || fail "User $USER_ID tidak memiliki appadmin.branch.* menus"
pass "Branch menus: $BRANCH_MENUS"

# ─── Branch: List ─────────────────────────────────────────────────────────────
section "Branch: List (active)"

LIST=$(curl -sf -b "$COOKIE_JAR" "$BASE_URL/api/appadmin/branches?page=1&limit=10&status_active=T")
TOTAL=$(echo "$LIST" | jq_val "['data']['pagination']['total']" || echo "?")
ROW_COUNT=$(echo "$LIST" | jq_val "len(['data']['rows'])" || echo "?")
pass "List OK — total=$TOTAL, rows=$ROW_COUNT"

# ─── Branch: Parents dropdown ─────────────────────────────────────────────────
section "Branch: List parent branches"

PARENTS=$(curl -sf -b "$COOKIE_JAR" "$BASE_URL/api/appadmin/branches/parents")
PARENT_COUNT=$(echo "$PARENTS" | jq_val "len(['data']['rows'])" || echo "?")
pass "Parents OK — count=$PARENT_COUNT"

# ─── Branch: Create ───────────────────────────────────────────────────────────
section "Branch: Create"

CREATE=$(curl -sf -b "$COOKIE_JAR" -X POST "$BASE_URL/api/appadmin/branches" \
  -H "Content-Type: application/json" \
  -d '{
    "branch_code": "E2ETST",
    "branch_name": "E2E Test Branch",
    "branch_type": "CP",
    "parent_branch_code": "001",
    "office_name": "Kantor Test E2E",
    "office_address": "Jl. Test E2E No. 123"
  }')
NEW_CODE=$(echo "$CREATE" | jq_val "['data']['branch_code']" || true)
[ "$NEW_CODE" = "E2ETST" ] || fail "Create gagal: $(echo $CREATE | head -c 200)"
CREATED_BY=$(echo "$CREATE" | jq_val "['data']['created_by']" || echo "?")
pass "Create OK — code=$NEW_CODE, created_by=$CREATED_BY, is_active=$(echo $CREATE | jq_val "['data']['is_active']")"

# ─── Branch: Get Detail ───────────────────────────────────────────────────────
section "Branch: Get Detail"

DETAIL=$(curl -sf -b "$COOKIE_JAR" "$BASE_URL/api/appadmin/branches/E2ETST")
DETAIL_CODE=$(echo "$DETAIL" | jq_val "['data']['branch_code']" || true)
[ "$DETAIL_CODE" = "E2ETST" ] || fail "Get detail gagal"
pass "Detail OK — code=$DETAIL_CODE, name=$(echo $DETAIL | jq_val "['data']['branch_name']")"

# ─── Branch: Update ───────────────────────────────────────────────────────────
section "Branch: Update"

UPDATE=$(curl -sf -b "$COOKIE_JAR" -X PUT "$BASE_URL/api/appadmin/branches/E2ETST" \
  -H "Content-Type: application/json" \
  -d '{"branch_name":"E2E Updated Branch","branch_type":"CP","parent_branch_code":"001","office_name":"Kantor Updated"}')
UPDATED_NAME=$(echo "$UPDATE" | jq_val "['data']['branch_name']" || true)
[ "$UPDATED_NAME" = "E2E Updated Branch" ] || fail "Update gagal"
pass "Update OK — name=$UPDATED_NAME"

# ─── Branch: Deactivate ───────────────────────────────────────────────────────
section "Branch: Deactivate"

DEACTIVATE=$(curl -sf -b "$COOKIE_JAR" -X PATCH "$BASE_URL/api/appadmin/branches/E2ETST/deactivate" \
  -H "Content-Type: application/json" -d '{}')
IS_ACTIVE=$(echo "$DEACTIVATE" | jq_val "['data']['is_active']" || true)
[ "$IS_ACTIVE" = "False" ] || fail "Deactivate gagal — is_active=$IS_ACTIVE"
pass "Deactivate OK — is_active=False"

# ─── Branch: Activate ─────────────────────────────────────────────────────────
section "Branch: Activate"

ACTIVATE=$(curl -sf -b "$COOKIE_JAR" -X PATCH "$BASE_URL/api/appadmin/branches/E2ETST/activate" \
  -H "Content-Type: application/json" -d '{}')
IS_ACTIVE=$(echo "$ACTIVATE" | jq_val "['data']['is_active']" || true)
[ "$IS_ACTIVE" = "True" ] || fail "Activate gagal — is_active=$IS_ACTIVE"
pass "Activate OK — is_active=True"

# ─── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║  Semua E2E tests PASSED ✓             ║${NC}"
echo -e "${GREEN}${BOLD}║  Fitur: Branch Management            ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""
echo "  ✓ Login (appadmin.branch.* menus)"
echo "  ✓ List branches (filter status_active=T)"
echo "  ✓ List parent branches (dropdown)"
echo "  ✓ Create branch E2ETST (user_input dari session)"
echo "  ✓ Get branch detail"
echo "  ✓ Update branch (nama + office)"
echo "  ✓ Deactivate (is_active=False)"
echo "  ✓ Activate (is_active=True)"
echo "  ✓ Cleanup: E2ETST deleted"
