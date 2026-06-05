#!/usr/bin/env bash
# testing/e2e-histori-transaksi.sh
# Smoke test untuk fitur Histori Transaksi.
# Jalankan terhadap api-python langsung (port 8001).
set -e
API="http://localhost:8001"
TODAY=$(date +%Y-%m-%d)
FIRST=$(date +%Y-%m-01)

echo "=== E2E: Histori Transaksi ==="

echo ""
echo "1. Search (SPV mode, semua transaksi bulan ini):"
curl -s "$API/api/transaksi-histori/search?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST&limit=5" \
  | python3 -m json.tool | head -30

echo ""
echo "2. Export template (HEAD check):"
curl -sI "$API/api/transaksi-histori/search/export.xlsx?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST" \
  | grep -i "content-type"

echo ""
echo "3. Detail transaksi pertama (jika ada):"
FIRST_ID=$(curl -s "$API/api/transaksi-histori/search?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST&limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data', [{}])[0].get('transactionid', 'NONE') if isinstance(d.get('data'), list) and len(d.get('data', [])) > 0 else 'NONE')" 2>/dev/null)
if [ "$FIRST_ID" != "NONE" ] && [ -n "$FIRST_ID" ]; then
  echo "  Transaction ID: $FIRST_ID"
  curl -s "$API/api/transaksi-histori/transactions/$FIRST_ID" | python3 -m json.tool | head -30
else
  echo "  Tidak ada transaksi — skip detail test"
fi

echo ""
echo "=== Done ==="
echo "Untuk full BFF flow (dengan session + menu gating):"
echo "  Login ke http://localhost:5173 sebagai KEU/SPVKEU user"
echo "  Buka menu Keuangan > Histori Transaksi di sidebar"
