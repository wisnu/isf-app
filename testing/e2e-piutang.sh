#!/bin/bash

################################################################################
# E2E Smoke Test: Piutang (Pinjam & Bayar)
# Tests: CRUD operations, approval flow, debitur lookup
# Portal: zakat
# Date: 2026-06-17
################################################################################

set -e

# Configuration
API_BASE="http://localhost:7000"
AUTH_HEADER_ZAKAT="Authorization: Bearer ${TOKEN_ZAKAT:-test-token-zakat}"
BRANCH_ID="${BRANCH_ID:-1}"
PORTAL="${PORTAL:-zakat}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TESTS_PASSED=0
TESTS_FAILED=0

################################################################################
# Helper Functions
################################################################################

log_test() {
  echo -e "${YELLOW}TEST: $1${NC}"
}

log_success() {
  echo -e "${GREEN}✓ PASS: $1${NC}"
  ((TESTS_PASSED++))
}

log_error() {
  echo -e "${RED}✗ FAIL: $1${NC}"
  ((TESTS_FAILED++))
}

check_response() {
  local response=$1
  local expected_status=$2
  local test_name=$3

  local http_status=$(echo "$response" | tail -n1)

  if [[ "$http_status" == "$expected_status" ]]; then
    log_success "$test_name (HTTP $http_status)"
    return 0
  else
    log_error "$test_name (expected $expected_status, got $http_status)"
    echo "Response body:"
    echo "$response" | head -n -1
    return 1
  fi
}

################################################################################
# Test 1: Lookup Debitur (Karyawan + Non-Karyawan)
################################################################################

test_lookup_debitur() {
  log_test "GET /api/transaction/piutang/debitur/ - Lookup debitur"

  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/debitur/?q=&limit=10")

  check_response "$response" "200" "Debitur lookup"

  body=$(echo "$response" | head -n -1)

  # Verify response structure
  if echo "$body" | grep -q '"debtorid"'; then
    log_success "Debitur response has debtorid field"
  else
    log_error "Debitur response missing debtorid field"
  fi

  if echo "$body" | grep -q '"debtortype"'; then
    log_success "Debitur response has debtortype field (E|X)"
  else
    log_error "Debitur response missing debtortype field"
  fi
}

################################################################################
# Test 2: Create Piutang - Pinjam (EAR)
################################################################################

test_create_piutang_pinjam() {
  log_test "POST /api/transaction/piutang/ - Create Piutang (Pinjam/EAR)"

  # Sample payload - EAR (Pinjam via Kas)
  payload=$(cat <<'EOF'
{
  "actualdate": "2026-06-17",
  "transactiontype": "P",
  "channeltype": "C",
  "cashaccountno": "KAS-001",
  "debtorid": "E0001",
  "amount": 3000000.00,
  "referenceno": "CHK-E001",
  "description": "Pinjaman modal kerja karyawan",
  "casher": "RAIS"
}
EOF
)

  response=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "$AUTH_HEADER_ZAKAT" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$API_BASE/api/transaction/piutang/")

  check_response "$response" "201" "Create Piutang Pinjam (EAR)"

  body=$(echo "$response" | head -n -1)

  # Verify critical fields in response
  if echo "$body" | grep -q '"transactionno"'; then
    log_success "Response has transactionno (auto-generated)"
    PIUTANG_NO=$(echo "$body" | grep -o '"transactionno":"[^"]*' | head -1 | cut -d'"' -f4)
    echo "  → TransactionNo: $PIUTANG_NO"
  else
    log_error "Response missing transactionno"
  fi

  if echo "$body" | grep -q '"status"'; then
    status=$(echo "$body" | grep -o '"status":"[^"]*' | head -1 | cut -d'"' -f4)
    log_success "Response has status: $status"

    if [[ "$status" == "AUTHORIZED" ]]; then
      log_success "Amount <= limit: auto-approved (AUTHORIZED)"
    elif [[ "$status" == "PENDING" ]]; then
      log_success "Amount > limit: pending manual approval (PENDING)"
    else
      log_error "Unexpected status: $status"
    fi
  else
    log_error "Response missing status"
  fi

  if echo "$body" | grep -q '"transactiontype":"P"'; then
    log_success "TransactionType correctly set to P (Pinjam)"
  else
    log_error "TransactionType not P"
  fi
}

################################################################################
# Test 3: Create Piutang - Bayar (PEAR)
################################################################################

test_create_piutang_bayar() {
  log_test "POST /api/transaction/piutang/ - Create Piutang (Bayar/PEAR)"

  # Sample payload - PEAR (Bayar via Ledger)
  payload=$(cat <<'EOF'
{
  "actualdate": "2026-06-17",
  "transactiontype": "B",
  "channeltype": "G",
  "glaccount": "101000",
  "debtorid": "E0001",
  "amount": 1000000.00,
  "referenceno": "BYR-E001",
  "description": "Pembayaran piutang karyawan",
  "casher": "RAIS"
}
EOF
)

  response=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "$AUTH_HEADER_ZAKAT" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$API_BASE/api/transaction/piutang/")

  check_response "$response" "201" "Create Piutang Bayar (PEAR)"

  body=$(echo "$response" | head -n -1)

  if echo "$body" | grep -q '"transactiontype":"B"'; then
    log_success "TransactionType correctly set to B (Bayar)"
  else
    log_error "TransactionType not B"
  fi

  if echo "$body" | grep -q '"transactionno"'; then
    log_success "Bayar transaction has transactionno"
  fi
}

################################################################################
# Test 4: Create Piutang - External Debtor
################################################################################

test_create_piutang_external() {
  log_test "POST /api/transaction/piutang/ - Create Piutang (Non-Karyawan/X)"

  # Sample payload - EAR untuk non-karyawan (ExternalDebtor)
  payload=$(cat <<'EOF'
{
  "actualdate": "2026-06-17",
  "transactiontype": "P",
  "channeltype": "C",
  "cashaccountno": "KAS-001",
  "debtorid": "X0001",
  "amount": 5000000.00,
  "referenceno": "CHK-X001",
  "description": "Pinjaman untuk PT ABC Jaya",
  "casher": "RAIS"
}
EOF
)

  response=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "$AUTH_HEADER_ZAKAT" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$API_BASE/api/transaction/piutang/")

  check_response "$response" "201" "Create Piutang External Debtor"

  body=$(echo "$response" | head -n -1)

  if echo "$body" | grep -q '"debtortype":"X"'; then
    log_success "DebtorType correctly set to X (Non-Karyawan)"
  fi
}

################################################################################
# Test 5: List Piutang with Pagination
################################################################################

test_list_piutang() {
  log_test "GET /api/transaction/piutang/ - List piutang dengan pagination"

  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/?page=1&limit=25")

  check_response "$response" "200" "List Piutang"

  body=$(echo "$response" | head -n -1)

  # Verify pagination structure
  if echo "$body" | grep -q '"pagination"'; then
    log_success "Response has pagination object"

    if echo "$body" | grep -q '"total"'; then
      log_success "Pagination has total count"
    fi

    if echo "$body" | grep -q '"total_pages"'; then
      log_success "Pagination has total_pages"
    fi
  else
    log_error "Response missing pagination object"
  fi

  # Verify data structure
  if echo "$body" | grep -q '"rows"'; then
    log_success "Response has rows array"

    # Count rows
    row_count=$(echo "$body" | grep -o '"transactionno"' | wc -l)
    echo "  → Found $row_count transaction(s) in result"
  else
    log_error "Response missing rows array"
  fi
}

################################################################################
# Test 6: Filter Piutang by Type
################################################################################

test_filter_piutang_by_type() {
  log_test "GET /api/transaction/piutang/ - Filter by transaction_type (P/B)"

  # Test filter Pinjam (P)
  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/?transaction_type=P&page=1&limit=25")

  check_response "$response" "200" "Filter Pinjam (P)"

  # Test filter Bayar (B)
  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/?transaction_type=B&page=1&limit=25")

  check_response "$response" "200" "Filter Bayar (B)"
}

################################################################################
# Test 7: Filter Piutang by Debtor Type
################################################################################

test_filter_piutang_by_debtor_type() {
  log_test "GET /api/transaction/piutang/ - Filter by debtor_type (E/X)"

  # Test filter Karyawan (E)
  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/?debtor_type=E&page=1&limit=25")

  check_response "$response" "200" "Filter Karyawan (E)"

  # Test filter Non-Karyawan (X)
  response=$(curl -s -w "\n%{http_code}" \
    -H "$AUTH_HEADER_ZAKAT" \
    "$API_BASE/api/transaction/piutang/?debtor_type=X&page=1&limit=25")

  check_response "$response" "200" "Filter Non-Karyawan (X)"
}

################################################################################
# Test 8: Validation - Missing Required Fields
################################################################################

test_validation_required_fields() {
  log_test "POST /api/transaction/piutang/ - Validation: missing required fields"

  # Missing amount
  payload=$(cat <<'EOF'
{
  "actualdate": "2026-06-17",
  "transactiontype": "P",
  "channeltype": "C",
  "cashaccountno": "KAS-001",
  "debtorid": "E0001"
}
EOF
)

  response=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "$AUTH_HEADER_ZAKAT" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$API_BASE/api/transaction/piutang/")

  http_status=$(echo "$response" | tail -n1)

  if [[ "$http_status" == "422" ]]; then
    log_success "Validation error for missing amount (422)"
  else
    log_error "Expected 422 for missing amount, got $http_status"
  fi
}

################################################################################
# Test 9: Validation - Invalid Amount
################################################################################

test_validation_amount() {
  log_test "POST /api/transaction/piutang/ - Validation: amount <= 0"

  payload=$(cat <<'EOF'
{
  "actualdate": "2026-06-17",
  "transactiontype": "P",
  "channeltype": "C",
  "cashaccountno": "KAS-001",
  "debtorid": "E0001",
  "amount": -1000.00
}
EOF
)

  response=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "$AUTH_HEADER_ZAKAT" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$API_BASE/api/transaction/piutang/")

  http_status=$(echo "$response" | tail -n1)

  if [[ "$http_status" == "422" ]]; then
    log_success "Validation error for negative amount (422)"
  else
    log_error "Expected 422 for negative amount, got $http_status"
  fi
}

################################################################################
# Test 10: Auth - Missing Token
################################################################################

test_auth_missing_token() {
  log_test "GET /api/transaction/piutang/ - Auth: missing token"

  response=$(curl -s -w "\n%{http_code}" \
    "$API_BASE/api/transaction/piutang/")

  http_status=$(echo "$response" | tail -n1)

  if [[ "$http_status" == "401" ]]; then
    log_success "Unauthorized without token (401)"
  else
    log_error "Expected 401 without token, got $http_status"
  fi
}

################################################################################
# Main Test Suite
################################################################################

main() {
  echo "========================================"
  echo "E2E Smoke Test: Piutang (Pinjam & Bayar)"
  echo "Portal: $PORTAL"
  echo "API Base: $API_BASE"
  echo "========================================"
  echo

  # Run tests
  test_lookup_debitur
  echo

  test_create_piutang_pinjam
  echo

  test_create_piutang_bayar
  echo

  test_create_piutang_external
  echo

  test_list_piutang
  echo

  test_filter_piutang_by_type
  echo

  test_filter_piutang_by_debtor_type
  echo

  test_validation_required_fields
  echo

  test_validation_amount
  echo

  test_auth_missing_token
  echo

  # Summary
  echo "========================================"
  echo "Test Summary"
  echo "========================================"
  echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
  echo -e "${RED}Failed: $TESTS_FAILED${NC}"
  echo

  if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
  else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
  fi
}

main "$@"
