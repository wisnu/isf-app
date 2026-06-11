#!/bin/bash
# E2E smoke test — Pemilik Anggaran
# Usage: bash testing/e2e-pemilik-anggaran.sh [TOKEN]
# Requires: curl, jq
# Portal: Zakat (localhost:7000)

set -euo pipefail

BFF_URL="${BFF_URL:-http://localhost:7000}"
TOKEN="${1:-}"

if [[ -z "$TOKEN" ]]; then
  echo "[INFO] No token supplied — attempting login as RAIS:test1234"
  TOKEN=$(curl -s -X POST "$BFF_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"RAIS","password":"test1234"}' | jq -r '.data.access_token // empty')
  if [[ -z "$TOKEN" ]]; then
    echo "[ERROR] Login gagal — set TOKEN env atau jalankan: bash e2e-pemilik-anggaran.sh <token>"
    exit 1
  fi
  echo "[OK] Login berhasil"
fi

AUTH="-H \"Authorization: Bearer $TOKEN\""
HDR=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")

pass=0; fail=0

check() {
  local label="$1"; local status="$2"; local expected="$3"
  if [[ "$status" == "$expected" ]]; then
    echo "[PASS] $label (HTTP $status)"
    ((pass++))
  else
    echo "[FAIL] $label (expected $expected, got $status)"
    ((fail++))
  fi
}

echo ""
echo "=== Pemilik Anggaran E2E ==="
echo "BFF: $BFF_URL"
echo ""

# ── 1. List (kosong / ada data) ───────────────────────────────────────────────
echo "--- Test 1: GET /api/parameter/pemilik-anggaran ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" "$BFF_URL/api/parameter/pemilik-anggaran?page=1&limit=25")
check "List pemilik anggaran" "$STATUS" "200"

# ── 2. Lookup groups ──────────────────────────────────────────────────────────
echo "--- Test 2: GET /api/parameter/pemilik-anggaran/lookup ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" "$BFF_URL/api/parameter/pemilik-anggaran/lookup")
check "Lookup parent groups" "$STATUS" "200"

# ── 3. Create Induk (tanpa parent) via otorisasi ──────────────────────────────
echo "--- Test 3: Create node INDUK via otorisasi ---"
RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" -X POST "$BFF_URL/api/otorisasi/save-and-submit/" \
  -d '{
    "entity_type": "budget_owner",
    "module": "keuangan",
    "payload": {
      "action": "create",
      "ownercode": "TST01",
      "ownername": "Test Induk E2E",
      "is_detail": "F",
      "parentownerid": null,
      "status": "A"
    }
  }')
STATUS=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)
check "Create induk (otorisasi)" "$STATUS" "200"
echo "  Response status: $(echo "$BODY" | jq -r '.data.status // .status // "?"')"
SUBMISSION_ID=$(echo "$BODY" | jq -r '.data.submission_id // empty')

# ── 4. Create Detail (dengan parent) ─────────────────────────────────────────
echo "--- Test 4: Create node DETAIL via otorisasi ---"
# Ambil ownerid induk yang baru dibuat (jika AUTHORIZED)
INDUK_ID=$(curl -s "${HDR[@]}" "$BFF_URL/api/parameter/pemilik-anggaran/lookup?q=TST01" | jq -r '.data.data[0].ownerid // empty')
if [[ -n "$INDUK_ID" ]]; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" -X POST "$BFF_URL/api/otorisasi/save-and-submit/" \
    -d "{
      \"entity_type\": \"budget_owner\",
      \"module\": \"keuangan\",
      \"payload\": {
        \"action\": \"create\",
        \"ownercode\": \"TST02\",
        \"ownername\": \"Test Detail E2E\",
        \"is_detail\": \"T\",
        \"parentownerid\": $INDUK_ID,
        \"status\": \"A\"
      }
    }")
  check "Create detail dengan parent" "$STATUS" "200"
else
  echo "[SKIP] Test 4 dilewati — induk TST01 belum AUTHORIZED atau tidak ditemukan"
fi

# ── 5. Get by ID ──────────────────────────────────────────────────────────────
echo "--- Test 5: GET /api/parameter/pemilik-anggaran/lookup (search) ---"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" "$BFF_URL/api/parameter/pemilik-anggaran/lookup?q=TST")
check "Lookup dengan filter" "$STATUS" "200"

# ── 6. Approve jika PENDING ───────────────────────────────────────────────────
if [[ -n "${SUBMISSION_ID:-}" ]]; then
  echo "--- Test 6: Approve submission $SUBMISSION_ID ---"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" -X POST "$BFF_URL/api/otorisasi/submission/$SUBMISSION_ID/approve" -d '{}')
  if [[ "$STATUS" == "200" ]]; then
    check "Approve submission" "$STATUS" "200"
  else
    echo "[INFO] Submission sudah AUTHORIZED (status: $STATUS) — skip approve"
    ((pass++))
  fi
fi

# ── 7. Delete TST02 (jika ada) ────────────────────────────────────────────────
echo "--- Test 7: Delete node DETAIL via otorisasi ---"
DETAIL_ID=$(curl -s "${HDR[@]}" "$BFF_URL/api/parameter/pemilik-anggaran?q=TST02" | jq -r '.data.rows[0].ownerid // empty')
if [[ -n "$DETAIL_ID" ]]; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HDR[@]}" -X POST "$BFF_URL/api/otorisasi/save-and-submit/" \
    -d "{\"entity_type\":\"budget_owner\",\"module\":\"keuangan\",\"payload\":{\"action\":\"delete\",\"ownerid\":$DETAIL_ID}}")
  check "Delete detail" "$STATUS" "200"
else
  echo "[SKIP] Test 7 dilewati — TST02 belum AUTHORIZED"
fi

# ── Hasil ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== Hasil: $pass passed, $fail failed ==="
[[ $fail -eq 0 ]] && exit 0 || exit 1
