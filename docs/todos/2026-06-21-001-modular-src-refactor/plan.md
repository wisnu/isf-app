# Plan — Modular `src/` Refactor + Domain Navigation

**Slug:** `2026-06-21-001-modular-src-refactor`
**Portal:** Zakat first → Wakaf after
**See:** [`specs.md`](./specs.md)
**Commit tag:** `[MODULAR-REFACTOR]`
**Strategy:** One phase per logical boundary. Each phase ends with `make health` + browser smoke. No logic changes — every file move is pure structural.

> **Invariant throughout:** Named route names never change. BFF contract never changes. File internals never change.

---

## Phase 0 — Scaffold new directories

- [ ] Create `src/app/`, `src/app/router/`, `src/app/stores/`, `src/app/views/`, `src/app/views/profile/`
- [ ] Create `src/layouts/`
- [ ] Create `src/shared/api/`, `src/shared/components/`, `src/shared/composables/`, `src/shared/utils/`, `src/shared/constants/`
- [ ] Create `src/modules/finance/`, `src/modules/finance/components/`, `src/modules/finance/types/`
- [ ] Create `src/modules/finance/views/` subtree (all 8 folders: dashboard, master, budget, transaction, inquiry, upload, reports, monitoring + their subfolders)
- [ ] Create `src/modules/administration/views/users/`, `src/modules/administration/views/role-menu/`
- [ ] Create stub folders: `src/modules/fundraising/views/`, `src/modules/distribution/`, `src/modules/enterprise/`
- [ ] Verify: `git status` shows only new empty dirs (no file changes yet)

---

## Phase 1 — `lib/` → `shared/`

- [ ] `git mv lib/api/client.ts shared/api/client.ts`
- [ ] `git mv lib/date.ts shared/utils/date.ts`
- [ ] `git mv lib/format.ts shared/utils/format.ts`
- [ ] `git mv lib/charts.ts shared/utils/charts.ts`
- [ ] `git mv lib/utils.ts shared/utils/utils.ts`
- [ ] `git mv lib/download.ts shared/utils/download.ts`
- [ ] `git mv lib/portal.ts shared/utils/portal.ts`
- [ ] `git mv lib/useFetch.ts shared/composables/useFetch.ts`
- [ ] `git mv lib/useToast.ts shared/composables/useToast.ts`
- [ ] `git mv lib/menu/registry.ts shared/constants/menu-keys.ts`
- [ ] Update all `@/lib/` import paths across all `.vue` + `.ts` files (grep + sed or IDE replace-all):
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
- [ ] Delete empty `lib/` directory
- [ ] `make health` → green. Browser: login + one page load.

---

## Phase 2 — `components/ui/` + `components/layout/` → `shared/components/`

- [ ] `git mv components/ui/*.vue shared/components/` (25 files)
- [ ] `git mv components/layout/*.vue shared/components/` (5 files)
- [ ] Update all `@/components/ui/` → `@/shared/components/` imports
- [ ] Update all `@/components/layout/` → `@/shared/components/` imports
- [ ] Delete empty `components/ui/` and `components/layout/`
- [ ] `make health` → green. Browser smoke.

---

## Phase 3 — `components/App*.vue` + root → `layouts/`

- [ ] `git mv components/AppHeader.vue layouts/AppHeader.vue`
- [ ] `git mv components/AppSidebar.vue layouts/AppSidebar.vue`
- [ ] `git mv components/AppLogo.vue layouts/AppLogo.vue`
- [ ] `git mv components/NotificationBell.vue layouts/NotificationBell.vue`
- [ ] `git mv components/SystemDate.vue layouts/SystemDate.vue`
- [ ] `git mv components/UserAvatar.vue layouts/UserAvatar.vue`
- [ ] `git mv components/UserMenu.vue layouts/UserMenu.vue`
- [ ] Update `@/components/App*` + root component imports → `@/layouts/*` (in `App.vue`, `AppHeader.vue`)
- [ ] `make health` → green. Browser smoke.

---

## Phase 4 — Domain-specific `components/` → `modules/finance/components/`

- [ ] `git mv components/authorization/ modules/finance/components/authorization/`
- [ ] `git mv components/finance/ modules/finance/components/finance/`
- [ ] `git mv components/modals/ modules/finance/components/modals/`
- [ ] `git mv components/parameter/ modules/finance/components/parameter/`
- [ ] `git mv components/widgets/ modules/finance/components/widgets/`
- [ ] Update all imports from `@/components/authorization/`, `@/components/finance/`, `@/components/modals/`, `@/components/parameter/`, `@/components/widgets/`
- [ ] `make health` → green. Browser smoke.

---

## Phase 5 — `stores/` → `app/stores/` (+ rename `*.store.ts`)

- [ ] `git mv stores/auth.ts app/stores/auth.store.ts`
- [ ] `git mv stores/sidebar.ts app/stores/sidebar.store.ts`
- [ ] `git mv stores/notifications.ts app/stores/notification.store.ts`
- [ ] `git mv stores/theme.ts app/stores/theme.store.ts`
- [ ] Update all `@/stores/auth` → `@/app/stores/auth.store` imports
- [ ] Update all `@/stores/sidebar` → `@/app/stores/sidebar.store` imports
- [ ] Update all `@/stores/notifications` → `@/app/stores/notification.store` imports
- [ ] Update all `@/stores/theme` → `@/app/stores/theme.store` imports
- [ ] Delete empty `stores/`
- [ ] `make health` → green. Browser smoke.

---

## Phase 6 — `pages/` → `modules/*/views/` (+ `Page` → `View` rename)

Largest phase. Do with `git mv` in batches per sub-folder.

### 6a — Auth + profile
- [ ] `git mv pages/LoginPage.vue app/views/LoginView.vue`
- [ ] `git mv pages/NoTenantPage.vue app/views/NoTenantView.vue`
- [ ] `git mv pages/profile/PasswordPage.vue app/views/profile/PasswordView.vue`
- [ ] `git mv pages/DonorDetailPage.vue modules/fundraising/views/DonorDetailView.vue`

### 6b — Dashboard
- [ ] `git mv pages/dashboard/DashboardPage.vue modules/finance/views/dashboard/DashboardView.vue`
- [ ] `git mv pages/dashboard/DashboardFinancePage.vue modules/finance/views/dashboard/DashboardFinanceView.vue`
- [ ] `git mv pages/dashboard/DashboardDistributionPage.vue modules/finance/views/dashboard/DashboardDistributionView.vue`
- [ ] `git mv pages/dashboard/DashboardCollectionPage.vue modules/finance/views/dashboard/DashboardCollectionView.vue`

### 6c — Finance master
- [ ] Move `pages/finance/coa/` → `modules/finance/views/master/coa/` (2 files)
- [ ] Move `pages/finance/cash/` → `modules/finance/views/master/cash/` (2 files)
- [ ] Move `pages/finance/bank/` → `modules/finance/views/master/bank/` (2 files)
- [ ] Move `pages/finance/petty-cash/` → `modules/finance/views/master/petty-cash/` (2 files)
- [ ] `git mv pages/parameter/BudgetOwnerPage.vue modules/finance/views/master/budget-owner/BudgetOwnerView.vue`

### 6d — Finance budget
- [ ] Move `pages/finance/budget-import/` → `modules/finance/views/budget/import/` (1 file, rename)
- [ ] Move `pages/finance/budget-revise/` → `modules/finance/views/budget/revise/` (2 files)
- [ ] `git mv pages/parameter/BudgetItemPage.vue modules/finance/views/budget/item/BudgetItemView.vue`
- [ ] `git mv pages/parameter/BudgetPeriodPage.vue modules/finance/views/budget/period/BudgetPeriodView.vue`

### 6e — Finance inquiry
- [ ] Move `pages/finance/budget-inquiry/` → `modules/finance/views/inquiry/budget/` (3 files, rename)
- [ ] Move `pages/finance/transaction-history/` → `modules/finance/views/inquiry/transaction-history/` (2 files)

### 6f — Finance transaction
- [ ] Move `pages/finance/fund-collection/` → `modules/finance/views/transaction/fund-collection/` (2 files)
- [ ] Move `pages/finance/fund-distribution/` → `modules/finance/views/transaction/fund-distribution/` (2 files)
- [ ] Move `pages/finance/cash-advance/` → `modules/finance/views/transaction/cash-advance/` (2 files)
- [ ] Move `pages/finance/cash-advance-lpj/` → `modules/finance/views/transaction/cash-advance-lpj/` (2 files)
- [ ] Move `pages/finance/fund-transfer/` → `modules/finance/views/transaction/fund-transfer/` (2 files)
- [ ] Move `pages/finance/general-transaction/` → `modules/finance/views/transaction/general/` (2 files)
- [ ] Move `pages/finance/amil-income/` → `modules/finance/views/transaction/amil-income/` (2 files)
- [ ] Move `pages/finance/amil-expense/` → `modules/finance/views/transaction/amil-expense/` (2 files)
- [ ] Move `pages/finance/receivable/` → `modules/finance/views/transaction/receivable/` (2 files)

### 6g — Finance upload
- [ ] Move `pages/finance/upload-collection-multi/` → `modules/finance/views/upload/collection/` (3 files, rename Multi→ drop)
- [ ] Move `pages/finance/upload-collection-hc/` → `modules/finance/views/upload/zis-routine/` (2 files, rename HCZis→ZisRoutine)

### 6h — Finance reports
- [ ] Move all `pages/finance/reports/Report*Page.vue` → `modules/finance/views/reports/Report*View.vue` (19 files)

### 6i — Finance monitoring
- [ ] `git mv pages/finance/AuthorizationPage.vue modules/finance/views/monitoring/AuthorizationView.vue`
- [ ] `git mv pages/finance/SubmissionHistoryPage.vue modules/finance/views/monitoring/SubmissionHistoryView.vue`

### 6j — Administration
- [ ] `git mv pages/admin/UsersPage.vue modules/administration/views/users/UsersView.vue`
- [ ] `git mv pages/admin/RoleMenuPage.vue modules/administration/views/role-menu/RoleMenuView.vue`

### 6k — Update all router `component: () => import(...)` paths
- [ ] Update every import path in `router/index.ts` to match new view locations
- [ ] Update URL paths for 5 changed routes (specs §6)
- [ ] Delete empty `pages/`, `parameter/` directories
- [ ] `make health` → green. Full browser smoke: login, dashboard, 3 transaction pages, 1 report, otorisasi.

---

## Phase 7 — Per-module `routes.ts` split

- [ ] Create `modules/finance/routes.ts` — extract all finance + dashboard routes from router/index.ts
- [ ] Create `modules/administration/routes.ts` — extract admin routes
- [ ] Create stub `modules/fundraising/routes.ts`, `modules/distribution/routes.ts`, `modules/enterprise/routes.ts`
- [ ] Rewrite `app/router/index.ts` (or current `router/index.ts`) to import + spread module routes
- [ ] Move `router/guards.ts` — extract `beforeEach` logic to separate file
- [ ] `make health` → green. Full smoke test. Check route guards (login redirect, menu_key guard).

---

## Phase 8 — Navigation: `AppDomainRail.vue` + `AppSidebar.vue` rewrite

- [ ] Create `lib/nav/index.ts` → `shared/constants/domains.ts` with `DomainConfig` type + `DOMAIN_MAP`
- [ ] Create `modules/finance/menu.ts` — full DomainConfig for Finance (all 8 groups)
- [ ] Create `modules/administration/menu.ts` — DomainConfig for Administration
- [ ] Create `layouts/AppDomainRail.vue`:
  - Reads `route.meta.domain` for active state
  - On click unlocked domain: `router.push(domain.defaultRoute)` + expand sidebar if collapsed
  - Tooltip on hover per domain button
  - Locked domains (fundraising, distribution, enterprise): greyed, tooltip shows phase
- [ ] Rewrite `layouts/AppSidebar.vue`:
  - Remove hardcoded `groups` array
  - Read `DOMAIN_MAP[route.meta.domain]` for current domain config
  - Add domain header section (label + sub)
  - Add search input (client-side filter, shows group label in result)
  - Keep existing expand/collapse + localStorage persist behavior
  - Keep `visibleChildren()` RBAC filter logic
- [ ] Update `App.vue` layout grid: add rail column (`56px`) left of sidebar
- [ ] Add `meta.domain` to all routes in module routes files
- [ ] `make health` → green. Full smoke: domain switch Keuangan↔Administrasi, search "piutang", collapse sidebar, domain rail tooltips.

---

## Phase 9 — `main.ts` + `App.vue` → `app/`

- [ ] `git mv src/main.ts src/app/main.ts`
- [ ] `git mv src/App.vue src/app/App.vue`
- [ ] `git mv src/router/ src/app/router/` (if not already done in phase 7)
- [ ] Update `vite.config.ts`: set `input` (or `entry`) to `src/app/main.ts`
- [ ] Update any remaining `src/main.ts` references
- [ ] `make health` → green. Full smoke.

---

## Phase 10 — Wakaf portal mirror

- [ ] Apply phases 0–9 to `apps_wakaf/web-vue/src/` (fewer files, same structure)
- [ ] Wakaf-specific page renames (see specs §12)
- [ ] `make health` (wakaf) → green. Browser smoke `:5174`.

---

## Post-refactor

- [ ] Update `CLAUDE.md` folder structure section to reflect new paths
- [ ] Update `nuwis-ui-builder` skill path references
- [ ] Grep for any remaining `@/lib/`, `@/pages/`, `@/stores/[^a]`, `@/components/ui/`, `Page.vue` → confirm zero stale refs
- [ ] Single commit per phase, tag `[MODULAR-REFACTOR]`
