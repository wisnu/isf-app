#!/usr/bin/env bash
# E2E manual verification untuk fitur ganti password (POST /api/auth/change-password).
#
# Run 7 checks:
#   1. Health
#   2. Login dengan password lama (atau baru — self-healing)
#   3. Change password (current → new)
#   4. Session cleared setelah change (GET /me → 401)
#   5. Login dengan password lama → 401
#   6. Login dengan password baru → 200
#   7. Revert: change kembali ke password lama (final state idempotent)
#
# Pakai:
#   ./testing/e2e-change-password.sh zakat
#   ./testing/e2e-change-password.sh wakaf
#
# Prerequisite: `./testing/setup-e2e-users.sh <stack>` sudah dijalankan
# (script ini pakai FULL_USER yang sama dengan e2e-rbac).
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

if [[ "$STACK" == "zakat" ]]; then
    API_PORT=8000
    BFF_PORT=7000
else
    API_PORT=8001
    BFF_PORT=7001
fi

API_URL="http://localhost:${API_PORT}"
BFF_URL="http://localhost:${BFF_PORT}"
COOKIE="/tmp/c-${STACK}-chgpwd.txt"
OLD_PASSWORD="e2e-test-123"
NEW_PASSWORD="e2e-new-pwd-456"

rm -f "$COOKIE"

declare -a RESULTS=()
PASS_COUNT=0
FAIL_COUNT=0

record() {
    local num="$1"
    local name="$2"
    local status="$3"
    local detail="${4:-}"
    if [[ "$status" == "PASS" ]]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        RESULTS+=("✓ Check $num: $name — PASS")
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        RESULTS+=("✗ Check $num: $name — FAIL: $detail")
    fi
}

# Discover FULL_USER: user yang ada di BOTH isf_auth.users (bisa login) DAN
# enterprise.userapp (identity service ketemu). DB enterprise & isf_auth sekarang
# terpisah; query 2 step app-side.
echo ">>> Discovery FULL_USER (intersect isf_auth.users ∩ enterprise.userapp)..."
FULL_USER=$($COMPOSE -f "$COMPOSE_FILE" exec -T api-python python -c "
import asyncio, asyncpg, os
async def run():
    isf = await asyncpg.connect(os.environ['ISF_AUTH_DATABASE_URL'])
    auth_users = {r['username'] for r in await isf.fetch(
        \"SELECT username FROM isf_auth.users WHERE status='active'\"
    )}
    peran_set = {r['id_peran'] for r in await isf.fetch(
        'SELECT DISTINCT id_peran FROM isf_auth.role_menu'
    )}
    await isf.close()
    if not auth_users or not peran_set:
        print('NONE'); return
    ent = await asyncpg.connect(os.environ['DATABASE_URL'])
    user = await ent.fetchrow('''
        SELECT u.id_user FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        WHERE u.status_profil = 'A'
          AND u.id_user = ANY(\$1::text[])
          AND lpu.id_peran = ANY(\$2::text[])
        GROUP BY u.id_user
        ORDER BY COUNT(DISTINCT lpu.id_peran) DESC, u.id_user
        LIMIT 1
    ''', list(auth_users), list(peran_set))
    print(user['id_user'] if user else 'NONE')
    await ent.close()
asyncio.run(run())
" | tr -d '\r')

if [[ "$FULL_USER" == "NONE" || -z "$FULL_USER" ]]; then
    echo "ERROR: tidak ada user yang sekaligus ada di isf_auth.users dan enterprise.userapp." >&2
    echo "Seed dulu setidaknya satu user via BFF (lihat auth_seed.py)." >&2
    exit 2
fi
echo "    FULL_USER=$FULL_USER"

# Setup: pastikan FULL_USER punya password = OLD_PASSWORD (idempotent reset).
# Tanpa ini script tidak tahu password awal user. End-state script juga revert
# ke OLD_PASSWORD sehingga aman re-run.
echo ">>> Setup: reset password $FULL_USER ke OLD_PASSWORD"
$COMPOSE -f "$COMPOSE_FILE" exec -T bff-api python -c "
import asyncio, bcrypt
from app.services.auth_db import AuthDB
from app.shared.db import init_pool, close_pool
async def run():
    await init_pool()
    db = AuthDB()
    user = await db.get_user_by_username('$FULL_USER')
    if not user:
        print('USER_NOT_IN_ISF_AUTH'); await close_pool(); return
    pwd_hash = bcrypt.hashpw(b'$OLD_PASSWORD', bcrypt.gensalt()).decode()
    await db.set_password(user['id'], pwd_hash)
    await close_pool()
    print('OK')
asyncio.run(run())
" 2>&1 | tail -5
echo ""

# Helper: login + return http code
login_with() {
    local password="$1"
    local cookie="$2"
    rm -f "$cookie"
    curl -s -c "$cookie" -o /dev/null -w "%{http_code}" -X POST "$BFF_URL/api/auth/login" \
        -H 'Content-Type: application/json' \
        -d "{\"username\":\"$FULL_USER\",\"password\":\"$password\"}"
}

# ─── Check 1: Health ───────────────────────────────────────────────────────
echo ">>> Check 1: Health BFF + api-python"
R1=$(curl -s -o /dev/null -w "%{http_code}" "$BFF_URL/health")
R2=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health")
if [[ "$R1" == "200" && "$R2" == "200" ]]; then
    record 1 "Health endpoints" PASS
else
    record 1 "Health endpoints" FAIL "bff=$R1 api=$R2"
fi

# ─── Check 2: Login dengan OLD_PASSWORD (self-healing — coba NEW kalau OLD gagal) ──
echo ">>> Check 2: Login as $FULL_USER (self-healing)"
CODE=$(login_with "$OLD_PASSWORD" "$COOKIE")
CURRENT_PASSWORD="$OLD_PASSWORD"
if [[ "$CODE" != "200" ]]; then
    echo "    OLD_PASSWORD gagal, coba NEW_PASSWORD (recovery dari run sebelumnya yang ter-interrupt)"
    CODE=$(login_with "$NEW_PASSWORD" "$COOKIE")
    CURRENT_PASSWORD="$NEW_PASSWORD"
fi
if [[ "$CODE" == "200" ]]; then
    record 2 "Login happy path (current=$CURRENT_PASSWORD)" PASS
else
    record 2 "Login happy path" FAIL "code=$CODE — manual reset needed"
    echo ""
    for line in "${RESULTS[@]}"; do echo "  $line"; done
    exit 1
fi

# Tentukan target password
if [[ "$CURRENT_PASSWORD" == "$OLD_PASSWORD" ]]; then
    TARGET_PASSWORD="$NEW_PASSWORD"
else
    TARGET_PASSWORD="$OLD_PASSWORD"
fi

# ─── Check 3: Change password ──────────────────────────────────────────────
echo ">>> Check 3: POST /api/auth/change-password ($CURRENT_PASSWORD → $TARGET_PASSWORD)"
# Pakai -b + -c agar Set-Cookie response (session cleared) di-capture ulang ke file,
# mimicking browser behavior. Tanpa -c, cookie file masih punya session lama.
R=$(curl -s -b "$COOKIE" -c "$COOKIE" -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/change-password" \
    -H 'Content-Type: application/json' \
    -d "{\"current_password\":\"$CURRENT_PASSWORD\",\"new_password\":\"$TARGET_PASSWORD\"}")
CODE=$(echo "$R" | tail -1)
BODY=$(echo "$R" | sed '$d')
if [[ "$CODE" == "200" ]] && echo "$BODY" | grep -q '"logged_out":true'; then
    record 3 "Change password (200 + logged_out)" PASS
else
    record 3 "Change password" FAIL "code=$CODE body=$BODY"
fi

# ─── Check 4: Session cleared (GET /me → 401) ──────────────────────────────
echo ">>> Check 4: GET /me setelah change → expect 401"
CODE=$(curl -s -b "$COOKIE" -o /dev/null -w "%{http_code}" "$BFF_URL/api/auth/me")
if [[ "$CODE" == "401" ]]; then
    record 4 "Session cleared (401 on /me)" PASS
else
    record 4 "Session cleared" FAIL "code=$CODE"
fi

# ─── Check 5: Login dengan password lama → 401 ─────────────────────────────
echo ">>> Check 5: Login dengan password lama ($CURRENT_PASSWORD) → expect 401"
CODE=$(login_with "$CURRENT_PASSWORD" "/tmp/c-${STACK}-old.txt")
rm -f "/tmp/c-${STACK}-old.txt"
if [[ "$CODE" == "401" ]]; then
    record 5 "Old password rejected (401)" PASS
else
    record 5 "Old password rejected" FAIL "code=$CODE (still working — change tidak persist?)"
fi

# ─── Check 6: Login dengan password baru → 200 ─────────────────────────────
echo ">>> Check 6: Login dengan password baru ($TARGET_PASSWORD) → expect 200"
CODE=$(login_with "$TARGET_PASSWORD" "$COOKIE")
if [[ "$CODE" == "200" ]]; then
    record 6 "New password works (200)" PASS
else
    record 6 "New password works" FAIL "code=$CODE"
fi

# ─── Check 7: Revert ke OLD_PASSWORD (idempotent end-state) ────────────────
echo ">>> Check 7: Revert kembali ke $OLD_PASSWORD"
if [[ "$TARGET_PASSWORD" == "$OLD_PASSWORD" ]]; then
    # Sudah di OLD_PASSWORD, skip revert
    record 7 "Revert (already OLD)" PASS
else
    R=$(curl -s -b "$COOKIE" -c "$COOKIE" -w "\n%{http_code}" -X POST "$BFF_URL/api/auth/change-password" \
        -H 'Content-Type: application/json' \
        -d "{\"current_password\":\"$TARGET_PASSWORD\",\"new_password\":\"$OLD_PASSWORD\"}")
    CODE=$(echo "$R" | tail -1)
    if [[ "$CODE" == "200" ]]; then
        # Verifikasi: login dengan OLD harus sukses
        VERIFY=$(login_with "$OLD_PASSWORD" "/tmp/c-${STACK}-verify.txt")
        rm -f "/tmp/c-${STACK}-verify.txt"
        if [[ "$VERIFY" == "200" ]]; then
            record 7 "Revert ($TARGET_PASSWORD → $OLD_PASSWORD)" PASS
        else
            record 7 "Revert" FAIL "revert OK tapi login verify code=$VERIFY"
        fi
    else
        record 7 "Revert" FAIL "code=$CODE — manual reset to OLD_PASSWORD needed"
    fi
fi

rm -f "$COOKIE"

# ─── Summary ────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  E2E Change Password verification — $STACK"
echo "════════════════════════════════════════════════════════════════════"
for line in "${RESULTS[@]}"; do
    echo "  $line"
done
echo "────────────────────────────────────────────────────────────────────"
echo "  PASS: $PASS_COUNT     FAIL: $FAIL_COUNT     TOTAL: 7"
echo "════════════════════════════════════════════════════════════════════"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    exit 1
fi
exit 0
