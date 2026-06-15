#!/usr/bin/env bash
# E2E smoke test — Transfer Antar Rekening (TI)
# Requires: active user with keuangan.transaksi.transfer-antar-rekening menu access
# Usage:   bash testing/e2e-transfer-antar-rekening.sh [BFF_PORT]

set -euo pipefail

BFF="${1:-7000}"
BASE="http://localhost:${BFF}/api"
COOKIE_JAR=$(mktemp)
TODAY=$(date +%Y-%m-%d)

echo "=== Transfer Antar Rekening E2E ==="
echo "BFF: $BASE"

# ── 1. Login ──────────────────────────────────────────────────────────────────
echo -e "\n[1] Login HADI (ACC role, branch_access=all)"
curl -s -c "$COOKIE_JAR" -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}' | python3 -m json.tool --no-ensure-ascii

# ── 2. Lookup cash accounts ────────────────────────────────────────────────────
echo -e "\n[2] Lookup cash accounts (search 'kas')"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/transfer-antar-rekening/lookup/cash-accounts?search=kas" | python3 -m json.tool --no-ensure-ascii

echo -e "\n[2b] Lookup cash accounts (search 'bni')"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/transfer-antar-rekening/lookup/cash-accounts?search=bni" | python3 -m json.tool --no-ensure-ascii

# ── 3. List transfers (today) ──────────────────────────────────────────────────
echo -e "\n[3] List transfers tanggal hari ini"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/transfer-antar-rekening/?date_from=${TODAY}&date_to=${TODAY}&page=1&limit=25" \
  | python3 -m json.tool --no-ensure-ascii

# ── 4. Create Transfer (adjust account numbers to match real data) ─────────────
# NOTE: Ganti source_account_no dan dest_account_no dengan cashaccountno yang valid
# dari hasil lookup di step [2]. Pastikan source != dest.
echo -e "\n[4] Create Transfer Antar Rekening (dry-run — sesuaikan account_no)"
curl -s -b "$COOKIE_JAR" -X POST "$BASE/transaksi/transfer-antar-rekening/" \
  -H "Content-Type: application/json" \
  -d "{
    \"actual_date\": \"${TODAY}\",
    \"source_account_no\": \"KAS001\",
    \"dest_account_no\": \"KAS002\",
    \"amount\": 1000000,
    \"description\": \"Test transfer E2E\",
    \"reference_no\": \"REF-E2E-001\"
  }" | python3 -m json.tool --no-ensure-ascii

# ── 5. List after create ───────────────────────────────────────────────────────
echo -e "\n[5] List transfers setelah create"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/transfer-antar-rekening/?date_from=${TODAY}&date_to=${TODAY}&page=1&limit=25" \
  | python3 -m json.tool --no-ensure-ascii

echo -e "\n=== Done ==="
rm -f "$COOKIE_JAR"
