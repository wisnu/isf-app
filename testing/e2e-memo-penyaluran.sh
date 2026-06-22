#!/usr/bin/env bash
# E2E Smoke Test: Memo Penyaluran (Rutin + Non Rutin)
# Portal: Zakat — BFF :7000
# Requires: curl, jq
# Dev user: HADI (DIST/SPVDIST) — password: test1234
set -euo pipefail

BFF="http://localhost:7000"
COOKIE_JAR=$(mktemp)
MEMO_ID_REGULAR=""
MEMO_ID_NON_REGULAR=""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; rm -f "$COOKIE_JAR"; exit 1; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

bff_get()  { curl -sf -b "$COOKIE_JAR" "$BFF$1" "${@:2}"; }
bff_post() { curl -sf -b "$COOKIE_JAR" -X POST -H "Content-Type: application/json" -d "$2" "$BFF$1"; }
bff_put()  { curl -sf -b "$COOKIE_JAR" -X PUT  -H "Content-Type: application/json" -d "$2" "$BFF$1"; }
bff_del()  { curl -sf -b "$COOKIE_JAR" -X DELETE "$BFF$1"; }

# ── 0. Health ─────────────────────────────────────────────────────────────────
info "Health checks..."
bff_get /health | jq -e '.data.status == "ok"' > /dev/null && ok "BFF health" || fail "BFF unreachable"

# ── 1. Login ──────────────────────────────────────────────────────────────────
info "Login as HADI (DIST/SPVDIST)..."
LOGIN=$(curl -sf -c "$COOKIE_JAR" -X POST "$BFF/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}')
echo "$LOGIN" | jq -e '.data.user.username' > /dev/null && ok "Login HADI" || fail "Login failed: $LOGIN"

# verify memo menus exist in session
echo "$LOGIN" | jq -e '.data.user.menus | contains(["distribution.program.memo-regular","distribution.program.memo-non-regular"])' > /dev/null \
  && ok "Memo menu keys in session" || fail "Memo menu keys not found in session"

# ── 2. Lookup programs (regular) ──────────────────────────────────────────────
info "Lookup programs rutin..."
PROG=$(bff_get "/api/distribution/realization-memo/regular/lookup/programs?search=")
echo "$PROG" | jq -e '.data.data | type == "array"' > /dev/null && ok "Lookup regular programs (array)" || fail "Lookup failed: $PROG"
PROG_ID=$(echo "$PROG" | jq -r '.data.data[0].mustahiq_product_id // empty')
info "First regular program_id: ${PROG_ID:-none}"

# ── 3. Create Regular Memo ────────────────────────────────────────────────────
if [ -n "$PROG_ID" ]; then
  info "Create Memo Penyaluran Rutin..."
  CREATE=$(bff_post "/api/distribution/realization-memo/regular" \
    "{\"memo_number\":\"TEST-R/00001/2026\",\"memo_subject\":\"E2E Test Memo Rutin\",\"memo_from\":\"Unit Test Sender\",\"memo_to\":\"Unit Test Recipient\",\"memo_date\":\"2026-06-22\",\"details\":[{\"mustahiq_product_id\":$PROG_ID,\"amount\":1500000}]}")
  MEMO_ID_REGULAR=$(echo "$CREATE" | jq -r '.data.memo_id // empty')
  [ -n "$MEMO_ID_REGULAR" ] && ok "Create regular memo (id=$MEMO_ID_REGULAR)" || fail "Create failed: $CREATE"
else
  info "Skip create regular memo — no programs available"
fi

# ── 4. List Regular Memos ─────────────────────────────────────────────────────
info "List Memo Rutin..."
LIST=$(bff_get "/api/distribution/realization-memo/regular?page=1&page_size=10")
echo "$LIST" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List regular memos" || fail "List failed: $LIST"
TOTAL=$(echo "$LIST" | jq -r '.data.pagination.total')
info "Total regular memos: $TOTAL"

# ── 5. Get Detail Regular Memo ────────────────────────────────────────────────
if [ -n "$MEMO_ID_REGULAR" ]; then
  info "Get detail memo $MEMO_ID_REGULAR..."
  DETAIL=$(bff_get "/api/distribution/realization-memo/regular/$MEMO_ID_REGULAR")
  echo "$DETAIL" | jq -e '.data.memo_id' > /dev/null && ok "Get regular memo detail" || fail "Get detail failed: $DETAIL"
  echo "$DETAIL" | jq -e '.data.details | length >= 1' > /dev/null && ok "Detail has items" || fail "Detail empty"
fi

# ── 6. Update Regular Memo ────────────────────────────────────────────────────
if [ -n "$MEMO_ID_REGULAR" ] && [ -n "$PROG_ID" ]; then
  info "Update Memo Rutin $MEMO_ID_REGULAR..."
  UPDATE=$(bff_put "/api/distribution/realization-memo/regular/$MEMO_ID_REGULAR" \
    "{\"memo_number\":\"TEST-R/00001/2026\",\"memo_subject\":\"E2E Test Memo Rutin (Updated)\",\"memo_from\":\"Sender Updated\",\"memo_to\":\"Recipient Updated\",\"memo_date\":\"2026-06-22\",\"details\":[{\"mustahiq_product_id\":$PROG_ID,\"amount\":2000000}]}")
  echo "$UPDATE" | jq -e '.data.memo_id' > /dev/null && ok "Update regular memo" || fail "Update failed: $UPDATE"
fi

# ── 7. Lookup programs (non-regular) ─────────────────────────────────────────
info "Lookup programs non rutin..."
PROG_NR=$(bff_get "/api/distribution/realization-memo/non-regular/lookup/programs?search=")
echo "$PROG_NR" | jq -e '.data.data | type == "array"' > /dev/null && ok "Lookup non-regular programs" || fail "Lookup NR failed: $PROG_NR"
PROG_NR_ID=$(echo "$PROG_NR" | jq -r '.data.data[0].mustahiq_product_id // empty')
info "First non-regular program_id: ${PROG_NR_ID:-none}"

# ── 8. Create Non-Regular Memo ────────────────────────────────────────────────
if [ -n "$PROG_NR_ID" ]; then
  info "Create Memo Penyaluran Non Rutin..."
  CREATE_NR=$(bff_post "/api/distribution/realization-memo/non-regular" \
    "{\"memo_number\":\"TEST-N/00001/2026\",\"memo_subject\":\"E2E Test Memo Non Rutin\",\"memo_from\":\"Sender NR\",\"memo_to\":\"Recipient NR\",\"memo_date\":\"2026-06-22\",\"details\":[{\"mustahiq_product_id\":$PROG_NR_ID,\"amount\":500000}]}")
  MEMO_ID_NON_REGULAR=$(echo "$CREATE_NR" | jq -r '.data.memo_id // empty')
  [ -n "$MEMO_ID_NON_REGULAR" ] && ok "Create non-regular memo (id=$MEMO_ID_NON_REGULAR)" || fail "Create NR failed: $CREATE_NR"
else
  info "Skip create non-regular memo — no programs available"
fi

# ── 9. List Non-Regular Memos ─────────────────────────────────────────────────
info "List Memo Non Rutin..."
LIST_NR=$(bff_get "/api/distribution/realization-memo/non-regular?page=1&page_size=10")
echo "$LIST_NR" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List non-regular memos" || fail "List NR failed: $LIST_NR"

# ── 10. Get Detail Non-Regular Memo ──────────────────────────────────────────
if [ -n "$MEMO_ID_NON_REGULAR" ]; then
  info "Get detail non-regular memo $MEMO_ID_NON_REGULAR..."
  DETAIL_NR=$(bff_get "/api/distribution/realization-memo/non-regular/$MEMO_ID_NON_REGULAR")
  echo "$DETAIL_NR" | jq -e '.data.memo_id' > /dev/null && ok "Get non-regular memo detail" || fail "Get NR detail failed: $DETAIL_NR"
fi

# ── 11. Delete Test Data ──────────────────────────────────────────────────────
if [ -n "$MEMO_ID_REGULAR" ]; then
  info "Delete regular memo $MEMO_ID_REGULAR..."
  DEL=$(bff_del "/api/distribution/realization-memo/regular/$MEMO_ID_REGULAR")
  echo "$DEL" | jq -e '.data.memo_id' > /dev/null && ok "Delete regular memo" || fail "Delete failed: $DEL"
fi

if [ -n "$MEMO_ID_NON_REGULAR" ]; then
  info "Delete non-regular memo $MEMO_ID_NON_REGULAR..."
  DEL_NR=$(bff_del "/api/distribution/realization-memo/non-regular/$MEMO_ID_NON_REGULAR")
  echo "$DEL_NR" | jq -e '.data.memo_id' > /dev/null && ok "Delete non-regular memo" || fail "Delete NR failed: $DEL_NR"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
rm -f "$COOKIE_JAR"
echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN} E2E Memo Penyaluran — SEMUA LULUS ✓    ${NC}"
echo -e "${GREEN}==========================================${NC}"
