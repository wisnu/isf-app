#!/usr/bin/env bash
# testing/e2e-upload-penghimpunan.sh
# E2E smoke test for upload penghimpunan feature.
# Runs against api-python directly (localhost:8001).
# For BFF-authenticated flow, test manually via browser with session cookie.
set -e
API="http://localhost:8001"

echo "=== E2E: Upload Penghimpunan ==="

# 1. Generate test fixture XLSX
python3 - <<'PYEOF'
from openpyxl import Workbook
import io
wb = Workbook()
ws = wb.active
ws.append(['NoRek','Tanggal','Ket','Ref','Total','ZP','ZM','ZF','ZPer',
           'Infaq','InfaqT','DPU','AY','AA','TW','TQ','Qurban','NH','Fidyah'])
ws.append(['1234567890','01/06/2026','Transfer DARI Budi TRANSFER','REF-TEST-001',
           500000, 300000, 200000, 0,0,0,0,0,0,0,0,0,0,0,0])
ws.append(['1234567890','02/06/2026','Transfer masuk infaq','REF-TEST-002',
           100000, 0, 0, 0, 0, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0])
buf = io.BytesIO()
wb.save(buf)
open('/tmp/e2e_upload.xlsx','wb').write(buf.getvalue())
print("Fixture created: /tmp/e2e_upload.xlsx")
PYEOF

echo ""
echo "1. Parse endpoint (api-python direct — no auth required for smoke test):"
curl -s -X POST "$API/api/transaction/upload/penghimpunan/parse" \
  -F "file=@/tmp/e2e_upload.xlsx" -F "branch_code=001" | python3 -m json.tool | head -50

echo ""
echo "2. Template download (HEAD check):"
curl -sI "$API/api/transaction/upload/penghimpunan/template" | grep -i "content-type"

echo ""
echo "3. List batches (no filter):"
curl -s "$API/api/transaction/upload/penghimpunan/batches" \
  | python3 -m json.tool | head -20

echo ""
echo "=== Done ==="
echo "For full BFF flow (parse → draft → list → otorisasi):"
echo "  Login via http://localhost:5173 as a user with role KEU or SPVKEU"
echo "  Use the Upload Penghimpunan menu under Keuangan in the sidebar"
echo ""
echo "After otorisasi, verify in DB:"
echo "  PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \\"
echo "    -c \"SELECT transactionno, amount, transactioncode FROM transaction.transaction WHERE transactioncode='SDMULTI' ORDER BY transactionid DESC LIMIT 5\""
