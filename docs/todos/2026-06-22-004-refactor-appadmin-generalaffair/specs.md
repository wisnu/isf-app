# Specs: Refactor Module — appadmin & generalaffair

**Portal**: zakat + wakaf (mirrored)
**Tipe**: Structural Refactor (rename modul, pindah views, update menu keys)
**Tanggal**: 2026-06-22

---

## Konteks

Dua modul frontend saat ini punya nama dan konten yang tidak mencerminkan fungsinya:

| Modul Lama | Masalah |
|---|---|
| `administration` | Berisi user & role management — bukan admin konten |
| `enterprise` | Stub kosong — label "Enterprise" tidak deskriptif |

Refactor ini menyelaraskan nama modul dengan domain bisnis yang benar:

| Modul Baru | Domain ID | UI Label | Konten |
|---|---|---|---|
| `appadmin` | `appadmin` | Pengaturan Akses | User, branch, role, menu, hak akses |
| `generalaffair` | `generalaffair` | Administrasi & Umum | Kepegawaian, surat, aset, peralatan (fase berikutnya) |

`UsersView` dan `RoleMenuView` yang saat ini di `administration` dipindah ke `appadmin`.

---

## Scope Perubahan per Layer

### 1. Frontend — `web-vue/src/`

**Modul dihapus:**
- `modules/administration/` — seluruh folder dihapus

**Modul dibuat:**
- `modules/appadmin/` — menggantikan `enterprise/`, menerima views dari `administration/`
- `modules/generalaffair/` — menggantikan `administration/`, stub kosong (locked)

**File yang dipindah:**
- `administration/views/users/UsersView.vue` → `appadmin/views/users/UsersView.vue`
- `administration/views/role-menu/RoleMenuView.vue` → `appadmin/views/role-menu/RoleMenuView.vue`

**File yang diubah:**
- `shared/constants/domains.ts` — DomainId, DOMAIN_MAP, DOMAIN_ORDER
- `shared/constants/menu-keys.ts` — rename menu key prefix
- `app/router/index.ts` — update imports

**URL paths:**

| Sekarang | Setelah |
|---|---|
| `/administration/users` | `/appadmin/users` |
| `/administration/role-menu` | `/appadmin/role-menu` |

**Menu keys:**

| Sekarang | Setelah |
|---|---|
| `admin.users` | `appadmin.users` |
| `admin.role_menu` | `appadmin.role_menu` |

**Domain config:**

| Field | Sekarang | Setelah |
|---|---|---|
| DomainId | `'administration' \| 'enterprise'` | `'generalaffair' \| 'appadmin'` |
| DOMAIN_ORDER posisi | `administration, enterprise` (akhir) | `appadmin, generalaffair` (akhir) |
| `appadmin` defaultRoute | — | `/appadmin/users` |
| `appadmin` locked | — | `false` |
| `generalaffair` locked | — | `true`, badge `"Belum tersedia"` |

---

### 2. BFF — `bff-api/app/modules/`

**Folder rename:**
- `administration/` → `appadmin/`
- File: `admin.py` (nama file tetap)

**Perubahan dalam `admin.py`:**

| Item | Sekarang | Setelah |
|---|---|---|
| Router prefix | `/api/administration` | `/api/appadmin` |
| GET proxy target | `/api/administration/role-menu` | `/api/appadmin/role-menu` |
| PUT proxy target | `/api/admin/role-menu` ← bug | `/api/appadmin/role-menu` |
| `require_menu` | `"admin.role_menu"` | `"appadmin.role_menu"` |

**`main.py`:**
- Update import path: `from app.modules.appadmin.admin import router as admin_router`
- Update comment section header

---

### 3. API Python — `api-python/app/modules/`

**Folder rename:**
- `administration/` → `appadmin/`
- Sub-modul `identity/` tidak berubah (nama internal, bukan domain boundary)

**Perubahan dalam `router.py`:**

| Item | Sekarang | Setelah |
|---|---|---|
| APIRouter prefix | `/administration` | `/appadmin` |
| Import path `schema` | `from app.modules.administration.schema` | `from app.modules.appadmin.schema` |
| Import path `service` | `from app.modules.administration.service` | `from app.modules.appadmin.service` |

**`app/main.py` api-python:**
- Update import: `from app.modules.appadmin...`

---

### 4. Database — Auth DB (kedua portal)

Tabel yang diupdate: `isf_auth.menu` dan `isf_auth.role_menu`

```sql
-- isf_auth_zakat + isf_auth_wakaf (jalankan di keduanya)
UPDATE isf_auth.menu     SET menu_key = 'appadmin.users'     WHERE menu_key = 'admin.users';
UPDATE isf_auth.menu     SET menu_key = 'appadmin.role_menu' WHERE menu_key = 'admin.role_menu';
UPDATE isf_auth.role_menu SET menu_key = 'appadmin.users'    WHERE menu_key = 'admin.users';
UPDATE isf_auth.role_menu SET menu_key = 'appadmin.role_menu' WHERE menu_key = 'admin.role_menu';
```

> Jalankan DB update **sebelum** deploy frontend/BFF baru — agar session login yang ada tidak crash saat membaca `menus[]`.

---

### 5. Tidak Berubah

- Semua file Vue di `views/users/` dan `views/role-menu/` — hanya pindah folder, konten sama
- Logic service, schema api-python — hanya import path yang berubah
- Tabel-tabel DB business (`mziss_laz`, `mziss_wakaf`) — tidak ada perubahan schema
- Report-api — tidak ada modul administration di sana

---

## Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| Session aktif user masih punya menu key `admin.*` | Update DB dulu, baru deploy; atau minta user re-login |
| Wakaf portal tidak di-update bersamaan | Scope refactor ini include kedua portal sekaligus |
| BFF PUT proxy bug (`/api/admin/role-menu`) sudah lama ada — mungkin ada workaround tersembunyi | Verifikasi fungsi role-menu setelah deploy dengan E2E test |
