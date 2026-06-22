#!/usr/bin/env bash
# E2E Smoke Test: Monitoring Program Penyaluran (Kunjungan Mustahiq)
# Portal: Zakat — BFF :7000
# Requires: curl, jq
# Dev user: HADI (DIST/SPVDIST) — password: test1234
set -euo pipefail

BFF="http://localhost:7000"
COOKIE_JAR=$(mktemp)
VISIT_ID=""
MUSTAHIQ_ID=""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; rm -f "$COOKIE_JAR"; exit 1; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }

bff_get()  { curl -sf -b "$COOKIE_JAR" "$BFF$1" "${@:2}"; }
bff_post() { curl -sf -b "$COOKIE_JAR" -X POST -H "Content-Type: application/json" -d "$2" "$BFF$1"; }
bff_put()  { curl -sf -b "$COOKIE_JAR" -X PUT -H "Content-Type: application/json" -d "$2" "$BFF$1"; }
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

# ── 2. Lookup Mustahiq ────────────────────────────────────────────────────────
info "Lookup mustahiq..."
LOOKUP_MUSTAHIQ=$(bff_get "/api/distribution/monitoring-visits/lookup/mustahiq?search=")
echo "$LOOKUP_MUSTAHIQ" | jq -e '.data.items | type == "array"' > /dev/null && ok "Lookup mustahiq (array)" || fail "Lookup mustahiq failed: $LOOKUP_MUSTAHIQ"
MUSTAHIQ_ID=$(echo "$LOOKUP_MUSTAHIQ" | jq -r '.data.items[0].mustahiq_id // empty')
info "First mustahiq_id: ${MUSTAHIQ_ID:-none}"

# If no mustahiq available, fail test
if [ -z "$MUSTAHIQ_ID" ]; then
  fail "No mustahiq found in lookup — cannot proceed with create test"
fi

# ── 3. Lookup Programs ────────────────────────────────────────────────────────
info "Lookup programs..."
LOOKUP_PROGRAMS=$(bff_get "/api/distribution/monitoring-visits/lookup/programs")
echo "$LOOKUP_PROGRAMS" | jq -e '.data.items | type == "array"' > /dev/null && ok "Lookup programs (array)" || fail "Lookup programs failed: $LOOKUP_PROGRAMS"

# ── 4. List monitoring visits (empty, before create) ───────────────────────────
info "List monitoring visits (2026-06-22)..."
LIST=$(bff_get "/api/distribution/monitoring-visits?begin_date=2026-06-22&end_date=2026-06-22")
echo "$LIST" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List monitoring visits" || fail "List failed: $LIST"
TOTAL_BEFORE=$(echo "$LIST" | jq -r '.data.pagination.total')
info "Total visits before create: $TOTAL_BEFORE"

# ── 5. Create Monitoring Visit ────────────────────────────────────────────────
info "Create monitoring visit..."
CREATE=$(bff_post "/api/distribution/monitoring-visits" \
  "{
    \"mustahiq_id\": $MUSTAHIQ_ID,
    \"mustahiq_product_id\": null,
    \"visit_address\": \"Jl. Test No. 1\",
    \"visit_location\": \"Rumah Mustahiq\",
    \"visit_date\": \"2026-06-22\",
    \"persons_amil\": [
      {\"visit_person_name\": \"Petugas Test\", \"visit_person_position\": \"Koordinator\"}
    ],
    \"persons_mustahiq\": [
      {\"visit_person_name\": \"Mustahiq Test\", \"visit_person_position\": \"Penerima\"}
    ],
    \"purposes\": [
      {\"visit_item_annotation\": \"Verifikasi penerimaan bantuan\"}
    ],
    \"results\": [
      {\"visit_item_annotation\": \"Bantuan sudah diterima\"}
    ],
    \"followups\": [
      {\"visit_item_annotation\": \"Pantau 3 bulan ke depan\"}
    ]
  }")
VISIT_ID=$(echo "$CREATE" | jq -r '.data.visit_id // empty')
[ -n "$VISIT_ID" ] && ok "Create monitoring visit (id=$VISIT_ID)" || fail "Create failed: $CREATE"

# ── 6. Get Detail Monitoring Visit ────────────────────────────────────────────
info "Get detail visit $VISIT_ID..."
DETAIL=$(bff_get "/api/distribution/monitoring-visits/$VISIT_ID")
echo "$DETAIL" | jq -e '.data.visit_id == '$VISIT_ID > /dev/null && ok "Get visit detail" || fail "Get detail failed: $DETAIL"
VISIT_LOCATION=$(echo "$DETAIL" | jq -r '.data.visit_location')
PERSONS_AMIL_COUNT=$(echo "$DETAIL" | jq -r '.data.persons_amil | length')
info "Visit location: $VISIT_LOCATION, persons_amil count: $PERSONS_AMIL_COUNT"

# ── 7. List After Create ──────────────────────────────────────────────────────
info "List monitoring visits after create..."
LIST_AFTER=$(bff_get "/api/distribution/monitoring-visits?begin_date=2026-06-22&end_date=2026-06-22")
echo "$LIST_AFTER" | jq -e '.data.rows | type == "array"' > /dev/null && ok "List after create" || fail "List after create failed: $LIST_AFTER"
TOTAL_AFTER=$(echo "$LIST_AFTER" | jq -r '.data.pagination.total')
info "Total visits after create: $TOTAL_AFTER"

# ── 8. Update Monitoring Visit ────────────────────────────────────────────────
info "Update visit $VISIT_ID..."
UPDATE=$(bff_put "/api/distribution/monitoring-visits/$VISIT_ID" \
  "{
    \"mustahiq_id\": $MUSTAHIQ_ID,
    \"mustahiq_product_id\": null,
    \"visit_address\": \"Jl. Test Update No. 2\",
    \"visit_location\": \"Kantor Updated\",
    \"visit_date\": \"2026-06-22\",
    \"persons_amil\": [
      {\"visit_person_name\": \"Petugas Test Updated\", \"visit_person_position\": \"Supervisor\"}
    ],
    \"persons_mustahiq\": [
      {\"visit_person_name\": \"Mustahiq Test\", \"visit_person_position\": \"Penerima\"}
    ],
    \"purposes\": [
      {\"visit_item_annotation\": \"Tujuan Updated\"}
    ],
    \"results\": [
      {\"visit_item_annotation\": \"Hasil Updated\"}
    ],
    \"followups\": [
      {\"visit_item_annotation\": \"Tindak Lanjut Updated\"}
    ]
  }")
echo "$UPDATE" | jq -e '.data.visit_id' > /dev/null && ok "Update visit" || fail "Update failed: $UPDATE"

# ── 9. Verify Update ──────────────────────────────────────────────────────────
info "Verify update (fetch detail again)..."
DETAIL_UPDATED=$(bff_get "/api/distribution/monitoring-visits/$VISIT_ID")
VISIT_LOCATION_UPDATED=$(echo "$DETAIL_UPDATED" | jq -r '.data.visit_location')
[ "$VISIT_LOCATION_UPDATED" == "Kantor Updated" ] && ok "Update verified (location=$VISIT_LOCATION_UPDATED)" || fail "Update verification failed: location=$VISIT_LOCATION_UPDATED"

# ── 10. Delete Monitoring Visit ───────────────────────────────────────────────
info "Delete visit $VISIT_ID..."
DEL=$(bff_del "/api/distribution/monitoring-visits/$VISIT_ID")
echo "$DEL" | jq -e '.data.visit_id' > /dev/null && ok "Delete visit" || fail "Delete failed: $DEL"

# ── 11. Verify Delete ─────────────────────────────────────────────────────────
info "Verify delete (fetch detail should return 404)..."
DEL_CHECK=$(curl -s -b "$COOKIE_JAR" "$BFF/api/distribution/monitoring-visits/$VISIT_ID")
if echo "$DEL_CHECK" | jq -e '.error' > /dev/null 2>&1; then
  ok "Delete verified (error response — visit gone)"
else
  fail "Delete verification failed: visit still exists: $DEL_CHECK"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
rm -f "$COOKIE_JAR"
echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN} E2E Monitoring Penyaluran — SEMUA LULUS ✓ ${NC}"
echo -e "${GREEN}==========================================${NC}"
