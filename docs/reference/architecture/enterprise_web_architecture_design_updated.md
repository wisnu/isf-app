# Enterprise Web Application Architecture Design

## 1. Background

This document describes the proposed architecture for converting an existing large desktop application into a modular web-based enterprise application.

The existing desktop application has many menus and business domains, including:

- Finance
- Distribution
- Fundraising
- Administration
- Enterprise

Each domain contains:

- Master data
- Input / transaction menus
- Reports
- Role-based access control
- Branch-based access control

The target technology stack is:

- Vue.js for frontend UI
- Python FastAPI for backend APIs
- BFF pattern for frontend-facing API
- Modular backend services
- Separate transaction service and report service

---

## 2. Main Design Goals

### 2.1 Modular by Business Domain

The application should be organized by business domain, not only by technical layer.

Business domains:

```text
finance
distribution
fundraising
administration
enterprise
```

This makes the application easier to maintain because each domain can grow independently.

### 2.2 Role-Based and Multi-Domain Access

One user role may have access to more than one domain.

Example:

```text
Finance Manager
  - Finance input
  - Finance reports

Branch Manager
  - Fundraising input
  - Distribution view
  - Finance summary report

System Administrator
  - Enterprise user management
  - Role management
  - Branch management
```

The menu should not be fully hardcoded in Vue. It should be generated based on user role and permission from the BFF.

### 2.3 Separation Between Transaction and Reporting

Operational application APIs should be separated from reporting APIs.

```text
Transaction Service
  - read: lookup, list, detail, pagination, autocomplete
  - write: create, update, delete, submit, verify, approve, reject, posting

Report Service
  - read-only reports
  - dashboards
  - aggregates
  - exports
```

This keeps the operational application fast and prevents heavy reports from affecting transaction performance.

### 2.4 BFF as the Frontend Gateway

Vue.js should only communicate with the BFF.

```text
Vue.js Web App
  |
  v
FastAPI BFF
  |
  |-- Transaction Service
  |     |-- read
  |     |-- write
  |
  |-- Report Service
        |-- read-only
```

Vue does not need to know which internal service handles the request.

---

## 3. High-Level Architecture

```text
Browser
  |
  v
Vue.js SPA
  |
  v
FastAPI BFF
  |
  |-- service-transaction
  |     |-- read API
  |     |-- write API
  |
  |-- service-report
  |     |-- report read-only API
  |
  v
Database / Legacy System / Reporting Database
```

---

## 4. Responsibility of Each Layer

### 4.1 Vue.js Frontend

Vue.js is responsible for:

```text
- UI layout
- sidebar menu
- domain navigation
- form rendering
- data table rendering
- report viewer
- frontend validation
- route guard
- permission guard
- user interaction
```

Vue should not contain heavy business rules.

### 4.2 FastAPI BFF

The BFF is responsible for:

```text
- frontend-facing API
- authentication/session handling
- role-based menu response
- permission mapping
- route-level access control
- active branch handling
- active period handling
- calling transaction service
- calling report service
- transforming internal API response into UI-friendly response
- hiding internal backend complexity from Vue
```

### 4.3 Transaction Service

The transaction service handles operational application data.

It contains two logical parts:

```text
read
  - lookup
  - dropdown
  - autocomplete
  - list
  - detail
  - pagination
  - search
  - preview before approval

write
  - create
  - update
  - delete
  - submit
  - verify
  - approve
  - reject
  - posting
  - cancel
```

Lookup and list with pagination should stay inside the transaction service, specifically under the read part.

### 4.4 Report Service

The report service is read-only for business data.

It handles:

```text
- official reports
- financial reports
- distribution realization reports
- fundraising reports
- administration reports
- user activity reports
- dashboards
- KPI summaries
- Excel export
- PDF export
```

The report service must not change business transaction data.

---

## 5. Recommended Monorepo Structure

```text
enterprise-web-app/
│
├── apps/
│   ├── web/                         # Vue.js frontend
│   ├── bff/                         # FastAPI BFF
│   ├── service-transaction/         # FastAPI transaction service: read + write
│   └── service-report/              # FastAPI report read-only service
│
├── packages/
│   ├── shared-contracts/            # OpenAPI schemas, shared types, constants
│   ├── shared-python/               # common Python utilities
│   └── design-system/               # optional reusable Vue UI components
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── menu-role-matrix/
│   ├── permission-matrix/
│   └── migration-desktop-to-web/
│
├── infra/
│   ├── nginx/
│   ├── docker/
│   ├── ci-cd/
│   ├── database/
│   └── deployment/
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## 6. Frontend Vue.js Structure

```text
apps/web/
│
├── public/
│
├── src/
│   ├── app/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   │   ├── index.ts
│   │   │   ├── guards.ts
│   │   │   └── routes.ts
│   │   ├── stores/
│   │   │   ├── auth.store.ts
│   │   │   ├── menu.store.ts
│   │   │   ├── permission.store.ts
│   │   │   ├── branch.store.ts
│   │   │   ├── period.store.ts
│   │   │   ├── preference.store.ts
│   │   │   └── notification.store.ts
│   │   └── plugins/
│   │       ├── pinia.ts
│   │       ├── axios.ts
│   │       └── permission.ts
│   │
│   ├── layouts/
│   │   ├── AuthLayout.vue
│   │   ├── MainLayout.vue
│   │   ├── ReportLayout.vue
│   │   └── BlankLayout.vue
│   │
│   ├── shared/
│   │   ├── api/
│   │   │   └── http.ts
│   │   ├── components/
│   │   │   ├── AppButton.vue
│   │   │   ├── AppInput.vue
│   │   │   ├── AppSelect.vue
│   │   │   ├── AppDataTable.vue
│   │   │   ├── AppModal.vue
│   │   │   ├── AppDateRange.vue
│   │   │   ├── AppPageHeader.vue
│   │   │   ├── AppReportToolbar.vue
│   │   │   └── AppPermissionGuard.vue
│   │   ├── composables/
│   │   │   ├── useApi.ts
│   │   │   ├── usePermission.ts
│   │   │   ├── useTable.ts
│   │   │   ├── useForm.ts
│   │   │   └── useReport.ts
│   │   ├── constants/
│   │   │   ├── domains.ts
│   │   │   ├── permissions.ts
│   │   │   └── menu-groups.ts
│   │   ├── utils/
│   │   │   ├── currency.ts
│   │   │   ├── date.ts
│   │   │   ├── number.ts
│   │   │   └── validation.ts
│   │   └── types/
│   │       ├── api.ts
│   │       ├── auth.ts
│   │       ├── menu.ts
│   │       └── report.ts
│   │
│   ├── modules/
│   │   ├── finance/
│   │   ├── distribution/
│   │   ├── fundraising/
│   │   ├── administration/
│   │   └── enterprise/
│   │
│   ├── assets/
│   ├── styles/
│   └── env.d.ts
│
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## 7. Vue Module Structure

Each domain should have the same internal structure.

Example: `distribution`

```text
src/modules/distribution/
│
├── routes.ts
├── menu.ts
├── permissions.ts
│
├── api/
│   ├── distribution.api.ts
│   ├── beneficiary.api.ts
│   └── distribution-report.api.ts
│
├── stores/
│   └── distribution.store.ts
│
├── views/
│   ├── DistributionDashboard.vue
│   │
│   ├── master/
│   │   ├── BeneficiaryMasterList.vue
│   │   ├── BeneficiaryMasterForm.vue
│   │   └── DistributionProgramList.vue
│   │
│   ├── input/
│   │   ├── DistributionInput.vue
│   │   ├── DistributionVerification.vue
│   │   └── DistributionApproval.vue
│   │
│   └── reports/
│       ├── DistributionRealizationReport.vue
│       ├── BeneficiaryReport.vue
│       └── DistributionSummaryReport.vue
│
├── components/
│   ├── DistributionSummaryCard.vue
│   ├── DistributionForm.vue
│   ├── BeneficiaryTable.vue
│   └── DistributionReportFilter.vue
│
├── composables/
│   ├── useDistribution.ts
│   ├── useBeneficiary.ts
│   └── useDistributionReport.ts
│
└── types/
    ├── distribution.types.ts
    ├── beneficiary.types.ts
    └── report.types.ts
```

---

## 8. UI Menu Design

The menu should support:

```text
- domain switcher
- role-based menu visibility
- menu search
- favorite menu
- recent menu
- grouped menu
- locked menu for unauthorized access
- responsive sidebar
```

Menu groups per domain:

```text
Master Data
Input / Transaction
Reports
```

Example:

```text
Finance
  Master Data
    - Account Master
    - Bank Master
    - Budget Master

  Input / Transaction
    - Cash In Input
    - Cash Out Input
    - Journal Input
    - Bank Reconciliation

  Reports
    - Cash Flow Report
    - General Ledger Report
    - Budget Realization Report
```

---

## 9. Dynamic Menu Response from BFF

The menu should be generated by the BFF based on the user role and permission.

Example response:

```json
[
  {
    "domain": "distribution",
    "label": "Distribution",
    "icon": "package",
    "groups": [
      {
        "group": "master",
        "label": "Master Data",
        "items": [
          {
            "code": "DIST.MASTER.BENEFICIARY",
            "label": "Beneficiary Master",
            "route": "/distribution/master/beneficiaries",
            "permission": "distribution.master.beneficiary.view"
          }
        ]
      },
      {
        "group": "input",
        "label": "Input / Transaction",
        "items": [
          {
            "code": "DIST.INPUT.DISTRIBUTION",
            "label": "Distribution Input",
            "route": "/distribution/input/distribution",
            "permission": "distribution.input.distribution.view"
          }
        ]
      },
      {
        "group": "reports",
        "label": "Reports",
        "items": [
          {
            "code": "DIST.REPORT.REALIZATION",
            "label": "Distribution Realization Report",
            "route": "/distribution/reports/realization",
            "permission": "distribution.reports.realization.view"
          }
        ]
      }
    ]
  }
]
```

---

## 10. Recommended Permission Pattern

Use a business-based permission format:

```text
{domain}.{group}.{resource}.{action}
```

Examples:

```text
finance.master.account.view
finance.master.account.create
finance.input.cash_in.view
finance.input.cash_in.create
finance.input.cash_in.approve
finance.reports.cash_flow.view
finance.reports.cash_flow.export

distribution.master.beneficiary.view
distribution.master.beneficiary.create
distribution.input.distribution.view
distribution.input.distribution.create
distribution.input.distribution.verify
distribution.input.distribution.approve
distribution.reports.realization.view
distribution.reports.realization.export

fundraising.input.donation.create
fundraising.reports.collection.view

enterprise.user.create
enterprise.role.assign_permission
enterprise.branch.update
```

Avoid permission names based on technical service names.

Do not use:

```text
service_read.distribution.view
service_write.distribution.create
service_report.distribution.view
```

Use business names instead.

---

## 11. Frontend Route Pattern

```text
/finance
/finance/master/accounts
/finance/input/cash-in
/finance/input/cash-out
/finance/reports/cash-flow

/distribution
/distribution/master/beneficiaries
/distribution/master/programs
/distribution/input/distribution
/distribution/input/verification
/distribution/input/approval
/distribution/reports/realization

/fundraising
/fundraising/master/donors
/fundraising/input/donation
/fundraising/reports/collection

/administration
/administration/master/letters
/administration/input/incoming-letter
/administration/reports/archive

/enterprise
/enterprise/users
/enterprise/roles
/enterprise/branches
```

---

## 12. BFF Structure

```text
apps/bff/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   │
│   ├── core/
│   │   ├── auth.py
│   │   ├── security.py
│   │   ├── permissions.py
│   │   ├── response.py
│   │   ├── pagination.py
│   │   └── audit.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── menu.py
│   │       ├── profile.py
│   │       ├── finance.py
│   │       ├── distribution.py
│   │       ├── fundraising.py
│   │       ├── administration.py
│   │       ├── enterprise.py
│   │       └── reports.py
│   │
│   ├── clients/
│   │   ├── transaction_read_client.py
│   │   ├── transaction_write_client.py
│   │   ├── report_client.py
│   │   └── auth_client.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   ├── menu.py
│   │   ├── auth.py
│   │   └── report.py
│   │
│   └── tests/
│
├── pyproject.toml
└── Dockerfile
```

---

## 13. Transaction Service Structure

The transaction service contains both read and write logic for operational application data.

```text
apps/service-transaction/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── transaction.py
│   │   ├── audit.py
│   │   └── events.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── v1/
│   │       ├── read/
│   │       │   ├── finance.py
│   │       │   ├── distribution.py
│   │       │   ├── fundraising.py
│   │       │   ├── administration.py
│   │       │   └── enterprise.py
│   │       │
│   │       └── write/
│   │           ├── finance.py
│   │           ├── distribution.py
│   │           ├── fundraising.py
│   │           ├── administration.py
│   │           └── enterprise.py
│   │
│   ├── modules/
│   │   ├── finance/
│   │   ├── distribution/
│   │   ├── fundraising/
│   │   ├── administration/
│   │   └── enterprise/
│   │
│   └── tests/
│
├── pyproject.toml
└── Dockerfile
```

---

## 14. Transaction Module Structure

Example: `distribution`

```text
apps/service-transaction/app/modules/distribution/
│
├── read/
│   ├── schemas/
│   │   ├── beneficiary_lookup.py
│   │   ├── distribution_list.py
│   │   ├── distribution_detail.py
│   │   └── filters.py
│   │
│   ├── services/
│   │   ├── beneficiary_query_service.py
│   │   ├── distribution_query_service.py
│   │   └── lookup_service.py
│   │
│   └── repositories/
│       ├── beneficiary_query_repository.py
│       ├── distribution_query_repository.py
│       └── lookup_repository.py
│
├── write/
│   ├── schemas/
│   │   ├── distribution_create.py
│   │   ├── distribution_update.py
│   │   ├── approval.py
│   │   └── verification.py
│   │
│   ├── services/
│   │   ├── distribution_command_service.py
│   │   ├── verification_service.py
│   │   └── approval_service.py
│   │
│   ├── repositories/
│   │   ├── distribution_repository.py
│   │   └── beneficiary_repository.py
│   │
│   ├── domain/
│   │   ├── distribution_entity.py
│   │   ├── distribution_rules.py
│   │   └── distribution_status.py
│   │
│   └── events/
│       ├── distribution_created.py
│       ├── distribution_verified.py
│       └── distribution_approved.py
│
└── permissions.py
```

---

## 15. Report Service Structure

```text
apps/service-report/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── export.py
│   │   ├── report_filter.py
│   │   ├── report_response.py
│   │   └── security.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── v1/
│   │       ├── finance_reports.py
│   │       ├── distribution_reports.py
│   │       ├── fundraising_reports.py
│   │       ├── administration_reports.py
│   │       └── enterprise_reports.py
│   │
│   ├── reports/
│   │   ├── finance/
│   │   ├── distribution/
│   │   ├── fundraising/
│   │   ├── administration/
│   │   └── enterprise/
│   │
│   └── tests/
│
├── pyproject.toml
└── Dockerfile
```

Example report domain:

```text
apps/service-report/app/reports/distribution/
│
├── router.py
│
├── schemas/
│   ├── realization_report.py
│   ├── beneficiary_report.py
│   └── summary_report.py
│
├── services/
│   ├── realization_report_service.py
│   ├── beneficiary_report_service.py
│   └── summary_report_service.py
│
├── repositories/
│   ├── realization_report_repository.py
│   ├── beneficiary_report_repository.py
│   └── summary_report_repository.py
│
├── exporters/
│   ├── realization_excel_exporter.py
│   └── realization_pdf_exporter.py
│
└── templates/
    ├── realization_report.html
    └── beneficiary_report.html
```

---

## 16. API Routing Strategy

### 16.1 Vue to BFF

Vue only calls the BFF.

```text
GET  /api/v1/distribution/beneficiaries
GET  /api/v1/distribution/distributions
POST /api/v1/distribution/distributions
GET  /api/v1/reports/distribution/realization
```

### 16.2 BFF to Internal Services

The BFF routes requests internally:

```text
GET lookup/list/detail/pagination
  -> service-transaction/read

POST/PUT/PATCH/DELETE/action
  -> service-transaction/write

GET /reports
  -> service-report
```

---

## 17. Example Endpoint Mapping

| Frontend / BFF Endpoint | Internal Target | Purpose |
|---|---|---|
| `GET /api/v1/distribution/beneficiaries/lookup` | `service-transaction/read` | Lookup beneficiaries |
| `GET /api/v1/distribution/distributions` | `service-transaction/read` | Paginated distribution list |
| `GET /api/v1/distribution/distributions/{id}` | `service-transaction/read` | Distribution detail |
| `POST /api/v1/distribution/distributions` | `service-transaction/write` | Create distribution |
| `POST /api/v1/distribution/distributions/{id}/verify` | `service-transaction/write` | Verify distribution |
| `POST /api/v1/distribution/distributions/{id}/approve` | `service-transaction/write` | Approve distribution |
| `GET /api/v1/reports/distribution/realization` | `service-report` | Distribution realization report |
| `GET /api/v1/reports/finance/cash-flow` | `service-report` | Finance cash flow report |

---

## 18. Example BFF Distribution Router

```python
from fastapi import APIRouter, Depends

from app.clients.transaction_read_client import transaction_read_client
from app.clients.transaction_write_client import transaction_write_client
from app.core.permissions import require_permission

router = APIRouter()


@router.get("/beneficiaries/lookup")
async def lookup_beneficiaries(
    q: str | None = None,
    current_user = Depends(require_permission("distribution.master.beneficiary.view")),
):
    return await transaction_read_client.get(
        "/api/v1/read/distribution/beneficiaries/lookup",
        params={"q": q},
        user=current_user,
    )


@router.get("/distributions")
async def list_distributions(
    page: int = 1,
    page_size: int = 20,
    current_user = Depends(require_permission("distribution.input.distribution.view")),
):
    return await transaction_read_client.get(
        "/api/v1/read/distribution/distributions",
        params={
            "page": page,
            "page_size": page_size,
        },
        user=current_user,
    )


@router.post("/distributions")
async def create_distribution(
    payload: dict,
    current_user = Depends(require_permission("distribution.input.distribution.create")),
):
    return await transaction_write_client.post(
        "/api/v1/write/distribution/distributions",
        json=payload,
        user=current_user,
    )


@router.post("/distributions/{distribution_id}/approve")
async def approve_distribution(
    distribution_id: str,
    current_user = Depends(require_permission("distribution.input.distribution.approve")),
):
    return await transaction_write_client.post(
        f"/api/v1/write/distribution/distributions/{distribution_id}/approve",
        user=current_user,
    )
```

---

## 19. Example BFF Report Router

```python
from fastapi import APIRouter, Depends

from app.clients.report_client import report_client
from app.core.permissions import require_permission

router = APIRouter()


@router.get("/distribution/realization")
async def distribution_realization_report(
    start_date: str,
    end_date: str,
    branch_id: str | None = None,
    current_user = Depends(require_permission("distribution.reports.realization.view")),
):
    return await report_client.get(
        "/api/v1/reports/distribution/realization",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "branch_id": branch_id,
        },
        user=current_user,
    )
```

---

## 20. Pagination Response Standard

All paginated list responses should use the same response format.

```json
{
  "data": [
    {
      "id": "DIST-2026-001",
      "date": "2026-06-21",
      "beneficiary_name": "Ahmad",
      "program_name": "Education Support",
      "amount": 15000000,
      "status": "approved"
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

---

## 21. Lookup Response Standard

Lookup responses should be lightweight and optimized for dropdowns or autocomplete.

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

---

## 22. Report Response Standard

Reports should return frontend-ready data.

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
    },
    {
      "label": "Feb",
      "amount": 75000000
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

---

## 23. Database Strategy

### 23.1 Simple Initial Option

```text
service-transaction -> main database
service-report      -> main database with read-only database user
```

This is the easiest option for the first implementation.

Important rule:

```text
service-report database user must be read-only
```

### 23.2 Intermediate Option

```text
service-transaction -> main database
service-report      -> read replica / reporting schema
```

This is better when reports are heavier.

### 23.3 Advanced Option

```text
service-transaction -> OLTP database
service-report      -> data warehouse / data mart
```

This is suitable if the reporting workload is very large.

---

## 24. Event Flow Option

In the future, the transaction service can publish events after important write actions.

```text
service-transaction/write
  |
  | event: DistributionApproved
  v
event bus / queue
  |
  |-- update read model
  |-- update reporting table
  |-- send notification
  |-- create audit log
```

Example event:

```json
{
  "event_id": "evt_001",
  "event_type": "distribution.approved",
  "occurred_at": "2026-06-21T10:00:00Z",
  "data": {
    "distribution_id": "DIST-2026-001",
    "branch_id": "JKT",
    "amount": 15000000,
    "approved_by": "user_123"
  }
}
```

This is optional for the first version.

---
# 25. Approval Workflow Design

All input and transaction processes should support an approval workflow.

The approval process should be configurable per domain, transaction type, branch, role, and transaction amount limit.

Examples:

```text
Finance Cash Out
  amount <= 5,000,000
    approval: Finance Supervisor

  amount > 5,000,000 and <= 50,000,000
    approval: Finance Manager

  amount > 50,000,000
    approval: Finance Manager + Director

Distribution Transaction
  amount <= branch limit
    approval: Branch Manager

  amount > branch limit
    approval: Regional Manager + Head Office
```

The approval engine should consider:

```text
- transaction type
- transaction amount
- user role
- branch
- department/domain
- approval level
- transaction status
- approval delegation
- approval escalation
- approval timeout
```

Recommended transaction status flow:

```text
draft
  -> submitted
  -> waiting_approval
  -> approved
  -> posted
  -> completed
```

Rejected or cancelled flow:

```text
waiting_approval
  -> rejected

draft / submitted / waiting_approval
  -> cancelled
```

Recommended approval table concept:

```text
approval_workflow
  - id
  - domain
  - transaction_type
  - branch_id
  - min_amount
  - max_amount
  - approval_level
  - approver_role
  - is_parallel
  - is_active

approval_task
  - id
  - transaction_id
  - workflow_id
  - approval_level
  - approver_user_id
  - approver_role
  - status
  - assigned_at
  - approved_at
  - rejected_at
  - remarks
```

The write API should not directly mark a transaction as final unless the approval requirement has been satisfied.

Example write endpoint:

```text
POST /api/v1/write/finance/cash-out
POST /api/v1/write/finance/cash-out/{id}/submit
POST /api/v1/write/finance/cash-out/{id}/approve
POST /api/v1/write/finance/cash-out/{id}/reject
POST /api/v1/write/finance/cash-out/{id}/post
```

The BFF should expose the approval state to the UI:

```json
{
  "transaction_id": "CO-2026-001",
  "status": "waiting_approval",
  "approval": {
    "current_level": 2,
    "required_level": 3,
    "next_approver_role": "Finance Manager",
    "can_approve": true,
    "can_reject": true
  }
}
```

---

# 26. Asynchronous Approval and Long-Running Process

Some approval processes may take a long time because they involve:

```text
- multi-level approval
- external validation
- document verification
- large transaction checking
- posting to finance
- report model update
- integration with legacy system
- notification to multiple approvers
```

For these cases, the system should support asynchronous processing.

Recommended pattern:

```text
User submits transaction
  |
  v
BFF calls service-transaction/write
  |
  v
Transaction saved as submitted / waiting_approval
  |
  v
Background job is created
  |
  v
Worker processes approval preparation, validation, notification, or posting
  |
  v
User checks status from read API
```

Example async flow:

```text
POST /api/v1/distribution/distributions/{id}/submit
  -> returns job_id and transaction status

GET /api/v1/jobs/{job_id}
  -> returns job progress

GET /api/v1/distribution/distributions/{id}
  -> returns latest transaction status
```

Example response:

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

Recommended background job states:

```text
queued
processing
completed
failed
cancelled
retrying
```

Recommended components:

```text
service-transaction/write
  - creates transaction
  - creates approval task
  - publishes event or creates background job

worker
  - processes long-running validation
  - sends notification
  - updates approval task
  - updates read model
  - updates report model if needed

service-transaction/read
  - provides transaction status
  - provides approval task status
  - provides job status

BFF
  - returns UI-friendly status
  - hides worker/internal queue details from Vue
```

Possible technologies:

```text
- Celery
- RQ
- Dramatiq
- FastAPI BackgroundTasks for simple cases
- Redis or RabbitMQ as queue
```

For production and important approval processes, prefer a real queue such as Redis/RabbitMQ with Celery, RQ, or Dramatiq. FastAPI background tasks are better for simple, non-critical short tasks.

UI behavior for async approval:

```text
- after submit, show processing state
- disable duplicate submit button
- show approval timeline
- allow user to refresh status
- optionally use polling
- optionally use WebSocket/SSE for real-time update
```

Polling example:

```text
GET /api/v1/distribution/distributions/{id}/status
GET /api/v1/jobs/{job_id}
```

---

# 27. Dashboard Lazy Loading Design

Dashboards should use lazy loading because dashboard data can come from multiple sources and may contain heavy queries.

The dashboard should not load all widgets at once.

Recommended dashboard loading strategy:

```text
1. Load dashboard shell first
2. Load user permission and accessible widgets
3. Load high-priority KPI cards first
4. Load charts after KPI cards
5. Load heavy tables or trend data last
6. Load hidden/collapsed widgets only when opened
```

Example dashboard API pattern:

```text
GET /api/v1/dashboard/distribution/layout
GET /api/v1/dashboard/distribution/widgets/summary
GET /api/v1/dashboard/distribution/widgets/monthly-trend
GET /api/v1/dashboard/distribution/widgets/top-programs
GET /api/v1/dashboard/distribution/widgets/pending-approval
```

Dashboard data can come from:

```text
BFF
  |
  |-- service-transaction/read
  |     for operational widgets, such as pending approvals
  |
  |-- service-report
        for aggregate widgets, KPI, charts, trends
```

Example dashboard widget response:

```json
{
  "widget_id": "distribution_summary",
  "title": "Distribution Summary",
  "status": "loaded",
  "data": {
    "total_amount": 250000000,
    "total_beneficiaries": 140,
    "pending_approval": 12
  },
  "last_updated_at": "2026-06-21T10:00:00Z"
}
```

Frontend dashboard pattern:

```text
DashboardPage.vue
  - loads dashboard layout
  - renders widget placeholders
  - lazy loads each widget component
  - fetches each widget data independently
  - shows skeleton loading per widget
  - handles widget-level error state
```

Vue component structure:

```text
modules/distribution/views/DistributionDashboard.vue
modules/distribution/components/dashboard/DistributionSummaryWidget.vue
modules/distribution/components/dashboard/PendingApprovalWidget.vue
modules/distribution/components/dashboard/MonthlyTrendWidget.vue
modules/distribution/components/dashboard/TopProgramsWidget.vue
```

Recommended UI behavior:

```text
- use skeleton loader per widget
- avoid blocking the entire dashboard
- retry failed widget independently
- cache dashboard widgets where possible
- refresh widgets individually
- defer heavy charts until visible
```

Lazy loading benefits:

```text
- faster initial dashboard display
- reduced backend load
- better user experience
- easier widget-level permission control
- easier dashboard personalization
```

---


## 28. Deployment Design

```text
Nginx / Gateway
│
├── /                     -> Vue static build
├── /api/v1               -> BFF
│
├── internal only:
│   ├── service-transaction
│   └── service-report
```

Browser only sees:

```text
https://app.domain.com/
https://app.domain.com/api/v1/...
```

Internal services:

```text
http://service-transaction:8000
http://service-report:8000
```

---

## 29. Docker Compose Example

```yaml
services:
  web:
    build: ./apps/web
    ports:
      - "3000:80"

  bff:
    build: ./apps/bff
    environment:
      TRANSACTION_SERVICE_URL: http://service-transaction:8000
      REPORT_SERVICE_URL: http://service-report:8000
    ports:
      - "8000:8000"

  service-transaction:
    build: ./apps/service-transaction
    environment:
      DATABASE_URL: postgresql://app_user:password@db:5432/appdb

  service-report:
    build: ./apps/service-report
    environment:
      REPORT_DATABASE_URL: postgresql://report_readonly_user:password@db:5432/appdb

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: password
```

For production, do not store passwords directly in `docker-compose.yml`. Use secret manager or secure environment variables.

---

## 30. Implementation Phases

### Phase 1: Foundation

```text
- login
- authentication/session
- role and permission
- dynamic menu from BFF
- main layout
- domain switcher
- active branch
- active period
```

### Phase 2: One Vertical Slice per Domain

```text
Finance
  - Cash In Input
  - Cash Flow Report

Distribution
  - Distribution Input
  - Distribution Realization Report

Fundraising
  - Donation Input
  - Fundraising Collection Report

Administration
  - Incoming Letter Input
  - Archive Report

Enterprise
  - User Input
  - User Activity Report
```

### Phase 3: Standard Components

```text
- AppForm
- AppDataTable
- AppModal
- AppDateRange
- AppReportToolbar
- AppPermissionGuard
- AppLookupSelect
```

### Phase 4: Migrate Remaining Menus

After the architecture is stable, migrate all remaining menus domain by domain.

---

## 31. Final Summary

The recommended design is:

```text
Vue.js
  - UI only
  - calls BFF only

BFF
  - frontend API gateway
  - role/menu/permission orchestration
  - routes request to internal services

service-transaction
  - operational application data
  - read: lookup, list, detail, pagination
  - write: create, update, submit, approve
  - approval workflow based on transaction limit
  - async processing for long-running approval or posting

service-report
  - report read-only
  - dashboard aggregate data
  - export
  - heavy aggregation

dashboard
  - lazy loaded widgets
  - independent widget loading
  - skeleton loading and widget-level retry
```

The main principle is:

```text
Design the system by business domain.
Separate operational transaction APIs from reporting APIs.
Keep Vue simple.
Keep the BFF as the only API surface for the frontend.
Keep report service read-only for business data.
```
