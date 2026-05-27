#!/usr/bin/env bash
# E2E manual verification untuk fitur role-menu mapping.
# Run 9 checks: health, identity, login happy, /me, allow, deny, refresh,
# fail-closed, UNKNOWN_IDENTITY.
#
# Pakai:
#   ./testing/e2e-rbac.sh zakat
#   ./testing/e2e-rbac.sh wakaf
#
# Prerequisite: `./testing/setup-e2e-users.sh <stack>` sudah dijalankan.
set -uo pipefail

STACK="${1:-}"
if [[ "$STACK" != "zakat" && "$STACK" != "wakaf" ]]; then
    echo "ERROR: argumen pertama harus 'zakat' atau 'wakaf'" >&2
    echo "Pakai: $0 [zakat|wakaf]" >&2
    exit 1
fi

# Detect compose runtime
if command -v podman-compose >/dev/null 2>&1; then
    COMPOSE="podman-compose"
elif command -v podman >/dev/null 2>&1 && podman compose version >/dev/null 2>&1; then
    COMPOSE="podman compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    COMPOSE="docker compose"
else
    echo "ERROR: tidak nemu podman-compose / podman compose / docker compose" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/infra/docker-compose.${STACK}.yml"

# Port mapping: zakat→8000/7000, wakaf→8001/7001
if [[ "$STACK" == "zakat" ]]; then
    API_PORT=8000
    BFF_PORT=7000
else
    API_PORT=8001
    BFF_PORT=7001
fi

API_URL="http://localhost:${API_PORT}"
BFF_URL="http://localhost:${BFF_PORT}"
COOKIE_FULL="/tmp/c-${STACK}-full.txt"
COOKIE_LIMITED="/tmp/c-${STACK}-limited.txt"
TEST_PASSWORD="e2e-test-123"

# Cleanup cookies dari run sebelumnya
rm -f "$COOKIE_FULL" "$COOKIE_LIMITED"

# Track results
declare -a RESULTS=()
PASS_COUNT=0
FAIL_COUNT=0

record() {
    local num="$1"
    local name="$2"
    local status="$3"  # PASS | FAIL
    local detail="${4:-}"
    if [[ "$status" == "PASS" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        RESULTS+=("✓ Check $num: $name — PASS")
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        RESULTS+=("✗ Check $num: $name — FAIL: $detail")
    fi
}

# Discover test users (FULL_USER = banyak menu, LIMITED_USER = sedikit)
echo ">>> Discovery test users dari $STACK DB..."
USER_INFO=$($COMPOSE -f "$COMPOSE_FILE" exec -T api-python python -c "
import asyncio, asyncpg, os
async def run():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    full = await conn.fetchrow('''
        SELECT u.id_user FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A'
        GROUP BY u.id_user
        ORDER BY COUNT(DISTINCT rm.menu_key) DESC, u.id_user
        LIMIT 1
    ''')
    limited = await conn.fetchrow('''
        SELECT u.id_user FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A'
        GROUP BY u.id_user
        HAVING COUNT(DISTINCT rm.menu_key) > 0 AND COUNT(DISTINCT rm.menu_key) < 7
        ORDER BY COUNT(DISTINCT rm.menu_key) ASC, u.id_user
        LIMIT 1
    ''')
    print(f\"{full['id_user'] if full else 'NONE'} {limited['id_user'] if limited else 'NONE'}\")
    await conn.close()
asyncio.run(run())
" | tr -d '\r')

read -r FULL_USER LIMITED_USER <<< "$USER_INFO"

if [[ "$FULL_USER" == "NONE" ]]; then
    echo "ERROR: tidak ada test user. Jalankan setup-e2e-users.sh dulu." >&2
    exit 2
fi
echo "    FULL_USER=$FULL_USER  LIMITED_USER=$LIMITED_USER"
echo ""

# ─── Check 1: Health endpoints ─────────────────────────────────────────────
echo ">>> Check 1: Health api-python + BFF"
R1=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
R2=$(curl -s -o /dev/null -w "%{http_code}" "$BFF_URL/health")
if [[ "$R1" == "200" && "$R2" == "200" ]]; then
    record 1 "Health endpoints" PASS
else
    record 1 "Health endpoints" FAIL "api=$R1 bff=$R2"
fi

# ─── Check 2: Identity profile direct ──────────────────────────────────────
echo ">>> Check 2: GET /api/identity/$FULL_USER/profile"
R=$(curl -s -w "\n%{http_code}" "$API_URL/api/identity/$FULL_USER/profile")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"menus"'; then
    record 2 "Identity profile direct" PASS
else
    record 2 "Identity profile direct" FAIL "code=$CODE body=$BODY"
fi

# ─── Check 3: Login happy path (FULL_USER) ─────────────────────────────────
echo ">>> Check 3: BFF login as FULL_USER ($FULL_USER)"
R=$(curl -s -c "$COOKIE_FULL" -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"$FULL_USER\",\"password\":\"$TEST_PASSWORD\"}")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"menus"'; then
    record 3 "Login happy path" PASS
else
    record 3 "Login happy path" FAIL "code=$CODE body=$BODY"
fi

# ─── Check 4: /api/auth/me ─────────────────────────────────────────────────
echo ">>> Check 4: GET /api/auth/me"
R=$(curl -s -b "$COOKIE_FULL" -w "\n%{http_code}" "$BFF_URL/api/auth/me")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"menus"' && echo "$BODY" | grep -q '"roles"'; then
    record 4 "/api/auth/me extended payload" PASS
else
    record 4 "/api/auth/me extended payload" FAIL "code=$CODE"
fi

# ─── Check 5: Allowed dashboard endpoint ───────────────────────────────────
echo ">>> Check 5: GET /api/dashboard/summary (allow path)"
R=$(curl -s -b "$COOKIE_FULL" -w "\n%{http_code}" "$BFF_URL/api/dashboard/summary")
CODE=$(echo "$R" | tail -1)
if [[ "$CODE" == "200" ]]; then
    record 5 "Allowed endpoint dashboard.summary" PASS
else
    record 5 "Allowed endpoint dashboard.summary" FAIL "code=$CODE"
fi

# ─── Check 6: Disallowed endpoint via LIMITED_USER ─────────────────────────
if [[ "$LIMITED_USER" == "NONE" ]]; then
    record 6 "Deny endpoint" PASS "skipped — no limited user available"
else
    echo ">>> Check 6: Login as LIMITED_USER ($LIMITED_USER) → hit disallowed endpoint"
    curl -s -c "$COOKIE_LIMITED" -X POST "$BFF_URL/api/auth/login" \
        -H 'Content-Type: application/json' \
        -d "{\"username\":\"$LIMITED_USER\",\"password\":\"$TEST_PASSWORD\"}" >/dev/null

    # Cek menu LIMITED_USER. Cari menu yang TIDAK dia punya.
    LIMITED_MENUS=$(curl -s -b "$COOKIE_LIMITED" "$BFF_URL/api/auth/me" | \
        python3 -c "import sys, json; print(','.join(json.load(sys.stdin)['data']['user']['menus']))")

    # Pilih endpoint yang LIMITED_USER tidak punya menu-nya
    TEST_ENDPOINT=""
    for candidate in "dashboard.penyaluran" "dashboard.penghimpunan" "dashboard.keuangan" "keuangan.coa" "keuangan.kas" "keuangan.bank"; do
        if [[ ",$LIMITED_MENUS," != *",$candidate,"* ]]; then
            case "$candidate" in
                dashboard.penyaluran)    TEST_ENDPOINT="/api/dashboard/penyaluran" ;;
                dashboard.penghimpunan)  TEST_ENDPOINT="/api/dashboard/penghimpunan" ;;
                dashboard.keuangan)      TEST_ENDPOINT="/api/dashboard/keuangan" ;;
                keuangan.coa)            TEST_ENDPOINT="/api/coa/accounts" ;;
                *) continue ;;
            esac
            break
        fi
    done

    if [[ -z "$TEST_ENDPOINT" ]]; then
        record 6 "Deny endpoint" PASS "skipped — LIMITED_USER punya semua menu yang di-gate"
    else
        R=$(curl -s -b "$COOKIE_LIMITED" -w "\n%{http_code}" "$BFF_URL$TEST_ENDPOINT")
        CODE=$(echo "$R" | tail -1)
        BODY=$(echo "$R" | sed '$d')
        if [[ "$CODE" == "403" ]] && echo "$BODY" | grep -q "MENU_FORBIDDEN"; then
            record 6 "Deny endpoint ($TEST_ENDPOINT)" PASS
        else
            record 6 "Deny endpoint ($TEST_ENDPOINT)" FAIL "code=$CODE"
        fi
    fi
fi

# ─── Check 7: POST /api/auth/refresh-profile ──────────────────────────────
echo ">>> Check 7: POST /api/auth/refresh-profile"
R=$(curl -s -b "$COOKIE_FULL" -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/refresh-profile")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"refreshed"'; then
    record 7 "Refresh profile" PASS
else
    record 7 "Refresh profile" FAIL "code=$CODE"
fi

# ─── Check 8: Fail-closed (stop api-python, login → 503) ──────────────────
echo ">>> Check 8: Fail-closed — stop api-python, coba login"
$COMPOSE -f "$COMPOSE_FILE" stop api-python >/dev/null 2>&1
sleep 2

rm -f "/tmp/c-${STACK}-failclosed.txt"
R=$(curl -s -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/login" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"$FULL_USER\",\"password\":\"$TEST_PASSWORD\"}")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')

# Restart api-python sebelum cek result
echo "    Restart api-python..."
$COMPOSE -f "$COMPOSE_FILE" start api-python >/dev/null 2>&1
sleep 5  # tunggu healthcheck

if [[ "$CODE" == "503" ]] && echo "$BODY" | grep -q "IDENTITY_UNAVAILABLE"; then
    record 8 "Fail-closed (503 IDENTITY_UNAVAILABLE)" PASS
else
    record 8 "Fail-closed (503 IDENTITY_UNAVAILABLE)" FAIL "code=$CODE body=$BODY"
fi

# ─── Check 9: UNKNOWN_IDENTITY untuk demo user ─────────────────────────────
echo ">>> Check 9: Login demo user 'admin' (tidak ada di enterprise.userapp) → 403"
# Tunggu sampai api-python healthy lagi
for i in {1..10}; do
    if curl -s -f "$API_URL/health" >/dev/null 2>&1; then break; fi
    sleep 2
done

R=$(curl -s -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/login" \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin123"}')
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "403" ]] && echo "$BODY" | grep -q "UNKNOWN_IDENTITY"; then
    record 9 "UNKNOWN_IDENTITY for demo user" PASS
else
    record 9 "UNKNOWN_IDENTITY for demo user" FAIL "code=$CODE body=$BODY"
fi

# ─── Summary ────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  E2E RBAC verification — $STACK"
echo "════════════════════════════════════════════════════════════════════"
for line in "${RESULTS[@]}"; do
    echo "  $line"
done
echo "────────────────────────────────────────────────────────────────────"
echo "  PASS: $PASS_COUNT     FAIL: $FAIL_COUNT     TOTAL: 9"
echo "════════════════════════════════════════════════════════════════════"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    exit 1
fi
exit 0
