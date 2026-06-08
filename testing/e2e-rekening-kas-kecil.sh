#!/usr/bin/env bash
# testing/e2e-rekening-kas-kecil.sh
# E2E smoke tests untuk Rekening Kas Kecil (Petty Cash)
# Jalankan saat stack zakat running: cd infra && podman-compose -f docker-compose.zakat.yml up -d

set -e
BASE_BFF="http://localhost:7000"
BASE_API="http://localhost:8000"
COOKIES="/tmp/cookies-kas-kecil.txt"
TODAY=$(date +%Y-%m-%d)

echo "=== E2E: Rekening Kas Kecil ==="

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "0. Login sebagai RAIS (ACC/KEU role)"
curl -sf -c "$COOKIES" "$BASE_BFF/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"RAIS","password":"test1234"}' | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert d.get('data'), 'Login gagal: ' + str(d)
print('  OK — login berhasil, user:', d['data'].get('username','?'))"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "1. [api-python] GET /api/kas-kecil/accounts — list harus ada rows"
curl -sf "$BASE_API/api/kas-kecil/accounts?page=1&page_size=10" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d.get('rows', [])
pag=d.get('pagination',{})
assert isinstance(rows, list), 'rows bukan list'
print('  OK —', len(rows), 'rows, total:', pag.get('total','?'))"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "2. [bff-api] GET /api/kas-kecil/accounts — via BFF (require_menu check)"
curl -sf -b "$COOKIES" "$BASE_BFF/api/kas-kecil/accounts?page=1&page_size=5" | python3 -c "
import json,sys
d=json.load(sys.stdin)
data=d.get('data',{})
rows=data.get('rows',[])
assert isinstance(rows, list), 'Expected list in data.rows'
print('  OK —', len(rows), 'rows via BFF')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "3. [bff-api] GET /api/kas-kecil/lookup/branches"
curl -sf -b "$COOKIES" "$BASE_BFF/api/kas-kecil/lookup/branches" | python3 -c "
import json,sys
d=json.load(sys.stdin)
items=d.get('data',{}).get('data',[])
assert len(items) > 0, 'Branch lookup kosong'
print('  OK —', len(items), 'cabang')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "4. [bff-api] GET /api/kas-kecil/lookup/currencies"
curl -sf -b "$COOKIES" "$BASE_BFF/api/kas-kecil/lookup/currencies" | python3 -c "
import json,sys
d=json.load(sys.stdin)
items=d.get('data',{}).get('data',[])
assert len(items) > 0, 'Currency lookup kosong'
print('  OK —', len(items), 'valuta')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "5. [bff-api] GET /api/kas-kecil/lookup/gl_accounts?search=110"
curl -sf -b "$COOKIES" "$BASE_BFF/api/kas-kecil/lookup/gl_accounts?search=110" | python3 -c "
import json,sys
d=json.load(sys.stdin)
items=d.get('data',{}).get('data',[])
print('  OK —', len(items), 'GL accounts matching 110')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "6. [bff-api] POST /api/kas-kecil/accounts — create rekening baru"
RESULT=$(curl -sf -b "$COOKIES" -X POST "$BASE_BFF/api/kas-kecil/accounts" \
  -H "Content-Type: application/json" \
  -d "{
    \"account_name\": \"E2E Test Kas Kecil\",
    \"account_interface\": \"110102\",
    \"currency_code\": \"IDR\",
    \"branch_code\": \"001\",
    \"opening_date\": \"$TODAY\"
  }")
echo "$RESULT" | python3 -c "
import json,sys
d=json.load(sys.stdin)
account_no=d.get('data',{}).get('account_no','')
assert account_no.startswith('PC.'), 'account_no format salah: ' + account_no
print('  OK — account_no:', account_no)"
ACCOUNT_NO=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['account_no'])")

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "7. [bff-api] GET /api/kas-kecil/accounts/$ACCOUNT_NO — detail rekening baru"
curl -sf -b "$COOKIES" "$BASE_BFF/api/kas-kecil/accounts/$ACCOUNT_NO" | python3 -c "
import json,sys
d=json.load(sys.stdin)
det=d.get('data',{})
assert det.get('account_no'), 'account_no tidak ada di response'
assert det.get('account_name') == 'E2E Test Kas Kecil', 'account_name tidak match'
print('  OK — detail:', det.get('account_name'), '/', det.get('branch_code'))"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "8. [bff-api] PUT /api/kas-kecil/accounts/$ACCOUNT_NO — update nama"
curl -sf -b "$COOKIES" -X PUT "$BASE_BFF/api/kas-kecil/accounts/$ACCOUNT_NO" \
  -H "Content-Type: application/json" \
  -d "{
    \"account_name\": \"E2E Test Kas Kecil UPDATED\",
    \"account_interface\": \"110102\",
    \"currency_code\": \"IDR\",
    \"opening_date\": \"$TODAY\"
  }" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'error' not in d, 'Update error: ' + str(d)
print('  OK — update sukses')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "9. [bff-api] DELETE /api/kas-kecil/accounts/$ACCOUNT_NO — hapus rekening test"
curl -sf -b "$COOKIES" -X DELETE "$BASE_BFF/api/kas-kecil/accounts/$ACCOUNT_NO" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'error' not in d, 'Delete error: ' + str(d)
print('  OK — delete sukses')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "10. [bff-api] GET /api/kas-kecil/accounts/$ACCOUNT_NO — harus 404 setelah delete"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIES" \
  "$BASE_BFF/api/kas-kecil/accounts/$ACCOUNT_NO")
python3 -c "
code=$HTTP_CODE
assert code == 404, f'Expected 404 setelah delete, got {code}'
print('  OK — 404 confirmed setelah delete')"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "=== SEMUA TEST PASSED ==="
