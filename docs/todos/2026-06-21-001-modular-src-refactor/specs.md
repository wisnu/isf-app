# Specs — Modular `src/` Refactor + Domain Navigation

**Slug:** `2026-06-21-001-modular-src-refactor`
**Type:** Structural Refactor (frontend only, zero logic change)
**Portal:** Zakat first (`apps_zakat/web-vue/`), mirror to Wakaf after
**Companion:** [`plan.md`](./plan.md)

---

## 1. Problem Statement

The current `web-vue/src/` is a flat, feature-mixed structure:

- All pages live in `pages/` regardless of domain — budget pages alongside amil-income pages alongside reports
- `pages/parameter/` is orphaned — logically belongs to Finance but has no domain home
- `pages/admin/` has no relationship to its domain name (`/admin` URL)
- `lib/` mixes utilities, composables, API client, and menu config with no sub-categorization
- `components/` mixes layout chrome, shared UI primitives, and domain-specific finance components
- `router/index.ts` is 550+ lines with all routes in one file — adding a new domain requires editing this one file
- The sidebar is a single monolithic component with hardcoded menu data — no separation between Finance and Admin menus
- Navigation has no domain-level grouping; when Program/Penghimpunan/Enterprise domains arrive (Fase 3/4), the sidebar will become unmanageable

---

## 2. Goals

1. Align `src/` with the Enterprise Web Architecture doc (sections 6 & 7)
2. Each business domain is self-contained: its own routes, menu config, views, components, types
3. Shared code is explicitly separated from domain code
4. Navigation adds a **domain rail** (leftmost icon column) + **per-domain sidebar panel** + **menu search**
5. Pure structural change: zero logic change to any `.vue` file internals, zero backend impact

---

## 3. Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Page file suffix | `*View.vue` (was `*Page.vue`) | Matches architecture doc + Vue ecosystem convention |
| Pages folder | `modules/*/views/` (was `pages/`) | Domain-scoped; mirrors backend module structure |
| Utilities folder | `shared/` (was `lib/`) | Signals "cross-domain", matches architecture doc |
| UI primitives | `shared/components/` (was `components/ui/` + `components/layout/`) | Same reasoning |
| Layout chrome | `layouts/` (was `components/App*.vue`) | Separates navigation shell from domain components |
| Router | Per-module `routes.ts` imported by `app/router/index.ts` | One file per domain; easy to add Fase 3/4 domains |
| Domain nav | `AppDomainRail.vue` (new) + rewritten `AppSidebar.vue` | Enables module-grouped navigation |
| Domain state | Derived from `route.meta.domain` — no extra store | Always in sync with URL; survives hard refresh |
| Domain switch | Auto-expand sidebar + navigate to `domain.defaultRoute` | User confirmed: A (sidebar + content sync) |
| Transaction views folder | `transaction/` (singular) | Separates write workflow from inquiry and reports |
| Inquiry views folder | `inquiry/` (separate from `reports/`) | Reports = aggregate exports; Inquiry = drill-down lookup |

---

## 4. New `src/` Structure

```
src/
  app/
    main.ts
    App.vue
    router/
      index.ts          ← imports module routes + mounts guards
      guards.ts         ← extracted beforeEach logic
    stores/
      auth.store.ts
      sidebar.store.ts
      notification.store.ts
      theme.store.ts
    views/
      LoginView.vue
      NoTenantView.vue
      profile/
        PasswordView.vue

  layouts/
    AppHeader.vue
    AppDomainRail.vue   ← NEW
    AppSidebar.vue      ← REWRITE
    AppLogo.vue
    UserAvatar.vue
    UserMenu.vue
    SystemDate.vue
    NotificationBell.vue

  shared/
    api/
      client.ts
    components/         ← all shared UI primitives
      Alert.vue           AmountInput.vue     AppDataTable.vue
      AppTable.vue        Button.vue          Card.vue
      CardContent.vue     CardDescription.vue CardHeader.vue
      CardTitle.vue       DateField.vue       DropdownMenu.vue
      DropdownMenuItem.vue Input.vue          Label.vue
      Modal.vue           PeriodFilter.vue    SearchSelect.vue
      TablePagination.vue Toast.vue           Tooltip.vue
      CrudLayout.vue      DataPanel.vue       FilterGroup.vue
      FilterPanel.vue     PageHeader.vue
    composables/
      useFetch.ts
      useToast.ts
    utils/
      date.ts
      format.ts
      download.ts
      utils.ts
      charts.ts
      portal.ts
    constants/
      menu-keys.ts      ← was lib/menu/registry.ts; exports MENU_KEYS unchanged

  modules/
    finance/
      routes.ts
      menu.ts
      components/
        authorization/
          StatusBadge.vue
          SubmissionDetailDrawer.vue
        finance/
          TransactionDeleteDialog.vue
        modals/
          CashAdvanceFormModal.vue
          CashAdvanceLPJFormModal.vue
        parameter/
          BudgetOwnerDeleteModal.vue
          BudgetOwnerFormModal.vue
        widgets/
          AsnafDonutWidget.vue      BudgetProgressWidget.vue
          FundraisingProgressWidget.vue KpiCardWidget.vue
          MemoListWidget.vue        RecentActivityWidget.vue
          RekeningListWidget.vue    TrendChartWidget.vue
      types/
      views/
        dashboard/
          DashboardView.vue
          DashboardFinanceView.vue
          DashboardDistributionView.vue
          DashboardCollectionView.vue
        master/
          coa/
            CoaListView.vue
            CoaCreateView.vue
          cash/
            CashListView.vue
            CashCreateView.vue
          bank/
            BankListView.vue
            BankCreateView.vue
          petty-cash/
            PettyCashListView.vue
            PettyCashCreateView.vue
          budget-owner/
            BudgetOwnerView.vue
        budget/
          import/
            BudgetImportView.vue
          revise/
            BudgetReviseListView.vue
            BudgetReviseCreateView.vue
          item/
            BudgetItemView.vue
          period/
            BudgetPeriodView.vue
        transaction/
          fund-collection/
            FundCollectionListView.vue
            FundCollectionCreateView.vue
          fund-distribution/
            FundDistributionListView.vue
            FundDistributionCreateView.vue
          cash-advance/
            CashAdvanceListView.vue
            CashAdvanceCreateView.vue
          cash-advance-lpj/
            CashAdvanceLPJListView.vue
            CashAdvanceLPJCreateView.vue
          fund-transfer/
            FundTransferListView.vue
            FundTransferCreateView.vue
          general/
            GeneralTransactionListView.vue
            GeneralTransactionCreateView.vue
          amil-income/
            AmilIncomeListView.vue
            AmilIncomeCreateView.vue
          amil-expense/
            AmilExpenseListView.vue
            AmilExpenseCreateView.vue
          receivable/
            ReceivableListView.vue
            ReceivableCreateView.vue
        inquiry/
          transaction-history/
            TransactionHistoryListView.vue
            TransactionHistoryDetailView.vue
          budget/
            BudgetInquiryView.vue
            BudgetInquiryOwnerView.vue
            BudgetInquiryTransaksiView.vue
          cash-advance/
            (placeholder — cash advance inquiry by employee/person)
        upload/
          collection/
            UploadCollectionView.vue
            UploadCollectionListView.vue
            UploadCollectionDetailView.vue
          zis-routine/
            UploadZisRoutineView.vue
            UploadZisRoutineListView.vue
        reports/
          ReportDailyJournalView.vue
          ReportGeneralTransactionView.vue
          ReportCashDailyView.vue
          ReportCashSummaryView.vue
          ReportCashMonthlyView.vue
          ReportTrialBalanceView.vue
          ReportBalanceSheetView.vue
          ReportCashFlowView.vue
          ReportGeneralLedgerView.vue
          ReportFundChangeView.vue
          ReportFundChangeDetailView.vue
          ReportAmilView.vue
          ReportARSummaryView.vue
          ReportFundCollectionView.vue
          ReportFundDistributionView.vue
          ReportCashAdvanceListView.vue
          ReportMemoRealizationView.vue
          ReportReceivableRealizationView.vue
          ReportUpzView.vue
        monitoring/
          AuthorizationView.vue
          SubmissionHistoryView.vue

    administration/
      routes.ts
      menu.ts
      views/
        users/
          UsersView.vue
        role-menu/
          RoleMenuView.vue

    fundraising/            ← Fase 3
      routes.ts             ← stub
      views/
        DonorDetailView.vue

    distribution/           ← Fase 3 stub
      routes.ts

    enterprise/             ← Fase 4 stub
      routes.ts
```

---

## 5. Complete File Move Table — Zakat Portal

### `lib/` → `shared/`

| From | To |
|---|---|
| `lib/api/client.ts` | `shared/api/client.ts` |
| `lib/date.ts` | `shared/utils/date.ts` |
| `lib/format.ts` | `shared/utils/format.ts` |
| `lib/charts.ts` | `shared/utils/charts.ts` |
| `lib/utils.ts` | `shared/utils/utils.ts` |
| `lib/download.ts` | `shared/utils/download.ts` |
| `lib/portal.ts` | `shared/utils/portal.ts` |
| `lib/useFetch.ts` | `shared/composables/useFetch.ts` |
| `lib/useToast.ts` | `shared/composables/useToast.ts` |
| `lib/menu/registry.ts` | `shared/constants/menu-keys.ts` |

### `components/ui/` + `components/layout/` → `shared/components/`

All 25 files are pure renames (directory change only).

### `components/App*.vue` + layout root → `layouts/`

| From | To |
|---|---|
| `components/AppHeader.vue` | `layouts/AppHeader.vue` |
| `components/AppSidebar.vue` | `layouts/AppSidebar.vue` (REWRITE) |
| `components/AppLogo.vue` | `layouts/AppLogo.vue` |
| `components/NotificationBell.vue` | `layouts/NotificationBell.vue` |
| `components/SystemDate.vue` | `layouts/SystemDate.vue` |
| `components/UserAvatar.vue` | `layouts/UserAvatar.vue` |
| `components/UserMenu.vue` | `layouts/UserMenu.vue` |
| *(new)* | `layouts/AppDomainRail.vue` |

### `components/` domain-specific → `modules/finance/components/`

| From | To |
|---|---|
| `components/authorization/StatusBadge.vue` | `modules/finance/components/authorization/StatusBadge.vue` |
| `components/authorization/SubmissionDetailDrawer.vue` | `modules/finance/components/authorization/SubmissionDetailDrawer.vue` |
| `components/finance/TransactionDeleteDialog.vue` | `modules/finance/components/finance/TransactionDeleteDialog.vue` |
| `components/modals/CashAdvanceFormModal.vue` | `modules/finance/components/modals/CashAdvanceFormModal.vue` |
| `components/modals/CashAdvanceLPJFormModal.vue` | `modules/finance/components/modals/CashAdvanceLPJFormModal.vue` |
| `components/parameter/BudgetOwnerDeleteModal.vue` | `modules/finance/components/parameter/BudgetOwnerDeleteModal.vue` |
| `components/parameter/BudgetOwnerFormModal.vue` | `modules/finance/components/parameter/BudgetOwnerFormModal.vue` |
| `components/widgets/*.vue` (8 files) | `modules/finance/components/widgets/*.vue` |

### `stores/` → `app/stores/` (+ rename)

| From | To |
|---|---|
| `stores/auth.ts` | `app/stores/auth.store.ts` |
| `stores/sidebar.ts` | `app/stores/sidebar.store.ts` |
| `stores/notifications.ts` | `app/stores/notification.store.ts` |
| `stores/theme.ts` | `app/stores/theme.store.ts` |

### `pages/` → `modules/*/views/` (+ suffix `Page` → `View`)

| From | To |
|---|---|
| `pages/LoginPage.vue` | `app/views/LoginView.vue` |
| `pages/NoTenantPage.vue` | `app/views/NoTenantView.vue` |
| `pages/DonorDetailPage.vue` | `modules/fundraising/views/DonorDetailView.vue` |
| `pages/profile/PasswordPage.vue` | `app/views/profile/PasswordView.vue` |
| `pages/dashboard/DashboardPage.vue` | `modules/finance/views/dashboard/DashboardView.vue` |
| `pages/dashboard/DashboardFinancePage.vue` | `modules/finance/views/dashboard/DashboardFinanceView.vue` |
| `pages/dashboard/DashboardDistributionPage.vue` | `modules/finance/views/dashboard/DashboardDistributionView.vue` |
| `pages/dashboard/DashboardCollectionPage.vue` | `modules/finance/views/dashboard/DashboardCollectionView.vue` |
| `pages/finance/coa/CoaListPage.vue` | `modules/finance/views/master/coa/CoaListView.vue` |
| `pages/finance/coa/CoaCreatePage.vue` | `modules/finance/views/master/coa/CoaCreateView.vue` |
| `pages/finance/cash/CashListPage.vue` | `modules/finance/views/master/cash/CashListView.vue` |
| `pages/finance/cash/CashCreatePage.vue` | `modules/finance/views/master/cash/CashCreateView.vue` |
| `pages/finance/bank/BankListPage.vue` | `modules/finance/views/master/bank/BankListView.vue` |
| `pages/finance/bank/BankCreatePage.vue` | `modules/finance/views/master/bank/BankCreateView.vue` |
| `pages/finance/petty-cash/PettyCashListPage.vue` | `modules/finance/views/master/petty-cash/PettyCashListView.vue` |
| `pages/finance/petty-cash/PettyCashCreatePage.vue` | `modules/finance/views/master/petty-cash/PettyCashCreateView.vue` |
| `pages/parameter/BudgetOwnerPage.vue` | `modules/finance/views/master/budget-owner/BudgetOwnerView.vue` |
| `pages/finance/budget-import/BudgetImportCreatePage.vue` | `modules/finance/views/budget/import/BudgetImportView.vue` |
| `pages/finance/budget-revise/BudgetReviseListPage.vue` | `modules/finance/views/budget/revise/BudgetReviseListView.vue` |
| `pages/finance/budget-revise/BudgetReviseCreatePage.vue` | `modules/finance/views/budget/revise/BudgetReviseCreateView.vue` |
| `pages/finance/budget-inquiry/BudgetInquiryPage.vue` | `modules/finance/views/inquiry/budget/BudgetInquiryView.vue` |
| `pages/finance/budget-inquiry/BudgetInquiryOwnerPage.vue` | `modules/finance/views/inquiry/budget/BudgetInquiryOwnerView.vue` |
| `pages/finance/budget-inquiry/BudgetInquiryTransaksiPage.vue` | `modules/finance/views/inquiry/budget/BudgetInquiryTransaksiView.vue` |
| `pages/parameter/BudgetItemPage.vue` | `modules/finance/views/budget/item/BudgetItemView.vue` |
| `pages/parameter/BudgetPeriodPage.vue` | `modules/finance/views/budget/period/BudgetPeriodView.vue` |
| `pages/finance/transaction-history/TransactionHistoryListPage.vue` | `modules/finance/views/inquiry/transaction-history/TransactionHistoryListView.vue` |
| `pages/finance/transaction-history/TransactionHistoryDetailPage.vue` | `modules/finance/views/inquiry/transaction-history/TransactionHistoryDetailView.vue` |
| `pages/finance/fund-collection/FundCollectionListPage.vue` | `modules/finance/views/transaction/fund-collection/FundCollectionListView.vue` |
| `pages/finance/fund-collection/FundCollectionCreatePage.vue` | `modules/finance/views/transaction/fund-collection/FundCollectionCreateView.vue` |
| `pages/finance/fund-distribution/FundDistributionListPage.vue` | `modules/finance/views/transaction/fund-distribution/FundDistributionListView.vue` |
| `pages/finance/fund-distribution/FundDistributionCreatePage.vue` | `modules/finance/views/transaction/fund-distribution/FundDistributionCreateView.vue` |
| `pages/finance/cash-advance/CashAdvanceListPage.vue` | `modules/finance/views/transaction/cash-advance/CashAdvanceListView.vue` |
| `pages/finance/cash-advance/CashAdvanceCreatePage.vue` | `modules/finance/views/transaction/cash-advance/CashAdvanceCreateView.vue` |
| `pages/finance/cash-advance-lpj/CashAdvanceLPJListPage.vue` | `modules/finance/views/transaction/cash-advance-lpj/CashAdvanceLPJListView.vue` |
| `pages/finance/cash-advance-lpj/CashAdvanceLPJCreatePage.vue` | `modules/finance/views/transaction/cash-advance-lpj/CashAdvanceLPJCreateView.vue` |
| `pages/finance/fund-transfer/FundTransferListPage.vue` | `modules/finance/views/transaction/fund-transfer/FundTransferListView.vue` |
| `pages/finance/fund-transfer/FundTransferCreatePage.vue` | `modules/finance/views/transaction/fund-transfer/FundTransferCreateView.vue` |
| `pages/finance/general-transaction/GeneralTransactionListPage.vue` | `modules/finance/views/transaction/general/GeneralTransactionListView.vue` |
| `pages/finance/general-transaction/GeneralTransactionCreatePage.vue` | `modules/finance/views/transaction/general/GeneralTransactionCreateView.vue` |
| `pages/finance/amil-income/AmilIncomeListPage.vue` | `modules/finance/views/transaction/amil-income/AmilIncomeListView.vue` |
| `pages/finance/amil-income/AmilIncomeCreatePage.vue` | `modules/finance/views/transaction/amil-income/AmilIncomeCreateView.vue` |
| `pages/finance/amil-expense/AmilExpenseListPage.vue` | `modules/finance/views/transaction/amil-expense/AmilExpenseListView.vue` |
| `pages/finance/amil-expense/AmilExpenseCreatePage.vue` | `modules/finance/views/transaction/amil-expense/AmilExpenseCreateView.vue` |
| `pages/finance/receivable/ReceivableListPage.vue` | `modules/finance/views/transaction/receivable/ReceivableListView.vue` |
| `pages/finance/receivable/ReceivableCreatePage.vue` | `modules/finance/views/transaction/receivable/ReceivableCreateView.vue` |
| `pages/finance/upload-collection-multi/UploadCollectionMultiPage.vue` | `modules/finance/views/upload/collection/UploadCollectionView.vue` |
| `pages/finance/upload-collection-multi/UploadCollectionMultiListPage.vue` | `modules/finance/views/upload/collection/UploadCollectionListView.vue` |
| `pages/finance/upload-collection-multi/UploadCollectionMultiDetailPage.vue` | `modules/finance/views/upload/collection/UploadCollectionDetailView.vue` |
| `pages/finance/upload-collection-hc/UploadCollectionHCZisPage.vue` | `modules/finance/views/upload/zis-routine/UploadZisRoutineView.vue` |
| `pages/finance/upload-collection-hc/UploadCollectionHCZisListPage.vue` | `modules/finance/views/upload/zis-routine/UploadZisRoutineListView.vue` |
| `pages/finance/reports/ReportDailyJournalPage.vue` | `modules/finance/views/reports/ReportDailyJournalView.vue` |
| `pages/finance/reports/ReportGeneralTransactionPage.vue` | `modules/finance/views/reports/ReportGeneralTransactionView.vue` |
| `pages/finance/reports/ReportCashDailyPage.vue` | `modules/finance/views/reports/ReportCashDailyView.vue` |
| `pages/finance/reports/ReportCashSummaryPage.vue` | `modules/finance/views/reports/ReportCashSummaryView.vue` |
| `pages/finance/reports/ReportCashMonthlyPage.vue` | `modules/finance/views/reports/ReportCashMonthlyView.vue` |
| `pages/finance/reports/ReportTrialBalancePage.vue` | `modules/finance/views/reports/ReportTrialBalanceView.vue` |
| `pages/finance/reports/ReportBalanceSheetPage.vue` | `modules/finance/views/reports/ReportBalanceSheetView.vue` |
| `pages/finance/reports/ReportCashFlowPage.vue` | `modules/finance/views/reports/ReportCashFlowView.vue` |
| `pages/finance/reports/ReportGeneralLedgerPage.vue` | `modules/finance/views/reports/ReportGeneralLedgerView.vue` |
| `pages/finance/reports/ReportFundChangePage.vue` | `modules/finance/views/reports/ReportFundChangeView.vue` |
| `pages/finance/reports/ReportFundChangeDetailPage.vue` | `modules/finance/views/reports/ReportFundChangeDetailView.vue` |
| `pages/finance/reports/ReportAmilPage.vue` | `modules/finance/views/reports/ReportAmilView.vue` |
| `pages/finance/reports/ReportARSummaryPage.vue` | `modules/finance/views/reports/ReportARSummaryView.vue` |
| `pages/finance/reports/ReportFundCollectionPage.vue` | `modules/finance/views/reports/ReportFundCollectionView.vue` |
| `pages/finance/reports/ReportFundDistributionPage.vue` | `modules/finance/views/reports/ReportFundDistributionView.vue` |
| `pages/finance/reports/ReportCashAdvanceListPage.vue` | `modules/finance/views/reports/ReportCashAdvanceListView.vue` |
| `pages/finance/reports/ReportMemoRealizationPage.vue` | `modules/finance/views/reports/ReportMemoRealizationView.vue` |
| `pages/finance/reports/ReportReceivableRealizationPage.vue` | `modules/finance/views/reports/ReportReceivableRealizationView.vue` |
| `pages/finance/reports/ReportUpzPage.vue` | `modules/finance/views/reports/ReportUpzView.vue` |
| `pages/finance/AuthorizationPage.vue` | `modules/finance/views/monitoring/AuthorizationView.vue` |
| `pages/finance/SubmissionHistoryPage.vue` | `modules/finance/views/monitoring/SubmissionHistoryView.vue` |
| `pages/admin/UsersPage.vue` | `modules/administration/views/users/UsersView.vue` |
| `pages/admin/RoleMenuPage.vue` | `modules/administration/views/role-menu/RoleMenuView.vue` |

### Root files → `app/`

| From | To |
|---|---|
| `src/main.ts` | `src/app/main.ts` |
| `src/App.vue` | `src/app/App.vue` |
| `src/router/index.ts` | `src/app/router/index.ts` (trimmed) + `guards.ts` |

`vite.config.ts` entry updated: `entry: 'src/app/main.ts'`

---

## 6. URL Path Changes

| Old URL | New URL | Reason |
|---|---|---|
| `/parameter/budget-owner` | `/finance/master/budget-owner` | Belongs to Finance domain |
| `/parameter/anggaran/item` | `/finance/budget/item` | Belongs to Finance domain |
| `/parameter/anggaran/periode` | `/finance/budget/period` | Belongs to Finance domain |
| `/admin/users` | `/administration/users` | Matches domain name |
| `/admin/role-menu` | `/administration/role-menu` | Matches domain name |

All other `/finance/...`, `/dashboard/...`, `/profile/...` URLs unchanged.

---

## 7. Import Alias Changes

`tsconfig.json` + `vite.config.ts` — `@/` stays pointing to `src/`. No alias rename needed.

All files with `@/lib/` imports become `@/shared/` (grep-and-replace):
```
@/lib/api/client       → @/shared/api/client
@/lib/date             → @/shared/utils/date
@/lib/format           → @/shared/utils/format
@/lib/utils            → @/shared/utils/utils
@/lib/download         → @/shared/utils/download
@/lib/portal           → @/shared/utils/portal
@/lib/charts           → @/shared/utils/charts
@/lib/useFetch         → @/shared/composables/useFetch
@/lib/useToast         → @/shared/composables/useToast
@/lib/menu/registry    → @/shared/constants/menu-keys
```

`@/components/ui/` → `@/shared/components/`
`@/components/layout/` → `@/shared/components/`
`@/components/App*` → `@/layouts/App*`
`@/components/authorization/` → `@/modules/finance/components/authorization/`
`@/components/finance/` → `@/modules/finance/components/finance/`
`@/components/modals/` → `@/modules/finance/components/modals/`
`@/components/parameter/` → `@/modules/finance/components/parameter/`
`@/components/widgets/` → `@/modules/finance/components/widgets/`
`@/stores/auth` → `@/app/stores/auth.store`
`@/stores/sidebar` → `@/app/stores/sidebar.store`
`@/stores/notifications` → `@/app/stores/notification.store`
`@/stores/theme` → `@/app/stores/theme.store`

---

## 8. New Navigation Components

### `layouts/AppDomainRail.vue`

```
Props: none
Reads: route.meta.domain (computed active domain)
Emits: none

Behavior:
- Renders domain buttons for: finance, administration, fundraising, distribution, enterprise
- Active = route.meta.domain matches domain id
- Click unlocked domain:
    if sidebar collapsed → open sidebar
    router.push(domain.defaultRoute)
- Click locked domain: no-op (tooltip shows phase label)
- Tooltip on hover (right-aligned, shows domain label)
Width: 56px fixed, always visible
```

### `layouts/AppSidebar.vue` (rewrite)

```
Reads: route.meta.domain → DOMAIN_MAP[domain] → DomainConfig
New sections vs current:
  - Domain header (label + sub)    [NEW]
  - Search input                   [NEW]
  - Menu groups (expand/collapse)  [existing behavior, refactored]
  - Sidebar footer (version)       [existing]

Removed from current:
  - Hardcoded groups array
  - MZISS / Modul Akuntansi header (moved to header-brand in AppHeader)

Search behavior: client-side filter on current domain's menu items;
  shows group label as right-aligned secondary text per result
```

### `modules/finance/menu.ts` (new)

```ts
// DomainConfig for Finance/Keuangan
// Contains: id, label, sub, icon, locked, defaultRoute, groups[]
// groups follow: dashboard / master / budget / transaction / inquiry / upload / reports / monitoring
// Each item carries: label, to (URL path), menu_key (MenuKey from shared/constants/menu-keys.ts)
```

### `modules/administration/menu.ts` (new)

```ts
// DomainConfig for Administration
// groups: user-management (List User, Role & Menu)
// defaultRoute: 'administration-users'
```

### `lib/nav/index.ts` → `shared/constants/domains.ts`

```ts
// DOMAIN_MAP: Record<DomainId, DomainConfig>
// Used by AppDomainRail + AppSidebar to look up config by route.meta.domain
```

---

## 9. Route `meta.domain` Additions

All routes gain `meta.domain: DomainId`:

| Route prefix | domain |
|---|---|
| `/`, `/dashboard/*` | `'finance'` |
| `/finance/*`, `/parameter/*` | `'finance'` |
| `/administration/*` | `'administration'` |
| `/profile/*`, `/login`, `/no-tenant` | `undefined` (no domain highlight) |

---

## 10. Per-Module `routes.ts` Structure

```ts
// modules/finance/routes.ts
import type { RouteRecordRaw } from 'vue-router'
export const financeRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('./views/dashboard/DashboardView.vue'),
    meta: { title: 'Dashboard', menu_key: 'dashboard.overview', domain: 'finance' },
  },
  // ... all ~50 finance + dashboard routes
]
```

```ts
// app/router/index.ts
import { financeRoutes } from '@/modules/finance/routes'
import { administrationRoutes } from '@/modules/administration/routes'

const router = createRouter({
  routes: [
    ...financeRoutes,
    ...administrationRoutes,
    { path: '/login', ... },
    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})
```

---

## 11. What Does NOT Change

- All `.vue` file internals — zero logic, template, or style changes
- Named route names (e.g. `'finance-coa'`, `'finance-transactions-fund-collection'`)
- All BFF routes and API endpoints
- `shared/constants/menu-keys.ts` exports identical `MENU_KEYS` object (only path changes)
- Auth store shape (`user`, `roles`, `menus[]`, `branches`, `active_tenant_id`)
- `hasMenu()` logic, route guards behavior
- Existing `infra/db/migrations/` — no DB impact

---

## 12. Wakaf Portal

Apply the same restructure to `apps_wakaf/web-vue/src/`. Wakaf has fewer files (~19 pages) but the target structure is identical. Do Wakaf in a separate commit after Zakat is verified green.

Current Wakaf-specific pages:
- `pages/finance/BankPage.vue` → `modules/finance/views/master/bank/BankView.vue`
- `pages/finance/CoaPage.vue` → `modules/finance/views/master/coa/CoaView.vue`
- `pages/finance/KasPage.vue` → `modules/finance/views/master/cash/CashView.vue`
- `pages/finance/reports/Report*Page.vue` → `modules/finance/views/reports/Report*View.vue`
- Dashboard pages at root → `modules/finance/views/dashboard/`
