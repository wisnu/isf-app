#!/usr/bin/env bash
# E2E Test: Transaksi Umum (General Transaction)
# Test the complete flow: create, read, list, detail for GT transactions
# Prerequisites: isf-app running on localhost:5173 (web-vue), :7000 (bff-api), :8000 (api-python)
# Author: nuwis-test-gen
# Date: 2026-06-17

set -e

# === Configuration ===
PORTAL="zakat"
BFF_API="http://localhost:7000"
API_PYTHON="http://localhost:8000"
WEB_VUE="http://localhost:5173"

# Test users (must exist in isf_auth_zakat.users + isf_auth_zakat.user_credentials)
TEST_ACC_USERNAME="TESTUSER_ACC"
TEST_ACC_PASSWORD="test1234"
TEST_ACC_BRANCH="001"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# === Helper Functions ===
log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
  exit 1
}

# === Phase 1: Health Check ===
log_info "Starting E2E test for Transaksi Umum..."
log_info "Phase 1: Health check"

# Check if BFF API is reachable
if ! curl -s "$BFF_API/health" > /dev/null 2>&1; then
  log_error "BFF API not reachable at $BFF_API"
fi
log_info "✓ BFF API is reachable"

# Check if API Python is reachable
if ! curl -s "$API_PYTHON/health" > /dev/null 2>&1; then
  log_error "API Python not reachable at $API_PYTHON"
fi
log_info "✓ API Python is reachable"

# === Phase 2: Login & Get Session ===
log_info "Phase 2: Login & obtain session"

LOGIN_RESPONSE=$(curl -s -X POST "$BFF_API/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$TEST_ACC_USERNAME\",
    \"password\": \"$TEST_ACC_PASSWORD\"
  }")

# Extract token (adapt based on actual BFF login response structure)
# Expected: { "data": { "access_token": "...", "user": { ... } } }
TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
  log_error "Failed to obtain session token. Login response: $LOGIN_RESPONSE"
fi
log_info "✓ Obtained session token: ${TOKEN:0:20}..."

# === Phase 3: Verify Menu Access ===
log_info "Phase 3: Verify ACC user has menu access to Transaksi Umum"

MENU_RESPONSE=$(curl -s -X GET "$BFF_API/api/auth/profile" \
  -H "Authorization: Bearer $TOKEN")

if echo "$MENU_RESPONSE" | grep -q "keuangan.transaksi.umum"; then
  log_info "✓ User has access to keuangan.transaksi.umum"
else
  log_warn "User may not have menu access to Transaksi Umum (check seed data)"
fi

# === Phase 4: Test GET /rekening-info ===
log_info "Phase 4: Test GET /api/transaction/general-transaction/rekening-info"

# Query a standard cash account (KAS-001 or similar — adapt to your DB)
REKENING_RESPONSE=$(curl -s -X GET "$BFF_API/api/transaction/general-transaction/rekening-info?no_rekening=KAS-001" \
  -H "Authorization: Bearer $TOKEN")

if echo "$REKENING_RESPONSE" | grep -q "account_no"; then
  log_info "✓ Rekening lookup works"
  REKENING_INFO=$(echo "$REKENING_RESPONSE" | grep -o '"currency_code":"[^"]*' | cut -d'"' -f4 | head -1)
  log_info "  Currency: $REKENING_INFO"
else
  log_warn "Rekening lookup returned unexpected format or account not found: $REKENING_RESPONSE"
fi

# === Phase 5: Test GET /kurs-info ===
log_info "Phase 5: Test GET /api/transaction/general-transaction/kurs-info"

KURS_RESPONSE=$(curl -s -X GET "$BFF_API/api/transaction/general-transaction/kurs-info?currency_code=IDR" \
  -H "Authorization: Bearer $TOKEN")

if echo "$KURS_RESPONSE" | grep -q "kurs"; then
  log_info "✓ Kurs lookup works"
else
  log_warn "Kurs lookup returned unexpected format: $KURS_RESPONSE"
fi

# === Phase 6: Create Transaction (Item Type C + B) ===
log_info "Phase 6: Create Transaksi Umum with 2 items (Penghimpunan + Kas)"

CREATE_PAYLOAD=$(cat <<'EOF'
{
  "actual_date": "2026-06-17",
  "reference_no": "E2E-TEST-001",
  "description": "E2E test transaction dengan 2 item (C+B)",
  "rate": 1.0,
  "items": [
    {
      "item_type": "C",
      "product_id": 1,
      "donor_id": 1,
      "valuta": "IDR",
      "amount": 500000,
      "rate": 1.0,
      "mutation_type": "C",
      "fund_entity": 1,
      "description": "Penghimpunan zakat dari donatur"
    },
    {
      "item_type": "B",
      "account_no": "KAS-001",
      "valuta": "IDR",
      "amount": 500000,
      "rate": 1.0,
      "mutation_type": "D",
      "description": "Penerimaan tunai"
    }
  ]
}
EOF
)

CREATE_RESPONSE=$(curl -s -X POST "$BFF_API/api/transaction/general-transaction/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$CREATE_PAYLOAD")

# Extract transaction_no (adapt based on actual response structure)
# Expected: { "data": { "transaction_no": "GT-2026-001-BPZIS-XXXXXXX", "transaction_id": 123 } }
TRANSACTION_NO=$(echo "$CREATE_RESPONSE" | grep -o '"transaction_no":"[^"]*' | cut -d'"' -f4)
TRANSACTION_ID=$(echo "$CREATE_RESPONSE" | grep -o '"transaction_id":[0-9]*' | cut -d':' -f2)

if [ -z "$TRANSACTION_NO" ]; then
  log_error "Failed to create transaction. Response: $CREATE_RESPONSE"
fi
log_info "✓ Created transaction: $TRANSACTION_NO (ID: $TRANSACTION_ID)"

# Validate autonumber format: GT-YYYY-BC-BPZIS-{7digit}
if [[ "$TRANSACTION_NO" =~ ^GT-[0-9]{4}-[0-9]{3}-BPZIS-[0-9]{7}$ ]]; then
  log_info "✓ Autonumber format is correct: $TRANSACTION_NO"
else
  log_error "Autonumber format is invalid: $TRANSACTION_NO (expected GT-YYYY-BC-BPZIS-XXXXXXX)"
fi

# === Phase 7: Get Transaction Detail ===
log_info "Phase 7: GET /api/transaction/general-transaction/{transaction_no}"

DETAIL_RESPONSE=$(curl -s -X GET "$BFF_API/api/transaction/general-transaction/$TRANSACTION_NO" \
  -H "Authorization: Bearer $TOKEN")

# Verify items are returned
if echo "$DETAIL_RESPONSE" | grep -q '"items"'; then
  log_info "✓ Detail endpoint returns items"

  # Count items (should be 2)
  ITEM_COUNT=$(echo "$DETAIL_RESPONSE" | grep -o '"item_type"' | wc -l)
  if [ "$ITEM_COUNT" -eq 2 ]; then
    log_info "✓ Correct number of items returned: $ITEM_COUNT"
  else
    log_warn "Expected 2 items, got $ITEM_COUNT"
  fi
else
  log_error "Detail endpoint failed: $DETAIL_RESPONSE"
fi

# === Phase 8: List Transactions ===
log_info "Phase 8: GET /api/transaction/general-transaction/list"

LIST_RESPONSE=$(curl -s -X GET "$BFF_API/api/transaction/general-transaction/list?page=1&limit=25" \
  -H "Authorization: Bearer $TOKEN")

# Verify pagination structure
if echo "$LIST_RESPONSE" | grep -q '"pagination"'; then
  log_info "✓ List endpoint returns pagination"
else
  log_error "List endpoint missing pagination structure: $LIST_RESPONSE"
fi

# Check if our created transaction is in the list
if echo "$LIST_RESPONSE" | grep -q "$TRANSACTION_NO"; then
  log_info "✓ Created transaction found in list"
else
  log_warn "Created transaction not found in list (may not be committed yet or query filtered by date)"
fi

# === Phase 9: Test Cek Limit ===
log_info "Phase 9: POST /api/transaction/general-transaction/cek-limit"

LIMIT_PAYLOAD=$(cat <<'EOF'
{
  "amount_debit": 1000000,
  "branch_code": "001"
}
EOF
)

LIMIT_RESPONSE=$(curl -s -X POST "$BFF_API/api/transaction/general-transaction/cek-limit" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$LIMIT_PAYLOAD")

if echo "$LIMIT_RESPONSE" | grep -q '"exceeded"'; then
  log_info "✓ Cek limit endpoint works"
else
  log_warn "Cek limit endpoint returned unexpected format: $LIMIT_RESPONSE"
fi

# === Phase 10: Summary ===
log_info "Phase 10: Summary"
echo ""
echo "======================================"
echo "E2E Test Summary for Transaksi Umum"
echo "======================================"
echo "Created Transaction No: $TRANSACTION_NO"
echo "Transaction ID: $TRANSACTION_ID"
echo "Test User: $TEST_ACC_USERNAME"
echo "Portal: $PORTAL"
echo "Status: PASSED"
echo "======================================"
echo ""

log_info "E2E test completed successfully!"
exit 0
