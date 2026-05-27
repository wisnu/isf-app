#!/usr/bin/env bash
# Setup 2 user test E2E di BFF SQLite auth.sqlite untuk stack target.
# Idempotent: aman di-re-run; pakai UPSERT.
#
# Pakai:
#   ./testing/setup-e2e-users.sh zakat
#   ./testing/setup-e2e-users.sh wakaf
#
# Output: print id_user yang dipilih (FULL_USER + LIMITED_USER) ke stdout
#         supaya bisa dipakai e2e-rbac.sh.
set -euo pipefail

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
TEST_PASSWORD="e2e-test-123"

echo ">>> [1/3] Cari user existing dengan menu banyak/sedikit di $STACK..."

USER_INFO=$($COMPOSE -f "$COMPOSE_FILE" exec -T api-python python -c "
import asyncio, asyncpg, os
async def run():
    conn = await asyncpg.connect(os.environ['DATABASE_URL'])
    # Cari FULL: user dengan menu_count terbanyak
    full = await conn.fetchrow('''
        SELECT u.id_user, COUNT(DISTINCT rm.menu_key) AS n_menu
        FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A'
        GROUP BY u.id_user
        ORDER BY n_menu DESC, u.id_user
        LIMIT 1
    ''')
    # Cari LIMITED: user dengan menu_count paling sedikit (>0)
    limited = await conn.fetchrow('''
        SELECT u.id_user, COUNT(DISTINCT rm.menu_key) AS n_menu
        FROM enterprise.userapp u
        JOIN enterprise.listperanuser lpu ON lpu.id_user = u.id_user
        JOIN isf_auth.role_menu rm ON rm.id_peran = lpu.id_peran
        WHERE u.status_profil = 'A'
        GROUP BY u.id_user
        HAVING COUNT(DISTINCT rm.menu_key) > 0 AND COUNT(DISTINCT rm.menu_key) < 7
        ORDER BY n_menu ASC, u.id_user
        LIMIT 1
    ''')
    if not full:
        print('NONE NONE 0 0')
        return
    if not limited:
        # Fallback: pakai user yang sama (tidak ada user limited)
        print(f\"{full['id_user']} {full['id_user']} {full['n_menu']} {full['n_menu']}\")
    else:
        print(f\"{full['id_user']} {limited['id_user']} {full['n_menu']} {limited['n_menu']}\")
    await conn.close()
asyncio.run(run())
" | tr -d '\r')

read -r FULL_USER LIMITED_USER FULL_MENUS LIMITED_MENUS <<< "$USER_INFO"

if [[ "$FULL_USER" == "NONE" ]]; then
    echo "ERROR: tidak ada user di enterprise.userapp yang punya role + role_menu mapping" >&2
    echo "Pastikan migration 003_role_menu_seed.sql sudah di-apply" >&2
    exit 1
fi

echo "    FULL_USER:    $FULL_USER ($FULL_MENUS menus)"
echo "    LIMITED_USER: $LIMITED_USER ($LIMITED_MENUS menus)"
if [[ "$FULL_USER" == "$LIMITED_USER" ]]; then
    echo "    NOTE: full=limited (semua role punya menu count sama)"
fi

echo ""
echo ">>> [2/3] Upsert user ke BFF SQLite auth.sqlite..."

$COMPOSE -f "$COMPOSE_FILE" exec -T bff-api python -c "
import asyncio, bcrypt
from app.services.auth_db import AuthDB
async def run():
    db = AuthDB('/data/auth.sqlite')
    await db.init_schema()
    for username in ['$FULL_USER', '$LIMITED_USER']:
        if username == 'NONE':
            continue
        existing = await db.get_user_by_username(username)
        if existing:
            uid = existing['id']
            print(f'  exists: {username} -> {uid}')
        else:
            uid = await db.create_user(username=username, display_name='E2E Test')
            print(f'  created: {username} -> {uid}')
        pwd_hash = bcrypt.hashpw(b'$TEST_PASSWORD', bcrypt.gensalt()).decode()
        await db.set_password(uid, pwd_hash)
        await db.add_tenant_membership(uid, 'perusahaan_a', is_default=True)
asyncio.run(run())
"

echo ""
echo ">>> [3/3] Done. Test users siap pakai:"
echo "    FULL_USER:    $FULL_USER"
echo "    LIMITED_USER: $LIMITED_USER"
echo "    Password:     $TEST_PASSWORD"
echo "    Tenant:       perusahaan_a (default)"
echo ""
echo "Untuk run RBAC checks:"
echo "    ./testing/e2e-rbac.sh $STACK"
