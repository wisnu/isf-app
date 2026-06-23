# Design: Refactor Role-Menu — Action-Level Permissions

**Date:** 2026-06-23  
**Status:** Design Approved

## Latar Belakang

Halaman Pengaturan Menu saat ini menampilkan matrix boolean (role × menu) dengan 99 kolom sekaligus — terlalu padat dan tidak mendukung granularitas aksi. Refactor ini menambah 5 aksi per menu (view, tambah, edit, hapus, detail) dan mengubah UI ke pendekatan role-first dengan accordion per domain.

---

## Scope Perubahan

| Layer | Perubahan |
|---|---|
| DB (`isf_auth_zakat` + `isf_auth_wakaf`) | Ganti `role_menu` dengan `role_menu_permission` |
| api-python (appadmin) | Endpoint baru: GET/PUT permission + GET export |
| BFF | Update `require_menu()` + update session menus[] |
| web-vue (auth store) | Tipe `menus[]` berubah ke `{menu_key, actions[]}[]` |
| web-vue (composable) | Baru: `usePermission(menuKey)` |
| web-vue (RoleMenuView) | Redesign total: role-first + accordion domain + action cols |

---

## Section 1 — Database Schema

### Tabel Baru: `isf_auth.role_menu_permission`

```sql
CREATE TABLE isf_auth.role_menu_permission (
    id         SERIAL PRIMARY KEY,
    role_id    VARCHAR(50)  NOT NULL,
    menu_key   VARCHAR(100) NOT NULL,
    action     VARCHAR(20)  NOT NULL
               CHECK (action IN ('view','tambah','edit','hapus','detail')),
    updated_by VARCHAR(100),
    updated_at TIMESTAMPTZ  DEFAULT NOW(),
    UNIQUE (role_id, menu_key, action)
);
```

### Migration

Satu Flyway script (`V###__replace_role_menu_with_permissions.sql`):

1. Create `role_menu_permission`
2. Migrate existing rows: setiap baris `role_menu` → insert `action='view'`
3. Drop `role_menu` setelah BFF diupdate

Migration diaplikasikan ke **kedua** DB: `isf_auth_zakat` dan `isf_auth_wakaf`.

---

## Section 2 — Backend

### api-python — Endpoint Baru (`appadmin/router.py`)

| Method | Path | Keterangan |
|---|---|---|
| `GET` | `/appadmin/role-menu-permission` | Semua roles + menus + mapping per action |
| `PUT` | `/appadmin/role-menu-permission` | Simpan mapping satu role (full replace untuk role itu) |
| `GET` | `/appadmin/role-menu-permission/export` | Excel matrix semua role × menu × action |

Response `GET /appadmin/role-menu-permission`:
```json
{
  "roles": [{ "role_id": "KEU", "role_name": "Keuangan", "user_count": 3 }],
  "menus": [{ "menu_key": "finance.dashboard", "label": "Dashboard", "domain": "finance", "sort_order": 1 }],
  "permissions": [{ "role_id": "KEU", "menu_key": "finance.dashboard", "action": "view" }]
}
```

Request body `PUT /appadmin/role-menu-permission`:
```json
{
  "role_id": "KEU",
  "permissions": [
    { "menu_key": "finance.dashboard", "actions": ["view"] },
    { "menu_key": "finance.jurnal", "actions": ["view", "tambah", "edit"] }
  ]
}
```

Save strategy: DELETE all rows for `role_id`, lalu INSERT semua dari request. Audit log mencatat diff (added/removed).

### BFF — Dua Perubahan

**1. `require_menu()` decorator** — ganti query dari `role_menu` ke `role_menu_permission`:
```python
# Sebelum
WHERE id_peran = $1 AND menu_key = $2

# Sesudah
WHERE role_id = $1 AND menu_key = $2 AND action = 'view'
```

**2. Session login — struktur `menus[]`:**
```python
# Sebelum: ["finance.dashboard", "finance.jurnal"]

# Sesudah:
[
  {"menu_key": "finance.dashboard", "actions": ["view"]},
  {"menu_key": "finance.jurnal", "actions": ["view", "tambah", "edit"]}
]
```

Tidak ada perubahan pada cookie. `menus[]` sudah difetch dari role cache (bukan disimpan di cookie — warisan SESSION-FIX).

---

## Section 3 — Frontend: Auth Store + Composable

### Auth Store (`auth.store.ts`)

```ts
// Sebelum
menus: string[]

// Sesudah
menus: { menu_key: string; actions: string[] }[]
```

Semua guard/sidebar yang pakai `menus.includes(key)` diupdate ke:
```ts
menus.some(m => m.menu_key === key)
```

### Composable Baru: `shared/composables/usePermission.ts`

```ts
export function usePermission(menuKey: string) {
  const auth = useAuthStore()
  const entry = computed(() => auth.menus.find(m => m.menu_key === menuKey))
  return {
    canView:   computed(() => entry.value?.actions.includes('view')   ?? false),
    canAdd:    computed(() => entry.value?.actions.includes('tambah') ?? false),
    canEdit:   computed(() => entry.value?.actions.includes('edit')   ?? false),
    canDelete: computed(() => entry.value?.actions.includes('hapus')  ?? false),
    canDetail: computed(() => entry.value?.actions.includes('detail') ?? false),
  }
}
```

Pemakaian di komponen lain:
```ts
const { canAdd, canEdit, canDelete } = usePermission(MENU_KEYS.FINANCE_FUND_COLLECTION)
// <Button v-if="canAdd">Tambah</Button>
```

---

## Section 4 — Frontend: UI Halaman Pengaturan Menu

### Layout

```
┌────────────────────────────────────────────────────────────┐
│ Pengaturan Menu                         [Export Excel]      │
│ Role: [SPVDIST            ▾]  [Refresh] [Discard] [Simpan] │
├────────────────────────────────────────────────────────────┤
│ ▼ KEUANGAN  (12 menu aktif)              [Aktifkan Semua]  │
│  ┌──────────────────────┬───┬───┬───┬───┬───┐             │
│  │ Menu                 │ V │ T │ E │ H │ D │             │
│  ├──────────────────────┼───┼───┼───┼───┼───┤             │
│  │ Dashboard            │ ✓ │   │   │   │   │             │
│  │ Jurnal Harian        │ ✓ │ ✓ │ ✓ │   │ ✓ │             │
│  └──────────────────────┴───┴───┴───┴───┴───┘             │
│ ▶ PENYALURAN  (8 menu)                                     │
│ ▶ ADMINISTRASI  (5 menu)                                   │
│ ▶ PENGATURAN AKSES  (3 menu)                               │
│ ▶ PENGHIMPUNAN  (4 menu)                                   │
└────────────────────────────────────────────────────────────┘
```

Kolom: **V** = view · **T** = tambah · **E** = edit · **H** = hapus · **D** = detail

### Aturan UX

| Skenario | Perilaku |
|---|---|
| Uncheck V (view) | Otomatis clear T, E, H, D |
| Check T / E / H / D | Otomatis check V |
| `[Aktifkan Semua]` per domain | Set semua 5 aksi untuk seluruh menu di domain itu |
| Accordion | Default collapsed, expand manual |
| Dirty cell | Highlight amber |
| Save | Hanya untuk role yang sedang dipilih |
| Ganti role dengan perubahan belum disimpan | Confirm dialog sebelum pindah |
| Export Excel | Satu sheet per domain; kolom = V/T/E/H/D per menu; baris = roles |

### File yang Diubah / Dibuat

| File | Aksi |
|---|---|
| `apps_{portal}/web-vue/src/app/stores/auth.store.ts` | Update type `menus[]` |
| `apps_{portal}/web-vue/src/shared/composables/usePermission.ts` | Baru |
| `apps_{portal}/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue` | Redesign total |
| `apps_{portal}/bff-api/app/modules/appadmin/admin.py` | Update `require_menu` query + session menus |
| `apps_{portal}/api-python/app/modules/appadmin/router.py` | Endpoint baru |
| `apps_{portal}/api-python/app/modules/appadmin/service.py` | Logic baru |
| `infra/db/migrations/isf_auth/V###__replace_role_menu_with_permissions.sql` | Migration baru |

---

## Urutan Implementasi (aman untuk tidak downtime)

1. **DB migration** — buat `role_menu_permission`, migrate data, tapi **belum** drop `role_menu`
2. **api-python** — endpoint baru (read dari `role_menu_permission`)
3. **BFF** — update `require_menu()` ke tabel baru + update session menus[]
4. **web-vue** — update auth store + buat `usePermission` + redesign `RoleMenuView`
5. **Drop `role_menu`** — setelah semua layer live & validated
6. **E2E test** — `testing/e2e-role-menu-permission.sh`

---

## Tidak Dalam Scope

- Perubahan skema menu (`isf_auth.menu`) — tidak diubah
- Enforcement di level API (api-python) per aksi — BFF yang enforce via `require_menu()`; granular action enforcement ditambah di iterasi berikutnya jika diperlukan
- Portal wakaf — implementasi ini terlebih dahulu untuk zakat, lalu mirror ke wakaf
