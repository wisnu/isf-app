# Vue.js Frontend Structure and Process Flow for Backend Engineers

## 1. Purpose

This document explains the proposed Vue.js frontend structure from the perspective of a Backend Engineer.

The goal is to make the frontend structure easy to understand for backend teams, especially in relation to:

- API flow
- BFF integration
- Menu and permission flow
- Lookup and pagination flow
- Transaction input flow
- Approval flow
- Report flow
- Dashboard lazy loading
- Frontend module structure
- Backend contract expectations

The frontend application is designed to work with:

```text
Vue.js Web App
  |
  v
FastAPI BFF
  |
  |-- service-transaction
  |     |-- read
  |     |-- write
  |
  |-- service-report
        |-- read-only reports
```

---

# 2. High-Level Vue Structure

Recommended frontend structure:

```text
apps/web/
└── src/
    ├── app/
    ├── layouts/
    ├── shared/
    └── modules/
        ├── finance/
        ├── distribution/
        ├── fundraising/
        ├── administration/
        └── enterprise/
```

Conceptually:

```text
app/
  global application setup

layouts/
  page shell and application layout

shared/
  reusable components, composables, utilities, and types

modules/
  business domain features
```

From a backend perspective:

```text
app/
  similar to main.py, root router, global dependencies

layouts/
  similar to a common response shell, but for UI

shared/
  similar to shared/common package

modules/
  similar to backend domain modules
```

---

# 3. Main Application Flow

When a user opens the web application:

```text
User opens web app
  |
  v
main.ts
  |
  v
App.vue
  |
  v
Vue Router
  |
  v
Route guard checks login/session
  |
  v
Load profile, permissions, and menu from BFF
  |
  v
MainLayout.vue
  |
  v
Render sidebar, header, and selected module page
```

Detailed flow:

```text
1. main.ts initializes the Vue application.
2. App.vue becomes the root component.
3. Router determines which page should be opened.
4. guards.ts checks whether the user is authenticated.
5. auth.store.ts stores the logged-in user and token.
6. menu.store.ts fetches menu data from the BFF.
7. permission.store.ts stores user permissions.
8. MainLayout.vue renders sidebar, header, branch selector, and page content.
9. The selected module page is rendered based on the route.
```

---

# 4. Folder: app/

```text
src/app/
├── main.ts
├── App.vue
├── router/
│   ├── index.ts
│   ├── guards.ts
│   └── routes.ts
├── stores/
│   ├── auth.store.ts
│   ├── menu.store.ts
│   ├── permission.store.ts
│   ├── branch.store.ts
│   ├── period.store.ts
│   ├── preference.store.ts
│   └── notification.store.ts
└── plugins/
    ├── pinia.ts
    ├── axios.ts
    └── permission.ts
```

## 4.1 main.ts

`main.ts` is the frontend entry point.

Backend analogy:

```text
main.py
```

Responsibilities:

```text
- create Vue app
- register router
- register Pinia store
- register global plugins
- mount app into HTML
```

Example concept:

```ts
createApp(App)
  .use(router)
  .use(pinia)
  .mount('#app')
```

---

## 4.2 App.vue

`App.vue` is the root component.

Usually it only contains:

```vue
<RouterView />
```

This means every page is rendered based on the active route.

---

## 4.3 router/index.ts

This file initializes Vue Router.

Responsibilities:

```text
- register all routes
- install route guards
- handle redirect
```

---

## 4.4 router/routes.ts

This file combines routes from all modules.

Example:

```ts
import financeRoutes from '@/modules/finance/routes'
import distributionRoutes from '@/modules/distribution/routes'
import fundraisingRoutes from '@/modules/fundraising/routes'
import administrationRoutes from '@/modules/administration/routes'
import enterpriseRoutes from '@/modules/enterprise/routes'

export const routes = [
  ...financeRoutes,
  ...distributionRoutes,
  ...fundraisingRoutes,
  ...administrationRoutes,
  ...enterpriseRoutes,
]
```

Each module owns its own route configuration.

---

## 4.5 router/guards.ts

`guards.ts` is similar to middleware in the backend.

Flow:

```text
User accesses /distribution/input/distribution
  |
  v
Route guard runs
  |
  |-- Does the route require login?
  |-- Is the user logged in?
  |-- Are permissions already loaded?
  |-- Does the user have the required permission?
  |-- Is active branch selected?
  |-- Is active period selected?
  |
  v
Continue / redirect / show forbidden page
```

Example route metadata:

```ts
{
  path: '/distribution/input/distribution',
  component: DistributionInput,
  meta: {
    requiresAuth: true,
    permission: 'distribution.input.distribution.create',
    layout: 'main',
  },
}
```

Backend analogy:

```python
Depends(require_permission("distribution.input.distribution.create"))
```

Important note:

```text
Frontend route guard is only for user experience.
Final permission validation must still happen in BFF/backend.
```

---

# 5. Folder: stores/

Stores are used for global frontend state.

Backend analogy:

```text
client-side session context / lightweight cache
```

Recommended stores:

```text
auth.store.ts
menu.store.ts
permission.store.ts
branch.store.ts
period.store.ts
preference.store.ts
notification.store.ts
```

---

## 5.1 auth.store.ts

Stores authentication state.

Contains:

```text
- access token
- refresh token if used
- user profile
- login status
```

Login flow:

```text
Login page submit
  |
  v
auth.store.login()
  |
  v
POST /api/v1/auth/login
  |
  v
store token and profile
```

---

## 5.2 menu.store.ts

Stores role-based menu data from the BFF.

Flow:

```text
After login
  |
  v
GET /api/v1/menu
  |
  v
menu.store saves menu
  |
  v
Sidebar renders menu
```

The menu should not be fully hardcoded in Vue.

Example BFF menu response:

```json
[
  {
    "domain": "distribution",
    "label": "Distribution",
    "groups": [
      {
        "group": "input",
        "items": [
          {
            "label": "Distribution Input",
            "route": "/distribution/input/distribution",
            "permission": "distribution.input.distribution.view"
          }
        ]
      }
    ]
  }
]
```

---

## 5.3 permission.store.ts

Stores user permissions.

Used by:

```text
- route guard
- sidebar menu
- action buttons
- component-level visibility
```

Example:

```text
User has:
distribution.input.distribution.view
distribution.input.distribution.create

User does not have:
distribution.input.distribution.approve
```

UI behavior:

```text
- create button is visible
- approve button is hidden or disabled
```

Final validation must remain in BFF/backend.

---

## 5.4 branch.store.ts

Stores the active branch.

Example:

```text
active_branch_id = JKT
```

This is important because many backend queries require branch context.

Possible request:

```text
GET /api/v1/distribution/distributions?branch_id=JKT
```

Alternatively, the BFF may read branch context from session/header.

---

## 5.5 period.store.ts

Stores the active period.

Example:

```text
active_period = 2026-06
```

Used for:

```text
- finance transactions
- reports
- dashboard
- default filters
```

---

## 5.6 notification.store.ts

Used for global messages.

Examples:

```text
Data saved successfully
Approval submitted
Export is being processed
Session expired
```

---

# 6. Folder: layouts/

```text
src/layouts/
├── AuthLayout.vue
├── MainLayout.vue
├── ReportLayout.vue
└── BlankLayout.vue
```

---

## 6.1 AuthLayout.vue

Used for authentication pages:

```text
/login
/forgot-password
```

Usually there is no sidebar.

---

## 6.2 MainLayout.vue

Main application shell.

Contains:

```text
- sidebar domain/menu
- topbar
- user profile menu
- branch selector
- period selector
- notification area
- breadcrumb
- content area
```

Flow:

```text
MainLayout.vue
  |
  |-- reads menu from menu.store
  |-- reads user info from auth.store
  |-- reads active branch from branch.store
  |-- renders Sidebar
  |-- renders RouterView for selected module page
```

---

## 6.3 ReportLayout.vue

Used for report pages that need more space.

Common elements:

```text
- filter panel
- report toolbar
- export button
- full-width table
- chart section
```

---

## 6.4 BlankLayout.vue

Used for special pages:

```text
- print preview
- embedded page
- error page
- public page
```

---

# 7. Folder: shared/

```text
src/shared/
├── api/
├── components/
├── composables/
├── constants/
├── utils/
└── types/
```

This is the reusable frontend library.

Backend analogy:

```text
common/
shared/
utils/
base schemas/
```

---

## 7.1 shared/api/http.ts

HTTP client wrapper.

Usually built with Axios or Fetch.

Responsibilities:

```text
- set BFF base URL
- attach access token
- handle 401
- handle common error
- normalize response
```

Request flow:

```text
Component
  |
  v
Module API function
  |
  v
shared/api/http.ts
  |
  v
BFF endpoint
```

Example:

```ts
export const http = axios.create({
  baseURL: '/api/v1',
})
```

Interceptor concept:

```text
Request interceptor:
  - inject Authorization header
  - inject active branch if needed
  - inject active period if needed

Response interceptor:
  - handle 401
  - handle validation error
  - handle network error
```

---

# 8. Shared Components

```text
shared/components/
├── AppButton.vue
├── AppInput.vue
├── AppSelect.vue
├── AppDataTable.vue
├── AppModal.vue
├── AppDateRange.vue
├── AppPageHeader.vue
├── AppReportToolbar.vue
├── AppPermissionGuard.vue
└── AppLookupSelect.vue
```

---

## 8.1 AppDataTable.vue

Used for paginated lists.

Flow:

```text
List page
  |
  v
AppDataTable
  |
  |-- page change
  |-- sorting
  |-- filter
  |
  v
Call API again
```

Backend request example:

```text
GET /api/v1/distribution/distributions?page=1&page_size=20&sort=date:desc
```

---

## 8.2 AppLookupSelect.vue

Used for dropdown or autocomplete fields.

Flow:

```text
User types beneficiary name
  |
  v
AppLookupSelect debounce 300ms
  |
  v
GET /api/v1/distribution/beneficiaries/lookup?q=ahmad
  |
  v
Show options
```

Recommended backend response:

```json
{
  "data": [
    {
      "id": "BEN-001",
      "label": "Ahmad - Jakarta",
      "value": "BEN-001",
      "metadata": {
        "branch_id": "JKT"
      }
    }
  ]
}
```

---

## 8.3 AppPermissionGuard.vue

Used to hide or disable elements based on permission.

Example:

```vue
<AppPermissionGuard permission="distribution.input.distribution.approve">
  <AppButton>Approve</AppButton>
</AppPermissionGuard>
```

Important:

```text
This is only a frontend guard.
The backend must still validate permission.
```

---

# 9. Shared Composables

Composable means reusable frontend logic.

Backend analogy:

```text
service/helper function
```

Examples:

```text
useApi.ts
usePermission.ts
useTable.ts
useForm.ts
useReport.ts
```

---

## 9.1 useTable.ts

Used for paginated list pages.

Manages:

```text
- page
- page_size
- filters
- sorting
- loading
- error
- reload
```

Flow:

```text
List page mounted
  |
  v
useTable.load()
  |
  v
GET list API
  |
  v
Data is passed to AppDataTable
```

---

## 9.2 useForm.ts

Used for input forms.

Manages:

```text
- form state
- validation
- dirty state
- submit
- reset
- backend error mapping
```

Flow:

```text
User fills form
  |
  v
Submit
  |
  v
Frontend validation
  |
  v
POST to BFF
  |
  v
Handle success or error
```

---

## 9.3 useReport.ts

Used for report pages.

Manages:

```text
- filter
- report loading
- summary
- chart
- table
- export
```

Flow:

```text
User selects date filter
  |
  v
Click Generate
  |
  v
GET /api/v1/reports/distribution/realization
  |
  v
Render summary, chart, and table
```

---

# 10. Folder: modules/

```text
src/modules/
├── finance/
├── distribution/
├── fundraising/
├── administration/
└── enterprise/
```

This is the most important part of the frontend structure.

Each domain has the same internal structure:

```text
src/modules/distribution/
├── routes.ts
├── menu.ts
├── permissions.ts
├── api/
├── stores/
├── views/
├── components/
├── composables/
└── types/
```

---

# 11. Example Module: distribution

## 11.1 routes.ts

Contains routes for the distribution domain.

Example:

```ts
export default [
  {
    path: '/distribution',
    component: DistributionDashboard,
    meta: {
      requiresAuth: true,
      permission: 'distribution.dashboard.view',
    },
  },
  {
    path: '/distribution/input/distribution',
    component: DistributionInput,
    meta: {
      requiresAuth: true,
      permission: 'distribution.input.distribution.create',
    },
  },
  {
    path: '/distribution/reports/realization',
    component: DistributionRealizationReport,
    meta: {
      requiresAuth: true,
      permission: 'distribution.reports.realization.view',
      layout: 'report',
    },
  },
]
```

---

## 11.2 menu.ts

Optional.

If menu is fully controlled by the BFF, this file can be used only for local development or fallback.

Production menu should come from the BFF.

---

## 11.3 permissions.ts

Contains permission constants for the domain.

Purpose:

```text
Avoid hardcoding permission strings in many files.
```

Example:

```ts
export const DISTRIBUTION_PERMISSIONS = {
  VIEW: 'distribution.input.distribution.view',
  CREATE: 'distribution.input.distribution.create',
  APPROVE: 'distribution.input.distribution.approve',
  REPORT_VIEW: 'distribution.reports.realization.view',
}
```

---

## 11.4 api/

Contains functions that call BFF endpoints.

```text
api/
├── distribution.api.ts
├── beneficiary.api.ts
└── distribution-report.api.ts
```

Example:

```ts
// distribution.api.ts

export function getDistributions(params) {
  return http.get('/distribution/distributions', { params })
}

export function getDistributionDetail(id) {
  return http.get(`/distribution/distributions/${id}`)
}

export function createDistribution(payload) {
  return http.post('/distribution/distributions', payload)
}

export function approveDistribution(id, payload) {
  return http.post(`/distribution/distributions/${id}/approve`, payload)
}
```

Important rule:

```text
The frontend API files call the BFF only.
They do not call service-transaction or service-report directly.
```

---

## 11.5 views/

Contains page-level components.

```text
views/
├── DistributionDashboard.vue
├── master/
├── input/
└── reports/
```

Backend perspective:

```text
views are the main consumers of BFF endpoints
```

---

## 11.6 components/

Contains domain-specific components.

Examples:

```text
DistributionForm.vue
BeneficiaryTable.vue
DistributionSummaryCard.vue
DistributionReportFilter.vue
```

Rule:

```text
If a component is only used by distribution, keep it here.
If it is used by multiple domains, move it to shared/components.
```

---

## 11.7 composables/

Contains domain-specific reusable logic.

Examples:

```text
useDistribution.ts
useBeneficiary.ts
useDistributionReport.ts
```

Example responsibility of `useDistribution.ts`:

```text
- load distribution list
- get distribution detail
- submit distribution
- approve distribution
- map backend errors into form state
```

---

## 11.8 types/

Contains TypeScript types for the domain.

Example:

```ts
export type DistributionStatus =
  | 'draft'
  | 'submitted'
  | 'waiting_approval'
  | 'approved'
  | 'rejected'
  | 'posted'
```

Ideally, these types can later be generated from the BFF OpenAPI contract.

---

# 12. List Pagination Flow

Example page:

```text
/distribution/input/distribution
```

Flow:

```text
DistributionList.vue
  |
  v
useTable()
  |
  v
distribution.api.getDistributions(params)
  |
  v
GET /api/v1/distribution/distributions
  |
  v
BFF
  |
  v
service-transaction/read
```

Request from Vue to BFF:

```text
GET /api/v1/distribution/distributions?page=1&page_size=20&status=waiting_approval
```

Recommended response:

```json
{
  "data": [
    {
      "id": "DIST-2026-001",
      "date": "2026-06-21",
      "beneficiary_name": "Ahmad",
      "program_name": "Education Support",
      "amount": 15000000,
      "status": "waiting_approval"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 125,
    "total_pages": 7,
    "has_next": true,
    "has_previous": false
  }
}
```

Frontend parts involved:

```text
DistributionList.vue
AppDataTable.vue
useTable.ts
distribution.api.ts
```

---

# 13. Lookup / Dropdown Flow

Example field:

```text
beneficiary lookup
```

Flow:

```text
DistributionForm.vue
  |
  v
AppLookupSelect.vue
  |
  v
beneficiary.api.lookupBeneficiaries(q)
  |
  v
GET /api/v1/distribution/beneficiaries/lookup?q=ahmad
  |
  v
BFF
  |
  v
service-transaction/read
```

Response:

```json
{
  "data": [
    {
      "id": "BEN-001",
      "label": "Ahmad - Jakarta",
      "value": "BEN-001",
      "metadata": {
        "branch_id": "JKT",
        "category": "Education"
      }
    }
  ]
}
```

Backend recommendation:

```text
Lookup endpoint should be lightweight:
- do not return all fields
- support q/search
- support limit
- support branch filter
- can be cached
```

---

# 14. Transaction Input Flow

Example page:

```text
/distribution/input/distribution
```

Flow:

```text
DistributionInput.vue
  |
  v
DistributionForm.vue
  |
  v
useDistributionForm()
  |
  v
distribution.api.createDistribution(payload)
  |
  v
POST /api/v1/distribution/distributions
  |
  v
BFF
  |
  v
service-transaction/write
```

Payload example:

```json
{
  "beneficiary_id": "BEN-001",
  "program_id": "PRG-001",
  "amount": 15000000,
  "distribution_date": "2026-06-21",
  "description": "Education support"
}
```

Response example:

```json
{
  "id": "DIST-2026-001",
  "status": "draft",
  "message": "Distribution draft has been created"
}
```

---

# 15. Submit and Approval Flow

After a draft is created:

```text
User clicks Submit
  |
  v
POST /api/v1/distribution/distributions/{id}/submit
  |
  v
BFF
  |
  v
service-transaction/write
  |
  v
Backend checks approval rule based on transaction limit
```

Approval rule examples:

```text
amount <= branch limit
  -> Branch Manager approval

amount > branch limit
  -> Regional Manager + Head Office approval
```

Response example if approval is required:

```json
{
  "transaction_id": "DIST-2026-001",
  "status": "waiting_approval",
  "approval": {
    "current_level": 1,
    "required_level": 2,
    "next_approver_role": "Distribution Supervisor",
    "can_approve": false
  }
}
```

UI should display:

```text
- waiting approval status
- approval timeline
- current approver
- approve button only if eligible
```

---

# 16. Asynchronous Approval Flow

Some approval processes may take a long time.

Examples:

```text
- external validation
- document verification
- posting to finance
- legacy system integration
- notification to multiple approvers
- large transaction checking
```

Recommended flow:

```text
User submits transaction
  |
  v
BFF -> service-transaction/write
  |
  v
Backend returns job_id
  |
  v
Vue shows processing state
  |
  v
Vue polls job or transaction status
```

Response example:

```json
{
  "transaction_id": "DIST-2026-001",
  "status": "waiting_approval",
  "job": {
    "job_id": "JOB-2026-0001",
    "status": "processing",
    "message": "Approval preparation is in progress"
  }
}
```

Vue flow:

```text
useDistributionForm.submit()
  |
  |-- if response contains job_id:
  |     start polling GET /api/v1/jobs/{job_id}
  |
  |-- update UI status
  |-- disable submit button
  |-- show progress
```

Related frontend parts:

```text
DistributionInput.vue
DistributionForm.vue
ApprovalTimeline.vue
useDistribution.ts
distribution.api.ts
notification.store.ts
```

---

# 17. Report Flow

Example page:

```text
/distribution/reports/realization
```

Flow:

```text
DistributionRealizationReport.vue
  |
  v
DistributionReportFilter.vue
  |
  v
useDistributionReport()
  |
  v
distribution-report.api.ts
  |
  v
GET /api/v1/reports/distribution/realization
  |
  v
BFF
  |
  v
service-report
```

Response example:

```json
{
  "summary": {
    "total_amount": 250000000,
    "total_beneficiaries": 140,
    "total_programs": 8
  },
  "chart": [
    {
      "label": "Jan",
      "amount": 50000000
    }
  ],
  "table": [
    {
      "date": "2026-06-21",
      "program": "Education Support",
      "beneficiary": "Ahmad",
      "branch": "Jakarta",
      "amount": 15000000
    }
  ]
}
```

UI renders:

```text
- summary cards
- chart
- table
- export button
```

---

# 18. Dashboard Lazy Loading Flow

Dashboard should not load all data at once.

Flow:

```text
User opens /distribution
  |
  v
DistributionDashboard.vue
  |
  v
Load dashboard layout
  |
  v
Render skeleton widgets
  |
  |-- Load SummaryWidget
  |-- Load PendingApprovalWidget
  |-- Load MonthlyTrendWidget
  |-- Load TopProgramsWidget
```

Request examples:

```text
GET /api/v1/dashboard/distribution/layout
GET /api/v1/dashboard/distribution/widgets/summary
GET /api/v1/dashboard/distribution/widgets/pending-approval
GET /api/v1/dashboard/distribution/widgets/monthly-trend
GET /api/v1/dashboard/distribution/widgets/top-programs
```

Internal mapping:

```text
pending approval widget
  -> service-transaction/read

summary/trend/top programs widget
  -> service-report
```

Frontend components:

```text
DistributionDashboard.vue
components/dashboard/DistributionSummaryWidget.vue
components/dashboard/PendingApprovalWidget.vue
components/dashboard/MonthlyTrendWidget.vue
components/dashboard/TopProgramsWidget.vue
```

Benefits of lazy loading:

```text
- faster initial dashboard display
- heavy widgets do not block the page
- one widget error does not break the whole dashboard
- easier caching per widget
- easier permission control per widget
```

---

# 19. Action Button Permission Flow

Example: approve button.

```text
DistributionDetail.vue
  |
  v
permission.store.has('distribution.input.distribution.approve')
  |
  v
also check backend response: approval.can_approve
  |
  v
show approve button
```

Rule:

```text
Approve button is visible if:
- user has approve permission
- transaction status is waiting_approval
- backend response can_approve = true
```

The UI must combine:

```text
user permission
+
transaction state from backend
+
approval eligibility from backend
```

---

# 20. Error Handling Flow

Example backend validation error:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "fields": {
      "amount": "Amount exceeds allowed limit",
      "beneficiary_id": "Beneficiary is required"
    }
  }
}
```

Vue flow:

```text
API call failed
  |
  v
http.ts interceptor / useForm
  |
  v
map field errors to form
  |
  v
show errors in AppInput/AppSelect
```

Backend recommendation:

```text
Use a consistent error response structure so the frontend can map errors easily.
```

---

# 21. Complete Flow Examples

## 21.1 Create Distribution

```text
DistributionInput.vue
  |
  v
DistributionForm.vue
  |
  v
useDistributionForm.ts
  |
  v
distribution.api.ts
  |
  v
shared/api/http.ts
  |
  v
BFF: POST /api/v1/distribution/distributions
  |
  v
service-transaction/write
```

---

## 21.2 Distribution List

```text
DistributionList.vue
  |
  v
useTable.ts
  |
  v
distribution.api.ts
  |
  v
BFF: GET /api/v1/distribution/distributions
  |
  v
service-transaction/read
```

---

## 21.3 Distribution Report

```text
DistributionRealizationReport.vue
  |
  v
useDistributionReport.ts
  |
  v
distribution-report.api.ts
  |
  v
BFF: GET /api/v1/reports/distribution/realization
  |
  v
service-report
```

---

## 21.4 Dashboard Widget

```text
DistributionDashboard.vue
  |
  v
DashboardWidget component
  |
  v
dashboard.api.ts
  |
  v
BFF: GET /api/v1/dashboard/distribution/widgets/summary
  |
  v
service-report or service-transaction/read
```

---

# 22. Backend Contracts Needed by Frontend

To make the Vue application easy to build, the BFF/backend should provide standard contracts for:

```text
1. Auth response
2. User profile
3. Menu response
4. Permission list
5. Pagination response
6. Lookup response
7. Detail response
8. Mutation response
9. Approval state response
10. Async job response
11. Report response
12. Dashboard widget response
13. Error response
```

Most important contract rules:

```text
- response structure must be consistent
- error code must be consistent
- pagination must be consistent
- permissions must be explicit
- approval state must come from backend
- lookup must be lightweight and fast
- report response should be frontend-ready
```

---

# 23. Final Summary for Backend Engineers

The Vue structure is designed to align with the backend modular architecture.

Frontend modules:

```text
finance/
distribution/
fundraising/
administration/
enterprise/
```

Backend modules:

```text
finance/
distribution/
fundraising/
administration/
enterprise/
```

Each Vue domain contains:

```text
routes.ts
  URL mapping for pages

api/
  BFF endpoint callers

views/
  page-level components

components/
  domain-specific components

composables/
  reusable frontend logic

types/
  TypeScript data contracts
```

Main frontend process flow:

```text
View
  -> Composable
  -> Module API
  -> Shared HTTP Client
  -> BFF
  -> Internal Backend Service
```

Design principle:

```text
Backend provides endpoint and response contracts.
Frontend consumes contracts through api/ and composables.
Vue does not know internal backend service topology.
BFF is the main boundary between Vue and backend.
```
