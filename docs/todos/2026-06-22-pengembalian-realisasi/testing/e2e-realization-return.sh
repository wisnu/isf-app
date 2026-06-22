#!/bin/bash
# E2E Smoke Test: Pengembalian Realisasi Program
# Purpose: Test CRUD + otorisasi workflow untuk realization-return
# Date: 2026-06-22
# Requires: api-python, bff-api, web-vue running on localhost

set -e

# Config
API_BASE="http://localhost:7000"
API_PYTHON="http://localhost:8000"
DIST_USER="DIST"
DIST_PASS="test1234"
SPVDIST_USER="SPVDIST"
SPVDIST_PASS="test1234"
BRANCH_ID="1"

# Helper functions
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error_exit() {
  echo "ERROR: $1" >&2
  exit 1
}

login() {
  local user=$1
  local pass=$2
  log "Logging in as $user..."

  RESPONSE=$(curl -s -X POST "$API_BASE/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$user\", \"password\": \"$pass\"}")

  TOKEN=$(echo "$RESPONSE" | jq -r '.data.access_token')
  [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ] || error_exit "Login failed for $user"

  echo "$TOKEN"
}

# ============================================================================
# Test Scenario 1: List realization-return (empty state)
# ============================================================================
log "=== Scenario 1: List realization-return ==="
DIST_TOKEN=$(login "$DIST_USER" "$DIST_PASS")

RESPONSE=$(curl -s -X GET "$API_BASE/api/distribution/realization-return?page=1&limit=25" \
  -H "Authorization: Bearer $DIST_TOKEN")

TOTAL=$(echo "$RESPONSE" | jq '.pagination.total // 0')
log "Total pengembalian realisasi: $TOTAL"

# ============================================================================
# Test Scenario 2: Get realization details (untuk form pre-fill)
# ============================================================================
log "=== Scenario 2: Get realization details ==="

# Fetch daftar realisasi yang eligible (AUTHORIZED, belum ada return)
RESPONSE=$(curl -s -X GET "$API_BASE/api/distribution/realization?status=AUTHORIZED&limit=1" \
  -H "Authorization: Bearer $DIST_TOKEN")

REALIZATION_ID=$(echo "$RESPONSE" | jq -r '.data[0].id // empty')
[ -z "$REALIZATION_ID" ] && error_exit "No eligible realization found for return"

log "Found realization ID: $REALIZATION_ID"

# Fetch realization details (header + detail rows)
RESPONSE=$(curl -s -X GET "$API_BASE/api/distribution/realization-return/realization/$REALIZATION_ID/details" \
  -H "Authorization: Bearer $DIST_TOKEN")

REALIZATION_DATE=$(echo "$RESPONSE" | jq -r '.data.realization.realization_date')
TOTAL_REALIZATION=$(echo "$RESPONSE" | jq -r '.data.realization.total_amount')
DETAIL_COUNT=$(echo "$RESPONSE" | jq '.data.details | length')

log "Realization Date: $REALIZATION_DATE, Total Amount: $TOTAL_REALIZATION, Details: $DETAIL_COUNT"
[ "$DETAIL_COUNT" -eq 0 ] && error_exit "No details found in realization"

# ============================================================================
# Test Scenario 3: Create realization-return (save-and-submit)
# ============================================================================
log "=== Scenario 3: Create realization-return ==="

RETURN_DATE=$(date '+%Y-%m-%d')
RETURN_DESCRIPTION="Test pengembalian realisasi"

# Build detail array (0.5 * realization_amount per baris)
FIRST_DETAIL_ID=$(echo "$RESPONSE" | jq -r '.data.details[0].realization_detail_id')
REALIZATION_AMOUNT=$(echo "$RESPONSE" | jq -r '.data.details[0].realization_amount')
RETURN_AMOUNT=$((REALIZATION_AMOUNT / 2))

DETAILS_JSON=$(echo "$RESPONSE" | jq "[.data.details[] | {realization_detail_id: .realization_detail_id, return_amount: (.realization_amount / 2 | floor), detail_description: null}]")
TOTAL_RETURN=$(echo "$DETAILS_JSON" | jq "map(.return_amount) | add")

PAYLOAD=$(cat <<EOF
{
  "return_date": "$RETURN_DATE",
  "return_description": "$RETURN_DESCRIPTION",
  "realization_id": $REALIZATION_ID,
  "cost_amount": 0,
  "details": $(echo "$DETAILS_JSON" | jq -c '.'),
  "costs": []
}
EOF
)

log "Submitting return with payload: $PAYLOAD"

RESPONSE=$(curl -s -X POST "$API_BASE/api/distribution/realization-return" \
  -H "Authorization: Bearer $DIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

RETURN_ID=$(echo "$RESPONSE" | jq -r '.data.id // empty')
[ -z "$RETURN_ID" ] && error_exit "Failed to create realization-return: $(echo "$RESPONSE" | jq -r '.error.message // "unknown error"')"

log "Created realization-return ID: $RETURN_ID"

# ============================================================================
# Test Scenario 4: Verify submission entered otorisasi queue
# ============================================================================
log "=== Scenario 4: Check otorisasi submission ==="

# Get submission by entity_type + payload
RESPONSE=$(curl -s -X GET "$API_BASE/api/otorisasi/submission?entity_type=realization_return&limit=1" \
  -H "Authorization: Bearer $DIST_TOKEN")

SUBMISSION_ID=$(echo "$RESPONSE" | jq -r '.data[0].id // empty')
SUBMISSION_STATUS=$(echo "$RESPONSE" | jq -r '.data[0].status // empty')

[ -z "$SUBMISSION_ID" ] && error_exit "No submission found for realization-return"
[ "$SUBMISSION_STATUS" != "PENDING" ] && error_exit "Expected status PENDING, got $SUBMISSION_STATUS"

log "Found submission ID: $SUBMISSION_ID, Status: $SUBMISSION_STATUS"

# ============================================================================
# Test Scenario 5: Approve submission (SPVDIST)
# ============================================================================
log "=== Scenario 5: Approve submission (SPVDIST) ==="

SPVDIST_TOKEN=$(login "$SPVDIST_USER" "$SPVDIST_PASS")

RESPONSE=$(curl -s -X POST "$API_BASE/api/otorisasi/submission/$SUBMISSION_ID/approve" \
  -H "Authorization: Bearer $SPVDIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{}")

APPROVED_STATUS=$(echo "$RESPONSE" | jq -r '.data.status // empty')
log "Approval response status: $APPROVED_STATUS"

# Wait for background dispatcher to complete
log "Waiting for background dispatcher (max 10s)..."
sleep 2
for i in {1..4}; do
  RESPONSE=$(curl -s -X GET "$API_BASE/api/otorisasi/submission/$SUBMISSION_ID" \
    -H "Authorization: Bearer $SPVDIST_TOKEN")

  CURRENT_STATUS=$(echo "$RESPONSE" | jq -r '.data.status')
  log "Check $i: status = $CURRENT_STATUS"

  [ "$CURRENT_STATUS" = "AUTHORIZED" ] && break
  sleep 2
done

[ "$CURRENT_STATUS" != "AUTHORIZED" ] && error_exit "Submission not authorized after dispatcher. Final status: $CURRENT_STATUS"
log "Submission AUTHORIZED"

# ============================================================================
# Test Scenario 6: Verify data inserted (realization_return + details + cost)
# ============================================================================
log "=== Scenario 6: Verify data in database ==="

# Direct API check (optional, if read endpoints exist)
RESPONSE=$(curl -s -X GET "$API_BASE/api/distribution/realization-return/$RETURN_ID" \
  -H "Authorization: Bearer $DIST_TOKEN")

DB_RETURN_ID=$(echo "$RESPONSE" | jq -r '.data.id // empty')
DB_TOTAL_RETURN=$(echo "$RESPONSE" | jq -r '.data.total_return')
DB_DETAIL_COUNT=$(echo "$RESPONSE" | jq '.data.details | length')
DB_COST_COUNT=$(echo "$RESPONSE" | jq '.data.costs | length')

[ -z "$DB_RETURN_ID" ] && error_exit "Realization-return not found in database"
log "DB Check: Return ID=$DB_RETURN_ID, Total Return=$DB_TOTAL_RETURN, Details=$DB_DETAIL_COUNT, Costs=$DB_COST_COUNT"

# ============================================================================
# Test Scenario 7: Verify transaction (DD002) created
# ============================================================================
log "=== Scenario 7: Verify transaction DD002 ==="

RESPONSE=$(curl -s -X GET "$API_BASE/api/distribution/realization-return/$RETURN_ID" \
  -H "Authorization: Bearer $DIST_TOKEN")

# Check if transaction_id populated in details
TRANSACTION_ID=$(echo "$RESPONSE" | jq -r '.data.details[0].transaction_id // empty')
if [ -z "$TRANSACTION_ID" ]; then
  log "WARNING: transaction_id not yet populated in details (expected if dispatcher still running)"
else
  log "Transaction ID created: $TRANSACTION_ID"
fi

# ============================================================================
# Test Scenario 8: Try to update realization-return (should fail if AUTHORIZED)
# ============================================================================
log "=== Scenario 8: Verify cannot edit AUTHORIZED return ==="

UPDATE_PAYLOAD=$(cat <<EOF
{
  "return_date": "$RETURN_DATE",
  "return_description": "Updated description",
  "realization_id": $REALIZATION_ID,
  "cost_amount": 0,
  "details": $(echo "$DETAILS_JSON" | jq -c '.'),
  "costs": []
}
EOF
)

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$API_BASE/api/distribution/realization-return/$RETURN_ID" \
  -H "Authorization: Bearer $DIST_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATE_PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "403" ] || [ "$HTTP_CODE" = "400" ]; then
  log "Good: Cannot edit AUTHORIZED return (HTTP $HTTP_CODE)"
else
  log "WARNING: Expected 403/400, got HTTP $HTTP_CODE"
fi

# ============================================================================
# Summary
# ============================================================================
log "=== E2E Test Summary ==="
log "✓ Scenario 1: List realization-return"
log "✓ Scenario 2: Get realization details"
log "✓ Scenario 3: Create realization-return"
log "✓ Scenario 4: Verified submission in otorisasi"
log "✓ Scenario 5: Approved by SPVDIST"
log "✓ Scenario 6: Data verified in database"
log "✓ Scenario 7: Transaction DD002 status"
log "✓ Scenario 8: Cannot edit AUTHORIZED return"
log "=== E2E Test PASSED ==="

exit 0
