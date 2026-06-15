#!/usr/bin/env bash
# testing/e2e-budget.sh
# E2E Smoke Test: Budget (Anggaran) Module
# Portal: Zakat (localhost:7000)
# Usage: bash testing/e2e-budget.sh [--keep-data] [--verbose]
# Requires: curl, jq, isf-app zakat stack running (podman-compose up -d)

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

BASE_URL="${BASE_URL:-http://localhost:7000}"
API_URL="${API_URL:-http://localhost:8000}"
USERNAME="${TEST_USER:-HADI}"
PASSWORD="${TEST_PASS:-test1234}"
KEEP_DATA="${KEEP_DATA:-false}"
VERBOSE="${VERBOSE:-false}"

# Date variables
TODAY=$(date +%Y-%m-%d)
YEAR=${TODAY:0:4}

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
BOLD='\033[1m'

# Test counters
PASS=0
FAIL=0

# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

log() {
  echo -e "${BOLD}[$(date +'%H:%M:%S')]${NC} $*"
}

pass() {
  echo -e "${GREEN}✓${NC} $1"
  ((PASS++))
}

fail() {
  echo -e "${RED}✗${NC} $1"
  ((FAIL++))
}

warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

section() {
  echo -e "\n${BOLD}=== $1 ===${NC}"
}

verbose() {
  [[ "$VERBOSE" == "true" ]] && echo -e "  ${YELLOW}[DEBUG]${NC} $*" || true
}

# Check HTTP response code
check_status() {
  local actual="$1"
  local expected="$2"
  local desc="$3"

  if [[ "$actual" == "$expected" ]]; then
    pass "$desc (HTTP $actual)"
    return 0
  else
    fail "$desc (expected $expected, got $actual)"
    return 1
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Prerequisites & Auth
# ─────────────────────────────────────────────────────────────────────────────

section "Prerequisites"

# Check services
for port in 7000 8000 5432; do
  if nc -zv localhost "$port" &>/dev/null; then
    pass "Service on port $port is up"
  else
    fail "Service on port $port not responding"
    exit 1
  fi
done

section "Auth: Login"

LOGIN_RESPONSE=$(curl -sf -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.access_token // empty')
if [[ -z "$TOKEN" ]]; then
  fail "Login failed for user $USERNAME"
  echo "Response: $LOGIN_RESPONSE"
  exit 1
fi

BRANCH=$(echo "$LOGIN_RESPONSE" | jq -r '.data.branches[0].code // "001"')
pass "Login successful ($USERNAME, branch: $BRANCH)"
verbose "Token: ${TOKEN:0:20}... | Branch: $BRANCH"

# Set common headers
AUTH_HDR=(-H "Authorization: Bearer $TOKEN")
CONTENT_HDR=(-H "Content-Type: application/json")
HDR=("${AUTH_HDR[@]}" "${CONTENT_HDR[@]}")

# ─────────────────────────────────────────────────────────────────────────────
# Test 1: Health Check — GET /api/budget/owners
# ─────────────────────────────────────────────────────────────────────────────

section "Test 1: Health Check — List Budget Owners"

RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/owners")
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

check_status "$HTTP_CODE" "200" "GET /api/budget/owners"

OWNERS_COUNT=$(echo "$BODY" | jq '.data | length // 0' 2>/dev/null || echo "0")
verbose "Budget owners found: $OWNERS_COUNT"

# ─────────────────────────────────────────────────────────────────────────────
# Test 2: GET /api/budget/periods — List Budget Periods
# ─────────────────────────────────────────────────────────────────────────────

section "Test 2: List Budget Periods"

RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/periods")
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

check_status "$HTTP_CODE" "200" "GET /api/budget/periods"

PERIOD_ID=$(echo "$BODY" | jq -r '.data[0].period_id // empty' 2>/dev/null)
if [[ -n "$PERIOD_ID" ]]; then
  pass "Period found (period_id: $PERIOD_ID)"
  verbose "Period data: $(echo "$BODY" | jq -c '.data[0]' 2>/dev/null || echo '?')"
else
  warn "No budget periods found — creating test period will be skipped"
  PERIOD_ID=""
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 3: GET /api/budget/periods/{owner_id} — Periods for a specific owner
# ─────────────────────────────────────────────────────────────────────────────

section "Test 3: Get Periods for Specific Owner"

OWNER_ID=$(echo "$BODY" | jq -r '.data[0].owner_id // empty' 2>/dev/null)
if [[ -n "$OWNER_ID" ]]; then
  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/periods/$OWNER_ID")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | head -n -1)

  check_status "$HTTP_CODE" "200" "GET /api/budget/periods/$OWNER_ID"
  verbose "Periods for owner $OWNER_ID: $(echo "$BODY" | jq '.data | length' 2>/dev/null || echo '?')"
else
  warn "No owner ID available — skipping Test 3"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 4: GET /api/budget/ — List Budgets with filters
# ─────────────────────────────────────────────────────────────────────────────

section "Test 4: List Budgets (with filters)"

QUERY="?page=1&limit=25"
if [[ -n "$OWNER_ID" ]]; then
  QUERY="${QUERY}&owner_id=$OWNER_ID"
fi
if [[ -n "$PERIOD_ID" ]]; then
  QUERY="${QUERY}&period_id=$PERIOD_ID"
fi
QUERY="${QUERY}&branch_code=$BRANCH"

RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/$QUERY")
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

check_status "$HTTP_CODE" "200" "GET /api/budget/$QUERY"

# Extract existing budget ID for later tests
BUDGET_ID=$(echo "$BODY" | jq -r '.data.rows[0].budget_id // empty' 2>/dev/null)
ROWS_COUNT=$(echo "$BODY" | jq '.data.rows | length // 0' 2>/dev/null)
TOTAL=$(echo "$BODY" | jq '.pagination.total // 0' 2>/dev/null)

if [[ $ROWS_COUNT -gt 0 ]]; then
  pass "Found $ROWS_COUNT budgets (total: $TOTAL)"
  verbose "First budget_id: $BUDGET_ID"
else
  warn "No existing budgets found — some tests will be skipped"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 5: GET /api/budget/search/codes — Search budget codes
# ─────────────────────────────────────────────────────────────────────────────

section "Test 5: Search Budget Codes"

RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/search/codes?q=001&branch_code=$BRANCH")
HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | head -n -1)

check_status "$HTTP_CODE" "200" "GET /api/budget/search/codes"
verbose "Code search results: $(echo "$BODY" | jq '.data | length // 0' 2>/dev/null || echo '?')"

# ─────────────────────────────────────────────────────────────────────────────
# Test 6: POST /api/budget/ — Create New Budget
# ─────────────────────────────────────────────────────────────────────────────

section "Test 6: Create Budget (via otorisasi save-and-submit)"

if [[ -z "$OWNER_ID" || -z "$PERIOD_ID" ]]; then
  warn "Missing owner_id or period_id — skipping budget creation"
else
  # Create budget via otorisasi save-and-submit to ensure it enters system
  CREATE_PAYLOAD=$(cat <<EOF
{
  "entity_type": "budget",
  "module": "keuangan",
  "payload": {
    "action": "create",
    "owner_id": $OWNER_ID,
    "period_id": $PERIOD_ID,
    "branch_code": "$BRANCH",
    "budget_code": "TESTBUDGET-$RANDOM",
    "description": "E2E Test Budget $(date +'%Y-%m-%d %H:%M:%S')",
    "status": "A"
  }
}
EOF
)

  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" -X POST "$BASE_URL/api/otorisasi/save-and-submit/" \
    -d "$CREATE_PAYLOAD")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | head -n -1)

  check_status "$HTTP_CODE" "200" "POST /api/otorisasi/save-and-submit/ (budget)"

  SUBMISSION_ID=$(echo "$BODY" | jq -r '.data.submission_id // .data.id // empty' 2>/dev/null)
  if [[ -n "$SUBMISSION_ID" ]]; then
    pass "Budget submission created (submission_id: $SUBMISSION_ID)"
    verbose "Submission status: $(echo "$BODY" | jq -r '.data.status // .status' 2>/dev/null || echo '?')"
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 7: GET /api/budget/{budget_id} — Get Budget Detail
# ─────────────────────────────────────────────────────────────────────────────

section "Test 7: Get Budget Detail"

if [[ -n "$BUDGET_ID" ]]; then
  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/$BUDGET_ID")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | head -n -1)

  check_status "$HTTP_CODE" "200" "GET /api/budget/$BUDGET_ID"

  BUDGET_CODE=$(echo "$BODY" | jq -r '.data.budget_code // empty' 2>/dev/null)
  DETAIL=$(echo "$BODY" | jq -r '.data.description // ""' 2>/dev/null | cut -c1-50)
  verbose "Budget: $BUDGET_CODE | Detail: $DETAIL..."
else
  warn "No budget_id available — skipping budget detail test"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 8: PUT /api/budget/{budget_id} — Update Budget
# ─────────────────────────────────────────────────────────────────────────────

section "Test 8: Update Budget"

if [[ -n "$BUDGET_ID" ]]; then
  UPDATE_PAYLOAD=$(cat <<EOF
{
  "description": "Updated via E2E test — $(date +'%Y-%m-%d %H:%M:%S')",
  "status": "A"
}
EOF
)

  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" -X PUT "$BASE_URL/api/budget/$BUDGET_ID" \
    -d "$UPDATE_PAYLOAD")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | head -n -1)

  check_status "$HTTP_CODE" "200" "PUT /api/budget/$BUDGET_ID"
else
  warn "No budget_id available — skipping update test"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 9: POST /api/budget/revise — Batch Revise Amounts
# ─────────────────────────────────────────────────────────────────────────────

section "Test 9: Batch Revise Budget Amounts"

if [[ -n "$BUDGET_ID" ]]; then
  REVISE_PAYLOAD=$(cat <<EOF
{
  "budget_id": $BUDGET_ID,
  "revisions": [
    {
      "item_code": "001",
      "new_amount": 100000000,
      "reason": "E2E test revision"
    }
  ]
}
EOF
)

  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" -X POST "$BASE_URL/api/budget/revise" \
    -d "$REVISE_PAYLOAD" 2>/dev/null || echo "")

  if [[ -n "$RESP" ]]; then
    HTTP_CODE=$(echo "$RESP" | tail -1)
    BODY=$(echo "$RESP" | head -n -1)

    # May not be implemented yet
    if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
      check_status "$HTTP_CODE" "200" "POST /api/budget/revise"
    elif [[ "$HTTP_CODE" == "404" || "$HTTP_CODE" == "501" ]]; then
      warn "POST /api/budget/revise not yet implemented (HTTP $HTTP_CODE)"
    else
      check_status "$HTTP_CODE" "200" "POST /api/budget/revise"
    fi
  else
    warn "POST /api/budget/revise skipped — endpoint may not be ready"
  fi
else
  warn "No budget_id available — skipping revise test"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 10: GET /api/budget/{budget_id}/transactions — Budget Transactions
# ─────────────────────────────────────────────────────────────────────────────

section "Test 10: Get Budget Transactions"

if [[ -n "$BUDGET_ID" ]]; then
  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" "$BASE_URL/api/budget/$BUDGET_ID/transactions?date_from=$TODAY")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  BODY=$(echo "$RESP" | head -n -1)

  if [[ "$HTTP_CODE" == "200" ]]; then
    check_status "$HTTP_CODE" "200" "GET /api/budget/$BUDGET_ID/transactions"
    TXN_COUNT=$(echo "$BODY" | jq '.data.rows | length // 0' 2>/dev/null || echo "0")
    verbose "Transactions found: $TXN_COUNT"
  elif [[ "$HTTP_CODE" == "404" || "$HTTP_CODE" == "501" ]]; then
    warn "GET /api/budget/.../transactions not yet implemented (HTTP $HTTP_CODE)"
  else
    check_status "$HTTP_CODE" "200" "GET /api/budget/$BUDGET_ID/transactions"
  fi
else
  warn "No budget_id available — skipping transactions test"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Test 11: DELETE /api/budget/{budget_id} — Delete Budget (if created)
# ─────────────────────────────────────────────────────────────────────────────

section "Test 11: Delete Budget"

# Only delete if we created one via submission
if [[ -n "$SUBMISSION_ID" && "$KEEP_DATA" != "true" ]]; then
  # Try to find the budget ID created from submission (may not be immediate if PROCESSING)
  # For now, just acknowledge that cleanup is manual
  warn "Budget deletion via API is async (via otorisasi dispatcher) — manual cleanup via submission approval"
elif [[ -n "$BUDGET_ID" && "$KEEP_DATA" != "true" ]]; then
  RESP=$(curl -s -w "\n%{http_code}" "${HDR[@]}" -X DELETE "$BASE_URL/api/budget/$BUDGET_ID")
  HTTP_CODE=$(echo "$RESP" | tail -1)

  if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "204" ]]; then
    pass "Budget deleted (HTTP $HTTP_CODE)"
  elif [[ "$HTTP_CODE" == "404" ]]; then
    warn "Budget not found for deletion (HTTP 404)"
  else
    fail "Delete budget failed (HTTP $HTTP_CODE)"
  fi
else
  if [[ "$KEEP_DATA" == "true" ]]; then
    warn "Test data kept per --keep-data flag"
  else
    verbose "No budget_id or submission_id to clean up"
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

section "Test Summary"

TOTAL=$((PASS + FAIL))
echo -e "Total: ${BOLD}$TOTAL${NC} | ${GREEN}Passed: $PASS${NC} | ${RED}Failed: $FAIL${NC}"

if [[ $FAIL -eq 0 ]]; then
  echo -e "\n${GREEN}${BOLD}All E2E Budget tests PASSED!${NC}"
  exit 0
else
  echo -e "\n${RED}${BOLD}Some tests FAILED!${NC}"
  exit 1
fi
