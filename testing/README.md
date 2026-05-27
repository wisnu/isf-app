# Testing — E2E manual verification scripts

Folder ini berisi skrip untuk **end-to-end manual verification** stack `isf-app` (zakat & wakaf) di luar unit test pytest. Skrip dipakai untuk smoke test setelah deploy/perubahan besar — terutama fitur role-menu mapping (lihat `docs/superpowers/specs/2026-05-24-role-menu-mapping-design.md`).

## Prasyarat

- Stack target (zakat dan/atau wakaf) sudah up: `podman-compose -f infra/docker-compose.{zakat,wakaf}.yml up -d`
- Container `api-python` & `bff-api` healthy
- DB existing (`mziss_laz` / `mziss_wakaf`) sudah punya schema `isf_auth` + seed `role_menu` (migration 001, 002, 003 sudah di-apply — lihat `docs/runbook-local.md` §11)

## Skrip

| Skrip | Fungsi | Idempotent |
|---|---|:-:|
| `setup-e2e-users.sh [zakat\|wakaf]` | Tambahkan 2 user E2E ke BFF SQLite (`auth.sqlite`): user dengan akses penuh + user akses terbatas. Username = id_user existing di `enterprise.userapp` (uppercase — konvensi BFF). Password fix `e2e-test-123`. | ✓ (boleh re-run; UPSERT) |
| `e2e-rbac.sh [zakat\|wakaf]` | Run 9 checks RBAC end-to-end: health, identity profile, login happy-path, /me, gated endpoint allow, gated endpoint deny, refresh-profile, fail-closed (stop api-python), UNKNOWN_IDENTITY untuk demo user. | ✓ |

## Cara pakai

```bash
# Setup user test (sekali per stack)
./testing/setup-e2e-users.sh zakat
./testing/setup-e2e-users.sh wakaf

# Jalankan RBAC checks
./testing/e2e-rbac.sh zakat
./testing/e2e-rbac.sh wakaf
```

Output akhir setiap script: tabel PASS/FAIL untuk setiap check. Exit code 0 kalau semua pass, !=0 kalau ada fail.

## User test yang dibuat

Script `setup-e2e-users.sh` query `enterprise.userapp` + `enterprise.listperanuser` + `isf_auth.role_menu` untuk cari otomatis:

- **FULL_USER:** user dengan menu paling banyak (idealnya 7 menu). Untuk uji happy-path.
- **LIMITED_USER:** user dengan menu paling sedikit (idealnya 1-2 menu). Untuk uji deny-path.

User test diasosiasikan ke tenant `perusahaan_a` (seed default BFF). Password fix `e2e-test-123` di-bcrypt-hash. Username disimpan uppercase di BFF SQLite (selaras dengan `enterprise.userapp.id_user`); login dari frontend menerima input case apapun (di-normalize ke uppercase di boundary BFF).

## Mengembalikan state setelah test

User test tetap di `auth.sqlite`. Aman karena password fix dan hanya bisa login kalau punya peran di `enterprise.peran` + `isf_auth.role_menu` mapping. Hapus manual jika perlu:

```bash
podman-compose -f infra/docker-compose.zakat.yml exec -T bff-api python -c "
import asyncio
from app.services.auth_db import AuthDB
async def run():
    db = AuthDB('/data/auth.sqlite')
    async with db.connect() as conn:
        await conn.execute(\"DELETE FROM users WHERE display_name = 'E2E Test'\")
        await conn.commit()
asyncio.run(run())
"
```

## Unit test

Untuk test pytest di tiap service, pakai wrapper `apps_{zakat,wakaf}/{api-python,bff-api}/test.sh` (lihat masing-masing folder service).
