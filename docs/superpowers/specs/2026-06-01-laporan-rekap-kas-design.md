# Rekapitulasi Transaksi Kas/Bank (fSummaryCash, zakat)

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem / Goal

Replikasi legacy `fSummaryCash` ("Rekapitulasi transaksi kas / bank"): ringkasan
**per rekening kas/bank** dalam satu cabang — 1 baris per rekening (Saldo Awal,
Debet, Kredit, Total=D−K, Saldo Akhir), dikelompokkan per valuta + subtotal valuta
+ grand total. Tanpa detail transaksi. Bagian seri laporan kas (setelah fDailyCash).

Fase view-based, reuse infra report (report-api modul report, BFF
`_resolve_branch`/`require_menu`/streaming, menu Laporan).

## Keputusan (brainstorming)

- Rekap **per-akun**, group per valuta + subtotal + grand total. **Tanpa pagination** (output bounded ~jumlah rekening).
- Saldo awal = akumulasi mutasi sebelum begin (konsisten dgn cash-daily).
- Semua rekening IDR → grand total = jumlah langsung; konversi rate multi-valuta = nanti.
- Filter cabang konkret + RBAC (single→primary; all→pilih cabang).
- Export sync. Zakat dulu.

## Sumber data

`accounttransactionitem a → transactionitem i → transaction t` + `cashaccountall ca`
(akun kas: accountname, currencycode, branchcode). Filter `i.branchcode = branch`
(mengikuti legacy `i.BranchCode`), `t.actualdate <= end`. Semua cash account = IDR (45 akun).

## Komponen

### A. View `dwh.v_cash_summary_src` (mziss_laz)

Migrasi `infra/db/migrations/dwh/v_cash_summary_src-zakat.sql`. Kolom:
`account_no`, `account_name`, `currency_code`, `branch_code` (=i.branchcode),
`actualdate`, `mutationtype`, `amount`.
Sumber: `accounttransactionitem JOIN transactionitem ON transactionitemid
JOIN transaction ON transactionid JOIN cashaccountall ca ON ca.accountno=a.accountno`.
(Join cashaccountall membatasi ke rekening kas + memberi nama/valuta.)

### B. report-api — modul report (tambah)

Baca via pool dwh read-only.
- `service.py`:
  - `cash_summary(branch, begin, end)`:
    ```sql
    SELECT account_no, account_name, currency_code,
      SUM(CASE WHEN mutationtype='D' AND actualdate>=$begin THEN amount ELSE 0 END)::float8 AS debit,
      SUM(CASE WHEN mutationtype='C' AND actualdate>=$begin THEN amount ELSE 0 END)::float8 AS credit,
      SUM(CASE WHEN actualdate<$begin THEN (CASE WHEN mutationtype='D' THEN amount ELSE -amount END) ELSE 0 END)::float8 AS begin_balance
    FROM dwh.v_cash_summary_src
    WHERE branch_code=$branch AND actualdate < ($end::date + 1)
    GROUP BY account_no, account_name, currency_code
    ORDER BY currency_code, account_no
    ```
    Lalu di Python: hitung `total=debit-credit`, `end_balance=begin+debit-credit`;
    group per `currency_code` → `{currency, rows:[...], subtotal:{begin,debit,credit,total,end}}`;
    grand total = Σ semua (IDR → langsung). Return
    `{groups:[...], grand:{begin_balance,total_debit,total_credit,total_end}, period}`.
  - (Filter hanya akun yang punya mutasi dalam window; akun tanpa mutasi & saldo 0 tak muncul — sesuai legacy.)
- `router.py`:
  - `GET /report/cash-summary?branch=&begin=&end=` → ok(payload).
  - `GET /report/cash-summary/export.xlsx?branch=&begin=&end=` → xlsx (grand total + tabel per valuta + subtotal).
- `export.py`: `build_cash_summary_xlsx(payload, branch_label, period_label)`.

### C. BFF — `routers/report.py`

`/report/cash-summary` + `/export.xlsx` + `/cash-summary/branches` dengan
`require_menu('keuangan.report.cash_summary')` + `_resolve_branch` (butuh cabang konkret;
None → 400 BRANCH_REQUIRED, sama pola cash-accounts).

### D. Frontend — `LaporanCashSummaryPage.vue`

Filter: Cabang (dropdown/locked sesuai branch_access) + Dari/Sampai (default bulan berjalan).
Kartu grand total (Saldo Awal/Debet/Kredit/Saldo Akhir). Tabel: untuk tiap valuta →
baris akun (Rekening, Saldo Awal, Debet, Kredit, Total, Saldo Akhir) + baris subtotal valuta.
Export `cashsummary-YYYYMMDD-HHMMSS.xlsx`. Menu **"Rekapitulasi transaksi kas/bank"**,
key `keuangan.report.cash_summary`, sidebar Laporan, route `/keuangan/laporan/rekap-kas`.
Branch dropdown via `/report/cash-summary/branches`.

### E. Seed (isf_auth_zakat)

Menu `keuangan.report.cash_summary` ("Rekapitulasi transaksi kas/bank", route
`/keuangan/laporan/rekap-kas`, sort 143) + role_menu ke **ADM, KEU, ACC, SPVKEU,
QAC, SPVACC** (AllowedGroups legacy TR0028). Apply isf_auth_zakat.

## Error handling

- report-api: `503 DB_UNAVAILABLE`.
- BFF: `401`/`403` (require_menu / branch), `400 BRANCH_REQUIRED` (cabang wajib).

## Testing / verification

1. View SQL + sanity.
2. report-api `/cash-summary` (cek per-akun begin/debit/credit/end + subtotal + grand;
   end_balance = begin + debit − credit; grand = Σ akun), `/export.xlsx`.
3. BFF authenticated (RAIS / finance), branch RBAC.
4. Browser drive: menu ▸ Rekapitulasi transaksi kas/bank → grand cards + tabel per valuta + subtotal + export.

## Di luar scope

- Konversi rate multi-valuta (semua IDR sekarang).
- Async export (fase 2); wakaf.
