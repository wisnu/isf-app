#!/usr/bin/env bash
# E2E Smoke Test: Realisasi Program Penyaluran (Rutin + Non Rutin)
# Portal: Zakat — BFF :7000
# Requires: curl, jq
# Dev user: HADI (DIST/SPVDIST) — password: test1234
set -euo pipefail

BFF="http://localhost:7000"
COOKIE_JAR=$(mktemp)
REALIZATION_ID_REGULAR=""
REALIZATION_ID_NON_REGULAR=""
MEMO_ID_REGULAR=""
MEMO_ID_NON_REGULAR=""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; rm -f "$COOKIE_JAR"; exit 1; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

bff_get()  { curl -sf -b "$COOKIE_JAR" "$BFF$1" "${@:2}"; }
bff_post() { curl -sf -b "$COOKIE_JAR" -X POST -H "Content-Type: application/json" -d "$2" "$BFF$1"; }
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

# verify realization menus exist in session
echo "$LOGIN" | jq -e '.data.user.menus | contains(["distribution.realization.regular.list","distribution.realization.non-regular.list"])' > /dev/null \
  && ok "Realization menu keys in session" || fail "Realization menu keys not found in session"

# ── 2. Lookup memos (regular) ─────────────────────────────────────────────────
info "Lookup memos rutin..."
MEMOS=$(bff_get "/api/distribution/realization/regular/lookup/memos?search=")
echo "$MEMOS" | jq -e '.data.data | type == "array"' > /dev/null && ok "Lookup regular memos (array)" || fail "Lookup failed: $MEMOS"
MEMO_ID_REGULAR=$(echo "$MEMOS" | jq -r '.data.data[0].realization_memo_id // empty')
info "First regular memo_id: ${MEMO_ID_REGULAR:-none}"

# ── 3. Get memo detail (regular) ──────────────────────────────────────────────
if [ -n "$MEMO_ID_REGULAR" ]; then
  info "Get memo detail for regular $MEMO_ID_REGULAR..."
  MEMO_DETAIL=$(bff_get "/api/distribution/realization/regular/lookup/memo-detail/$MEMO_ID_REGULAR")
  echo "$MEMO_DETAIL" | jq -e '.data.data | type == "array"' > /dev/null && ok "Get regular memo detail" || fail "Memo detail failed: $MEMO_DETAIL"
  DETAIL_ID=$(echo "$MEMO_DETAIL" | jq -r '.data.data[0].mustahiq_product_id // empty')
  info "First detail mustahiq_product_id: ${DETAIL_ID:-none}"
fi

# ── 4. List Regular Realizations ──────────────────────────────────────────────
info "List Realisasi Rutin..."
LIST=$(bff_get "/api/distribution/realization/regular?date_from=2015-01-01&date_to=2026-12-31&page=1&page_size=5")
echo "$LIST" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List regular realizations" || fail "List failed: $LIST"
TOTAL=$(echo "$LIST" | jq -r '.data.pagination.total')
info "Total regular realizations: $TOTAL"

# ── 5. Create Regular Realization ─────────────────────────────────────────────
if [ -n "$MEMO_ID_REGULAR" ] && [ -n "$DETAIL_ID" ]; then
  info "Create Realisasi Penyaluran Rutin..."
  CREATE=$(bff_post "/api/distribution/realization/regular" \
    "{\"realization_date\":\"2026-06-22\",\"description\":\"Test Realisasi E2E\",\"location\":\"Kantor Pusat\",\"memo_id\":$MEMO_ID_REGULAR,\"status_receivables\":\"T\",\"details\":[{\"mustahiq_product_id\":$DETAIL_ID,\"realization_amount\":100000,\"detail_description\":\"test\"}],\"budgets\":null,\"partners\":null}")
  REALIZATION_ID_REGULAR=$(echo "$CREATE" | jq -r '.data.realization_id // empty')
  [ -n "$REALIZATION_ID_REGULAR" ] && ok "Create regular realization (id=$REALIZATION_ID_REGULAR)" || fail "Create failed: $CREATE"
else
  info "Skip create regular realization — no memo/detail available"
fi

# ── 6. Get Detail Regular Realization ─────────────────────────────────────────
if [ -n "$REALIZATION_ID_REGULAR" ]; then
  info "Get detail realization $REALIZATION_ID_REGULAR..."
  DETAIL=$(bff_get "/api/distribution/realization/regular/$REALIZATION_ID_REGULAR")
  echo "$DETAIL" | jq -e '.data.realization_id' > /dev/null && ok "Get regular realization detail" || fail "Get detail failed: $DETAIL"
fi

# ── 7. Lookup memos (non-regular) ─────────────────────────────────────────────
info "Lookup memos non rutin..."
MEMOS_NR=$(bff_get "/api/distribution/realization/non-regular/lookup/memos?search=")
echo "$MEMOS_NR" | jq -e '.data.data | type == "array"' > /dev/null && ok "Lookup non-regular memos" || fail "Lookup NR failed: $MEMOS_NR"
MEMO_ID_NON_REGULAR=$(echo "$MEMOS_NR" | jq -r '.data.data[0].realization_memo_id // empty')
info "First non-regular memo_id: ${MEMO_ID_NON_REGULAR:-none}"

# ── 8. Get memo detail (non-regular) ──────────────────────────────────────────
if [ -n "$MEMO_ID_NON_REGULAR" ]; then
  info "Get memo detail for non-regular $MEMO_ID_NON_REGULAR..."
  MEMO_DETAIL_NR=$(bff_get "/api/distribution/realization/non-regular/lookup/memo-detail/$MEMO_ID_NON_REGULAR")
  echo "$MEMO_DETAIL_NR" | jq -e '.data.data | type == "array"' > /dev/null && ok "Get non-regular memo detail" || fail "NR memo detail failed: $MEMO_DETAIL_NR"
  DETAIL_ID_NR=$(echo "$MEMO_DETAIL_NR" | jq -r '.data.data[0].mustahiq_product_id // empty')
  info "First detail mustahiq_product_id: ${DETAIL_ID_NR:-none}"
fi

# ── 9. List Non-Regular Realizations ──────────────────────────────────────────
info "List Realisasi Non Rutin..."
LIST_NR=$(bff_get "/api/distribution/realization/non-regular?date_from=2015-01-01&date_to=2026-12-31&page=1&page_size=5")
echo "$LIST_NR" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List non-regular realizations" || fail "List NR failed: $LIST_NR"
TOTAL_NR=$(echo "$LIST_NR" | jq -r '.data.pagination.total')
info "Total non-regular realizations: $TOTAL_NR"

# ── 10. Create Non-Regular Realization ────────────────────────────────────────
if [ -n "$MEMO_ID_NON_REGULAR" ] && [ -n "$DETAIL_ID_NR" ]; then
  info "Create Realisasi Penyaluran Non Rutin..."
  CREATE_NR=$(bff_post "/api/distribution/realization/non-regular" \
    "{\"realization_date\":\"2026-06-22\",\"description\":\"Test Realisasi Non Rutin E2E\",\"location\":\"Lapangan\",\"memo_id\":$MEMO_ID_NON_REGULAR,\"status_receivables\":\"T\",\"details\":[{\"mustahiq_product_id\":$DETAIL_ID_NR,\"realization_amount\":50000,\"detail_description\":\"test non rutin\"}],\"budgets\":null,\"partners\":null}")
  REALIZATION_ID_NON_REGULAR=$(echo "$CREATE_NR" | jq -r '.data.realization_id // empty')
  [ -n "$REALIZATION_ID_NON_REGULAR" ] && ok "Create non-regular realization (id=$REALIZATION_ID_NON_REGULAR)" || fail "Create NR failed: $CREATE_NR"
else
  info "Skip create non-regular realization — no memo/detail available"
fi

# ── 11. Get Detail Non-Regular Realization ────────────────────────────────────
if [ -n "$REALIZATION_ID_NON_REGULAR" ]; then
  info "Get detail non-regular realization $REALIZATION_ID_NON_REGULAR..."
  DETAIL_NR=$(bff_get "/api/distribution/realization/non-regular/$REALIZATION_ID_NON_REGULAR")
  echo "$DETAIL_NR" | jq -e '.data.realization_id' > /dev/null && ok "Get non-regular realization detail" || fail "Get NR detail failed: $DETAIL_NR"
fi

# ── 12. Delete Test Data ──────────────────────────────────────────────────────
if [ -n "$REALIZATION_ID_REGULAR" ]; then
  info "Delete regular realization $REALIZATION_ID_REGULAR..."
  DEL=$(bff_del "/api/distribution/realization/regular/$REALIZATION_ID_REGULAR")
  echo "$DEL" | jq -e '.data.realization_id' > /dev/null && ok "Delete regular realization" || fail "Delete failed: $DEL"
fi

if [ -n "$REALIZATION_ID_NON_REGULAR" ]; then
  info "Delete non-regular realization $REALIZATION_ID_NON_REGULAR..."
  DEL_NR=$(bff_del "/api/distribution/realization/non-regular/$REALIZATION_ID_NON_REGULAR")
  echo "$DEL_NR" | jq -e '.data.realization_id' > /dev/null && ok "Delete non-regular realization" || fail "Delete NR failed: $DEL_NR"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
rm -f "$COOKIE_JAR"
echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN} E2E Realisasi Program — SEMUA LULUS ✓  ${NC}"
echo -e "${GREEN}==========================================${NC}"
