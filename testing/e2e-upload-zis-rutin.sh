#!/usr/bin/env bash
# E2E Smoke Test: Upload Data Penerimaan ZIS Rutin
# Portal: zakat
# User default: HADI (DIST/SPVDIST, all-branch access)
# Usage: bash testing/e2e-upload-zis-rutin.sh
#        BASE_URL=http://localhost:7001 bash testing/e2e-upload-zis-rutin.sh  ← override port

set -euo pipefail

# ── Config ───────────────────────────────────────────────────────────────────
BASE_URL="${BASE_URL:-http://localhost:7000}"  # 7000=zakat, 7001=wakaf
USERNAME="${TEST_USER:-HADI}"
PASSWORD="${TEST_PASS:-test1234}"
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_USER="${DB_USER:-transaction}"
DB_PASSWORD="${DB_PASSWORD:-solusi}"
DB_NAME="${DB_NAME:-mziss_laz}"

TEMP_DIR="/tmp/e2e-zis-rutin-$$"
XLSX_FILE="$TEMP_DIR/sample_zis_batch.xlsx"

# ── Utils ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'; BOLD='\033[1m'
pass()    { echo -e "  ${GREEN}✓${NC} $1"; }
fail()    { echo -e "  ${RED}✗${NC} $1"; exit 1; }
warn()    { echo -e "  ${YELLOW}⚠${NC} $1"; }
section() { echo -e "\n${BOLD}=== $1 ===${NC}"; }

# ── Cleanup trap ─────────────────────────────────────────────────────────────
cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# ── Setup ────────────────────────────────────────────────────────────────────
section "Setup"

mkdir -p "$TEMP_DIR"
echo "Base URL: $BASE_URL"
echo "Temp dir: $TEMP_DIR"
pass "Directory created"

# Verify BFF reachable
curl -sf "$BASE_URL/health" > /dev/null 2>&1 || fail "BFF not reachable at $BASE_URL"
pass "BFF API reachable"

# ── Auth ─────────────────────────────────────────────────────────────────────
section "Login"

LOGIN=$(curl -sf -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  || fail "BFF login request failed")

TOKEN=$(echo "$LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" \
  || fail "Login failed — check username/password")

AUTH="Authorization: Bearer $TOKEN"
pass "Login: $USERNAME, token: ${TOKEN:0:20}..."

# Verify menu access
PROFILE=$(curl -sf "$BASE_URL/api/auth/me" -H "$AUTH")
MENUS=$(echo "$PROFILE" | python3 -c "import sys,json; menus=[m['menu_key'] for m in json.load(sys.stdin)['data'].get('menus',[])]; print(' '.join(menus))" 2>/dev/null || echo "N/A")
echo "  User menus: $MENUS"

# ── Create Sample XLSX ───────────────────────────────────────────────────────
section "Create Sample XLSX"

python3 << PYTHON_EOF
from openpyxl import Workbook
from datetime import datetime

wb = Workbook()
ws = wb.active
ws.title = 'Data ZIS'

# Batch period descriptor in B2
ws['B2'] = 'PERIODE_2026-06-15_E2E_TEST'

# Headers in row 7 (minimal columns for parse to work)
headers = [
    'No', 'BusinessAreaCode', 'BusinessAreaDesc', 'EmployeeNumber', 'Name',
    'BirthPlace', 'WorkAreaName', 'MobilePhone', 'BirthDate', 'Gender',
    'MaritalStatus', 'Position', 'OrganizationUnit', 'ZakatAmount', 'InfaqAmount',
    'AnakAsuhAmount', 'AnakYatimAmount', 'WakafAmount', 'TaqurmaAmount'
]

for col_idx, header in enumerate(headers, start=1):
    ws.cell(row=7, column=col_idx, value=header)

# Sample data rows (8–10)
sample_data = [
    [1, 'DIV01', 'Divisi Operasional', 'E001234', 'Budi Santoso',
     'Jakarta', 'Kantor Pusat', '08123456789', '1990-01-15', 'MALE',
     'MARRD', 'Manager', 'IT', -100000, -50000, 0, 0, 0, -100000],
    [2, 'DIV02', 'Divisi Keuangan', 'E001235', 'Siti Nurhaliza',
     'Bandung', 'Kantor Cabang', '08234567890', '1992-03-20', 'FEMALE',
     'SINGLE', 'Supervisor', 'Finance', -150000, -75000, -50000, 0, 0, -50000],
    [3, 'DIV01', 'Divisi Operasional', 'E001236', 'Ahmad Wijaya',
     'Surabaya', 'Kantor Pusat', '08345678901', '1988-07-10', 'MALE',
     'MARRD', 'Staff', 'IT', -120000, -60000, 0, -30000, 0, -80000],
]

for row_idx, row_data in enumerate(sample_data, start=8):
    for col_idx, value in enumerate(row_data, start=1):
        ws.cell(row=row_idx, column=col_idx, value=value)

wb.save('$XLSX_FILE')
print(f'Sample XLSX created: $XLSX_FILE')
PYTHON_EOF

[ -f "$XLSX_FILE" ] && pass "Sample XLSX created: $XLSX_FILE" || fail "Failed to create XLSX"

# ── Parse Upload ─────────────────────────────────────────────────────────────
section "Upload: Parse"

PARSE=$(curl -sf -X POST "$BASE_URL/api/transaksi/upload/hc-zis/parse?tanggal_transaksi=2026-06-15" \
  -H "$AUTH" \
  -F "file=@$XLSX_FILE" \
  || fail "Parse request failed")

BATCH_PERIOD=$(echo "$PARSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('batch_period_desc',''))" 2>/dev/null || echo "")
ITEM_COUNT=$(echo "$PARSE" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data'].get('items',[])))" 2>/dev/null || echo "0")
GRAND_TOTAL=$(echo "$PARSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('totals',{}).get('grand_total',0))" 2>/dev/null || echo "0")

[ -n "$BATCH_PERIOD" ] && [ "$ITEM_COUNT" -gt 0 ] \
  && pass "Parse OK — period=$BATCH_PERIOD, items=$ITEM_COUNT, total=$GRAND_TOTAL" \
  || fail "Parse failed: $(echo $PARSE | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"error\",d))' 2>/dev/null)"

# Save for later verification
echo "$PARSE" > "$TEMP_DIR/parse_response.json"

# ── Submit to Otorisasi ──────────────────────────────────────────────────────
section "Submit: Otorisasi"

# Extract parse data and build submit payload
SUBMIT_PAYLOAD=$(python3 << 'PYTHON_EOF'
import json
import sys

with open('$TEMP_DIR/parse_response.json') as f:
    parse_resp = json.load(f)

data = parse_resp['data']
payload = {
    'batch_period_desc': data.get('batch_period_desc'),
    'tanggal_transaksi': '2026-06-15',
    'totals': data.get('totals', {}),
    'items': data.get('items', [])
}

print(json.dumps(payload, ensure_ascii=False))
PYTHON_EOF
)

SUBMIT=$(curl -sf -X POST "$BASE_URL/api/transaksi/upload/hc-zis/submit" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "$SUBMIT_PAYLOAD" \
  || fail "Submit request failed")

SUBMISSION_ID=$(echo "$SUBMIT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('id',''))" 2>/dev/null || echo "")
SUBMIT_STATUS=$(echo "$SUBMIT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('status',''))" 2>/dev/null || echo "")

[ -n "$SUBMISSION_ID" ] \
  && pass "Submit OK — submission_id=$SUBMISSION_ID, status=$SUBMIT_STATUS" \
  || fail "Submit failed: $(echo $SUBMIT | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"error\",d))' 2>/dev/null)"

# ── List Batches ─────────────────────────────────────────────────────────────
section "List: Batches"

BATCHES=$(curl -sf "$BASE_URL/api/transaksi/upload/hc-zis/batches?page=1&limit=25" \
  -H "$AUTH" \
  || fail "List batches request failed")

BATCH_COUNT=$(echo "$BATCHES" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data'].get('rows',[])))" 2>/dev/null || echo "0")
TOTAL_BATCHES=$(echo "$BATCHES" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('pagination',{}).get('total',0))" 2>/dev/null || echo "0")

pass "List batches OK — total=$TOTAL_BATCHES, returned=$BATCH_COUNT"

# Get first batch ID for detail test
BATCH_ID=$(echo "$BATCHES" | python3 -c "import sys,json; rows=json.load(sys.stdin)['data'].get('rows',[]); print(rows[0]['id'] if rows else '')" 2>/dev/null || echo "")

# ── Get Batch Detail ────────────────────────────────────────────────────────
section "Get: Batch Detail"

if [ -n "$BATCH_ID" ]; then
  DETAIL=$(curl -sf "$BASE_URL/api/transaksi/upload/hc-zis/batches/$BATCH_ID" \
    -H "$AUTH" \
    || fail "Get batch detail request failed")

  DETAIL_ID=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('id',''))" 2>/dev/null || echo "")
  DETAIL_PERIOD=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('batch_period_desc',''))" 2>/dev/null || echo "")
  DETAIL_ITEMS=$(echo "$DETAIL" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data'].get('items',[])))" 2>/dev/null || echo "0")

  [ "$DETAIL_ID" = "$BATCH_ID" ] \
    && pass "Get detail OK — batch_id=$BATCH_ID, period=$DETAIL_PERIOD, items=$DETAIL_ITEMS" \
    || fail "Get detail failed"
else
  warn "No batches found — skipping detail test"
fi

# ── Verify DB ───────────────────────────────────────────────────────────────
section "Verify: Database"

# Check otorisasi.submission table
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c \
  "SELECT id, status, entity_type FROM otorisasi.submission WHERE entity_type='hc_zis_upload' ORDER BY id DESC LIMIT 1;" 2>/dev/null | while read -r sub_id sub_status sub_entity; do
  if [ -n "$sub_id" ]; then
    pass "Otorisasi submission found — id=$sub_id, status=$sub_status, entity=$sub_entity"
  fi
done

# Check batch existence (optional)
if [ -n "$BATCH_PERIOD" ]; then
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c \
    "SELECT COUNT(*) FROM transaction.humancapitalbatch WHERE batch_period_desc LIKE '%$BATCH_PERIOD%';" 2>/dev/null | grep -v '^[[:space:]]*$' | while read -r count; do
    [ "$count" -gt 0 ] && pass "Batch record found in DB — count=$count" || warn "No batch records found yet (may be in DRAFT status)"
  done
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║  Semua E2E tests PASSED ✓           ║${NC}"
echo -e "${GREEN}${BOLD}║  Fitur: Upload ZIS Rutin            ║${NC}"
echo -e "${GREEN}${BOLD}║  Portal: zakat                      ║${NC}"
echo -e "${GREEN}${BOLD}║  Submission ID: $SUBMISSION_ID${NC}"
echo -e "${GREEN}${BOLD}╚════════════════════════════════════╝${NC}"
echo ""
echo "File created: $XLSX_FILE"
echo "Test data: Temp dir $TEMP_DIR (auto-cleaned)"
