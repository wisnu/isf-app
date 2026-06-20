# Trial Balance & Neraca (zakat) — legacy-faithful (dailybalance)

**Date:** 2026-06-01
**Status:** Approved (design)

## Goal

Implement laporan **Trial Balance** (Neraca Saldo per cabang) & **Neraca**
(Balance Sheet), faithful ke legacy:
- `dialogs/reports/fTrialBalance*` + `scripts/reports/GetTrialBalancePerCabang.py` (+ `GetTrialBalanceKonsolidasi.py`)
- `dialogs/reports/fNeraca*` + `scripts/reports/neraca5.py`

## Keputusan (brainstorming)

- **Sumber saldo: legacy-faithful** — `transaction.dailybalance.balancecumulative`
  (max `datevalue` ≤ tanggal per `accountinstance`) + `accountinstance` (branch,
  currency, `balance_sign`) + `accounthierarchy` (rollup child→parent). Trial
  Balance menambah mutasi journalitem "hari ini" bila `end >= today`.
  ⚠️ `dailybalance` terisi s/d **2025-12-31** → data 2026 belum akurat sampai ETL
  balance dibangun (dicatat sbg known-limitation; diverifikasi pakai periode 2025).
- **Neraca: hierarkis** (neraca5) — accounthierarchy rollup, tipe **A/L/E**, tampil
  per `account_level` (indent), kolom **pembanding periode lalu**, cek Aktiva=Pasiva.
- **Valuta**: single IDR → picker dihilangkan (filter currency default semua/IDR).
- **Cabang RBAC**: user `single` terkunci primary; `all` boleh pilih cabang atau
  Konsolidasi (semua cabang).

## Validasi (dari _intr.py)

- Trial Balance: `TanggalAwal ≤ TanggalAkhir` (else error); cabang per-RBAC; onlydetail.
- Neraca: cabang **wajib kecuali Konsolidasi**; `tanggal` posisi; `jenisperiode`
  Tahunan→pembanding = akhir tahun lalu (`1 Jan tahun` − 1), Bulanan→akhir bulan lalu
  (`1 <bulan>` − 1); `level` kedalaman (default semua).

## Sumber data (mziss_laz; dwh pool read-only)

View `dwh.v_daily_balance` (portal-neutral): `accountinstance ai JOIN dailybalance d`
+ `account` → kolom: `accountinstance_id, account_code, account_name, account_type,
account_level, is_detail, branch_code, currency_code, balance_sign, datevalue,
balancecumulative, debit, credit, balance`. Logika max-date & rollup di report-api.
(accounthierarchy & journalitem dibaca langsung dari `transaction.*` oleh service.)

## Komponen

### A. Trial Balance — `keuangan.report.trial_balance`

- Param: `begin`, `end`, `branch` (atau ALL/konsolidasi). Validasi begin≤end.
- Per **detail account** (`is_detail='T'`, type A/L/E/I/X):
  - `saldo_awal` = balancecumulative max(datevalue ≤ begin−1)
  - `saldo_akhir` = balancecumulative max(datevalue ≤ end)
  - `debit`/`credit` = Σ dailybalance dalam [begin,end]; **+ journalitem** [begin,end]
    bila `end ≥ today` (mutasi belum ter-dailybalance).
- Group per tipe + subtotal + grand total; cek ΣDebet = ΣKredit.
- report-api `/report/trial-balance` + `/export.xlsx`. Branch ALL → tanpa filter ai.branch_code.

### B. Neraca — `keuangan.report.neraca`

- Param: `tanggal`, `jenisperiode` (T/B), `level`, `branch` (atau konsolidasi).
- Saldo per account (rollup via accounthierarchy: balancecumulative anak dijumlah ke
  parent), max(datevalue ≤ tanggal) & ≤ tanggal_prev (pembanding).
- Filter `account_type in ('A','L','E')`, `account_level < level`.
- Susun: **AKTIVA** (A) lalu **PASIVA** (L,E), indent per level; Total Aktiva (level-0 A),
  Total Pasiva (level-0 L+E); status BALANCE (Aktiva−Pasiva≈0).
- report-api `/report/neraca` + `/export.xlsx`.

### C. BFF + Frontend + Seed (pola standar)

- BFF: routes `require_menu('keuangan.report.trial_balance' / '.neraca')` + `_resolve_branch`
  (+ dukung Konsolidasi=ALL utk user 'all'), streaming xlsx, branches.
- Frontend: `LaporanTrialBalancePage.vue` (filter periode+cabang, tabel group tipe + saldo
  awal/debet/kredit/akhir + totals), `LaporanNeracaPage.vue` (filter tanggal+periode+level+cabang,
  tabel hierarkis Aktiva/Pasiva + pembanding + status balance). Load-on-Tampilkan.
  Aktifkan placeholder di sidebar (Akuntansi) → link; tambah menu_key di registry; route.
- Seed: menu `keuangan.report.trial_balance`, `keuangan.report.cash_*`... + role_menu
  `ADM,KEU,ACC,SPVKEU,QAC,SPVACC`; apply isf_auth_zakat.

## Error handling

- report-api 503 DB down; 422 bila begin>end (trial balance) / param invalid.
- BFF 401/403 (require_menu/branch), 400 branch wajib (neraca non-konsolidasi).

## Testing / verification

- Pakai periode **2025** (dailybalance tersedia). Trial Balance: ΣDebet=ΣKredit, saldo
  akhir = awal + debet − kredit. Neraca: Aktiva ≈ Pasiva (status BALANCE).
- report-api langsung → BFF authenticated (RAIS/finance) → browser drive + xlsx.

## Di luar scope

- Konsolidasi-lintas-cabang-induk varian (pakai filter sederhana: ALL = semua cabang user).
- Currency multi (IDR only).
- Akurasi 2026 (perlu ETL dailybalance / fallback journalitem) — fase berikut.
- Wakaf (mirror setelah zakat).
