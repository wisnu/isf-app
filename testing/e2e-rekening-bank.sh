#!/usr/bin/env bash
# testing/e2e-rekening-bank.sh
# E2E smoke tests untuk Rekening Bank (TR0006 migration + CRUD via otorisasi)
# Jalankan saat stack zakat running: make run / podman-compose up

set -e
BASE_BFF="http://localhost:7000"
BASE_API="http://localhost:8000"

echo "=== E2E: Rekening Bank ==="

echo ""
echo "0. Login sebagai RAIS (ACC/KEU role)"
curl -sf -c /tmp/cookies-rekening-bank.txt "$BASE_BFF/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"RAIS","password":"test1234"}' | python3 -c "
import json,sys; d=json.load(sys.stdin)
assert d.get('data'), f'Login gagal: {d}'
print('  OK — login berhasil')"

echo ""
echo "1. [api-python] GET /api/bank/accounts — list rekening bank"
curl -sf "$BASE_API/api/bank/accounts?page=1&page_size=5" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d['data']['rows']; p=d['data']['pagination']
assert isinstance(rows, list), 'Expected list'
assert p['total'] > 0, 'No records found'
print(f'  OK — {len(rows)} rows, total={p[\"total\"]}')"

echo ""
echo "2. [api-python] GET /api/bank/accounts/{account_no} — detail rekening"
FIRST_ID=$(curl -sf "$BASE_API/api/bank/accounts?page=1&page_size=1" | python3 -c "
import json,sys; print(json.load(sys.stdin)['data']['rows'][0]['account_no'])")
curl -sf "$BASE_API/api/bank/accounts/$FIRST_ID" | python3 -c "
import json,sys
d=json.load(sys.stdin)['data']
assert d.get('account_no'), 'No account_no'
assert 'is_amil_account' in d, 'Missing is_amil_account'
print(f'  OK — {d[\"account_no\"]} | {d[\"account_name\"]} | amil={d[\"is_amil_account\"]}')"

echo ""
echo "3. [api-python] Lookup: banks, branches, currencies, gl_accounts, products"
curl -sf "$BASE_API/api/bank/lookup/banks" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0, 'No banks'
print(f'  OK — banks: {len(d)} items')"

curl -sf "$BASE_API/api/bank/lookup/branches" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0, 'No branches'
print(f'  OK — branches: {len(d)} items')"

curl -sf "$BASE_API/api/bank/lookup/currencies" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0, 'No currencies'
print(f'  OK — currencies: {len(d)} items')"

curl -sf "$BASE_API/api/bank/lookup/gl_accounts?search=110" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0, 'No gl accounts'
assert 'account_code' in d[0], 'Missing account_code'
print(f'  OK — gl_accounts search=110: {len(d)} items')"

curl -sf "$BASE_API/api/bank/lookup/products" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
print(f'  OK — products: {len(d)} items')"

echo ""
echo "4. [bff-api] GET /api/bank/accounts — via BFF + auth"
curl -sf -b /tmp/cookies-rekening-bank.txt "$BASE_BFF/api/bank/accounts?page=1&page_size=5" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d['data']['rows']; p=d['data']['pagination']
assert isinstance(rows, list), 'Expected list'
print(f'  OK — {len(rows)} rows via BFF, total={p[\"total\"]}')"

echo ""
echo "5. [bff-api] GET /api/bank/lookup/banks — via BFF"
curl -sf -b /tmp/cookies-rekening-bank.txt "$BASE_BFF/api/bank/lookup/banks" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0, 'No banks'
print(f'  OK — {len(d)} banks via BFF')"

echo ""
echo "6. [bff-api] GET /api/bank/lookup/branches — via BFF"
curl -sf -b /tmp/cookies-rekening-bank.txt "$BASE_BFF/api/bank/lookup/branches" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0
print(f'  OK — {len(d)} branches via BFF')"

echo ""
echo "7. [bff-api] GET /api/bank/lookup/gl_accounts?search=110 — via BFF"
curl -sf -b /tmp/cookies-rekening-bank.txt "$BASE_BFF/api/bank/lookup/gl_accounts?search=110" | python3 -c "
import json,sys; d=json.load(sys.stdin)['data']['data']
assert len(d)>0
print(f'  OK — {len(d)} GL accounts via BFF')"

echo ""
echo "=== SEMUA TEST PASSED ==="
