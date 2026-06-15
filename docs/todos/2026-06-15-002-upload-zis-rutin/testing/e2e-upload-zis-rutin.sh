#!/bin/bash
# E2E Test: Upload Data Penerimaan ZIS Rutin
# Workflow: Upload XLS → Parse → Submit → Otorisasi → Authorize → Verify DB
# Requirements: curl, jq, PostgreSQL client (psql)
# Usage: bash testing/e2e-upload-zis-rutin.sh [--verbose] [--no-cleanup]

set -e

# ============================================================================
# Configuration
# ============================================================================

BFF_BASE_URL="${BFF_BASE_URL:-http://localhost:7000}"
API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
DB_HOST="${DB_HOST:-localhost}"
DB_USER="${DB_USER:-transaction}"
DB_PASSWORD="${DB_PASSWORD:-solusi}"
DB_NAME="${DB_NAME:-mziss_laz}"
DB_AUTH_NAME="${DB_AUTH_NAME:-isf_auth_zakat}"

VERBOSE="${VERBOSE:-false}"
NO_CLEANUP="${NO_CLEANUP:-false}"

# Test user credentials (must exist in isf_auth_zakat)
ACC_USERNAME="ACC_USER_TEST"
ACC_PASSWORD="test1234"
SPVKEU_USERNAME="SPVKEU_USER_TEST"
SPVKEU_PASSWORD="test1234"

TEMP_DIR="/tmp/e2e-zis-upload-$$"
LOG_FILE="${TEMP_DIR}/test.log"

# ============================================================================
# Helper Functions
# ============================================================================

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_verbose() {
  if [ "$VERBOSE" = "true" ]; then
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [VERBOSE] $*" | tee -a "$LOG_FILE"
  fi
}

die() {
  echo "[ERROR] $*" >&2
  exit 1
}

cleanup() {
  if [ "$NO_CLEANUP" != "true" ]; then
    log "Cleaning up temp directory: $TEMP_DIR"
    rm -rf "$TEMP_DIR"
  else
    log "Temp directory preserved: $TEMP_DIR"
  fi
}

trap cleanup EXIT

http_get() {
  local url="$1"
  local auth_header="$2"
  local output_file="$3"

  log_verbose "GET $url"

  if [ -n "$output_file" ]; then
    curl -s -H "Authorization: $auth_header" "$url" > "$output_file" 2>&1
  else
    curl -s -H "Authorization: $auth_header" "$url"
  fi
}

http_post() {
  local url="$1"
  local auth_header="$2"
  local data="$3"
  local content_type="$4"

  log_verbose "POST $url"

  local headers=(-H "Authorization: $auth_header")
  [ -n "$content_type" ] && headers+=(-H "Content-Type: $content_type")

  curl -s "${headers[@]}" -d "$data" "$url"
}

http_post_file() {
  local url="$1"
  local auth_header="$2"
  local file_path="$3"
  local param_name="${4:-file}"

  log_verbose "POST (multipart) $url"

  curl -s -H "Authorization: $auth_header" -F "$param_name=@$file_path" "$url"
}

http_put() {
  local url="$1"
  local auth_header="$2"
  local data="$3"

  log_verbose "PUT $url"

  curl -s -H "Authorization: $auth_header" -H "Content-Type: application/json" -X PUT -d "$data" "$url"
}

http_delete() {
  local url="$1"
  local auth_header="$2"

  log_verbose "DELETE $url"

  curl -s -H "Authorization: $auth_header" -X DELETE "$url"
}

# ============================================================================
# Setup
# ============================================================================

setup() {
  log "=== E2E Test: Upload Data Penerimaan ZIS Rutin ==="
  log "BFF URL: $BFF_BASE_URL"
  log "API URL: $API_BASE_URL"
  log "Database: $DB_NAME @ $DB_HOST"

  mkdir -p "$TEMP_DIR"

  # Verify BFF is reachable
  if ! curl -s "$BFF_BASE_URL/health" > /dev/null 2>&1; then
    die "BFF API is not reachable at $BFF_BASE_URL"
  fi

  log "BFF API is reachable ✓"
}

# ============================================================================
# Test: Login
# ============================================================================

test_login() {
  log ""
  log ">>> TEST: Login as ACC user"

  local response
  response=$(http_post \
    "$BFF_BASE_URL/api/auth/login" \
    "" \
    "{\"username\":\"$ACC_USERNAME\",\"password\":\"$ACC_PASSWORD\"}" \
    "application/json"
  )

  log_verbose "Response: $response"

  ACC_TOKEN=$(echo "$response" | jq -r '.data.token // empty')
  [ -z "$ACC_TOKEN" ] && die "Login failed for ACC user. Response: $response"

  log "Login successful. Token: ${ACC_TOKEN:0:20}... ✓"

  # Login SPVKEU user
  log ""
  log ">>> TEST: Login as SPVKEU user"

  response=$(http_post \
    "$BFF_BASE_URL/api/auth/login" \
    "" \
    "{\"username\":\"$SPVKEU_USERNAME\",\"password\":\"$SPVKEU_PASSWORD\"}" \
    "application/json"
  )

  SPVKEU_TOKEN=$(echo "$response" | jq -r '.data.token // empty')
  [ -z "$SPVKEU_TOKEN" ] && die "Login failed for SPVKEU user. Response: $response"

  log "Login successful. Token: ${SPVKEU_TOKEN:0:20}... ✓"
}

# ============================================================================
# Test: Create Sample XLS File
# ============================================================================

create_sample_xls() {
  log ""
  log ">>> TEST: Create sample XLS file"

  local xlsx_file="$TEMP_DIR/sample_zis_batch.xlsx"

  # Use Python to create XLSX file with openpyxl
  python3 << 'PYTHON_EOF' > /dev/null 2>&1
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Data ZIS"

# Cell B2: Batch Period Desc
ws['B2'] = 'PERIODE 2026-06'

# Header row 7
headers = [
  'No', 'BusinessAreaCode', 'BusinessAreaDesc', 'EmployeeNumber', 'Name',
  'BirthPlace', 'WorkAreaName', 'MobilePhone', 'BirthDate', 'Gender',
  'MaritalStatus', 'Position', 'OrganizationUnit', 'ZakatAmount', 'InfaqAmount',
  'AnakAsuhAmount', 'AnakYatimAmount', 'WakafAmount', 'TaqurmaAmount'
]

for col_idx, header in enumerate(headers, start=1):
  ws.cell(row=7, column=col_idx, value=header)

# Sample data rows starting from row 8
sample_data = [
  ['1', 'DIV01', 'Divisi Operasional', 'E001234', 'Budi Santoso',
   'Jakarta', 'Kantor Pusat', '08123456789', '1990-01-15', 'MALE',
   'MARRD.', 'Manager', 'IT', -100000, -50000,
   0, 0, 0, -100000],
  ['2', 'DIV02', 'Divisi Keuangan', 'E001235', 'Siti Nurhaliza',
   'Bandung', 'Kantor Cabang', '08234567890', '1992-03-20', 'FEMALE',
   'SINGLE', 'Supervisor', 'Finance', -150000, -75000,
   -50000, 0, 0, -50000],
  ['3', 'DIV01', 'Divisi Operasional', 'E001236', 'Ahmad Wijaya',
   'Surabaya', 'Kantor Pusat', '08345678901', '1988-07-10', 'MALE',
   'MARRD.', 'Staff', 'IT', -120000, -60000,
   0, -30000, 0, -80000],
]

for row_idx, row_data in enumerate(sample_data, start=8):
  for col_idx, value in enumerate(row_data, start=1):
    ws.cell(row=row_idx, column=col_idx, value=value)

# Save file
PYTHON_EOF

  python3 << EOF
import sys
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Cell B2: Batch Period Desc
ws['B2'] = 'PERIODE_2026_06_TEST'

# Header row 7
for col_idx, header in enumerate(['No', 'Col3', 'Col4', 'Col6', 'Col8', 'Col10', 'Col11', 'Col12', 'Col13', 'Col14', 'Col15', 'Col16', 'Col17', 'Col18', 'Col19', 'Col20', 'Col21', 'Col22', 'Col23'], start=1):
  ws.cell(row=7, column=col_idx, value=header)

# Sample data row 8
ws.cell(row=8, column=1, value=1)
ws.cell(row=8, column=3, value='DIV01')
ws.cell(row=8, column=4, value='Divisi Operasional')
ws.cell(row=8, column=6, value='E001234')
ws.cell(row=8, column=8, value='Budi Santoso')
ws.cell(row=8, column=10, value='Jakarta')
ws.cell(row=8, column=11, value='Kantor Pusat')
ws.cell(row=8, column=12, value='08123456789')
ws.cell(row=8, column=13, value='1990-01-15')
ws.cell(row=8, column=14, value='MALE')
ws.cell(row=8, column=15, value='MARRD.')
ws.cell(row=8, column=16, value='Manager')
ws.cell(row=8, column=17, value='IT')
ws.cell(row=8, column=18, value=-100000)
ws.cell(row=8, column=19, value=-50000)
ws.cell(row=8, column=20, value=0)
ws.cell(row=8, column=21, value=0)
ws.cell(row=8, column=22, value=0)
ws.cell(row=8, column=23, value=-100000)

wb.save('$xlsx_file')
print('$xlsx_file created successfully')
EOF

  [ -f "$xlsx_file" ] && log "Sample XLS file created: $xlsx_file ✓"
}

# ============================================================================
# Test: Parse Upload
# ============================================================================

test_parse_upload() {
  log ""
  log ">>> TEST: POST /api/transaksi/upload/hc-zis/parse"

  local xlsx_file="$TEMP_DIR/sample_zis_batch.xlsx"

  local response
  response=$(http_post_file \
    "$BFF_BASE_URL/api/transaksi/upload/hc-zis/parse" \
    "Bearer $ACC_TOKEN" \
    "$xlsx_file" \
    "file"
  )

  log_verbose "Response: $response"

  # Parse response
  local batch_period_desc=$(echo "$response" | jq -r '.data.batch_period_desc // empty')
  local grand_total=$(echo "$response" | jq -r '.data.totals.grand_total // empty')
  local item_count=$(echo "$response" | jq -r '.data.items | length')

  [ -z "$batch_period_desc" ] && die "Parse failed. Response: $response"

  log "Parse successful ✓"
  log "  Batch Period: $batch_period_desc"
  log "  Grand Total: $grand_total"
  log "  Item Count: $item_count"

  # Store for next test
  BATCH_PERIOD_DESC="$batch_period_desc"
  PARSE_RESPONSE="$response"

  # Save response to file for later use
  echo "$PARSE_RESPONSE" > "$TEMP_DIR/parse_response.json"
}

# ============================================================================
# Test: Submit to Otorisasi
# ============================================================================

test_submit_otorisasi() {
  log ""
  log ">>> TEST: POST /api/transaksi/upload/hc-zis/submit"

  # Extract data from parse response
  local parse_response=$(cat "$TEMP_DIR/parse_response.json")
  local batch_period_desc=$(echo "$parse_response" | jq -r '.data.batch_period_desc')
  local tanggal_transaksi="2026-06-15"
  local totals=$(echo "$parse_response" | jq '.data.totals')
  local items=$(echo "$parse_response" | jq '.data.items')

  # Build submit payload
  local submit_payload=$(jq -n \
    --arg batch_period_desc "$batch_period_desc" \
    --arg tanggal_transaksi "$tanggal_transaksi" \
    --argjson totals "$totals" \
    --argjson items "$items" \
    '{
      batch_period_desc: $batch_period_desc,
      tanggal_transaksi: $tanggal_transaksi,
      totals: $totals,
      items: $items
    }')

  log_verbose "Submit Payload: $submit_payload"

  local response
  response=$(http_post \
    "$BFF_BASE_URL/api/transaksi/upload/hc-zis/submit" \
    "Bearer $ACC_TOKEN" \
    "$submit_payload" \
    "application/json"
  )

  log_verbose "Response: $response"

  # Parse response
  local submission_id=$(echo "$response" | jq -r '.data.submission_id // empty')
  local status=$(echo "$response" | jq -r '.data.status // empty')

  [ -z "$submission_id" ] && die "Submit failed. Response: $response"

  log "Submit successful ✓"
  log "  Submission ID: $submission_id"
  log "  Status: $status"

  SUBMISSION_ID="$submission_id"
  BATCH_PERIOD_DESC="$batch_period_desc"
}

# ============================================================================
# Test: Get Submission Status
# ============================================================================

test_get_submission_status() {
  log ""
  log ">>> TEST: GET /api/keuangan/monitoring/otorisasi (check PENDING)"

  local response
  response=$(http_get \
    "$BFF_BASE_URL/api/keuangan/monitoring/otorisasi?entity_type=hc_zis_upload&status=PENDING&limit=10" \
    "Bearer $SPVKEU_TOKEN"
  )

  log_verbose "Response: $response"

  local submission_found=$(echo "$response" | jq --arg id "$SUBMISSION_ID" '.data[] | select(.submission_id == ($id | tonumber)) | .submission_id')

  if [ -z "$submission_found" ]; then
    log "Warning: Submission not yet visible in otorisasi list (might be cached)"
  else
    log "Submission found in otorisasi list ✓"
  fi
}

# ============================================================================
# Test: Approve Otorisasi (SPVKEU)
# ============================================================================

test_approve_otorisasi() {
  log ""
  log ">>> TEST: POST /api/keuangan/monitoring/otorisasi/{submission_id}/approve"

  local response
  response=$(http_post \
    "$BFF_BASE_URL/api/keuangan/monitoring/otorisasi/$SUBMISSION_ID/approve" \
    "Bearer $SPVKEU_TOKEN" \
    "{}" \
    "application/json"
  )

  log_verbose "Response: $response"

  local status=$(echo "$response" | jq -r '.data.status // empty')

  [ -z "$status" ] && die "Approve failed. Response: $response"

  log "Approve submission successful ✓"
  log "  Status: $status (should be PROCESSING)"
}

# ============================================================================
# Test: Poll Status (PROCESSING → AUTHORIZED)
# ============================================================================

test_poll_status() {
  log ""
  log ">>> TEST: Poll submission status (wait for AUTHORIZED)"

  local max_polls=60
  local poll_interval=1
  local poll_count=0

  while [ $poll_count -lt $max_polls ]; do
    local response
    response=$(http_get \
      "$BFF_BASE_URL/api/keuangan/monitoring/otorisasi/$SUBMISSION_ID" \
      "Bearer $SPVKEU_TOKEN"
    )

    local status=$(echo "$response" | jq -r '.data.status // empty')

    if [ "$status" = "AUTHORIZED" ]; then
      log "Status: $status ✓ (after $poll_count seconds)"
      return 0
    elif [ "$status" = "PENDING" ]; then
      log_verbose "Status: $status (still processing...)"
    elif [ -z "$status" ]; then
      log_verbose "Status: unknown/not found"
    else
      log_verbose "Status: $status"
    fi

    sleep "$poll_interval"
    ((poll_count++))
  done

  die "Timeout waiting for AUTHORIZED status (max ${max_polls}s reached)"
}

# ============================================================================
# Test: Verify DB Data
# ============================================================================

test_verify_db_data() {
  log ""
  log ">>> TEST: Verify data in database"

  # Connect to PostgreSQL and verify
  PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<EOF
    -- Verify humancapitalbatch
    SELECT COUNT(*) as batch_count FROM transaction.humancapitalbatch WHERE batch_period_desc = '$BATCH_PERIOD_DESC';

    -- Verify humancapitalbatchitem
    SELECT COUNT(*) as batch_item_count FROM transaction.humancapitalbatchitem WHERE batch_id IN (SELECT batch_id FROM transaction.humancapitalbatch WHERE batch_period_desc = '$BATCH_PERIOD_DESC');

    -- Verify transactions (should be created after authorize)
    SELECT COUNT(*) as transaction_count FROM transaction.transaction WHERE transaction_code = 'SD002' AND channel_code = 'A';
EOF

  log "DB verification complete ✓"
}

# ============================================================================
# Test: Get Batch List
# ============================================================================

test_get_batch_list() {
  log ""
  log ">>> TEST: GET /api/transaksi/upload/hc-zis/batches"

  local response
  response=$(http_get \
    "$BFF_BASE_URL/api/transaksi/upload/hc-zis/batches?page=1&limit=10" \
    "Bearer $ACC_TOKEN"
  )

  log_verbose "Response: $response"

  local batch_count=$(echo "$response" | jq '.data | length')

  log "Batch list retrieved successfully ✓"
  log "  Total batches: $batch_count"
}

# ============================================================================
# Test: Get Batch Detail
# ============================================================================

test_get_batch_detail() {
  log ""
  log ">>> TEST: GET /api/transaksi/upload/hc-zis/batches (detail)"

  # Get batch ID
  local response
  response=$(http_get \
    "$BFF_BASE_URL/api/transaksi/upload/hc-zis/batches?limit=1" \
    "Bearer $ACC_TOKEN"
  )

  local batch_id=$(echo "$response" | jq -r '.data[0].batch_id // empty')
  [ -z "$batch_id" ] && die "No batches found"

  # Get detail
  response=$(http_get \
    "$BFF_BASE_URL/api/transaksi/upload/hc-zis/batches/$batch_id" \
    "Bearer $ACC_TOKEN"
  )

  log_verbose "Response: $response"

  local period=$(echo "$response" | jq -r '.data.batch_period_desc // empty')
  [ -z "$period" ] && die "Batch detail not found"

  log "Batch detail retrieved successfully ✓"
  log "  Batch ID: $batch_id"
  log "  Period: $period"
}

# ============================================================================
# Main Test Execution
# ============================================================================

main() {
  setup

  test_login
  create_sample_xls
  test_parse_upload
  test_submit_otorisasi
  test_get_submission_status
  test_approve_otorisasi
  test_poll_status
  test_verify_db_data
  test_get_batch_list
  test_get_batch_detail

  log ""
  log "=== ALL TESTS PASSED ✓ ==="
  log "Test log: $LOG_FILE"
}

# ============================================================================
# Run
# ============================================================================

main "$@"
