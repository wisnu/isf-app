# Laporan List Transaksi Umum (zakat) — view-based + export Excel grouped

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem / Goal

Laporan daftar **Transaksi Umum** (general transaction / jurnal voucher,
`transactioncode='GT'`) di portal zakat — replikasi legacy
`docs/legacy-apps/core/dialogs/Report/fGeneralTransaction*`. Master-detail:
header transaksi + beberapa item (ref account, debit/kredit, nominal, budget).
Form filter cabang + rentang tanggal, tabel preview **grouped**, export Excel.

Fase view-based (`dwh`), paralel dengan Laporan Jurnal Harian
(`2026-06-01-laporan-jurnal-harian-design.md`). Reuse infrastruktur yang sudah
ada: report-api modul report, BFF `_resolve_branch`/`require_menu`/streaming,
`/report/branches`, menu subgrup "Laporan", `auth.branch_access`.

## Keputusan (brainstorming)

- **Tampilan**: **grouped** (baris header transaksi + baris item) di tabel web
  dan export, meniru Excel legacy.
- **Periode**: default **bulan berjalan** (1 s/d hari ini); rentang bebas; cap
  server **50.000 item rows**.
- **Export**: **sync** (async + menu "Hasil Laporan" = fase 2, lihat spec jurnal harian).
- **Filter cabang**: sama pola RBAC (`single` terkunci primary; `all` boleh pilih/semua).
- **Scope**: zakat dulu.

## Sumber data

Tabel live di schema `transaction.*`. Filter `t.transactioncode='GT'`,
`t.branchcode`, `t.actualdate` BETWEEN. ~9.6k transaksi GT.

## Komponen

### A. View `dwh.v_general_transaction` (mziss_laz)

Grain = `transactionitem`. Migrasi `infra/db/migrations/dwh/v_general_transaction-zakat.sql`
(CREATE OR REPLACE VIEW).

| Kolom | Asal |
|---|---|
| `branch_code` | `t.branchcode` — **filter** |
| `actualdate` | `t.actualdate` — **filter** |
| `transactionid`, `transactionno` | `t.*` |
| `transactiondate` | `t.transactiondate` |
| `header_description` | `t.description` |
| `inputer` | `t.inputer` |
| `refaccountno`, `refaccountname` | `ti.*` |
| `mutationtype` | `ti.mutationtype` (D/C) |
| `amount` | `ti.amount` |
| `item_description` | `ti.description` |
| `budget_code` | budget subquery |
| `budget_item_description` | budget subquery |

Sumber: `transaction.transaction t, transaction.transactionitem ti`
LEFT JOIN `transaction.accounttransactionitem ati`,
LEFT JOIN budget subquery (`transaction.budget/budgettransaction/budgetitem`)
ON `transactionitemid`. `WHERE t.transactionid=ti.transactionid AND t.transactioncode='GT'`.
LEFT JOIN budget meniru legacy (potensi duplikasi item bila >1 budget — diterima).

### B. report-api — modul report (tambah endpoint)

Baca via pool **dwh** read-only. `CAP = 50_000` (reuse).
- `service.py`:
  - `general_transaction_count(branch, begin, end)` → `count(DISTINCT transactionid)`.
  - `general_transaction_page(branch, begin, end, page, page_size)`:
    1. page header transaksi (`GROUP BY transactionid, transactionno, ...`
       ORDER actualdate, transactionid LIMIT/OFFSET);
    2. ambil item utk `transactionid = ANY(page_ids)`;
    3. rakit `{transactions:[{transactionno, transactiondate, actualdate,
       description, inputer, items:[{refaccountno, refaccountname, mutationtype,
       amount, item_description, budget_code, budget_item_description}]}], total, capped}`.
  - `general_transaction_rows(branch, begin, end)` → semua item rows (LIMIT CAP) utk export.
  - `_gt_where()` (begin/end → date, branch optional) — sama pola journal.
- `router.py`:
  - `GET /report/general-transaction?begin=&end=&branch=&page=&page_size=` → ok(page).
  - `GET /report/general-transaction/export.xlsx?begin=&end=&branch=` →
    count item rows > CAP → 422 `REPORT_TOO_LARGE`; else group → xlsx grouped.
- `export.py`: `build_general_transaction_xlsx(transactions, branch_label, period_label)`
  — header (judul, Cabang, Periode), lalu per transaksi: baris header (No, Tgl Transaksi,
  Tgl Aktual, Deskripsi, Inputer) + baris item (Ref Account No/Nama, D/K, Nominal,
  Keterangan, Budget). Nominal format `#,##0.00`.

### C. BFF — `routers/report.py`

Tambah (pakai ulang `_resolve_branch`, `require_menu`, `get_report_api`, `stream_report_api`):
- `GET /report/general-transaction` — `require_menu('keuangan.report.general_transaction')` + resolve branch → proxy.
- `GET /report/general-transaction/export.xlsx` — idem → stream.

### D. Frontend — `apps_zakat/web-vue/`

- `pages/keuangan/LaporanGeneralTransactionPage.vue`: filter (cabang dropdown +
  "Semua cabang" bila `branch_access==='all'`, default primary; Dari/Sampai =
  bulan berjalan), Tampilkan (load grouped, paginated per transaksi, badge capped),
  Export Excel (`downloadBlob`, fallback `generaltransaction-YYYYMMDD-HHMMSS.xlsx`).
  Tabel **grouped**: per transaksi baris header (No/Tgl/Deskripsi/Inputer) lalu
  baris item (Ref Account, D/K, Nominal, Keterangan, Budget).
- Menu registry: tambah `keuangan.report.general_transaction`.
- Sidebar grup "Laporan" → tambah item "List Transaksi Umum" (di sebelah "Jurnal Harian").
- Router: `/keuangan/laporan/transaksi-umum`, `meta.menu_key`.
- Branches endpoint dipakai ulang (`/report/journal-daily/branches`) atau endpoint
  scope umum — **gunakan `/report/journal-daily/branches`** yang sudah ada (sama
  logikanya); tidak perlu endpoint branches baru.

### E. Seed menu (isf_auth_zakat)

`seed-menu-and-rolemenu.sql`: menu `keuangan.report.general_transaction` (sort 141) +
role_menu (finance roles ADM/SPVADM/KEU/SPVKEU/ACC/SPVACC + DIST/SPVDIST utk E2E HADI).
Apply ke isf_auth_zakat.

## Data flow

```
web-vue LaporanGeneralTransactionPage
  ├─ branches → bff /api/report/journal-daily/branches (reuse)
  ├─ preview  → bff /api/report/general-transaction → report-api → dwh.v_general_transaction (grouped)
  └─ export   → bff /api/report/general-transaction/export.xlsx (stream) → report-api → openpyxl grouped
        (BFF: require_menu + _resolve_branch)
```

## Error handling

- report-api: `503 DB_UNAVAILABLE`; `422 REPORT_TOO_LARGE` (item rows > CAP).
- BFF: `401`/`403` (require_menu / `BRANCH_FORBIDDEN`); passthrough lainnya.
- Preview cap: `capped=true` bila item rows total > CAP (badge peringatan).

## Testing / verification

1. View SQL: apply + sanity (header + items satu cabang/periode).
2. report-api (:8010): `/report/general-transaction` (grouped, paginated),
   `/export.xlsx` (xlsx valid grouped).
3. BFF authenticated (HADI 'all'): preview 200 grouped, export 200 xlsx.
4. Browser drive (:5173): menu Keuangan ▸ Laporan ▸ List Transaksi Umum →
   filter, Tampilkan (tabel grouped), Export (unduh `generaltransaction-…xlsx`).

## Di luar scope

- Async export + menu "Hasil Laporan" (fase 2).
- Portal wakaf (mirror setelah zakat stabil).
- Dedup budget LEFT JOIN (meniru legacy apa adanya).
