# Plan — Modular `src/` Refactor + Domain Navigation

**Slug:** `2026-06-21-001-modular-src-refactor`
**Portal:** Zakat first → Wakaf after
**See:** [`specs.md`](./specs.md)
**Commit tag:** `[MODULAR-REFACTOR]`
**Strategy:** One phase per logical boundary. Each phase ends with `make health` + browser smoke. No logic changes — every file move is pure structural.

> **Invariant throughout:** Named route names never change. BFF contract never changes. File internals never change.

---

## Phase 0 — Scaffold new directories

- [x] Create `src/app/`, `src/app/router/`, `src/app/stores/`, `src/app/views/`, `src/app/views/profile/`
- [x] Create `src/layouts/`
- [x] Create `src/shared/api/`, `src/shared/components/`, `src/shared/composables/`, `src/shared/utils/`, `src/shared/constants/`
- [x] Create `src/modules/finance/`, `src/modules/finance/components/`, `src/modules/finance/types/`
- [x] Create `src/modules/finance/views/` subtree (all 8 folders: dashboard, master, budget, transaction, inquiry, upload, reports, monitoring + their subfolders)
- [x] Create `src/modules/administration/views/users/`, `src/modules/administration/views/role-menu/`
- [x] Create stub folders: `src/modules/fundraising/views/`, `src/modules/distribution/`, `src/modules/enterprise/`
- [x] Verify: `git status` shows only new empty dirs (no file changes yet)

---

## Phase 1 — `lib/` → `shared/`

- [x] `git mv lib/api/client.ts shared/api/client.ts`
- [x] `git mv lib/date.ts shared/utils/date.ts`
- [x] `git mv lib/format.ts shared/utils/format.ts`
- [x] `git mv lib/charts.ts shared/utils/charts.ts`
- [x] `git mv lib/utils.ts shared/utils/utils.ts`
- [x] `git mv lib/download.ts shared/utils/download.ts`
- [x] `git mv lib/portal.ts shared/utils/portal.ts`
- [x] `git mv lib/useFetch.ts shared/composables/useFetch.ts`
- [x] `git mv lib/useToast.ts shared/composables/useToast.ts`
- [x] `git mv lib/menu/registry.ts shared/constants/menu-keys.ts`
- [x] Update all `@/lib/` import paths across all `.vue` + `.ts` files (grep + sed or IDE replace-all):
  - `@/lib/api/client` → `@/shared/api/client`
  - `@/lib/date` → `@/shared/utils/date`
  - `@/lib/format` → `@/shared/utils/format`
  - `@/lib/utils` → `@/shared/utils/utils`
  - `@/lib/download` → `@/shared/utils/download`
  - `@/lib/portal` → `@/shared/utils/portal`
  - `@/lib/charts` → `@/shared/utils/charts`
  - `@/lib/useFetch` → `@/shared/composables/useFetch`
  - `@/lib/useToast` → `@/shared/composables/useToast`
  - `@/lib/menu/registry` → `@/shared/constants/menu-keys`
- [x] Delete empty `lib/` directory
- [x] `make health` → green. Browser: login + one page load.

---

## Phase 2 — `components/ui/` + `components/layout/` → `shared/components/`

- [x] `git mv components/ui/*.vue shared/components/` (25 files)
- [x] `git mv components/layout/*.vue shared/components/` (5 files)
- [x] Update all `@/components/ui/` → `@/shared/components/` imports
- [x] Update all `@/components/layout/` → `@/shared/components/` imports
- [x] Delete empty `components/ui/` and `components/layout/`
- [x] `make health` → green. Browser smoke.

---

## Phase 3 — `components/App*.vue` + root → `layouts/`

- [x] `git mv components/AppHeader.vue layouts/AppHeader.vue`
- [x] `git mv components/AppSidebar.vue layouts/AppSidebar.vue`
- [x] `git mv components/AppLogo.vue layouts/AppLogo.vue`
- [x] `git mv components/NotificationBell.vue layouts/NotificationBell.vue`
- [x] `git mv components/SystemDate.vue layouts/SystemDate.vue`
- [x] `git mv components/UserAvatar.vue layouts/UserAvatar.vue`
- [x] `git mv components/UserMenu.vue layouts/UserMenu.vue`
- [x] Update `@/components/App*` + root component imports → `@/layouts/*` (in `App.vue`, `AppHeader.vue`)
- [x] `make health` → green. Browser smoke.

---

## Phase 4 — Domain-specific `components/` → `modules/finance/components/`

- [x] `git mv components/authorization/ modules/finance/components/authorization/`
- [x] `git mv components/finance/ modules/finance/components/finance/`
- [x] `git mv components/modals/ modules/finance/components/modals/`
- [x] `git mv components/parameter/ modules/finance/components/parameter/`
- [x] `git mv components/widgets/ modules/finance/components/widgets/`
- [x] Update all imports from `@/components/authorization/`, `@/components/finance/`, `@/components/modals/`, `@/components/parameter/`, `@/components/widgets/`
- [x] `make health` → green. Browser smoke.

---

## Phase 5 — `stores/` → `app/stores/` (+ rename `*.store.ts`)

- [x] `git mv stores/auth.ts app/stores/auth.store.ts`
- [x] `git mv stores/sidebar.ts app/stores/sidebar.store.ts`
- [x] `git mv stores/notifications.ts app/stores/notification.store.ts`
- [x] `git mv stores/theme.ts app/stores/theme.store.ts`
- [x] Update all `@/stores/auth` → `@/app/stores/auth.store` imports
- [x] Update all `@/stores/sidebar` → `@/app/stores/sidebar.store` imports
- [x] Update all `@/stores/notifications` → `@/app/stores/notification.store` imports
- [x] Update all `@/stores/theme` → `@/app/stores/theme.store` imports
- [x] Delete empty `stores/`
- [x] `make health` → green. Browser smoke.

---

## Phase 6 — `pages/` → `modules/*/views/` (+ `Page` → `View` rename)

Largest phase. Do with `git mv` in batches per sub-folder.

### 6a — Auth + profile
- [x] `git mv pages/LoginPage.vue app/views/LoginView.vue`
- [x] `git mv pages/NoTenantPage.vue app/views/NoTenantView.vue`
- [x] `git mv pages/profile/PasswordPage.vue app/views/profile/PasswordView.vue`
- [x] `git mv pages/DonorDetailPage.vue modules/fundraising/views/DonorDetailView.vue`

### 6b — Dashboard
- [x] `git mv pages/dashboard/DashboardPage.vue modules/finance/views/dashboard/DashboardView.vue`
- [x] `git mv pages/dashboard/DashboardFinancePage.vue modules/finance/views/dashboard/DashboardFinanceView.vue`
- [x] `git mv pages/dashboard/DashboardDistributionPage.vue modules/finance/views/dashboard/DashboardDistributionView.vue`
- [x] `git mv pages/dashboard/DashboardCollectionPage.vue modules/finance/views/dashboard/DashboardCollectionView.vue`

### 6c — Finance master
- [x] Move `pages/finance/coa/` → `modules/finance/views/master/coa/` (2 files)
- [x] Move `pages/finance/cash/` → `modules/finance/views/master/cash/` (2 files)
- [x] Move `pages/finance/bank/` → `modules/finance/views/master/bank/` (2 files)
- [x] Move `pages/finance/petty-cash/` → `modules/finance/views/master/petty-cash/` (2 files)
- [x] `git mv pages/parameter/BudgetOwnerPage.vue modules/finance/views/master/budget-owner/BudgetOwnerView.vue`

### 6d — Finance budget
- [x] Move `pages/finance/budget-import/` → `modules/finance/views/budget/import/` (1 file, rename)
- [x] Move `pages/finance/budget-revise/` → `modules/finance/views/budget/revise/` (2 files)
- [x] `git mv pages/parameter/BudgetItemPage.vue modules/finance/views/budget/item/BudgetItemView.vue`
- [x] `git mv pages/parameter/BudgetPeriodPage.vue modules/finance/views/budget/period/BudgetPeriodView.vue`

### 6e — Finance inquiry
- [x] Move `pages/finance/budget-inquiry/` → `modules/finance/views/inquiry/budget/` (3 files, rename)
- [x] Move `pages/finance/transaction-history/` → `modules/finance/views/inquiry/transaction-history/` (2 files)

### 6f — Finance transaction
- [x] Move `pages/finance/fund-collection/` → `modules/finance/views/transaction/fund-collection/` (2 files)
- [x] Move `pages/finance/fund-distribution/` → `modules/finance/views/transaction/fund-distribution/` (2 files)
- [x] Move `pages/finance/cash-advance/` → `modules/finance/views/transaction/cash-advance/` (2 files)
- [x] Move `pages/finance/cash-advance-lpj/` → `modules/finance/views/transaction/cash-advance-lpj/` (2 files)
- [x] Move `pages/finance/fund-transfer/` → `modules/finance/views/transaction/fund-transfer/` (2 files)
- [x] Move `pages/finance/general-transaction/` → `modules/finance/views/transaction/general/` (2 files)
- [x] Move `pages/finance/amil-income/` → `modules/finance/views/transaction/amil-income/` (2 files)
- [x] Move `pages/finance/amil-expense/` → `modules/finance/views/transaction/amil-expense/` (2 files)
- [x] Move `pages/finance/receivable/` → `modules/finance/views/transaction/receivable/` (2 files)

### 6g — Finance upload
- [x] Move `pages/finance/upload-collection-multi/` → `modules/finance/views/upload/collection/` (3 files, rename Multi→ drop)
- [x] Move `pages/finance/upload-collection-hc/` → `modules/finance/views/upload/zis-routine/` (2 files, rename HCZis→ZisRoutine)

### 6h — Finance reports
- [x] Move all `pages/finance/reports/Report*Page.vue` → `modules/finance/views/reports/Report*View.vue` (19 files)

### 6i — Finance monitoring
- [x] `git mv pages/finance/AuthorizationPage.vue modules/finance/views/monitoring/AuthorizationView.vue`
- [x] `git mv pages/finance/SubmissionHistoryPage.vue modules/finance/views/monitoring/SubmissionHistoryView.vue`

### 6j — Administration
- [x] `git mv pages/admin/UsersPage.vue modules/administration/views/users/UsersView.vue`
- [x] `git mv pages/admin/RoleMenuPage.vue modules/administration/views/role-menu/RoleMenuView.vue`

### 6k — Update all router `component: () => import(...)` paths
- [x] Update every import path in `router/index.ts` to match new view locations
- [x] Update URL paths for 5 changed routes (specs §6)
- [x] Delete empty `pages/`, `parameter/` directories
- [x] `make health` → green. Full browser smoke: login, dashboard, 3 transaction pages, 1 report, otorisasi.

---

## Phase 7 — Per-module `routes.ts` split

- [x] Create `modules/finance/routes.ts` — extract all finance + dashboard routes from router/index.ts
- [x] Create `modules/administration/routes.ts` — extract admin routes
- [x] Create stub `modules/fundraising/routes.ts`, `modules/distribution/routes.ts`, `modules/enterprise/routes.ts`
- [x] Rewrite `app/router/index.ts` (or current `router/index.ts`) to import + spread module routes
- [x] Move `router/guards.ts` — extract `beforeEach` logic to separate file
- [x] `make health` → green. Full smoke test. Check route guards (login redirect, menu_key guard).

---

## Phase 8 — Navigation: `AppDomainRail.vue` + `AppSidebar.vue` rewrite

- [x] Create `lib/nav/index.ts` → `shared/constants/domains.ts` with `DomainConfig` type + `DOMAIN_MAP`
- [x] Create `modules/finance/menu.ts` — full DomainConfig for Finance (all 8 groups)
- [x] Create `modules/administration/menu.ts` — DomainConfig for Administration
- [x] Create `layouts/AppDomainRail.vue`:
  - Reads `route.meta.domain` for active state
  - On click unlocked domain: `router.push(domain.defaultRoute)` + expand sidebar if collapsed
  - Tooltip on hover per domain button
  - Locked domains (fundraising, distribution, enterprise): greyed, tooltip shows phase
- [x] Rewrite `layouts/AppSidebar.vue`:
  - Remove hardcoded `groups` array
  - Read `DOMAIN_MAP[route.meta.domain]` for current domain config
  - Add domain header section (label + sub)
  - Add search input (client-side filter, shows group label in result)
  - Keep existing expand/collapse + localStorage persist behavior
  - Keep `visibleChildren()` RBAC filter logic
- [x] Update `App.vue` layout grid: add rail column (`56px`) left of sidebar
- [x] Add `meta.domain` to all routes in module routes files
- [x] `make health` → green. Full smoke: domain switch Keuangan↔Administrasi, search "piutang", collapse sidebar, domain rail tooltips.

---

## Phase 9 — `main.ts` + `App.vue` → `app/`

- [x] `git mv src/main.ts src/app/main.ts`
- [x] `git mv src/App.vue src/app/App.vue`
- [x] `git mv src/router/ src/app/router/` (if not already done in phase 7)
- [x] Update `vite.config.ts`: set `input` (or `entry`) to `src/app/main.ts`
- [x] Update any remaining `src/main.ts` references
- [x] `make health` → green. Full smoke.

---

## Phase 10 — Wakaf portal mirror

- [x] Apply phases 0–9 to `apps_wakaf/web-vue/src/` (fewer files, same structure)
- [x] Wakaf-specific page renames (see specs §12)
- [x] `make health` (wakaf) → green. Browser smoke `:5174`.

---

## Post-refactor

- [x] Update `CLAUDE.md` folder structure section to reflect new paths
- [x] Update `nuwis-ui-builder` skill path references
- [x] Grep for any remaining `@/lib/`, `@/pages/`, `@/stores/[^a]`, `@/components/ui/`, `Page.vue` → confirm zero stale refs
- [x] Single commit per phase, tag `[MODULAR-REFACTOR]`
