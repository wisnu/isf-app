# Monitoring Saldo Kas/Bank Bulanan (fSummaryCashMonthly, zakat)

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem / Goal

Replikasi legacy `fSummaryCashMonthly` ("Monitoring Saldo Kas / Bank Bulanan"):
matriks **per rekening kas/bank × 12 bulan** — saldo **kumulatif akhir tiap bulan**
dalam satu tahun. Dikelompokkan per tipe rekening (BANK / KAS CABANG / PETTY CASH)
dengan total per-tipe per bulan. Parameter = **tahun** + cabang. Laporan terakhir
seri kas (setelah fDailyCash, fSummaryCash).

Fase view-based, reuse infra report.

## Keputusan (brainstorming)

- Matriks per akun × 12 bulan; saldo kumulatif akhir bulan; group per tipe + total tipe.
- Akhir bulan = **tanggal kalender terakhir** tiap bulan (legacy pakai `accountingday`
  fiskal — disederhanakan; caveat). Saldo kumulatif sejak inception (konsisten cash report).
- Tipe rekening: `cashaccounttype` A=BANK, R=KAS CABANG, P=PETTY CASH.
- Filter cabang konkret + RBAC. Export sync. Semua IDR. Zakat dulu.

## Sumber data

Extend `dwh.v_cash_summary_src` (sudah ada) dgn kolom `account_type`
(`cashaccountall.cashaccounttype`). Filter `branch_code` (=i.branchcode), `actualdate`.

## Komponen

### A. View — `dwh.v_cash_summary_src` (extend)

Tambah kolom `account_type` = `ca.cashaccounttype`. Migrasi: update file
`infra/db/migrations/dwh/v_cash_summary_src-zakat.sql` (CREATE OR REPLACE) + re-apply.
Dipakai bersama fSummaryCash (rekap-kas) — kolom tambahan tidak merusak.

### B. report-api — `cash_monthly(branch, year)`

- Hitung 12 tanggal akhir-bulan kalender utk `year` (Python).
- Query agregat: per akun, 12 kolom `balance_m = SUM(CASE WHEN actualdate <= monthend_m
  THEN (CASE WHEN mutationtype='D' THEN amount ELSE -amount END) ELSE 0 END)`,
  filter `branch_code=$1 AND actualdate <= 'year-12-31'`, `GROUP BY account_no,
  account_name, account_type` ORDER `account_type, account_no`. (month-end dates
  di-pass sebagai param $2..$13.)
- Rakit di Python: groups per `account_type` →
  `{type, type_label, rows:[{account_no, account_name, balances:[12]}], totals:[12]}`.
  `type_label`: A→BANK, R→KAS CABANG, P→PETTY CASH (else "LAINNYA"). Output bounded.
  Return `{groups, year, months:["Jan".."Des"]}`.
- `router.py`: `GET /report/cash-monthly?branch=&year=` + `/export.xlsx`
  (matriks: header Rekening + 12 bulan; baris akun + baris Total <tipe>).
- `export.py`: `build_cash_monthly_xlsx(payload, branch_label, year)`.

### C. BFF — `routers/report.py`

`/report/cash-monthly` + `/export.xlsx` + `/cash-monthly/branches` dgn
`require_menu('keuangan.report.cash_monthly')` + `_resolve_branch` (cabang konkret;
None → 400 BRANCH_REQUIRED). `year` di-passthrough (int).

### D. Frontend — `LaporanCashMonthlyPage.vue`

Filter: Cabang (dropdown/locked) + **Tahun** (dropdown: tahun berjalan s/d −4).
Tabel lebar (scroll horizontal): kolom `Rekening | Jan | … | Des`; baris akun
dikelompokkan per tipe (sub-header tipe) + baris **Total <tipe>** per bulan.
Export `cashmonthly-YYYYMMDD-HHMMSS.xlsx`. Menu **"Monitoring Saldo Kas/Bank Bulanan"**,
key `keuangan.report.cash_monthly`, sidebar Laporan, route `/keuangan/laporan/saldo-bulanan`.
Branch dropdown via `/report/cash-monthly/branches`.

### E. Seed (isf_auth_zakat)

Menu `keuangan.report.cash_monthly` ("Monitoring Saldo Kas/Bank Bulanan", route
`/keuangan/laporan/saldo-bulanan`, sort 144) + role_menu ke **ADM, KEU, ACC, SPVKEU,
QAC, SPVACC** (AllowedGroups legacy TR0028A). Apply isf_auth_zakat.

## Error handling

- report-api: `503 DB_UNAVAILABLE`.
- BFF: `401`/`403` (require_menu / branch), `400 BRANCH_REQUIRED`.

## Testing / verification

1. View re-apply + sanity (account_type ada).
2. report-api `/cash-monthly` (cek balance_m monoton untuk akun aktif: saldo Des =
   saldo kumulatif akhir tahun; total tipe = Σ akun tipe per bulan), `/export.xlsx`.
3. BFF authenticated (RAIS / finance) + branch RBAC.
4. Browser drive: menu ▸ Monitoring Saldo Kas/Bank Bulanan → pilih tahun+cabang →
   matriks 12 bulan + total tipe + export.

## Di luar scope

- Periode fiskal (`accountingday`) — pakai kalender.
- Konversi multi-valuta (semua IDR).
- Async export; wakaf.
