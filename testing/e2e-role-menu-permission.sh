#!/usr/bin/env bash
# E2E smoke test: role-menu-permission endpoints (zakat portal)
set -euo pipefail

BASE="http://localhost:7000"
COOKIE="/tmp/e2e-rolemenu-$$.txt"
trap 'rm -f "$COOKIE"' EXIT

pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; exit 1; }

echo "=== Role-Menu Permission E2E (zakat) ==="

# 1. Login as admin user (ADM has appadmin.role_menu view permission)
echo "[1] Login as ADM..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -c "$COOKIE" -X POST "$BASE/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"ADM","password":"test1234"}')
[ "$STATUS" = "200" ] && pass "Login OK" || fail "Login failed ($STATUS)"

# 2. GET permissions for role KEU
echo "[2] GET permissions for role KEU..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/appadmin/role-menu-permission?role_id=KEU")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert 'data' in d, 'missing data key'
assert 'roles' in d['data'], 'missing roles'
assert 'menus' in d['data'], 'missing menus'
assert 'permissions' in d['data'], 'missing permissions'
print('  data shape OK')
"
pass "GET permissions shape OK"

# 3. PUT - set view permission for dashboard.finance
echo "[3] PUT permission for KEU on dashboard.finance..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE" -X PUT \
  "$BASE/api/appadmin/role-menu-permission" \
  -H "Content-Type: application/json" \
  -d '{"role_id":"KEU","permissions":[{"menu_key":"dashboard.finance","actions":["view"]}]}')
[ "$STATUS" = "200" ] && pass "PUT permission OK" || fail "PUT permission failed ($STATUS)"

# 4. Verify the change persisted
echo "[4] Verify permission persisted..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/appadmin/role-menu-permission?role_id=KEU")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
perms = {p['menu_key']: p['actions'] for p in d['data']['permissions']}
assert 'view' in perms.get('dashboard.finance', []), 'view action not found for dashboard.finance'
print('  persistence OK')
"
pass "Permission persisted OK"

# 5. Export Excel
echo "[5] Export Excel..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE" \
  "$BASE/api/appadmin/role-menu-permission/export")
[ "$STATUS" = "200" ] && pass "Export Excel OK" || fail "Export Excel failed ($STATUS)"

# 6. Login check: menus field is action-aware
echo "[6] Login menus field is action-aware..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/auth/me")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
menus = d['data']['user']['menus']
assert isinstance(menus, list), 'menus should be list'
if menus:
    first = menus[0]
    assert 'menu_key' in first, 'menus items should have menu_key'
    assert 'actions' in first, 'menus items should have actions'
    assert isinstance(first['actions'], list), 'actions should be list'
print('  menus format OK')
"
pass "Menus format is action-aware"

echo ""
echo "=== All tests passed ==="
