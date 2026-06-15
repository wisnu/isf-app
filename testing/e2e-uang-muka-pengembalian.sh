#!/usr/bin/env bash
# E2E smoke test — Pengembalian / LPJ Uang Muka (CAR)
# Requires: active session for user HADI (ACC role, branch 001)
# Usage:   bash testing/e2e-uang-muka-pengembalian.sh [BFF_PORT]

set -euo pipefail

BFF="${1:-7000}"
BASE="http://localhost:${BFF}/api"
COOKIE_JAR=$(mktemp)
TODAY=$(date +%Y-%m-%d)

echo "=== Uang Muka Pengembalian E2E ==="
echo "BFF: $BASE"

# ── 1. Login ──────────────────────────────────────────────────────────────────
echo -e "\n[1] Login HADI"
curl -s -c "$COOKIE_JAR" -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}' | python3 -m json.tool --no-ensure-ascii

# ── 2. Lookup employee ─────────────────────────────────────────────────────────
echo -e "\n[2] Lookup employee 'hadi'"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/uang-muka/lookup/employee?search=hadi" | python3 -m json.tool --no-ensure-ascii

# ── 3. Lookup open CA for a test employee (employee_id=1) ─────────────────────
echo -e "\n[3] Lookup open uang muka for employee_id=1"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/uang-muka-pengembalian/lookup/open-uang-muka?employee_id=1" | python3 -m json.tool --no-ensure-ascii

# ── 4. Lookup cash accounts ────────────────────────────────────────────────────
echo -e "\n[4] Lookup cash accounts"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/uang-muka/lookup/cash-account" | python3 -m json.tool --no-ensure-ascii

# ── 5. Create Pengembalian (adjust ref_transaction_item_id to a real open CA) ─
echo -e "\n[5] Create Pengembalian (dry-run — adjust IDs before submitting)"
# NOTE: Set ref_transaction_item_id to a real open CA item ID from step [3]
curl -s -b "$COOKIE_JAR" -X POST "$BASE/transaksi/uang-muka-pengembalian/" \
  -H "Content-Type: application/json" \
  -d "{
    \"actual_date\": \"${TODAY}\",
    \"ref_transaction_no\": \"KK-2026-001-LAZ-0000001\",
    \"ref_transaction_item_id\": 999999,
    \"ref_amount\": 500000,
    \"employee_id\": 1,
    \"employee_name\": \"Test Karyawan\",
    \"cash_account_no\": \"KAS001\",
    \"amount\": 500000,
    \"reference_no\": \"KWT-2026-001\",
    \"description\": \"LPJ uang muka kegiatan X\"
  }" | python3 -m json.tool --no-ensure-ascii

# ── 6. List Pengembalian ───────────────────────────────────────────────────────
echo -e "\n[6] List Pengembalian (today)"
curl -s -b "$COOKIE_JAR" \
  "$BASE/transaksi/uang-muka-pengembalian/?date_from=${TODAY}&date_to=${TODAY}" | python3 -m json.tool --no-ensure-ascii

rm -f "$COOKIE_JAR"
echo -e "\n=== Done ==="
