# isf-app / web-vue — Claude Code Instructions

## Active Skills

For any Vue component, page, layout, or UI code in this project, use **both** skills:

1. **`vue-primevue-zakat-ui`** (primary) — project-specific conventions, stack
   boundaries, PrimeVue unstyled patterns, pagination, date handling, report
   pages, brand tokens. **These rules override everything else. No exceptions.**

2. **`vue-best-practices`** (supporting) — general Vue 3 Composition API best
   practices, `<script setup>` patterns, reactivity, component design.
   Apply when `vue-primevue-zakat-ui` doesn't address the specific case.

When the two conflict, `vue-primevue-zakat-ui` always wins.

---

## Project Identity

**App:** isf-app — ZISWAF Platform (Zakat + Wakaf)
**Service:** `web-vue` — Vue 3 SPA, the only UI layer
**Portal Zakat:** runs on `:5173`, talks to `bff-api` on `:7000`
**Portal Wakaf:** runs on `:5174`, talks to `bff-api` on `:7001`

The frontend ONLY knows `VITE_API_BASE_URL` (points to bff-api).
Never call `api-python` (:8000) or `report-api` (:8010) directly from the browser.

---

## Topology: 2 Portal × 2 Database

Each portal has two separate databases:

| Portal | Business DB    | Auth DB           |
|--------|---------------|-------------------|
| Zakat  | `mziss_laz`   | `isf_auth_zakat`  |
| Wakaf  | `mziss_wakaf` | `isf_auth_wakaf`  |

Business DB schemas: `transaction` / `accounting` / `enterprise` / `fund` / `program` / `personalia` + `dwh` (datamart final).
Auth DB schema: `isf_auth` — tables: `users`, `user_credentials`, `tenants`, `tenant_memberships`, `menu`, `role_menu`, `audit_log`.

Env vars (in `infra/.env`):
- `DATABASE_URL_ZAKAT` / `DATABASE_URL_WAKAF` — business DB
- `ISF_AUTH_DATABASE_URL_ZAKAT` / `ISF_AUTH_DATABASE_URL_WAKAF` — auth DB
- DB credentials on this host: `transaction:solusi`

---

## Tech Stack (actual, from architecture.md)

| Layer              | Tool                                        |
|--------------------|---------------------------------------------|
| Framework          | Vue 3.5 + Vite 5 + **TypeScript**           |
| Component Library  | PrimeVue 4.5 — **unstyled** mode            |
| UI Primitives      | reka-ui (shadcn-vue pattern)                |
| Styling            | Tailwind CSS 4.0                            |
| State              | Pinia 2.2                                   |
| Routing            | Vue Router 4.4 (named routes only)          |
| Charts             | Chart.js 4.4 via vue-chartjs                |
| Icons              | **Lucide icons** (not PrimeIcons)           |
| HTTP               | `lib/api/client.ts` — custom fetch wrapper  |
| Testing            | Vitest + Vue Test Utils                     |

> ⚠️ PrimeVue is in **unstyled** mode — do NOT assume default PrimeVue styles.
> All visual styling comes from Tailwind + reka-ui + custom `components/ui/`.

---

## Non-Negotiable Rules

### 1. Pagination Always on Top
- NEVER use `:paginator="true"` on `<DataTable>`
- ALWAYS use a standalone `<Paginator>` component placed ABOVE the table
- Default rows per page: **25**
- Always show record count: "Showing X–Y of Z records"

### 2. Hybrid Stack — Strict Boundaries
- **PrimeVue** → complex headless components (DataTable, Dialog, Steps, etc.)
- **reka-ui / components/ui/** → buttons, inputs, cards, alerts, badges
- **Tailwind** → layout, spacing, flex/grid, responsive, all visual styling
- PrimeVue is unstyled — never rely on its default theme classes

### 3. Always TypeScript + `<script setup>`
- All files use `.ts` / `.vue` with `<script setup lang="ts">`
- No Options API, no `defineComponent()`, no `.js` files in `src/`
- Type all props, emits, and composable return values

### 4. API — Use `lib/api/client.ts` Only
- Use the project's fetch wrapper: `GET()`, `POST()`, `blob()` from `lib/api/client.ts`
- Never use raw `fetch()` or install Axios — client.ts is the only HTTP layer
- Base URL is always `VITE_API_BASE_URL` (resolves to bff-api)

### 5. Date Handling
- **Display:** always use `dmy()` from `lib/date.ts` → formats to `DD-MM-YYYY`
- **Internal / API payload:** always ISO `YYYY-MM-DD`
- **User input:** always use `components/ui/DateField.vue` (v-model = ISO string)
- Never format dates inline in templates — always go through `dmy()`
- Backend columns stay ISO (`to_char(...,'YYYY-MM-DD')`) — never alias to DD-MM-YYYY (breaks ORDER BY)

### 6. UI Components — Use Existing First
Before creating a new component, check `components/ui/` for:
- `Button`, `Card`, `Input`, `Alert` — standard primitives
- `DateField.vue` — all date inputs
- `SearchSelect.vue` — all long dropdowns (combobox + keyboard nav + clear)
- `TablePagination.vue` — pagination display
- `Modal.vue` — dialogs/modals

Only create a new `components/ui/` component if nothing fits.

### 7. Report Pages — No Auto-Load
- Report/laporan pages must NOT fetch data on mount
- Data is fetched only when the user clicks "Tampilkan" (Show)
- Always show an empty/prompt state before the button is clicked
- Export disabled until data is present

### 8. Menu Keys — Use Registry
- All menu keys must be registered in `lib/menu/registry.ts` (MENU_KEYS)
- Every route that requires a menu permission must have `meta.menu_key`
- Never hardcode menu key strings outside of the registry

### 9. Async Feedback Is Mandatory
Every async operation must have all three:
- `loading = true` before the call
- success toast on success
- error toast on failure + `finally` resets loading
- Never use `alert()`, `confirm()`, or `console.log` in components

### 10. Role-Based UI
- Use `v-if` tied to Pinia `auth` store — never CSS `display:none`
- Auth store (`stores/auth.ts`) exposes: `user`, `roles`, `menus[]`, `branches`, `active_tenant_id`
- Check menu access via `menus[]` — session snapshot from login
- `menus[]` is populated at login time; new `role_menu` rows only take effect after **logout + login**

---

## Actual Folder Structure

```
src/
├── main.ts                   ← entry: mount + Pinia + router + PrimeVue
├── App.vue
├── router/
│   └── index.ts              ← 60+ named routes, meta.menu_key per route
├── stores/
│   ├── auth.ts               ← user, roles, menus[], branches, active_tenant
│   ├── sidebar.ts            ← collapsed state, active menu
│   ├── notifications.ts
│   └── theme.ts              ← dark/light mode
├── pages/
│   ├── LoginPage.vue
│   ├── DashboardPage.vue
│   ├── dashboard/            ← KeuanganPage, PenyaluranPage, PenghimpunanPage
│   ├── keuangan/             ← all financial pages (CoaPage, KasPage, etc.)
│   ├── HistoriTransaksiPage.vue
│   ├── admin/                ← RoleMenuPage, UsersPage
│   └── profile/              ← PasswordPage
├── components/
│   ├── AppHeader.vue
│   ├── AppSidebar.vue
│   ├── AppLogo.vue
│   ├── UserMenu.vue
│   ├── SystemDate.vue
│   ├── NotificationBell.vue
│   ├── widgets/              ← chart widgets per dashboard domain
│   └── ui/                   ← Button, Card, Input, Alert, DateField,
│                                SearchSelect, TablePagination, Modal, ...
├── lib/
│   ├── api/client.ts         ← fetch wrapper: GET/POST/blob
│   ├── date.ts               ← dmy() — ISO → DD-MM-YYYY display
│   ├── format.ts             ← currency, number formatters
│   ├── charts.ts             ← Chart.js global plugin register
│   ├── menu/registry.ts      ← MENU_KEYS — single source of truth
│   └── useFetch.ts           ← composable: loading/error/data state
```

---

## API Response Shape

Always handle these shapes from bff-api:

```ts
// Single object
{ data: { ... }, meta: { request_id: string } }

// List with pagination
{
  data: [...],
  pagination: { page: number, limit: number, total: number, total_pages: number },
  meta: { request_id: string }
}

// Error
{ error: { code: string, message: string, details: null }, meta: { request_id: string } }
```

Common error codes to handle in UI:
- `UNAUTHORIZED` (401) → redirect to login
- `MENU_DENIED` (403) → show "Access Denied" message
- `BRANCH_DENIED` (403) → show branch restriction message
- `VALIDATION_ERROR` (422) → show field-level errors

---

## Table Page Layout (3-Part Structure)

```
┌────────────────────────────────────────────────────┐
│ TOOLBAR  [Search input]  [Filter btn]  [Add btn]   │  rounded-t border
├────────────────────────────────────────────────────┤
│ PAGINATION  Showing 1–25 of 342      [< 1 2 3 >]  │  border-x
├────────────────────────────────────────────────────┤
│ DataTable (lazy, no built-in paginator)            │  rounded-b border
└────────────────────────────────────────────────────┘
```

---

## Auth & RBAC (Frontend Context)

- **Login flow**: BFF authenticates → fetches profile via IdentityClient → populates session with `user_id`, `active_tenant_id`, `roles[]`, `branches[]`, `primary_branch`, `branch_access`, `menus[]`
- **Branch RBAC**: `branch_access='all'` if `enterprise.userapp.tipe_akses_cabang='S'` (Seluruh); else `'single'` (Tunggal — default branch only). BFF locks `'single'` users to `primary_branch` (403 on others)
- **Sidebar filtering**: sidebar children filtered by `auth.menus` (each item has `menu_key`). Wakaf portal filters; zakat portal currently does not
- **Username convention**: input case-insensitive, stored uppercase. Normalized at BFF boundary — `wisnu`, `WISNU`, `Wisnu` all match `username='WISNU'`
- **Dev E2E users** (password `test1234`, set manually in `isf_auth_*.user_credentials`): `HADI` (DIST/SPVDIST, branch_access=all) for dashboard/jurnal; `RAIS` (ACC/KEU, single-branch 001) for laporan kas/finance

---

## Dashboard — Independent Widget Load

Dashboard pages (`DashboardPage`, `DashboardKeuanganPage`, `DashboardPenyaluranPage`) have no shared loading state — each widget loads independently via `useFetch(fetcher)` in `lib/useFetch.ts`. A failed widget shows its own error; other widgets render normally.

---

## Report System (Laporan)

**report-api** = separate FastAPI service per portal, read-only to business DB + DWH.
Ports: zakat **:8010**, wakaf **:8011**. BFF proxies via `stream_report_api`.

### Adding a New Report Page (5-Step Pattern)

When asked to add a laporan/report page, always follow this order:

1. **DWH view** — `dwh.v_<name>` in `mziss_*` (backend, not frontend)
2. **report-api module** — `service.py` + `router.py` + `export.py` (openpyxl)
3. **BFF route** — `require_menu('keuangan.report.<key>')` + `_resolve_branch` + `stream_report_api` for xlsx
4. **Frontend** — new `pages/keuangan/Laporan*Page.vue` + key in `lib/menu/registry.ts` + sidebar child in "Laporan" group + route with `meta.menu_key`
5. **Seed** — menu + role_menu rows in `seed-menu-and-rolemenu.sql`, apply to `isf_auth_zakat`

Frontend step (4) is the only step this agent handles.

### Report UX Rules
- Filter: use `DateField.vue` (v-model = ISO string, displays DD-MM-YYYY) — never `<input type="date">`
- Preview: wrap date cells with `dmy()` from `lib/date.ts`
- Long dropdowns (rekening, akun): use `SearchSelect.vue`
- Export: BFF sets `Content-Disposition`; `downloadBlob` defers `revokeObjectURL` so Chrome preserves filename

### Active Reports: Zakat + Wakaf (mirrored 2026-06-01)
Jurnal Harian, List Transaksi Umum, Transaksi Kas/Bank Harian, Rekapitulasi Kas/Bank, Monitoring Saldo Bulanan.
DWH views are portal-neutral (`infra/db/migrations/dwh/v_*.sql`, applied to both DBs).

### Active Reports: Zakat Only (17 laporan)
Akuntansi: Trial Balance, Neraca, Arus Kas, Perubahan Dana, Perubahan Dana Detail, Buku Besar.
Transaksi: Penghimpunan (accounttitype='D'), Penyaluran ('Z'), Penerimaan/Pengeluaran Amil (akun 530000),
Piutang Karyawan/Non-Karyawan/Rekap Uang Muka (accountreceivabletype E/D/C), List UPZ (akun 210302/110109),
List Uang Muka, Realisasi Memo, Piutang Realisasi.

### Config Arus Kas/Perubahan Dana
- Config in `transaction.balancesum*` — portal-specific, do NOT cross-apply seeders
- Zakat: `infra/db/migrations/seed/balancesum-config-zakat.sql` (31 AK_MUT items)
- Wakaf: `infra/db/migrations/seed/balancesum-config-wakaf.sql` (6 items, different COA)

---

## Commit Convention

**Mandatory format:**

```
[TAG] type(scope): subject
```

- `[TAG]` = short UPPER-KEBAB tag relevant to the change (e.g. `[UX]`, `[DASHBOARD]`, `[UPLOAD-PENGHIMPUNAN]`). Reuse active tags or create a descriptive new one
- Conventional-commit follows: `feat`, `fix`, `chore`, `docs`, `refactor` + scope naming the feature/context
- Check history for examples: `git log --grep='\['`

Active tags: `UX`, `PRIMEVUE`, `INDEPENDENT-LOAD`, `DASHBOARD`, `DASHBOARD-KEUANGAN`, `ETL`, `DWH`, `DOCS`, `RECOVERY`, `ADMIN-USERS`, `CHANGE-PASSWORD`, `AUTH-PG`, `MIGRATE-AUTHDB`

---

## Testing Convention

Every new feature → reusable E2E script in `testing/`:
- `testing/e2e-<feature>.sh` (curl-based, targets localhost ports)
- Per-service test wrappers: `apps_*/api-python/test.sh`, `apps_*/bff-api/test.sh`
- Python tests in `tests/` with pytest. TDD for service logic with non-trivial branching

---

## Dev Workflow

**Host**: Fedora 44 / kernel 7 / crun / SELinux Enforcing.
`podman build` inside `podman-compose up --build` fails at `pip install`/`npm install` due to SELinux MCS mprotect block.
Workaround: pre-build with `--security-opt label=disable`, then `up -d` without `--build`.
Compose already carries `security_opt: [label=disable]` per service.

Use **`Makefile`** shortcuts: `make build`, `make run`, `make health`, `make migrate`.

```bash
# Pre-build (only when pyproject.toml / package.json changes — source is bind-mounted)
for portal in zakat wakaf; do
  for svc in api-python report-api bff-api web-vue; do
    (cd apps_$portal/$svc && \
     podman build --security-opt label=disable -t isf-$portal-$svc:dev -f Dockerfile.dev .)
  done
done

# Start (no --build)
cd infra
podman-compose -f docker-compose.zakat.yml up -d   # → http://localhost:5173
podman-compose -f docker-compose.wakaf.yml up -d   # → http://localhost:5174
```

`.env` optional — compose uses `${VAR:-...}` defaults for dev. Copy `.env.example → .env` to override HOST_IP, Google OAuth, etc.

> ⚠️ Never host the working repo on NTFS — the repo was lost once (2026-05-27) due to NTFS corruption. Working tree is now at `~/workshop/isf-app/` (ext4).

---

## What This Agent Does NOT Do

- No backend code (bff-api, api-python, report-api)
- No database queries or migrations
- No Docker/podman compose changes
- No direct calls to api-python (:8000) or report-api (:8010) from frontend
- No raw `fetch()` — always use `lib/api/client.ts`
- No Options API, no Vuex, no Axios
- No inline `style="..."` — Tailwind classes only
