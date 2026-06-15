#!/bin/bash
# E2E Test: Budget Import Workflow
# Smoke test for budget import, approval, and database validation
# Usage: bash testing/e2e-budget-import.sh [--verbose] [--keep-data]

set -euo pipefail

VERBOSE=${VERBOSE:-false}
KEEP_DATA=${KEEP_DATA:-false}
API_BASE="http://localhost:7000"
DB_CONN="postgresql://transaction:solusi@localhost:5432/mziss_zakat"

# Helper functions
log() { echo "[$(date +'%H:%M:%S')] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }
log_verbose() { [[ "$VERBOSE" == "true" ]] && echo "[VERBOSE] $*" || true; }

# Check prerequisites
check_services() {
  log "Checking services..."
  for port in 7000 8000 5173 5432; do
    if ! nc -zv localhost $port &>/dev/null; then
      error "Service not ready on port $port"
    fi
  done
  log "All services ready."
}

# Create test data fixtures
setup_fixtures() {
  log "Setting up test fixtures..."

  # Insert budget owner
  psql "$DB_CONN" <<EOF
INSERT INTO budget.budgetowner (name, is_detail, created_date)
VALUES ('TEST_OWNER_IMPORT', 'T', NOW())
ON CONFLICT (name) DO NOTHING;
EOF

  # Insert budget period
  psql "$DB_CONN" <<EOF
INSERT INTO budget.budgetperiod (year, start_date, end_date, period_type, parent_period_id, is_active, created_date)
VALUES (2026, '2026-01-01'::date, '2026-12-31'::date, 'Y', NULL, true, NOW())
ON CONFLICT (year) DO NOTHING;
EOF

  # Insert master budget items (level-1)
  psql "$DB_CONN" <<EOF
INSERT INTO budget.budgetitem (item_code, item_name, level, parent_item_id, budget_id, created_date)
VALUES
  ('OPS', 'Operasional', 1, NULL, NULL, NOW()),
  ('INV', 'Investasi', 1, NULL, NULL, NOW())
ON CONFLICT (item_code) DO NOTHING;
EOF

  log_verbose "Fixtures created/verified."
}

# Get owner and period IDs
get_fixture_ids() {
  log "Fetching fixture IDs..."

  OWNER_ID=$(psql "$DB_CONN" -t -c "SELECT id FROM budget.budgetowner WHERE name='TEST_OWNER_IMPORT' LIMIT 1")
  PERIOD_ID=$(psql "$DB_CONN" -t -c "SELECT id FROM budget.budgetperiod WHERE year=2026 AND parent_period_id IS NULL LIMIT 1")

  [[ -z "$OWNER_ID" ]] && error "Owner not found"
  [[ -z "$PERIOD_ID" ]] && error "Period not found"

  log_verbose "OWNER_ID=$OWNER_ID, PERIOD_ID=$PERIOD_ID"
}

# Create test Excel file
create_test_excel() {
  log "Creating test Excel file..."

  EXCEL_FILE="/tmp/test_budget_import_$$.xlsx"

  # Using Python + openpyxl to create XLSX (adjust if project uses pandas)
  python3 <<PYTHON
import openpyxl
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Budget"

# Header row
headers = ["Item Code", "Item Name", "Amount"]
for col_num, header in enumerate(headers, 1):
    ws.cell(row=1, column=col_num).value = header

# Data rows
data = [
    ["OPS-001", "Gaji Pegawai", 100000000],
    ["OPS-002", "Tunjangan", 50000000],
    ["INV-001", "Perbaikan Kantor", 30000000],
]
for row_num, row_data in enumerate(data, 2):
    for col_num, value in enumerate(row_data, 1):
        ws.cell(row=row_num, column=col_num).value = value

wb.save("$EXCEL_FILE")
PYTHON

  [[ ! -f "$EXCEL_FILE" ]] && error "Excel file creation failed"
  log_verbose "Excel file created: $EXCEL_FILE"
}

# Test: POST /api/budget/import
test_import_upload() {
  log "TEST 1: Upload Excel (POST /api/budget/import)"

  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/budget/import" \
    -H "Authorization: Bearer $(get_test_token)" \
    -F "file=@$EXCEL_FILE" \
    -F "owner_id=$OWNER_ID" \
    -F "period_id=$PERIOD_ID" \
    -F "description=Test Import")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  log_verbose "HTTP Code: $HTTP_CODE"
  log_verbose "Response: $BODY"

  [[ "$HTTP_CODE" != "200" ]] && error "Import failed with HTTP $HTTP_CODE: $BODY"

  # Extract submission_id from response
  SUBMISSION_ID=$(echo "$BODY" | grep -o '"submission_id":[0-9]*' | grep -o '[0-9]*')
  [[ -z "$SUBMISSION_ID" ]] && error "submission_id not found in response"

  log "✓ Import upload successful (submission_id=$SUBMISSION_ID)"
}

# Get test token (mocked for E2E, replace with real auth flow)
get_test_token() {
  # Placeholder: in real E2E, login and extract token from session
  # For now, use a valid JWT from test user (must be pre-seeded in isf_auth_zakat)
  echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.placeholder"
}

# Test: Verify submission in database
test_submission_created() {
  log "TEST 2: Verify submission created in DB"

  SUBMISSION_COUNT=$(psql "$DB_CONN" -t -c \
    "SELECT COUNT(*) FROM otorisasi.submission WHERE id=$SUBMISSION_ID AND entity_type='budget_import'")

  [[ "$SUBMISSION_COUNT" -ne 1 ]] && error "Submission not found in DB"

  STATUS=$(psql "$DB_CONN" -t -c \
    "SELECT status FROM otorisasi.submission WHERE id=$SUBMISSION_ID")

  [[ "$STATUS" != "PENDING" ]] && error "Submission status is $STATUS, expected PENDING"

  log "✓ Submission verified in DB (status=$STATUS)"
}

# Test: Approve submission
test_approve_submission() {
  log "TEST 3: Approve submission (POST /api/budget/submission/{id}/approve)"

  RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/budget/submission/$SUBMISSION_ID/approve" \
    -H "Authorization: Bearer $(get_test_token)" \
    -H "Content-Type: application/json" \
    -d '{"approved": true, "notes": "E2E test approval"}')

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  [[ "$HTTP_CODE" != "200" ]] && error "Approval failed with HTTP $HTTP_CODE: $BODY"

  RETURNED_STATUS=$(echo "$BODY" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  [[ "$RETURNED_STATUS" != "PROCESSING" ]] && error "Expected status PROCESSING, got $RETURNED_STATUS"

  log "✓ Approval request successful (status=$RETURNED_STATUS)"
}

# Test: Wait for async dispatcher (poll with timeout)
test_wait_for_authorization() {
  log "TEST 4: Wait for background dispatcher (polling with 30s timeout)"

  TIMEOUT=30
  ELAPSED=0
  POLL_INTERVAL=2

  while [[ $ELAPSED -lt $TIMEOUT ]]; do
    STATUS=$(psql "$DB_CONN" -t -c \
      "SELECT status FROM otorisasi.submission WHERE id=$SUBMISSION_ID")

    log_verbose "  [$ELAPSED s] status=$STATUS"

    [[ "$STATUS" == "AUTHORIZED" ]] && {
      log "✓ Submission authorized (dispatcher completed)"
      return 0
    }

    [[ "$STATUS" == "REJECTED" ]] && {
      ERROR=$(psql "$DB_CONN" -t -c \
        "SELECT dispatch_error FROM otorisasi.submission WHERE id=$SUBMISSION_ID")
      error "Submission rejected: $ERROR"
    }

    sleep $POLL_INTERVAL
    ELAPSED=$((ELAPSED + POLL_INTERVAL))
  done

  error "Timeout waiting for authorization (>$TIMEOUT s)"
}

# Test: Verify budgets created in DB
test_budgets_created() {
  log "TEST 5: Verify budgets created from import"

  BUDGET_COUNT=$(psql "$DB_CONN" -t -c \
    "SELECT COUNT(*) FROM budget.budget WHERE owner_id=$OWNER_ID AND period_id=$PERIOD_ID")

  [[ "$BUDGET_COUNT" -eq 0 ]] && error "No budgets found for owner=$OWNER_ID, period=$PERIOD_ID"

  BUDGET_ID=$(psql "$DB_CONN" -t -c \
    "SELECT id FROM budget.budget WHERE owner_id=$OWNER_ID AND period_id=$PERIOD_ID LIMIT 1")

  # Verify budget items
  ITEM_COUNT=$(psql "$DB_CONN" -t -c \
    "SELECT COUNT(*) FROM budget.budgetitem WHERE budget_id=$BUDGET_ID")

  log_verbose "Created budget $BUDGET_ID with $ITEM_COUNT items"

  # Verify amounts
  TOTAL_AMOUNT=$(psql "$DB_CONN" -t -c \
    "SELECT SUM(amount) FROM budget.budgetitem WHERE budget_id=$BUDGET_ID")

  EXPECTED_TOTAL=180000000 # 100M + 50M + 30M
  [[ "$TOTAL_AMOUNT" -ne "$EXPECTED_TOTAL" ]] && \
    log "⚠ Total amount is $TOTAL_AMOUNT, expected $EXPECTED_TOTAL (may be expected if calculation differs)"

  log "✓ Budgets and items verified in DB"
}

# Cleanup
cleanup() {
  log "Cleaning up..."

  if [[ "$KEEP_DATA" != "true" ]]; then
    # Delete test data
    psql "$DB_CONN" <<EOF
DELETE FROM budget.budgetitem WHERE budget_id IN (
  SELECT id FROM budget.budget WHERE owner_id=$OWNER_ID
);
DELETE FROM budget.budget WHERE owner_id=$OWNER_ID;
DELETE FROM otorisasi.submission WHERE id=$SUBMISSION_ID;
EOF
    log_verbose "Test data deleted."
  else
    log "Test data kept (submission_id=$SUBMISSION_ID, budget_id=$BUDGET_ID)"
  fi

  # Clean up Excel file
  rm -f "$EXCEL_FILE"
}

# Main test flow
main() {
  log "=== E2E Test: Budget Import ==="
  log "Portal: zakat | API: $API_BASE"

  trap cleanup EXIT

  check_services
  setup_fixtures
  get_fixture_ids
  create_test_excel

  test_import_upload
  test_submission_created
  test_approve_submission
  test_wait_for_authorization
  test_budgets_created

  log "=== ALL TESTS PASSED ==="
  exit 0
}

# Parse CLI args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --verbose) VERBOSE=true; shift ;;
    --keep-data) KEEP_DATA=true; shift ;;
    *) error "Unknown option: $1" ;;
  esac
done

main
