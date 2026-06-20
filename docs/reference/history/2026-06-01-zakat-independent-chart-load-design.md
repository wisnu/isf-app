# Independent chart load for zakat dashboards

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem

Zakat dashboard pages (`DashboardPage`, `DashboardKeuanganPage`, `DashboardPenyaluranPage`)
fetch one combined endpoint (`/api/dashboard/keuangan` or `/penyaluran`) into a single
shared `loading` / `errorMsg` state. If that one request fails or is slow, the **entire
page** blanks — no widget renders. The `useFetch` helper exists but is unused here.

The wakaf portal already solves this: each chart owns its own request and loading/error
state, so a failed widget shows its own error while siblings render normally (the pattern
documented in `CLAUDE.md` §"Independent chart load"). This spec ports that proven wakaf
pattern into zakat.

## Goal

Each chart/KPI group on the 3 live zakat dashboard pages loads independently:
- its own HTTP request (per-widget endpoint),
- its own loading spinner and error state,
- failure or slowness of one widget does not affect the others.

## Non-goals

- **Penghimpunan page** — currently 100% static dummy data with no backend. Giving it
  independent load requires building an entire penghimpunan backend (DB views, service,
  endpoints); that is a separate feature, out of scope here. Left untouched.
- No new visual design — reuse existing widget components and layout.
- No new query logic — the api-python service helpers already exist.

## Reference implementation

Wakaf is the working reference across all four layers. Mirror it:
- `apps_wakaf/api-python/app/modules/dashboard/router.py` + `service.py`
- `apps_wakaf/bff-api/app/routers/dashboard.py`
- `apps_wakaf/web-vue/src/components/widgets/{KpiCard,TrendChart,AsnafDonut,BudgetProgress}.vue`
- `apps_wakaf/web-vue/src/pages/{DashboardPage,DashboardKeuanganPage,DashboardPenyaluranPage}.vue`

## Design

### 1. api-python — `apps_zakat/api-python/app/modules/dashboard/`

Extract the monolithic `get_keuangan` / `get_penyaluran` composers into per-widget service
functions that reuse the **existing** helpers (`_sum_fund`, `_sum_dist`, `_saldo_total`,
`_otorisasi_pending`, `_trend_6bulan`, `_asnaf_dist`, `_anggaran_list`, `_rekening_list`,
`_memo_terbaru`, `_mustahiq_count`).

New endpoints (route + thin service fn each), matching wakaf:

| Endpoint | Returns |
|---|---|
| `/keuangan/kpis` | `{ period, kpis: {penerimaan, penyaluran, saldo, otorisasi_pending} }` |
| `/keuangan/trend` | `{ trend: TrendPoint[] }` |
| `/keuangan/asnaf` | `{ asnaf: AsnafItem2[] }` |
| `/keuangan/anggaran` | `{ anggaran: AnggaranItem[] }` |
| `/keuangan/rekening` | `{ rekening: RekeningItem[] }` |
| `/penyaluran/kpis` | `{ period, kpis: {penyaluran, mustahiq, otorisasi_pending} }` |
| `/penyaluran/anggaran` | `{ anggaran: AnggaranItem[] }` |
| `/penyaluran/memo` | `{ memo_terbaru: MemoItem[] }` |

Each returns 503 `DB_UNAVAILABLE` when `ping()` is false (same as today).

**Back-compat:** keep the existing combined `/keuangan` and `/penyaluran` endpoints.
Zero risk, lets pages migrate independently. Remove later if desired (not in this scope).

### 2. BFF — `apps_zakat/bff-api/app/routers/dashboard.py`

Add one auth-gated proxy route per new endpoint, copying wakaf's route bodies
(`current_user_id_or_401` → `get_api_python(...)` → passthrough JSON + status).

### 3. Widgets — `apps_zakat/web-vue/src/components/widgets/`

Add props mirroring wakaf:
- `KpiCard`, `TrendChart`, `AsnafDonut`: add `loading`, `error`, `error-message`.
- `BudgetProgress`: already has `loading`; add `error` / `error-message`.

Each widget renders its own spinner when `loading`, its own inline error when `error`.

### 4. Pages — `DashboardPage`, `DashboardKeuanganPage`, `DashboardPenyaluranPage`

Replace single `api.get` + shared state with:
- one `useFetch<T>(() => api.get('/api/dashboard/.../widget?...'))` per widget,
- `loadAll()` firing all `.load()` calls in parallel (not awaited sequentially),
- `onMounted(loadAll)` + `watch([bulan, tahun], loadAll)`,
- pass each query's `loading` / `error` into its widget's props,
- derive header `period` from the kpis query.

## Data flow

```
web-vue page
  ├─ kpisQ      → GET bff /api/dashboard/keuangan/kpis     → api-python /dashboard/keuangan/kpis
  ├─ trendQ     → GET bff /api/dashboard/keuangan/trend    → api-python /dashboard/keuangan/trend
  ├─ asnafQ     → GET bff /api/dashboard/keuangan/asnaf     → api-python /dashboard/keuangan/asnaf
  └─ anggaranQ  → GET bff /api/dashboard/keuangan/anggaran → api-python /dashboard/keuangan/anggaran
        (all fired in parallel by loadAll(); each owns loading/error)
```

## Error handling

- api-python: 503 `DB_UNAVAILABLE` when DB down (unchanged behavior, now per-widget).
- BFF: 401 if no session, 403 if no tenant (existing helpers), else passthrough.
- web-vue: `useFetch` catches `ApiError`, sets `error` string; widget shows inline error
  and siblings keep rendering.

## Testing / verification

- Per-widget endpoint smoke test: curl each new BFF + api-python route (extend
  `testing/` with an `e2e-dashboard-zakat.sh`, or a `make`-style health check).
- Browser drive at http://localhost:5173: confirm all widgets render, and that a single
  widget can show an error in isolation (e.g. point one query at a bad param) while the
  rest render normally.
- Source is bind-mounted with reload — no image rebuild needed.
