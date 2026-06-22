# Plan: Refactor Module — appadmin & generalaffair

**Dibuat**: 2026-06-22
**Portal**: zakat + wakaf
**Scope**: Rename modul administration→appadmin, enterprise→generalaffair di frontend, BFF, api-python, dan auth DB

---

## Urutan Eksekusi

```
Layer 0: DB (auth DB update menu keys)         ← HARUS PERTAMA
Layer 1: api-python (rename folder + imports)
Layer 2: BFF (rename folder + fix prefix + menu keys)
Layer 3: Frontend (rename modul, pindah views, update constants)
Layer 4: Verifikasi
```

Layer 1 dan 2 bisa paralel setelah Layer 0 selesai.
Layer 3 harus setelah Layer 0 (menu keys di DB sudah match sebelum frontend load).

---

## Layer 0 — Database Auth (BLOCKER, kerjakan pertama)

**Target**: `isf_auth_zakat` dan `isf_auth_wakaf`
**Tool**: `psql -U transaction -d isf_auth_zakat` (dan wakaf)

- [ ] Update menu key di tabel `isf_auth.menu` — zakat
  ```sql
  UPDATE isf_auth.menu SET menu_key = 'appadmin.users'     WHERE menu_key = 'admin.users';
  UPDATE isf_auth.menu SET menu_key = 'appadmin.role_menu' WHERE menu_key = 'admin.role_menu';
  ```
- [ ] Update menu key di tabel `isf_auth.role_menu` — zakat
  ```sql
  UPDATE isf_auth.role_menu SET menu_key = 'appadmin.users'     WHERE menu_key = 'admin.users';
  UPDATE isf_auth.role_menu SET menu_key = 'appadmin.role_menu' WHERE menu_key = 'admin.role_menu';
  ```
- [ ] Sama untuk `isf_auth_wakaf` (ulangi 2 query di atas)
- [ ] Verifikasi: `SELECT menu_key FROM isf_auth.menu WHERE menu_key LIKE 'admin%';` — harus 0 rows

---

## Layer 1 — api-python (zakat + wakaf)

**Path**: `apps_zakat/api-python/app/modules/` dan `apps_wakaf/api-python/app/modules/`

### Zakat

- [ ] Rename folder: `administration/` → `appadmin/`
- [ ] Update `appadmin/router.py`:
  - `APIRouter(prefix="/administration"` → `prefix="/appadmin"`
  - Import dari `app.modules.administration.*` → `app.modules.appadmin.*`
- [ ] Update `appadmin/schema.py`: import path jika ada cross-reference
- [ ] Update `appadmin/service.py`: import path jika ada cross-reference
- [ ] Update `appadmin/identity/router.py`: import path jika ada
- [ ] Update `app/main.py`:
  - Import: `from app.modules.appadmin...`

### Wakaf (mirror)

- [ ] Ulangi semua langkah di atas untuk `apps_wakaf/api-python/`

---

## Layer 2 — BFF (zakat + wakaf)

**Path**: `apps_zakat/bff-api/app/modules/` dan `apps_wakaf/bff-api/app/modules/`

### Zakat

- [ ] Rename folder: `administration/` → `appadmin/`
- [ ] Update `appadmin/admin.py`:
  - `APIRouter(prefix="/api/administration"` → `prefix="/api/appadmin"`
  - GET proxy: `/api/administration/role-menu` → `/api/appadmin/role-menu`
  - PUT proxy: `/api/admin/role-menu` → `/api/appadmin/role-menu` (fix bug sekalian)
  - `require_menu("admin.role_menu")` → `require_menu("appadmin.role_menu")`
- [ ] Update `app/main.py`:
  - Import: `from app.modules.appadmin.admin import router as admin_router`
  - Comment: `# Appadmin` (ganti `# Administration`)

### Wakaf (mirror)

- [ ] Ulangi semua langkah di atas untuk `apps_wakaf/bff-api/`

---

## Layer 3 — Frontend (zakat + wakaf)

**Path**: `apps_zakat/web-vue/src/` (dan wakaf mirror)

> Catatan: karena source Vue di-bind-mount ke container, perubahan file langsung terdeteksi Vite tanpa rebuild.

### 3a. Buat modul `appadmin`

- [ ] Buat `modules/appadmin/routes.ts`:
  ```ts
  // paths: /appadmin/users, /appadmin/role-menu
  // meta.domain: 'appadmin'
  // menu_key: 'appadmin.users', 'appadmin.role_menu'
  ```
- [ ] Buat `modules/appadmin/menu.ts`:
  ```ts
  // id: 'appadmin', label: 'Pengaturan Akses'
  // sub: 'Manajemen user & hak akses'
  // locked: false, defaultRoute: '/appadmin/users'
  // groups: Manajemen User (List User, Role & Menu)
  ```
- [ ] Buat folder `modules/appadmin/views/users/`
- [ ] Pindah `administration/views/users/UsersView.vue` → `appadmin/views/users/UsersView.vue`
- [ ] Update import di `UsersView.vue` jika ada relative path yang berubah
- [ ] Buat folder `modules/appadmin/views/role-menu/`
- [ ] Pindah `administration/views/role-menu/RoleMenuView.vue` → `appadmin/views/role-menu/RoleMenuView.vue`
- [ ] Update import di `RoleMenuView.vue` jika ada relative path yang berubah

### 3b. Buat modul `generalaffair` (stub)

- [ ] Buat `modules/generalaffair/routes.ts`: array kosong, komentar "Fase berikutnya"
- [ ] Buat `modules/generalaffair/menu.ts`:
  ```ts
  // id: 'generalaffair', label: 'Administrasi & Umum'
  // sub: 'Kepegawaian, surat, aset & perlengkapan'
  // locked: true, lockedBadge: 'Belum tersedia'
  ```

### 3c. Hapus modul lama

- [ ] Hapus seluruh `modules/administration/`
- [ ] Hapus seluruh `modules/enterprise/`

### 3d. Update shared constants

- [ ] `shared/constants/menu-keys.ts`:
  - `'admin.users'` → `'appadmin.users'`
  - `'admin.role_menu'` → `'appadmin.role_menu'`
- [ ] `shared/constants/domains.ts`:
  - `DomainId`: hapus `'administration' | 'enterprise'`, tambah `'generalaffair' | 'appadmin'`
  - Import: hapus `administrationMenu`, tambah `appadminMenu`, `generalaffairMenu`
  - `DOMAIN_MAP`: update entries `administration` → `generalaffair`, `enterprise` → `appadmin`
  - `DOMAIN_ORDER`: `[..., 'appadmin', 'generalaffair']`

### 3e. Update router

- [ ] `app/router/index.ts`:
  - Hapus import `administrationRoutes`, `enterpriseRoutes`
  - Tambah import `appadminRoutes`, `generalaffairRoutes`
  - Include keduanya di `routes` array

### 3f. Wakaf mirror

- [ ] Ulangi 3a–3e untuk `apps_wakaf/web-vue/src/`

---

## Layer 4 — Verifikasi

- [ ] Restart container BFF + api-python zakat (setelah Layer 1 & 2)
- [ ] Login sebagai HADI atau RAIS, buka "Pengaturan Akses"
- [ ] Verifikasi `/appadmin/users` tampil (List User)
- [ ] Verifikasi `/appadmin/role-menu` tampil (Role & Menu)
- [ ] Test PUT role-menu: mapping role-menu bisa disimpan tanpa error 500
- [ ] Verifikasi sidebar: label "Pengaturan Akses" muncul, "Administrasi & Umum" muncul (locked)
- [ ] Verifikasi tidak ada 404 atau broken route di console browser
- [ ] Ulangi verifikasi untuk portal wakaf

### E2E Smoke Test (opsional)

```bash
# Cek endpoint BFF baru
curl -s -X GET http://localhost:7000/api/appadmin/role-menu \
  -H "Cookie: isf_session=<session>" | jq '.data | length'

# Pastikan endpoint lama sudah tidak ada (harus 404)
curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:7000/api/administration/role-menu -H "Cookie: isf_session=<session>"
```

---

## Commit Convention

```
[REFACTOR-MODULE] refactor(modules): rename administration→appadmin, enterprise→generalaffair

- appadmin: user/branch/role management (was: administration)
- generalaffair: GA stub for HR/assets/correspondence (was: enterprise)
- Update menu keys admin.* → appadmin.* across frontend, BFF, api-python, auth DB
- Fix BFF PUT proxy bug: /api/admin/role-menu → /api/appadmin/role-menu
```
