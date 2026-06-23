# Plan: Laporan Penyaluran Zakat

**Dibuat**: 2026-06-22
**Portal**: zakat
**Scope**: 7 laporan (Proposal Masuk, Daftar Mustahiq, Realisasi Rutin, Realisasi Non Rutin, Piutang Realisasi, Pengembalian Realisasi, Penyaluran Per Mustahiq)

---

## Urutan Eksekusi

**Fase 1**: Konfirmasi Role + DWH Design
**Fase 2**: DB Migrations (7 DWH views)
**Fase 3**: report-api + BFF (endpoints + proxy)
**Fase 4**: Seed (menu keys, role_menu)
**Fase 5**: UI (7 laporan pages)
**Fase 6**: Testing (E2E smoke test)

Layer 1–3 bisa sedikit paralel setelah DWH design confirmed, tetapi DWH views HARUS selesai sebelum report-api bisa test.

---

## Layer 0 — Konfirmasi (1–2 hari)

**Owner**: nuwis-architect (lanj dari specs review)

- [ ] **[BLOCKER] Role QAC**: Konfirmasi status role QAC di isf-app
  - Apakah perlu ditambahkan? Atau mapping ke role existing?
  - Impact: 6 menu_keys di layer 4 (seed)

- [ ] **[BLOCKER] AllowedGroups Laporan By Mustahiq**: Tentukan role yang bisa akses endpoint 7
  - Default: same as others (DIST, SPVDIST) jika QAC resolved, atau DIST/SPVDIST only
  - Impact: seed-menu-and-rolemenu.sql di layer 4

**Delivery**: Approval tertulis, update specs.md "Ambiguitas & Konfirmasi" section

---

## Layer 1 — DB / DWH (nuwis-db-migrator, model: OPUS)

**Duration**: 3–5 hari (kompleksitas tinggi: 14-15 JOIN per view, window function, cross-schema)

### Migrations: 7 DWH Views

Create file: `infra/db/migrations/dwh/v_distribution_realization_reports.sql`
(Consolidate 7 views dalam 1 file untuk organizational simplicity)

- [ ] **dwh.v_report_proposal_incoming**
  - Source: program.(proposal, productgroup, mustahiq, customer) LEFT JOIN (realizationdetail, realization, realizationmemo, mustahiqproduct, financialaccount)
  - Window function: RANK() OVER (PARTITION BY rd.mustahiqproductid ORDER BY rd.realizationamount DESC) — ambil terbesar
  - Filter params: proposaldate BETWEEN (flexible di BFF), proposalstatus='B' (hardcoded)
  - Output cols: proposal_id, proposal_date, proposal_description, proposal_no, proposal_nominal, proposal_received_by, proposal_received_date, proposal_reference_by, customer_name, product_group_name, realization_date, realization_amount, memo_amount, realmemo_number, fund_source_no, fund_source_name, mustahiq_id, proposal_status

- [ ] **dwh.v_report_mustahiq_list**
  - Source: program.(mustahiq, customer, customercorporate, mustahiqproduct, product) LEFT JOIN (MustahiqAdditionalInfo, v_mustahiqdata), enum_varchar(eAshnaf)
  - Education fields nested (sd_kelas, sd_tahun_awal, sd_tahun_akhir, smp_*, sma_*, universitas_*)
  - Filter params (flexible di BFF): product_id, mustahiq_type ('MP'/'MC'), date_start_from, date_start_to
  - Output cols: mustahiq_id, mustahiq_type, customer_name, address_street, address_kelurahan, address_kecamatan, address_city, phone_number, cp_name, cp_phone_number, cp_mobile_number, ashnaf_label, product_name, product_id, date_start, distribution_amount, school_name, achievement, supervisor_name, [8 education fields]

- [ ] **dwh.v_report_realization_regular**
  - Source: program.(product, program, productgroup, realization, realizationdetail, mustahiq, customer, realizationmemo) LEFT JOIN (statusrecrepdetail, realizationbudget, transaction.Budget, transaction.BudgetItem)
  - **DISCRIMINATOR**: WHERE programtype='R'
  - Filter params (flexible di BFF): realizationdate BETWEEN date_from AND date_to
  - No BranchCode filter (cross-branch report)
  - Output cols: product_id, product_name, product_group_name, mustahiq_product_name, customer_name, address_street, realization_id, realization_date, status_receivables, realization_amount, report_amount, report_detail_status, budget_code, budget_item_description

- [ ] **dwh.v_report_realization_non_regular**
  - Source: program.(product, program, productgroup, realization, realizationdetail, mustahiq, customer, realizationmemo) LEFT JOIN (proposal, transaction.financialaccount, statusrecrepdetail, realizationbudget, transaction.Budget, transaction.BudgetItem)
  - **DISCRIMINATOR**: WHERE programtype='N'
  - Filter params: realizationdate BETWEEN, branch_code (from BFF), realization_amount BETWEEN amount_min AND amount_max
  - Output cols: [same as Regular] + proposal_no, proposal_description, proposal_nominal, proposal_reference_by, account_name, branch_code

- [ ] **dwh.v_report_realization_receivable**
  - Source: program.(realizationmemo, realization, vemployee) LEFT JOIN (realizationdetail, statusreceivablereport, statusrecrepdetail)
  - **DISCRIMINATOR**: WHERE statusreceivables='Y'
  - LEFT JOIN filter: statusrecrepdetail.reportdetailstatus IN ('1','2') — untuk hitung report_amount aggregate
  - Filter params: realizationdate BETWEEN (inclusive di akhir — pakai <= bukan <)
  - Output cols: realization_id, realization_date, realization_amount, realization_input_user, realization_type ('R'/'N'), realization_description, realmemo_number, employee_name, receivable_report_user_input, report_amount, receivable_report_date

- [ ] **dwh.v_report_realization_return**
  - Source: program.(realizationreturn, realization, realizationmemo) LEFT JOIN (realizationcost, costitem)
  - Filter params: returndate BETWEEN (BUKAN realizationdate!)
  - Output: 2 result sets — header (returnid, return_date, realization_amount, return_amount, realmemo_number, return_description, input_user, realization_id) + nested detail (cost_item_description, cost_amount per costitem)
  - Atau: flat join dengan multiple rows per return — ambil approach mana yang lebih mudah di report-api (recommend nested query di service.py vs flat view)

- [ ] **dwh.v_report_realization_by_mustahiq**
  - Source: program.(product, program, productgroup, realization, realizationdetail, mustahiq, customer, realizationmemo) LEFT JOIN (proposal, transaction.financialaccount, realizationbudget, transaction.Budget, transaction.BudgetItem)
  - NO DISCRIMINATOR on programtype — ambil R+N sekaligus (cross-type)
  - Filter params: realizationdate BETWEEN, branch_code (from BFF)
  - ORDER BY: customer_name, customer_id, realization_date, product_name — untuk grouping di UI/export
  - Output cols: customer_id, customer_name, address_street, product_id, product_name, product_group_name, realization_date, realization_amount, detail_description, account_name, proposal_no, proposal_nominal, proposal_description, proposal_reference_by, budget_code, budget_item_description, branch_code

**Apply setelah selesai**:
```bash
psql -U transaction -d mziss_zakat -f infra/db/migrations/dwh/v_distribution_realization_reports.sql
```

---

## Layer 2 — report-api (nuwis-python-builder, model: haiku)

**Duration**: 5–7 hari (7 endpoints, masing-masing punya service.py + router.py + export.py dengan openpyxl logic)

### Folder Structure

```
apps_zakat/report-api/app/modules/distribution/
├── __init__.py
├── router.py                 ← 7 GET endpoints
├── service.py                ← query logic per laporan
├── export.py                 ← Excel generation (openpyxl) per laporan
└── schemas.py                ← Pydantic models (request/response)
```

### Task Checklist

- [ ] **apps_zakat/report-api/app/modules/distribution/__init__.py** — modul init

- [ ] **apps_zakat/report-api/app/modules/distribution/schemas.py**
  - Request models: ProposalIncomingRequest, MustahiqListRequest, RealizationRegularRequest, dst
  - Response models: ProposalIncomingRow, MustahiqListRow, RealizationRegularRow, dst
  - List response wrapper: ReportResponse[T] dengan pagination

- [ ] **apps_zakat/report-api/app/modules/distribution/service.py** — 7 service classes (atau 1 class dengan 7 methods)
  - `class ProposalIncomingService`: query dwh.v_report_proposal_incoming
  - `class MustahiqListService`: query dwh.v_report_mustahiq_list
  - `class RealizationRegularService`: query dwh.v_report_realization_regular
  - `class RealizationNonRegularService`: query dwh.v_report_realization_non_regular (+ branch_code filter)
  - `class RealizationReceivableService`: query dwh.v_report_realization_receivable
  - `class RealizationReturnService`: query dwh.v_report_realization_return (+ nested query untuk costs)
  - `class RealizationByMustahiqService`: query dwh.v_report_realization_by_mustahiq (+ branch_code filter)
  - **Pattern**: each method returns `list[dict]` (DWH view raw JSON)

- [ ] **apps_zakat/report-api/app/modules/distribution/export.py** — 7 Excel generators (openpyxl)
  - `export_proposal_incoming(rows: list[dict]) → bytes` → 1 sheet
  - `export_mustahiq_list(rows: list[dict]) → bytes` → 1 sheet
  - `export_realization_regular(rows: list[dict]) → bytes` → 3 sheet (Detail with grouping+subtotal, Rekap per ProductGroup, RekapAnggaran per BudgetCode)
  - `export_realization_non_regular(rows: list[dict]) → bytes` → 3 sheet (same pattern as Regular)
  - `export_realization_receivable(rows: list[dict]) → bytes` → 1 sheet (compute sisa_piutang di export layer)
  - `export_realization_return(rows: list[dict], costs: list[list[dict]]) → bytes` → 1 sheet (nested costs — expandable row atau flat dengan multiple rows)
  - `export_realization_by_mustahiq(rows: list[dict]) → bytes` → 2 sheet (Detail grouped by customer_name with subtotal, Rekap per customer)

- [ ] **apps_zakat/report-api/app/modules/distribution/router.py** — 14 endpoints (7 preview + 7 export)

```python
# GET /api/report/distribution/proposal-incoming
@router.get("/proposal-incoming")
async def get_proposal_incoming(
    date_from: str,           # ISO YYYY-MM-DD
    date_to: str,
    mustahiq_id: int = None,
    product_group_id: int = None,
    page: int = 1,
    limit: int = 25,
    pool: asyncpg.Pool = Depends(get_pool),
) -> ReportResponse[ProposalIncomingRow]:
    service = ProposalIncomingService(pool)
    rows, total = await service.query(date_from, date_to, mustahiq_id, product_group_id, page, limit)
    return ReportResponse(data=rows, pagination={"page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit})

# GET /api/report/distribution/proposal-incoming/export
@router.get("/proposal-incoming/export")
async def export_proposal_incoming(
    date_from: str,
    date_to: str,
    mustahiq_id: int = None,
    product_group_id: int = None,
    pool: asyncpg.Pool = Depends(get_pool),
):
    service = ProposalIncomingService(pool)
    rows, _ = await service.query(date_from, date_to, mustahiq_id, product_group_id, page=1, limit=999999)
    xlsx_bytes = export_proposal_incoming(rows)
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=Laporan_Proposal_Masuk.xlsx"}
    )

# [Repeat pattern untuk 6 endpoint lainnya]
```

- [ ] **apps_zakat/report-api/app/main.py** — register router
  - `from app.modules.distribution.router import router as distribution_router`
  - `app.include_router(distribution_router, prefix="/api/report/distribution", tags=["distribution"])`

**Quality Gates**:
- [ ] All 7 endpoints return proper pagination (page, limit, total, total_pages)
- [ ] All 7 export endpoints return xlsx with proper Content-Disposition header + filename
- [ ] Discriminators enforced di query (programtype='R'/'N', statusreceivables='Y', etc.)
- [ ] Branch code filtering implemented untuk endpoints 4 & 7

---

## Layer 3 — BFF (nuwis-bff-builder, model: haiku)

**Duration**: 2–3 hari (7 routes, masing-masing proxy ke report-api)

### File: apps_zakat/bff-api/app/routers/distribution.py

```python
# Proxy pattern:
@router.get("/report/proposal-incoming")
async def get_proposal_incoming(
    date_from: str,
    date_to: str,
    mustahiq_id: int = None,
    product_group_id: int = None,
    page: int = 1,
    limit: int = 25,
    session: Session = Depends(require_menu("distribution.report.proposal-incoming")),
    report_client: httpx.AsyncClient = Depends(get_report_client),
):
    response = await report_client.get(
        "/api/report/distribution/proposal-incoming",
        params={"date_from": date_from, "date_to": date_to, "mustahiq_id": mustahiq_id, "product_group_id": product_group_id, "page": page, "limit": limit}
    )
    return response.json()

@router.get("/report/proposal-incoming/export")
async def export_proposal_incoming(
    date_from: str,
    date_to: str,
    mustahiq_id: int = None,
    product_group_id: int = None,
    session: Session = Depends(require_menu("distribution.report.proposal-incoming")),
    report_client: httpx.AsyncClient = Depends(get_report_client),
):
    return await stream_report_api(
        report_client,
        "/api/report/distribution/proposal-incoming/export",
        params={"date_from": date_from, "date_to": date_to, "mustahiq_id": mustahiq_id, "product_group_id": product_group_id},
        filename="Laporan_Proposal_Masuk.xlsx"
    )
```

### Checklist

- [ ] **apps_zakat/bff-api/app/routers/distribution.py**
  - [ ] Endpoint 1: GET /report/proposal-incoming + /export (2 routes)
  - [ ] Endpoint 2: GET /report/mustahiq-list + /export (2 routes)
  - [ ] Endpoint 3: GET /report/realization-regular + /export (2 routes)
  - [ ] Endpoint 4: GET /report/realization-non-regular + /export (2 routes) + _resolve_branch()
  - [ ] Endpoint 5: GET /report/realization-receivable + /export (2 routes)
  - [ ] Endpoint 6: GET /report/realization-return + /export (2 routes)
  - [ ] Endpoint 7: GET /report/realization-by-mustahiq + /export (2 routes) + _resolve_branch()
  - [ ] All routes decorated dengan `require_menu("distribution.report.*")` sesuai menu_key

- [ ] **apps_zakat/bff-api/app/main.py** — register distribution router
  - `from app.routers.distribution import router as distribution_router`
  - `app.include_router(distribution_router, prefix="/api")`

**Quality Gates**:
- [ ] All menu decorators applied correctly
- [ ] Branch code injected untuk endpoints 4 & 7 (via _resolve_branch)
- [ ] stream_report_api used untuk all export routes
- [ ] Content-Disposition filename correct per laporan

---

## Layer 4 — Seed (nuwis-seed-gen, model: haiku)

**Duration**: 1 hari (SQL seed: 7 menu + role_menu assignments)

### File: infra/db/migrations/seed/seed-menu-and-rolemenu-distribution-reports.sql

```sql
-- Seed menu rows (isf_auth_zakat.menu)
INSERT INTO menu (menu_key, menu_label, menu_icon, menu_order, menu_level, menu_parent, menu_path) VALUES
('distribution.report.proposal-incoming', 'Laporan Proposal Masuk', 'FileText', 1, 3, 'distribution.report', '/distribution/report/proposal-incoming'),
('distribution.report.mustahiq-list', 'Laporan Daftar Mustahiq', 'FileText', 2, 3, 'distribution.report', '/distribution/report/mustahiq-list'),
('distribution.report.realization-regular', 'Laporan Program Penyaluran Rutin', 'FileText', 3, 3, 'distribution.report', '/distribution/report/realization-regular'),
('distribution.report.realization-non-regular', 'Laporan Program Penyaluran Non Rutin', 'FileText', 4, 3, 'distribution.report', '/distribution/report/realization-non-regular'),
('distribution.report.realization-receivable', 'Laporan Piutang Realisasi Penyaluran', 'FileText', 5, 3, 'distribution.report', '/distribution/report/realization-receivable'),
('distribution.report.realization-return', 'Laporan Pengembalian Realisasi', 'FileText', 6, 3, 'distribution.report', '/distribution/report/realization-return'),
('distribution.report.realization-by-mustahiq', 'Laporan Penyaluran Per Mustahiq', 'FileText', 7, 3, 'distribution.report', '/distribution/report/realization-by-mustahiq');

-- Seed role_menu assignments
-- DIST, SPVDIST untuk semua 7 laporan
-- QAC (jika confirmed) atau fallback ke DIST/SPVDIST
INSERT INTO role_menu (role_id, menu_key) 
SELECT r.role_id, m.menu_key 
FROM role r, menu m
WHERE r.role_name IN ('DIST', 'SPVDIST')
AND m.menu_key LIKE 'distribution.report.%';

-- [CONDITIONAL] Jika QAC confirmed sebagai role baru:
-- INSERT INTO role_menu (role_id, menu_key) SELECT r.role_id, m.menu_key FROM role r, menu m WHERE r.role_name='QAC' AND m.menu_key LIKE 'distribution.report.%';

-- [CONDITIONAL] Jika endpoint 7 (realization-by-mustahiq) butuh role eksklusif:
-- INSERT INTO role_menu (role_id, menu_key) SELECT r.role_id, 'distribution.report.realization-by-mustahiq' FROM role r WHERE r.role_name='ADM';
```

### Checklist

- [ ] Create file: `infra/db/migrations/seed/seed-menu-and-rolemenu-distribution-reports.sql`

- [ ] Verify 3-way consistency:
  - [ ] Menu keys di seed SQL match specs.md endpoints
  - [ ] Menu keys match MENU_KEYS di shared/constants/menu-keys.ts (akan ditambah di layer 5)
  - [ ] Route meta.menu_key di router/index.ts match (akan ditambah di layer 5)

- [ ] **Apply seed**:
  ```bash
  psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-and-rolemenu-distribution-reports.sql
  ```

---

## Layer 5 — UI (nuwis-ui-builder, model: haiku)

**Duration**: 4–6 hari (7 laporan pages, masing-masing dengan filter + pagination + table + export button)

### File Structure

```
apps_zakat/web-vue/src/modules/distribution/
├── views/reports/
│   ├── LaporanProposalIncomingView.vue
│   ├── LaporanMustahiqListView.vue
│   ├── LaporanRealizationRegularView.vue
│   ├── LaporanRealizationNonRegularView.vue
│   ├── LaporanRealizationReceivableView.vue
│   ├── LaporanRealizationReturnView.vue
│   └── LaporanRealizationByMustahiqView.vue
├── routes.ts                  ← add 7 new routes (setiap dengan meta.menu_key)
└── menu.ts                    ← add 7 menu items ke group "Laporan" (level 3)
```

### Checklist

- [ ] **shared/constants/menu-keys.ts** — add 7 menu keys
  ```ts
  export const MENU_KEYS = {
    // ... existing ...
    distribution: {
      report: {
        'proposal-incoming': 'distribution.report.proposal-incoming',
        'mustahiq-list': 'distribution.report.mustahiq-list',
        'realization-regular': 'distribution.report.realization-regular',
        'realization-non-regular': 'distribution.report.realization-non-regular',
        'realization-receivable': 'distribution.report.realization-receivable',
        'realization-return': 'distribution.report.realization-return',
        'realization-by-mustahiq': 'distribution.report.realization-by-mustahiq',
      },
    },
  }
  ```

- [ ] **apps_zakat/web-vue/src/modules/distribution/routes.ts** — add 7 routes

- [ ] **apps_zakat/web-vue/src/modules/distribution/menu.ts** — add group "Laporan" dengan 7 children

- [ ] **LaporanProposalIncomingView.vue**
  - Filter: date_from (DateField, default awal bulan), date_to (DateField, default hari ini), mustahiq_id (SearchSelect opt), product_group_id (SearchSelect opt)
  - Button "Tampilkan" → fetch data (loading state), "Export" (disabled until data exists)
  - Table: pagination di atas (Paginator), 25 rows, kolom [Nama Mustahiq, Jenis Program, No Proposal, ...]
  - Tanggal display: gunakan dmy() dari shared/utils/date.ts

- [ ] **LaporanMustahiqListView.vue**
  - Filter: mustahiq_type (select Semua/Individu/Lembaga, default Semua), product_id (SearchSelect opt), date_start_from (DateField opt), date_start_to (DateField opt)
  - Button "Tampilkan", "Export", pagination 25
  - Table cols: [ID, Nama, Golongan, Ashnaf, Alamat, Telepon, Nama Kontak, ...]

- [ ] **LaporanRealizationRegularView.vue**
  - Filter: date_from (DateField required, default today), date_to (DateField required, default today)
  - Pagination, export 3-sheet xlsx
  - Table cols: [No, Jenis Program, Nama Program, Tgl Realisasi, Nama Mustahiq, ...]

- [ ] **LaporanRealizationNonRegularView.vue**
  - Filter: date_from, date_to, amount_min (Input number default 0), amount_max (Input number default 3000000)
  - Client validation: amount_min <= amount_max before fetch
  - Pagination, export 3-sheet xlsx

- [ ] **LaporanRealizationReceivableView.vue**
  - Filter: date_from (default today), date_to (default today)
  - Computed column di frontend: sisa_piutang = realization_amount - report_amount
  - Table cols: [No, Tgl Realisasi, No Memo, Jenis (Rutin/Non Rutin), ...]
  - Status badge: "Belum/Sudah/Batal" untuk report_detail_status

- [ ] **LaporanRealizationReturnView.vue**
  - Filter: date_from (default today), date_to (default today)
  - Table: nested costs di expandable row (DataTable expandRow) atau flat rows dengan rowspan
  - Table cols: [No, Tgl Pengembalian, Nominal Realisasi, Nominal Kembali, Rincian Biaya, No Memo, Keterangan, Input Oleh]

- [ ] **LaporanRealizationByMustahiqView.vue**
  - Filter: date_from (default today), date_to (default today)
  - Table: grouped by customer_name (bisa pakai DataTable rowGroupMode atau sorted + visual grouping)
  - Sub-total per mustahiq (realization_amount aggregate)
  - Pagination, export 2-sheet xlsx

**Common Pattern untuk semua 7 pages**:
- `<script setup lang="ts">` dengan Composition API
- `useFetch(fetcher)` composable untuk async load (tidak auto-load saat mount — Rule 7)
- DateField.vue untuk semua date inputs (v-model = ISO string)
- SearchSelect.vue untuk long dropdowns (mustahiq, program, productgroup)
- Standalone Paginator di atas DataTable (bukan built-in :paginator)
- Error handling: error toast on fail, finally reset loading
- Export button: use `shared/api/client.ts` + `downloadBlob` dari shared/utils/download.ts

---

## Layer 6 — Testing (nuwis-test-gen, model: haiku)

**Duration**: 2–3 hari (E2E smoke test + unit tests)

### E2E Script: testing/e2e-laporan-penyaluran-zakat.sh

```bash
#!/bin/bash
set -e

# Smoke test untuk 7 laporan penyaluran zakat
# Target: localhost ports 5173 (web-vue), 7000 (bff-api), 8010 (report-api)

echo "[E2E] Laporan Penyaluran Zakat — Smoke Test"

# Setup: login user + get session token
TOKEN=$(curl -s -X POST http://localhost:7000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}' | jq -r '.data.access_token')

echo "[OK] Logged in as HADI, token: ${TOKEN:0:10}..."

# Test 1: Laporan Proposal Masuk
echo "[Test 1] GET /api/report/distribution/proposal-incoming"
curl -s -X GET "http://localhost:7000/api/report/distribution/proposal-incoming?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination.total' | grep -q '[0-9]' && echo "[OK] Proposal Masuk list OK" || echo "[FAIL] Proposal Masuk list"

# Test 2: Laporan Daftar Mustahiq
echo "[Test 2] GET /api/report/distribution/mustahiq-list"
curl -s -X GET "http://localhost:7000/api/report/distribution/mustahiq-list" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination.total' | grep -q '[0-9]' && echo "[OK] Mustahiq List OK" || echo "[FAIL] Mustahiq List"

# Test 3: Laporan Realisasi Rutin
echo "[Test 3] GET /api/report/distribution/realization-regular"
curl -s -X GET "http://localhost:7000/api/report/distribution/realization-regular?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination.total' | grep -q '[0-9]' && echo "[OK] Realisasi Rutin OK" || echo "[FAIL] Realisasi Rutin"

# Test 4: Laporan Realisasi Non Rutin
echo "[Test 4] GET /api/report/distribution/realization-non-regular"
curl -s -X GET "http://localhost:7000/api/report/distribution/realization-non-regular?date_from=2026-01-01&date_to=2026-06-30&amount_min=0&amount_max=3000000" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination.total' | grep -q '[0-9]' && echo "[OK] Realisasi Non Rutin OK" || echo "[FAIL] Realisasi Non Rutin"

# Test 5: Laporan Piutang Realisasi
echo "[Test 5] GET /api/report/distribution/realization-receivable"
curl -s -X GET "http://localhost:7000/api/report/distribution/realization-receivable?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination' | grep -q 'page' && echo "[OK] Piutang Realisasi OK" || echo "[FAIL] Piutang Realisasi"

# Test 6: Laporan Pengembalian Realisasi
echo "[Test 6] GET /api/report/distribution/realization-return"
curl -s -X GET "http://localhost:7000/api/report/distribution/realization-return?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination' | grep -q 'page' && echo "[OK] Pengembalian Realisasi OK" || echo "[FAIL] Pengembalian Realisasi"

# Test 7: Laporan Penyaluran Per Mustahiq
echo "[Test 7] GET /api/report/distribution/realization-by-mustahiq"
curl -s -X GET "http://localhost:7000/api/report/distribution/realization-by-mustahiq?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" | jq '.pagination' | grep -q 'page' && echo "[OK] Penyaluran Per Mustahiq OK" || echo "[FAIL] Penyaluran Per Mustahiq"

# Test 8: Export — Proposal Masuk (xlsx)
echo "[Test 8] GET /api/report/distribution/proposal-incoming/export"
XLSX=$(curl -s -X GET "http://localhost:7000/api/report/distribution/proposal-incoming/export?date_from=2026-01-01&date_to=2026-06-30" \
  -H "Authorization: Bearer $TOKEN" -o /tmp/laporan_proposal.xlsx && file /tmp/laporan_proposal.xlsx)
echo "$XLSX" | grep -q 'XLSX' && echo "[OK] Export Proposal Masuk OK" || echo "[FAIL] Export Proposal Masuk"

# Test 9: Export — Mustahiq List (xlsx)
echo "[Test 9] GET /api/report/distribution/mustahiq-list/export"
curl -s -X GET "http://localhost:7000/api/report/distribution/mustahiq-list/export" \
  -H "Authorization: Bearer $TOKEN" -o /tmp/laporan_mustahiq.xlsx && \
  file /tmp/laporan_mustahiq.xlsx | grep -q 'XLSX' && echo "[OK] Export Mustahiq List OK" || echo "[FAIL] Export Mustahiq List"

echo "[SUMMARY] Smoke test completed. Check logs above for any [FAIL] marks."
```

### Checklist

- [ ] Create file: `testing/e2e-laporan-penyaluran-zakat.sh`
- [ ] Make executable: `chmod +x testing/e2e-laporan-penyaluran-zakat.sh`

- [ ] Python unit tests (optional, untuk query logic kompleks):
  - [ ] `apps_zakat/api-python/tests/test_distribution_reports.py` (jika ada query logic di service.py yang non-trivial)
    - Test ProposalIncomingService.query() dengan berbagai filter
    - Test RealizationRegularService.query() dengan programtype discriminator
    - Test RealizationNonRegularService.query() dengan amount_min/max validation
    - Test RealizationReceivableService.query() dengan statusreceivables='Y' filter
    - Etc.

- [ ] Run E2E:
  ```bash
  cd infra && podman-compose -f docker-compose.zakat.yml up -d
  bash testing/e2e-laporan-penyaluran-zakat.sh
  ```

---

## Verifikasi (End-to-End)

Setelah semua layer selesai:

```bash
# 1. Restart containers (DB migrations applied, seed loaded, services rebuilt)
cd infra
podman-compose -f docker-compose.zakat.yml down
podman-compose -f docker-compose.zakat.yml up -d
podman-compose -f docker-compose.zakat.yml logs -f  # wait until all healthy

# 2. Run E2E smoke test
bash testing/e2e-laporan-penyaluran-zakat.sh

# 3. Manual verification di browser
# - Login: http://localhost:5173 → HADI / test1234
# - Navigate: Sidebar → Distribution → Laporan → [pilih salah satu]
# - Fill filter, klik "Tampilkan"
# - Verify: data muncul, pagination works, "Export" button enabled
# - Click "Export" → download xlsx, verify file valid
# - Repeat untuk 7 laporan semuanya

# 4. Excel validation (spot-check)
# - Verify sheet names match spec (Detail, Rekap, RekapAnggaran)
# - Verify column headers match (no legacy DB column names)
# - Verify tanggal format DD-MM-YYYY (bukan ISO)
# - Verify angka nominal formatted dengan separator (jika diaplikasikan)
```

### Gates

- [ ] All 7 endpoints return JSON with correct pagination shape
- [ ] All 7 export endpoints return valid xlsx with correct filename
- [ ] All 7 pages load dalam browser tanpa error
- [ ] All filters work (date range, dropdowns, amount range)
- [ ] Menu keys propagated correctly (can access via sidebar based on role)
- [ ] Discriminators working: programtype='R'/'N', statusreceivables='Y', returndate filtering
- [ ] Branch code filtering works untuk endpoints 4 & 7 (single-branch users see correct data only)
- [ ] Role DIST/SPVDIST can access all 7 laporan
- [ ] [CONDITIONAL] Role QAC (if confirmed) can access 6 laporan
- [ ] [CONDITIONAL] Endpoint 7 access control per confirmed AllowedGroups

---

## Timeline Summary

| Layer | Duration | Owner | Dependencies |
|---|---|---|---|
| Layer 0 (Konfirmasi) | 1–2 hari | nuwis-architect | — |
| Layer 1 (DWH) | 3–5 hari | nuwis-db-migrator (model: OPUS) | Layer 0 approved |
| Layer 2 (report-api) | 5–7 hari | nuwis-python-builder (model: haiku) | Layer 1 applied |
| Layer 3 (BFF) | 2–3 hari | nuwis-bff-builder (model: haiku) | Layer 2 tested |
| Layer 4 (Seed) | 1 hari | nuwis-seed-gen (model: haiku) | Layer 0 approved, Layer 3 code ready |
| Layer 5 (UI) | 4–6 hari | nuwis-ui-builder (model: haiku) | Layer 3 endpoints tested, Layer 4 seed applied |
| Layer 6 (Testing) | 2–3 hari | nuwis-test-gen (model: haiku) | All layers complete |
| **Total** | **17–27 hari** | — | Sequential + some parallelization |

**Critical Path**: Layer 0 → Layer 1 (DWH applied) → Layer 2 (report-api tested) → Layer 3 (BFF) → [Parallel: Layer 4 seed + Layer 5 UI] → Layer 6 Testing
