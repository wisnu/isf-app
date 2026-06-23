# RBAC Permission Model — isf-app

**Berlaku sejak:** 2026-06-23
**Menggantikan:** model boolean `role_menu` (sebelum commit 8c80aaf)

---

## Ringkasan

isf-app menggunakan model RBAC (Role-Based Access Control) berbasis **aksi per menu**.
Setiap role dapat diberi kombinasi aksi spesifik (`view`, `tambah`, `edit`, `hapus`, `detail`)
untuk setiap menu key — bukan sekadar akses/tidak akses.

---

## 1. Skema Database

### Tabel Utama: `isf_auth.role_menu_permission`

```sql
CREATE TABLE isf_auth.role_menu_permission (
    id         SERIAL PRIMARY KEY,
    role_id    VARCHAR(50)  NOT NULL,
    menu_key   VARCHAR(100) NOT NULL,
    action     VARCHAR(20)  NOT NULL
               CHECK (action IN ('view','tambah','edit','hapus','detail')),
    updated_by VARCHAR(100),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_role_menu_action UNIQUE (role_id, menu_key, action)
);
```

**Tabel pendukung (tidak diubah):**

```
isf_auth.menu          → katalog menu: menu_key, label, group_label, route_path, sort_order, status
isf_auth.users         → user registry
enterprise.peran       → role master (id_peran, nama_peran, status_peran)
enterprise.listperanuser → user-role assignment
```

### Arti Aksi

| action  | Arti                                  |
|---------|---------------------------------------|
| `view`  | Bisa membuka/melihat halaman menu     |
| `tambah`| Bisa membuat data baru               |
| `edit`  | Bisa mengubah data yang ada           |
| `hapus` | Bisa menghapus data                   |
| `detail`| Bisa melihat halaman detail dari list |

### Aturan Dependency

- Check `tambah`/`edit`/`hapus`/`detail` tanpa `view` = tidak valid → FE auto-check `view` saat pilih aksi lain
- Uncheck `view` → FE auto-clear semua aksi lain

---

## 2. Alur Data: Login → BFF → Frontend

```
1. Login  → BFF query isf_auth.role_menu_permission
           → aggregate per menu_key:
             SELECT menu_key, array_agg(DISTINCT action) AS actions
             FROM isf_auth.role_menu_permission
             WHERE role_id = ANY($roles)
             GROUP BY menu_key

2. BFF    → build_user_public()
           → response: { menus: [{menu_key, actions[]}] }

3. Pinia  → auth.store.ts menerima menus: MenuPermission[]
           → menus computed  → string[]     (backward compat: menu_key list)
           → menuActions computed → Record<string, string[]>  (action lookup)

4. Vue    → usePermission(menuKey) → { canView, canAdd, canEdit, canDelete, canDetail }
           → v-if="canAdd" untuk sembunyikan tombol
```

**Session tidak menyimpan permission di cookie** — diambil dari role cache di BFF dengan TTL 5 menit.

---

## 3. Gate di BFF: `require_menu()`

```python
# apps_{portal}/bff-api/app/services/auth.py

def require_menu(menu_key: str):
    async def _check(request: Request):
        menus = await get_menus_for_roles(roles, db)
        # Gate: harus punya action 'view' untuk menu_key ini
        if not any(m["menu_key"] == menu_key and "view" in m.get("actions", []) for m in menus):
            raise AppHTTPError(403, err("MENU_FORBIDDEN", ...))
        return user_id
    return _check
```

> **Penting:** `require_menu("finance.coa")` hanya lolos jika role punya action `view` untuk menu tersebut.
> Role dengan hanya `tambah` tanpa `view` tidak akan lolos gate ini.

---

## 4. Frontend: Auth Store & Composable

### `auth.store.ts`

```ts
export interface MenuPermission {
  menu_key: string
  actions: string[]
}

// User.menus adalah MenuPermission[] (bukan string[])
// Backward compat: auth.menus computed → string[] (untuk menus.includes() yang sudah ada)
// New: auth.menuActions computed → Record<string, string[]>
```

### `usePermission(menuKey)` — `shared/composables/usePermission.ts`

```ts
const { canView, canAdd, canEdit, canDelete, canDetail } = usePermission(MENU_KEYS.FINANCE_COA)

// Pemakaian di template:
// <Button v-if="canAdd">Tambah</Button>
// <Button v-if="canEdit" @click="edit(row)">Edit</Button>
```

---

## 5. Admin UI: Pengaturan Menu

**Route:** `/appadmin/role-menu`
**Menu key:** `appadmin.role_menu`
**File:** `modules/appadmin/views/role-menu/RoleMenuView.vue`

**UX:**
1. Pilih role dari SearchSelect
2. Lihat accordion per domain group (`group_label` dari `isf_auth.menu`)
3. Setiap menu row punya 5 checkbox: V / T / E / H / D
4. Save → `PUT /api/appadmin/role-menu-permission` untuk role yang dipilih
5. Export → `GET /api/appadmin/role-menu-permission/export` → Excel matrix

---

## 6. API Endpoints

| Method | BFF Path | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/appadmin/role-menu-permission?role_id=X` | Semua roles + menus + permissions role X |
| `PUT` | `/api/appadmin/role-menu-permission` | Simpan semua permission untuk satu role (atomic replace) |
| `GET` | `/api/appadmin/role-menu-permission/export` | Excel matrix semua role × menu × action |

**PUT body:**
```json
{
  "role_id": "KEU",
  "permissions": [
    { "menu_key": "finance.dashboard", "actions": ["view"] },
    { "menu_key": "finance.jurnal", "actions": ["view", "tambah", "edit"] }
  ]
}
```

**Scope save:** satu role per request. DELETE all + INSERT all dalam satu transaction.

---

## 7. Seeding Permission Baru

Untuk menu baru, tambah baris ke `isf_auth.role_menu_permission`:

```sql
-- Seed permission untuk menu baru
INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
VALUES
  ('ADM',  'finance.new_feature', 'view'),
  ('ADM',  'finance.new_feature', 'tambah'),
  ('ADM',  'finance.new_feature', 'edit'),
  ('ADM',  'finance.new_feature', 'hapus'),
  ('ADM',  'finance.new_feature', 'detail'),
  ('KEU',  'finance.new_feature', 'view'),
  ('KEU',  'finance.new_feature', 'tambah')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;
```

**Apply ke kedua DB:**
```bash
psql -U transaction -d isf_auth_zakat -h localhost -f seed-new-feature-permission.sql
psql -U transaction -d isf_auth_wakaf  -h localhost -f seed-new-feature-permission.sql
```

---

## 8. Migrasi dari Model Lama

Model lama (`isf_auth.role_menu` dengan `id_peran` kolom) sudah dihapus per 2026-06-23.
Semua data dimigrasikan ke `role_menu_permission` dengan `action='view'`.

Referensi migration: `infra/db/migrations/isf_auth/add-role-menu-permission.sql`
