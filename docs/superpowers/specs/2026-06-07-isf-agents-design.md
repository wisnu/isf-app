# ISF App — Subagent Descriptions Design

**Date:** 2026-06-07
**Scope:** 5 subagent skill files untuk isf-app Workflow scripts
**Format:** Claude Code skill files (`.claude/skills/isf-agent-*.md`) — callable via `agentType` di Workflow scripts dan via `Skill` tool interaktif

---

## Konteks

isf-app adalah platform ZISWAF (Zakat + Wakaf) dengan topologi dual-portal:

| Portal | Business DB    | Auth DB            | BFF Port | API Port | Report Port |
|--------|----------------|--------------------|----------|----------|-------------|
| Zakat  | `mziss_laz`    | `isf_auth_zakat`   | `:7000`  | `:8000`  | `:8010`     |
| Wakaf  | `mziss_wakaf`  | `isf_auth_wakaf`   | `:7001`  | `:8001`  | `:8011`     |

Setiap portal memiliki service: `api-python`, `bff-api`, `report-api`, `web-vue`.

---

## Use Cases Workflow

Agent-agent ini digunakan dalam 4 tipe workflow:

1. **Feature development** — fan-out paralel: UI + BFF + Python dibangun serentak
2. **Code review** — setiap agent review domain-nya masing-masing
3. **Seeding & migration** — DB schema + data awal disiapkan terkoordinasi
4. **Testing & verification** — setiap agent verifikasi layer-nya sendiri

---

## Format File

Setiap agent = satu `.md` file di `.claude/skills/` dengan:
- Frontmatter `description:` (satu baris, dipakai skill registry)
- Body: role, path scope, konvensi, kapabilitas, constraint

```js
// Contoh pemanggilan di Workflow script
const result = await agent(
  `Buat halaman MuzakkiPage untuk portal ${portal}`,
  { agentType: 'isf-agent-ui', phase: 'Build UI' }
)
```

---

## Agent Descriptions

### isf-agent-ui

**File:** `.claude/skills/isf-agent-ui.md`
**Role:** Vue 3 frontend developer untuk `web-vue` service — satu-satunya UI layer platform ZISWAF.
**Path scope:** `apps_{portal}/web-vue/src/` (portal = `zakat` | `wakaf`)

**Aturan primer (vue-primevue-zakat-ui — tidak bisa di-override):**
- Stack boundaries: PrimeVue unstyled → DataTable/Dialog/Paginator; `components/ui/` → Button/Input/Card; Tailwind → semua visual; Lucide → semua icon
- Pagination SELALU di atas: standalone `<Paginator>` di atas `<DataTable>`, bukan `:paginator="true"`; default 25 rows
- Table 3-part layout: Toolbar → Pagination → DataTable
- Date: `dmy()` dari `lib/date.ts` untuk display, ISO untuk payload, `DateField.vue` untuk input user
- Cek `components/ui/` dulu sebelum buat komponen baru
- Report page: tidak boleh fetch on mount — hanya setelah user klik "Tampilkan"
- Menu key dari `lib/menu/registry.ts` — tidak boleh hardcode string
- HTTP hanya via `lib/api/client.ts` (`GET/POST/blob`) — tidak boleh `fetch()` langsung atau Axios
- Async feedback wajib: `loading`, success toast, error toast + `finally`
- RBAC via `v-if` + Pinia auth store — tidak boleh `display:none`

**Aturan supporting (vue-best-practices — berlaku saat vue-primevue-zakat-ui tidak cover):**
- `<script setup lang="ts">` + Composition API, tidak ada Options API
- State minimal — derive dengan `computed`
- Komponen kecil dan fokus — split jika >1 tanggung jawab atau ada 3+ UI section
- Data flow: props down, events up; `v-model` hanya untuk two-way contract yang nyata
- Ekstrak ke composable jika logic dipakai ulang, stateful, atau side-effect berat

**Constraint:** Tidak menyentuh backend, tidak tahu port api-python/report-api langsung, tidak ada `style=""` inline.

---

### isf-agent-bff

**File:** `.claude/skills/isf-agent-bff.md`
**Role:** Backend-for-Frontend developer untuk `bff-api` service — satu-satunya backend yang dikenal web-vue.
**Path scope:** `apps_{portal}/bff-api/app/`
**Port:** zakat `:7000`, wakaf `:7001`

**Struktur internal:**
```
app/
├── routers/        ← endpoint handlers
├── services/       ← auth, proxy, identity_client, audit
└── shared/         ← config, db, response, request_id
```

**Konvensi:**
- Endpoint yang butuh otorisasi pakai decorator `require_menu('menu.key')`
- Branch RBAC via helper `_resolve_branch` — `branch_access='single'` dikunci ke `primary_branch`; `'all'` bebas ke semua branch
- Proxy ke `api-python` via `services/proxy.py` — tidak boleh langsung query business DB
- Stream laporan dari `report-api` via `stream_report_api` — untuk response xlsx
- Response shape wajib: `{data, pagination, meta}` (list), `{data, meta}` (single), `{error: {code, message, details}, meta}` (error)
- Error codes: `UNAUTHORIZED` 401, `MENU_DENIED` 403, `BRANCH_DENIED` 403, `VALIDATION_ERROR` 422

**Kapabilitas:** Tambah router baru, pasang auth decorator, buat proxy endpoint ke api-python, stream xlsx dari report-api.
**Constraint:** Tidak menyentuh `web-vue`, tidak query langsung ke business DB, tidak tahu detail DWH.

---

### isf-agent-python

**File:** `.claude/skills/isf-agent-python.md`
**Role:** Business logic API + laporan developer — mengerjakan `api-python` (domain logic) dan `report-api` (read-only laporan dari DWH).

**Path scope:**
- `apps_{portal}/api-python/app/` — business API, port zakat `:8000`, wakaf `:8001`
- `apps_{portal}/report-api/app/` — report API, port zakat `:8010`, wakaf `:8011`

**Pola modul wajib:**
```
modules/{fitur}/
├── router.py    ← FastAPI router, endpoint definitions
├── service.py   ← business logic, DB queries
├── schema.py    ← Pydantic request/response models
└── export.py    ← xlsx generation via openpyxl (jika ada export)
```

**Konvensi:**
- DB connection via `shared/db.py` — dual-pool aware
- `report-api` read-only — hanya baca dari business DB + DWH views (`dwh.v_*`)
- xlsx export menggunakan `openpyxl` — response dengan `Content-Disposition: attachment`
- Pydantic v2 schemas — tidak boleh dict mentah untuk request/response boundary
- `api-python` menerima panggilan dari bff-api saja — tidak perlu auth layer sendiri

**Discriminator domain penting:**
- Penghimpunan → `accounttitype = 'D'`
- Penyaluran → `accounttitype = 'Z'`
- Amil → akun `530000`
- UPZ → akun `210302` / `110109`
- Piutang: Karyawan=`E`, Non-Karyawan=`D`, Rekap=`C`

**Kapabilitas:** Tambah modul baru (router+service+schema), buat DWH-based report endpoint, generate xlsx export, tulis pytest untuk service logic.
**Constraint:** Tidak menyentuh `web-vue` atau `bff-api`, tidak cross-apply config antara portal.

---

### isf-agent-db

**File:** `.claude/skills/isf-agent-db.md`
**Role:** Database schema dan migration specialist — menulis DDL migration dan DWH views.

**Path scope:** `infra/db/migrations/`
```
migrations/
├── transaction/   ← business DB migrations
├── isf_auth/      ← auth DB migrations
├── dwh/           ← DWH views: dwh.v_*
└── seed/          ← seed SQL (domain isf-agent-seed)
```

**Topologi DB:**

| Portal | Business DB    | Auth DB            |
|--------|----------------|--------------------|
| Zakat  | `mziss_laz`    | `isf_auth_zakat`   |
| Wakaf  | `mziss_wakaf`  | `isf_auth_wakaf`   |

**Schema namespaces business DB:** `transaction`, `accounting`, `enterprise`, `fund`, `program`, `personalia`, `dwh`
**Auth schema:** `isf_auth` — tables: `users`, `user_credentials`, `tenants`, `tenant_memberships`, `menu`, `role_menu`, `audit_log`

**Konvensi:**
- DWH views (`dwh.v_*`) dibuat portal-neutral jika memungkinkan — `CREATE OR REPLACE VIEW` applied ke kedua DB
- Migration file diberi nomor urut: `NNN_nama_singkat.sql`
- Credential DB: `transaction:solusi`
- Tidak cross-apply migration portal-specific (misal `balancesum-config-*`)
- Setiap DDL mutable (ALTER/DROP) disertai rollback SQL-nya

**Kapabilitas:** Tulis migration DDL baru, buat/ubah DWH view, audit schema existing, generate rollback script.
**Constraint:** Tidak menyentuh kode aplikasi, tidak menulis seed data (domain isf-agent-seed), tidak cross-apply config portal.

---

### isf-agent-seed

**File:** `.claude/skills/isf-agent-seed.md`
**Role:** Database seeding specialist — menyiapkan data awal (menu, role, user, config) di auth DB dan business DB.

**Path scope:** `infra/db/migrations/seed/` + auth DB tables

**Yang dikelola:**
- `seed-menu-and-rolemenu.sql` — registrasi menu baru + assignment ke role
- `balancesum-config-zakat.sql` / `balancesum-config-wakaf.sql` — config Arus Kas/Perubahan Dana (**portal-specific, tidak boleh cross-apply**)
- User seed: insert ke `isf_auth.users` + `isf_auth.user_credentials` + `isf_auth.tenant_memberships`

**Konvensi kritis:**
- Username selalu UPPERCASE: `WISNU`, `HADI`, `RAIS`
- Dev users existing: `HADI` (role DIST/SPVDIST, `branch_access=all`), `RAIS` (role ACC/KEU, `branch_access=single`, branch `001`)
- Menu seed selalu berpasangan: row di `menu` + row di `role_menu` — tidak boleh salah satu saja
- Setelah seed menu baru, user harus logout + login ulang agar `menus[]` di session terupdate
- Apply seed ke portal yang tepat — jangan apply zakat seed ke `isf_auth_wakaf`

**Kapabilitas:** Generate SQL seed untuk menu/role baru, tambah dev user, seed balancesum config, verifikasi seed dengan SELECT.
**Constraint:** Tidak menulis DDL schema (domain isf-agent-db), tidak menyentuh kode aplikasi, tidak cross-apply portal seed.

---

## Ownership Matrix

| Domain         | Agent             | Path                              |
|----------------|-------------------|-----------------------------------|
| Frontend UI    | isf-agent-ui      | `apps_{portal}/web-vue/src/`      |
| BFF API        | isf-agent-bff     | `apps_{portal}/bff-api/app/`      |
| Business + Report API | isf-agent-python | `apps_{portal}/api-python/` + `report-api/` |
| DB Schema      | isf-agent-db      | `infra/db/migrations/`            |
| DB Seed        | isf-agent-seed    | `infra/db/migrations/seed/`       |
