# Laporan Transaksi Kas/Bank Harian (fDailyCash, zakat)

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem / Goal

Replikasi legacy `fDailyCash` ("Transaksi kas / bank harian"): mutasi **satu
rekening kas/bank** dalam rentang tanggal dengan **Saldo Awal → running balance
per baris → Saldo Akhir** + ringkasan (Saldo Awal, Total Debet, Total Kredit,
Saldo Akhir). Bagian dari seri laporan kas: berikutnya fSummaryCash,
fSummaryCashMonthly.

Fase view-based (`dwh`), reuse infra report (report-api modul report, BFF
`_resolve_branch`/`require_menu`/streaming, menu subgrup "Laporan").

## Keputusan (brainstorming)

- **Single-account mode** dulu (pilih 1 rekening). Mode "Semua Kas" = fase berikutnya.
- **Saldo awal = akumulasi mutasi** sebelum tanggal awal (Σ D − C). `dailybalancecash`
  kosong → tidak dipakai. Caveat: asumsi inception 0; bisa diakurasi via tabel balance saat ETL.
- **Export sync** (async = fase 2).
- **Filter cabang + RBAC** (single terkunci primary; all boleh pilih).
- **Scope**: zakat dulu.

## Sumber data

`transaction.accounttransactionitem a` + `transactionitem i` + `transaction t`,
filter `a.accountno`, `t.actualdate` rentang. Drop join `transactionbatch` legacy
(BatchNo tak ditampilkan). Rekening kas dari `transaction.cashaccountall`.

## Komponen

### A. View `dwh.v_cash_mutation` (mziss_laz)

Grain = transactionitem per rekening. Migrasi `infra/db/migrations/dwh/v_cash_mutation-zakat.sql`.

| Kolom | Asal |
|---|---|
| `account_no` | `a.accountno` — **filter** |
| `actualdate` | `t.actualdate` — **filter** |
| `transactionid`, `transactionno` | `t.*` |
| `mutationtype` | `i.mutationtype` (D/C) |
| `amount` | `i.amount` |
| `reference_no` | `t.referenceno` |
| `description` | `t.description` |
| `auth_status` | `t.authstatus` |
| `inputer` | `t.inputer` |
| `transactionitemid` | `i.transactionitemid` (tie-break order) |

Sumber: `accounttransactionitem a JOIN transactionitem i ON a.transactionitemid=i.transactionitemid
JOIN transaction t ON i.transactionid=t.transactionid`. (Running balance & saldo awal
dihitung di report-api, bukan di view.)

### B. report-api — modul report (tambah)

Baca via pool dwh read-only. `CAP=50_000`.
- `service.py`:
  - `list_cash_accounts(branch)` → `cashaccountall` (accountno, accountname, type, branch, status='A').
  - `cash_begin_balance(account, begin)` → `Σ CASE D +amount C -amount FROM v_cash_mutation WHERE account_no=$ AND actualdate < $begin`.
  - `cash_mutation_sums(account, begin, end)` → total debit, total credit dalam rentang.
  - `cash_mutation_page(account, begin, end, page, page_size)`:
    - saldo awal + sums + saldo akhir (= awal + debit − credit);
    - rows page (ORDER actualdate, transactionitemid) + **running balance** dihitung
      atas seluruh rows sampai akhir page (offset dihitung dari saldo awal +
      net mutasi baris-baris sebelum offset);
    - return `{account_no, begin_balance, total_debit, total_credit, end_balance,
      rows:[{...,balance}], total, capped, page, page_size}`.
    - Running balance lintas-halaman: hitung saldo pada awal page =
      saldo_awal + Σ(net) baris 0..offset-1 (query agregat), lalu akumulasi per row di page.
  - `cash_mutation_rows(account, begin, end)` → semua rows (LIMIT CAP) utk export (running balance penuh).
- `router.py`:
  - `GET /report/cash-accounts?branch=`
  - `GET /report/cash-mutation?account=&begin=&end=&page=&page_size=`
  - `GET /report/cash-mutation/export.xlsx?account=&begin=&end=`
- `export.py`: `build_cash_mutation_xlsx(summary, rows, account_label, period_label)` —
  header ringkasan (Saldo Awal/Debet/Kredit/Saldo Akhir) + tabel mutasi + saldo berjalan +
  status (SUDAH/BELUM OTORISASI). Nominal `#,##0.00`.

### C. BFF — `routers/report.py`

- `GET /report/cash-accounts` — `require_menu('keuangan.report.cash_daily')` →
  resolve branch (gunakan resolved branch sebagai param ke report-api) → proxy.
- `GET /report/cash-mutation` & `/export.xlsx` — require_menu + (account wajib;
  branch RBAC tetap via cash-accounts scoping). Account tidak perlu re-validasi branch
  karena daftar account sudah discoping; tapi tetap aman (read-only).

### D. Frontend — `LaporanCashDailyPage.vue`

Filter: **Cabang** (dropdown, default primary; "Semua cabang" TIDAK relevan di sini —
single-account butuh cabang konkret, jadi untuk user `all` pilih cabang dulu; untuk
`single` terkunci primary) → **Rekening** (dependent dropdown, load `/cash-accounts`) →
Dari/Sampai (default bulan berjalan). Kartu ringkasan (Saldo Awal/Debet/Kredit/Saldo Akhir).
Tabel: Tgl, No Transaksi, D/K, Nominal, Saldo, Keterangan, Ref, Inputer, Status.
Export `cashdaily-YYYYMMDD-HHMMSS.xlsx`. Menu **"Transaksi kas / bank harian"**, key
`keuangan.report.cash_daily`, sidebar Laporan, route `/keuangan/laporan/kas-harian`.

> Catatan cabang: untuk single-account, "Semua cabang" tidak berlaku (perlu 1 rekening).
> User `all` memilih cabang dari dropdown (semua cabang), lalu rekening. User `single`
> cabang terkunci ke primary.

### E. Seed (isf_auth_zakat)

Menu `keuangan.report.cash_daily` ("Transaksi kas / bank harian", route
`/keuangan/laporan/kas-harian`, sort 142) + role_menu ke **ADM, KEU, ACC, SPVKEU,
QAC, SPVACC** (sesuai AllowedGroups legacy `TR0027`). Apply isf_auth_zakat.
E2E: set dev-password user role-finance (mis. UKTA) — HADI (DIST/SPVDIST) tak punya akses.

## Error handling

- report-api: `503 DB_UNAVAILABLE`; `422 REPORT_TOO_LARGE` (rows > CAP); account wajib → 422 bila kosong.
- BFF: `401`/`403` (require_menu / branch); passthrough.

## Testing / verification

1. View SQL + sanity (mutasi satu account+periode).
2. report-api: `/cash-accounts`, `/cash-mutation` (cek saldo awal/akhir + running balance benar:
   saldo akhir = awal + debet − kredit; row terakhir = saldo akhir), `/export.xlsx`.
3. BFF authenticated (user role-finance): preview + export.
4. Browser drive: menu Keuangan ▸ Laporan ▸ Transaksi kas/bank harian → pilih cabang+rekening+periode →
   ringkasan + tabel + Export.

## Di luar scope

- Mode "Semua Kas" (all-cash) — fase berikutnya.
- Async export (fase 2).
- Akurasi saldo awal via tabel balance/ETL.
- Wakaf.
