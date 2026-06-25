#!/usr/bin/env bash
# E2E smoke test: Cetak Bukti Setor Zakat (BSZ)
# Portal: Zakat | api-python :8000 | bff-api :7000
# Domain: fundraising / Penghimpunan
# Tanggal: 2026-06-26

set -euo pipefail

API="http://localhost:8000/api"
BFF="http://localhost:7000/api"
PASS=0
FAIL=0
CREATED_BSZ_ID=""

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

ok() { echo -e "${GREEN}[PASS]${NC} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}[FAIL]${NC} $1"; FAIL=$((FAIL+1)); }

check() {
  local label="$1"
  local url="$2"
  local expected_key="${3:-data}"
  local resp
  resp=$(curl -s "$url")
  if echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); assert '$expected_key' in d" 2>/dev/null; then
    ok "$label"
  else
    fail "$label → $resp"
  fi
}

echo "=== Cetak Bukti Setor Zakat — E2E Smoke Test ==="
echo ""

# ── 1. Zakat Objects ─────────────────────────────────────────────────────────
echo "--- Layer 1: Zakat Objects ---"
resp=$(curl -s "$API/fundraising/bsz/zakat-objects")
count=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']))" 2>/dev/null || echo "0")
[ "$count" -eq 7 ] && ok "GET /api/fundraising/bsz/zakat-objects → 7 items" || fail "Expected 7 zakat objects, got $count"

# ── 2. BSZ List ───────────────────────────────────────────────────────────────
echo "--- Layer 2: BSZ List ---"
check "GET /api/fundraising/bsz" "$API/fundraising/bsz?page=1&limit=10"

resp=$(curl -s "$API/fundraising/bsz?page=1&limit=10")
total=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['pagination']['total'])" 2>/dev/null || echo "0")
[ "$total" -ge 4 ] && ok "BSZ list total >= 4 (existing records)" || fail "Expected >= 4 BSZ records, got $total"

# ── 3. BSZ Detail ─────────────────────────────────────────────────────────────
echo "--- Layer 3: BSZ Detail ---"
check "GET /api/fundraising/bsz/88" "$API/fundraising/bsz/88"
check "GET /api/fundraising/bsz/93" "$API/fundraising/bsz/93"

resp=$(curl -s "$API/fundraising/bsz/88")
bsz_num=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['bsz_number'])" 2>/dev/null || echo "")
[ "$bsz_num" = "001/IV/BPZIS/2015" ] && ok "BSZ 88 number correct: $bsz_num" || fail "BSZ 88 number wrong: $bsz_num"

# ── 4. BSZ 404 ───────────────────────────────────────────────────────────────
echo "--- Layer 4: BSZ 404 ---"
resp=$(curl -s "$API/fundraising/bsz/99999")
code=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('code',''))" 2>/dev/null || echo "")
[ "$code" = "NOT_FOUND" ] && ok "GET /api/fundraising/bsz/99999 → 404 NOT_FOUND" || fail "Expected NOT_FOUND, got: $code"

# ── 5. Donor Lookup ──────────────────────────────────────────────────────────
echo "--- Layer 5: Donor Lookup ---"
resp=$(curl -s "$API/fundraising/bsz/lookup/donor?q=tedi")
count=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']))" 2>/dev/null || echo "0")
[ "$count" -ge 1 ] && ok "GET /api/fundraising/bsz/lookup/donor?q=tedi → $count results" || fail "Donor lookup returned 0 results"

# ── 6. Available Transactions ────────────────────────────────────────────────
echo "--- Layer 6: Available Transactions ---"
resp=$(curl -s "$API/fundraising/bsz/available-transactions?donor_id=20948&begin_date=2024-01-01&end_date=2024-12-31")
count=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']))" 2>/dev/null || echo "0")
[ "$count" -ge 1 ] && ok "GET available-transactions donor=20948 2024 → $count transactions" || fail "Expected transactions for donor 20948, got $count"

# ── 7. BSZ List filtered by donor ────────────────────────────────────────────
echo "--- Layer 7: BSZ List with donor filter ---"
resp=$(curl -s "$API/fundraising/bsz?donor_id=1542&page=1&limit=10")
donor_rows=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']['rows']))" 2>/dev/null || echo "0")
[ "$donor_rows" -ge 1 ] && ok "BSZ list filter donor_id=1542 → $donor_rows records" || fail "Expected BSZ for donor 1542, got $donor_rows"

# ── 8. Create BSZ (dry run with donor 20948) ─────────────────────────────────
echo "--- Layer 8: Create BSZ ---"
# Get a few transaction IDs to use
TRAN_IDS=$(curl -s "$API/fundraising/bsz/available-transactions?donor_id=20948&begin_date=2024-01-01&end_date=2024-01-31" | \
  python3 -c "
import sys,json
d=json.load(sys.stdin)
rows=d['data'][:3]
print(json.dumps(rows))
" 2>/dev/null || echo "[]")

TRAN_COUNT=$(echo "$TRAN_IDS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

if [ "$TRAN_COUNT" -ge 1 ]; then
  TOTAL=$(echo "$TRAN_IDS" | python3 -c "import sys,json; rows=json.load(sys.stdin); print(sum(r['amount'] for r in rows))" 2>/dev/null || echo "0")

  BODY=$(echo "$TRAN_IDS" | python3 -c "
import sys,json
rows=json.load(sys.stdin)
total=sum(r['amount'] for r in rows)
body={
  'donor_id': 20948,
  'period_begin': '2024-01-01',
  'period_end': '2024-01-31',
  'items': [{'item':6,'year':2024,'percentage':2.5,'basic_value':round(total/(2.5/100)),'zakah_value':total}],
  'transactions': [{'transaction_item_id':r['transaction_item_id'],'zakah_object':r['zakah_object']} for r in rows]
}
print(json.dumps(body))
" 2>/dev/null)

  resp=$(curl -s -X POST "$API/fundraising/bsz" \
    -H "Content-Type: application/json" \
    -d "$BODY")

  bsz_number=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['bsz_number'])" 2>/dev/null || echo "")
  CREATED_BSZ_ID=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['bsz_id'])" 2>/dev/null || echo "")

  [ -n "$bsz_number" ] && ok "POST /api/fundraising/bsz → created $bsz_number (id=$CREATED_BSZ_ID)" || fail "BSZ create failed: $resp"
else
  echo "[SKIP] No available transactions for donor 20948 in 2024-01"
fi

# ── 9. Delete created BSZ ────────────────────────────────────────────────────
echo "--- Layer 9: Delete BSZ ---"
if [ -n "$CREATED_BSZ_ID" ]; then
  resp=$(curl -s -X DELETE "$API/fundraising/bsz/$CREATED_BSZ_ID")
  status=$(echo "$resp" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['status'])" 2>/dev/null || echo "")
  [ "$status" = "deleted" ] && ok "DELETE /api/fundraising/bsz/$CREATED_BSZ_ID → deleted" || fail "Delete failed: $resp"
else
  echo "[SKIP] No BSZ created to delete"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "=== Summary: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
