#!/usr/bin/env bash
# testing/e2e-penyaluran.sh
# E2E smoke tests untuk Penyaluran Dana API
# Jalankan saat stack zakat running (make run / podman-compose up)

set -e
BASE_API="http://localhost:8000"
TODAY=$(date +%Y-%m-%d)
START="${TODAY:0:7}-01"

echo "=== E2E: Penyaluran Dana ==="

echo ""
echo "1. [api-python] GET /api/transaction/penyaluran/lookup/ashnaf"
curl -sf "$BASE_API/api/transaction/penyaluran/lookup/ashnaf" | python3 -c "
import json,sys
d=json.load(sys.stdin)
data=d.get('data',[])
assert len(data)==8, f'Expected 8 ashnaf, got {len(data)}'
print('  OK —', len(data), 'ashnaf')
"

echo ""
echo "2. [api-python] GET /api/transaction/penyaluran/lookup/rekening?type=bank"
curl -sf "$BASE_API/api/transaction/penyaluran/lookup/rekening?type=bank" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d.get('data',[])
assert len(rows)>0, 'No bank accounts found'
print('  OK —', len(rows), 'rekening bank')
print('  Sample:', rows[0]['account_no'], '—', rows[0]['account_name'])
"

echo ""
echo "3. [api-python] GET /api/transaction/penyaluran/lookup/produk?branch_code=001"
curl -sf "$BASE_API/api/transaction/penyaluran/lookup/produk?branch_code=001" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d.get('data',[])
assert len(rows)>0, 'No distribution products found for branch 001'
print('  OK —', len(rows), 'produk penyaluran')
"

echo ""
echo "4. [api-python] GET /api/transaction/penyaluran/ (list DD001)"
curl -sf "$BASE_API/api/transaction/penyaluran/?begin=$START&end=$TODAY&page=1&page_size=5" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'data' in d and 'pagination' in d, f'Bad shape: {list(d.keys())}'
print('  OK — total DD001:', d['pagination']['total'])
"

echo ""
echo "5. [api-python] POST /api/transaction/penyaluran/ — validation error (empty items)"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "$BASE_API/api/transaction/penyaluran/?user_id=TEST&branch_code=001" \
  -H "Content-Type: application/json" \
  -d '{"actual_date":"2026-06-07","payment_type":"B","fund_account_no":"X","product_branch_code":"001","items":[]}')
if [ "$STATUS" = "422" ]; then
  echo "  OK — 422 Validation Error (empty items)"
else
  echo "  WARN — expected 422, got $STATUS"
fi

echo ""
echo "=== Semua test selesai ==="
