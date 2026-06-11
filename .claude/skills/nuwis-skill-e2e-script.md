# Skill: nuwis-skill-e2e-script
## Pola E2E Smoke Test Script untuk isf-app

---

## Overview

E2E scripts di `testing/e2e-{slug}.sh` adalah curl-based smoke tests yang
memvalidasi API end-to-end melalui BFF (bukan langsung ke api-python).

---

## Struktur Script Standar

```bash
#!/usr/bin/env bash
# E2E Smoke Test: {Nama Fitur}
# Portal: {zakat | wakaf}
# User default: {USERNAME} ({role yang diperlukan})
# Usage: bash testing/e2e-{slug}.sh
#        BASE_URL=http://localhost:7001 bash testing/e2e-{slug}.sh  ← wakaf

set -euo pipefail

# ── Config ───────────────────────────────────────────────────────────────────
BASE_URL="${BASE_URL:-http://localhost:7000}"  # 7000=zakat, 7001=wakaf
USERNAME="${TEST_USER:-HADI}"
PASSWORD="${TEST_PASS:-test1234}"

# ── Utils ─────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'; BOLD='\033[1m'
pass()    { echo -e "  ${GREEN}✓${NC} $1"; }
fail()    { echo -e "  ${RED}✗${NC} $1"; exit 1; }
warn()    { echo -e "  ${YELLOW}⚠${NC} $1"; }
section() { echo -e "\n${BOLD}=== $1 ===${NC}"; }
json()    { python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin), indent=2, ensure_ascii=False))" 2>/dev/null || echo "$1"; }

# ── Auth ──────────────────────────────────────────────────────────────────────
section "Login"

LOGIN=$(curl -sf -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  || fail "BFF tidak bisa diakses di $BASE_URL")

TOKEN=$(echo "$LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" \
  || fail "Login gagal — cek username/password")

AUTH="Authorization: Bearer $TOKEN"
pass "Login: $USERNAME"
```

---

## Pola CRUD Test

```bash
# ── List ──────────────────────────────────────────────────────────────────────
section "{Resource}: List"

LIST=$(curl -sf "$BASE_URL/api/{domain}/{resource}?page=1&limit=10" -H "$AUTH")
TOTAL=$(echo "$LIST" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['pagination']['total'])")
ROW_COUNT=$(echo "$LIST" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data']['rows']))")
pass "List OK — total=$TOTAL, rows_returned=$ROW_COUNT"

# ── Create ────────────────────────────────────────────────────────────────────
section "{Resource}: Create"

CREATE=$(curl -sf -X POST "$BASE_URL/api/{domain}/{resource}" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "tanggal": "2026-01-15",
    "{field1}": "{value1}",
    "jumlah": 100000,
    "keterangan": "e2e test - hapus jika perlu"
  }')
NEW_ID=$(echo "$CREATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
[ -n "$NEW_ID" ] && [ "$NEW_ID" != "None" ] \
  && pass "Create OK — id=$NEW_ID" \
  || fail "Create gagal: $(echo $CREATE)"

# ── Get Detail ────────────────────────────────────────────────────────────────
section "{Resource}: Get Detail"

DETAIL=$(curl -sf "$BASE_URL/api/{domain}/{resource}/$NEW_ID" -H "$AUTH")
DETAIL_ID=$(echo "$DETAIL" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
[ "$DETAIL_ID" = "$NEW_ID" ] && pass "Get detail OK — id=$NEW_ID" || fail "Get detail gagal"

# ── Update ────────────────────────────────────────────────────────────────────
section "{Resource}: Update"

UPDATE=$(curl -sf -X PUT "$BASE_URL/api/{domain}/{resource}/$NEW_ID" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"keterangan": "updated via e2e"}')
pass "Update OK"

# ── Delete ────────────────────────────────────────────────────────────────────
section "{Resource}: Delete"

DEL=$(curl -sf -X DELETE "$BASE_URL/api/{domain}/{resource}/$NEW_ID" -H "$AUTH")
pass "Delete OK"

# Verifikasi benar-benar terhapus:
NOT_FOUND=$(curl -s -o /dev/null -w "%{http_code}" \
  "$BASE_URL/api/{domain}/{resource}/$NEW_ID" -H "$AUTH")
[ "$NOT_FOUND" = "404" ] && pass "Verified: data tidak ada setelah delete" \
  || warn "Delete mungkin soft-delete (HTTP $NOT_FOUND)"
```

---

## Pola Laporan Test

```bash
# ── Laporan Preview ───────────────────────────────────────────────────────────
section "Laporan: {Nama}"

LAPORAN=$(curl -sf \
  "$BASE_URL/api/{domain}/laporan/{nama}?tgl_awal=2026-01-01&tgl_akhir=2026-01-31" \
  -H "$AUTH")
ROW_COUNT=$(echo "$LAPORAN" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data']['rows']))")
pass "Laporan preview OK — rows=$ROW_COUNT"

# ── Export XLSX ───────────────────────────────────────────────────────────────
section "Laporan: Export XLSX"

EXPORT_STATUS=$(curl -s -o /tmp/laporan-test.xlsx -w "%{http_code}" \
  "$BASE_URL/api/{domain}/laporan/{nama}/export?tgl_awal=2026-01-01&tgl_akhir=2026-01-31" \
  -H "$AUTH")
FILE_SIZE=$(wc -c < /tmp/laporan-test.xlsx 2>/dev/null || echo 0)

if [ "$EXPORT_STATUS" = "200" ] && [ "$FILE_SIZE" -gt 1000 ]; then
  pass "Export XLSX OK — size=${FILE_SIZE} bytes, saved to /tmp/laporan-test.xlsx"
else
  fail "Export XLSX gagal — HTTP=$EXPORT_STATUS, size=$FILE_SIZE"
fi
```

---

## Summary Block (wajib di akhir script)

```bash
# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║  Semua E2E tests PASSED ✓           ║${NC}"
echo -e "${GREEN}${BOLD}║  Fitur: {Nama Fitur}                ║${NC}"
echo -e "${GREEN}${BOLD}║  Portal: {portal}                   ║${NC}"
echo -e "${GREEN}${BOLD}╚════════════════════════════════════╝${NC}"
```

---

## Tips

### Cleanup Data Test

```bash
# Opsi 1: Hapus di akhir script (jika resource mendukung delete)
trap "curl -sf -X DELETE '$BASE_URL/api/{domain}/{resource}/$NEW_ID' -H '$AUTH' > /dev/null" EXIT

# Opsi 2: Pakai data idempotent (buat jika tidak ada, update jika ada)
# Opsi 3: Biarkan — tambahkan keterangan "e2e test - safe to delete"
```

### Cek Menu Permission

```bash
# Verifikasi user punya akses menu:
PROFILE=$(curl -sf "$BASE_URL/api/auth/me" -H "$AUTH")
MENUS=$(echo "$PROFILE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['menus'])")
echo "Menus: $MENUS"
```

### Port Reference

| Portal | BFF Port | Default user |
|---|---|---|
| Zakat | 7000 | HADI (DIST/SPVDIST, all-branch) |
| Wakaf | 7001 | HADI atau user wakaf setara |
