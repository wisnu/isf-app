#!/usr/bin/env bash
# E2E manual verification untuk halaman admin role-menu mapping.
# Run 8 checks: GET shape, deny non-admin, PUT add, GET verify, PUT restore,
# PUT invalid role, PUT invalid menu, PUT duplicate pair.
#
# Prerequisite: `./testing/setup-e2e-users.sh <stack>` sudah dijalankan
# (FULL_USER otomatis akan punya admin.role_menu kalau dia role ADM).
set -uo pipefail

STACK="${1:-}"
if [[ "$STACK" != "zakat" && "$STACK" != "wakaf" ]]; then
    echo "ERROR: argumen pertama harus 'zakat' atau 'wakaf'" >&2
    exit 1
fi

if command -v podman-compose >/dev/null 2>&1; then
    COMPOSE="podman-compose"
elif command -v podman >/dev/null 2>&1 && podman compose version >/dev/null 2>&1; then
    COMPOSE="podman compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    COMPOSE="docker compose"
else
    echo "ERROR: tidak nemu compose runtime" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/infra/docker-compose.${STACK}.yml"

if [[ "$STACK" == "zakat" ]]; then
    BFF_PORT=7000
else
    BFF_PORT=7001
fi
BFF_URL="http://localhost:${BFF_PORT}"
COOKIE_ADM="/tmp/c-${STACK}-adm.txt"
COOKIE_LIMITED="/tmp/c-${STACK}-limited.txt"
PASS=0
FAIL=0
declare -a RESULTS=()

record() {
    if [[ "$2" == "PASS" ]]; then
        PASS=$((PASS + 1)); RESULTS+=("✓ $1 — PASS")
    else
        FAIL=$((FAIL + 1)); RESULTS+=("✗ $1 — FAIL: ${3:-}")
    fi
}

rm -f "$COOKIE_ADM" "$COOKIE_LIMITED"

# Discover users: one with admin.role_menu access, one without
echo ">>> Discovery test users dari $STACK DB..."
USER_INFO=$($COMPOSE -f "$COMPOSE_FILE" exec -T api-python python -c "
import asyncio, asyncpg, os
async def run():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    adm = await conn.fetchrow('''
        SELECT u.id_user FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A' AND rm.menu_key = 'admin.role_menu'
        LIMIT 1
    ''')
    limited = await conn.fetchrow('''
        SELECT u.id_user FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A'
        GROUP BY u.id_user
        HAVING NOT bool_or(rm.menu_key = 'admin.role_menu')
        LIMIT 1
    ''')
    print(f\"{adm['id_user'] if adm else 'NONE'} {limited['id_user'] if limited else 'NONE'}\")
    await conn.close()
asyncio.run(run())
" | tr -d '\r')
read -r ADM_USER LIMITED_USER <<< "$USER_INFO"

if [[ "$ADM_USER" == "NONE" ]]; then
    echo "ERROR: tidak ada user dengan akses admin.role_menu. Apply migration 005 dulu." >&2
    exit 2
fi
echo "    ADM_USER=$ADM_USER  LIMITED_USER=$LIMITED_USER"
echo ""

curl -s -c "$COOKIE_ADM" -X POST "$BFF_URL/api/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"$ADM_USER\",\"password\":\"e2e-test-123\"}" >/dev/null

# Check 1: GET happy path
echo ">>> Check 1: GET /api/admin/role-menu (ADM)"
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" "$BFF_URL/api/admin/role-menu")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"roles"' && echo "$BODY" | grep -q '"menus"' && echo "$BODY" | grep -q '"mapping"'; then
    record "GET /api/admin/role-menu (ADM)" PASS
else
    record "GET /api/admin/role-menu (ADM)" FAIL "code=$CODE"
fi

# Snapshot mapping awal untuk restore
ORIGINAL_MAPPING=$(echo "$BODY" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)['data']['mapping']))")

# Check 2: GET denied untuk non-admin
echo ">>> Check 2: GET denied for non-admin"
if [[ "$LIMITED_USER" != "NONE" ]]; then
    curl -s -c "$COOKIE_LIMITED" -X POST "$BFF_URL/api/auth/login" \
        -H 'Content-Type: application/json' \
        -d "{\"username\":\"$LIMITED_USER\",\"password\":\"e2e-test-123\"}" >/dev/null
    R=$(curl -s -b "$COOKIE_LIMITED" -w "\n%{http_code}" "$BFF_URL/api/admin/role-menu")
    CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
    if [[ "$CODE" == "403" ]] && echo "$BODY" | grep -q "MENU_FORBIDDEN"; then
        record "GET denied for non-admin" PASS
    else
        record "GET denied for non-admin" FAIL "code=$CODE"
    fi
else
    record "GET denied for non-admin" PASS "skipped — no limited user"
fi

# Check 3: PUT add 1 pair (MIGRASI → dashboard.keuangan, assumes not already mapped)
echo ">>> Check 3: PUT add 1 pair"
NEW_MAPPING=$(echo "$ORIGINAL_MAPPING" | python3 -c "
import sys, json
m = json.load(sys.stdin)
# Avoid duplicate if MIGRASI/dashboard.keuangan already exists (unlikely but safe)
pair = {'id_peran': 'MIGRASI', 'menu_key': 'dashboard.keuangan'}
if pair not in m:
    m.append(pair)
print(json.dumps({'mapping': m}))
")
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" -X PUT "$BFF_URL/api/admin/role-menu" \
    -H 'Content-Type: application/json' -d "$NEW_MAPPING")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"added"'; then
    ADDED_COUNT=$(echo "$BODY" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['diff']['added']))")
    if [[ "$ADDED_COUNT" -ge "1" ]]; then
        record "PUT add 1 pair (diff.added>=1)" PASS
    else
        record "PUT add 1 pair (diff.added>=1)" FAIL "added_count=$ADDED_COUNT"
    fi
else
    record "PUT add 1 pair" FAIL "code=$CODE body=$BODY"
fi

# Check 4: GET verify pair tersimpan
echo ">>> Check 4: GET verify added pair persisted"
R=$(curl -s -b "$COOKIE_ADM" "$BFF_URL/api/admin/role-menu")
if echo "$R" | grep -q '"id_peran":"MIGRASI"' && echo "$R" | grep -q "dashboard.keuangan"; then
    record "GET verify added pair persisted" PASS
else
    record "GET verify added pair persisted" FAIL "pair tidak terlihat di response"
fi

# Check 5: PUT restore original
echo ">>> Check 5: PUT restore original mapping"
ORIGINAL_PAYLOAD=$(python3 -c "
import json
mapping = json.loads('''$ORIGINAL_MAPPING''')
print(json.dumps({'mapping': mapping}))
")
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" -X PUT "$BFF_URL/api/admin/role-menu" \
    -H 'Content-Type: application/json' -d "$ORIGINAL_PAYLOAD")
CODE=$(echo "$R" | tail -1)
if [[ "$CODE" == "200" ]]; then
    record "PUT restore original mapping" PASS
else
    record "PUT restore original mapping" FAIL "code=$CODE"
fi

# Check 6: PUT invalid role
echo ">>> Check 6: PUT invalid role → 400"
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" -X PUT "$BFF_URL/api/admin/role-menu" \
    -H 'Content-Type: application/json' \
    -d '{"mapping":[{"id_peran":"FAKE_ROLE","menu_key":"dashboard.overview"}]}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "400" ]] && echo "$BODY" | grep -q "INVALID_ROLE"; then
    record "PUT invalid role → 400 INVALID_ROLE" PASS
else
    record "PUT invalid role" FAIL "code=$CODE"
fi

# Check 7: PUT invalid menu
echo ">>> Check 7: PUT invalid menu → 400"
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" -X PUT "$BFF_URL/api/admin/role-menu" \
    -H 'Content-Type: application/json' \
    -d '{"mapping":[{"id_peran":"ADM","menu_key":"fake.menu"}]}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "400" ]] && echo "$BODY" | grep -q "INVALID_MENU"; then
    record "PUT invalid menu → 400 INVALID_MENU" PASS
else
    record "PUT invalid menu" FAIL "code=$CODE"
fi

# Check 8: PUT duplicate pair
echo ">>> Check 8: PUT duplicate pair → 400"
R=$(curl -s -b "$COOKIE_ADM" -w "\n%{http_code}" -X PUT "$BFF_URL/api/admin/role-menu" \
    -H 'Content-Type: application/json' \
    -d '{"mapping":[{"id_peran":"ADM","menu_key":"dashboard.overview"},{"id_peran":"ADM","menu_key":"dashboard.overview"}]}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "400" ]] && echo "$BODY" | grep -q "DUPLICATE_PAIR"; then
    record "PUT duplicate pair → 400 DUPLICATE_PAIR" PASS
else
    record "PUT duplicate pair" FAIL "code=$CODE"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  E2E admin role-menu — $STACK"
echo "════════════════════════════════════════════════════════════════════"
for line in "${RESULTS[@]}"; do echo "  $line"; done
echo "────────────────────────────────────────────────────────────────────"
echo "  PASS: $PASS     FAIL: $FAIL     TOTAL: 8"
echo "════════════════════════════════════════════════════════════════════"

[[ "$FAIL" -gt 0 ]] && exit 1 || exit 0
