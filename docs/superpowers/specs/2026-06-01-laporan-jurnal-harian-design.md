# Laporan Jurnal Harian (zakat) — fase view-based + export Excel

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem / Goal

Sediakan **Laporan Jurnal Harian** di portal zakat: form dengan filter cabang +
rentang tanggal, tabel preview di layar, dan **export Excel**. Mereplikasi report
legacy `docs/legacy-apps/core/dialogs/Report/fListJournalDaily*`
(query inti di `fListJournalDaily_data.py`).

Fase ini memakai **view di schema `dwh`** sebagai sumber. Ke depan kemungkinan
diganti **ETL → tabel independen di dwh**; kontrak API & view name dijaga agar
peralihan itu non-breaking.

## Keputusan (hasil brainstorming)

- **Export**: **sync streaming** (generate xlsx in-request, stream via BFF) untuk
  fase ini. **Async + menu "Hasil Laporan" ditunda ke fase 2** (follow-up
  terdokumentasi) saat volume/timeout menuntut.
- **Form**: filter + **tabel preview** (paginated, dengan cap) + tombol Export.
- **Cabang**: berdasarkan `enterprise.userapp.tipe_akses_cabang`:
  - `T` = Tunggal → akses **hanya cabang default** (primary_branch). Cabang
    terkunci, tanpa opsi "semua cabang".
  - `S` = Seluruh → akses **semua cabang**; dropdown semua cabang + opsi
    "Semua cabang".
- **Periode**: default = **hari ini**; bisa rentang; **cap 50.000 baris** server.
- **Menu**: subgrup baru **"Laporan"** di bawah Keuangan → "Jurnal Harian",
  menu key `keuangan.report.journal_daily`.
- **Scope**: **zakat dulu**.

## Sumber data

Tabel live ada di schema **`transaction.*`** (`transaction.journalitem` ~398k baris;
`accounting.*` hampir kosong). View dibuat di `dwh` tapi membaca `transaction.*`.

## Komponen

### A. View `dwh.v_journal_daily` (mziss_laz)

Membungkus query legacy. Kolom (≈ legacy `GetData`):

| Kolom | Asal |
|---|---|
| `branch_code` | `j.branch_code` — **filter** |
| `journal_date` | `j.journal_date` — **filter** |
| `journal_no` | `j.journal_no` |
| `transactionno` | `t.transactionno` |
| `account_branch_code` | `ji.branch_code` |
| `account_code` / `account_type` / `account_name` | `ac.*` |
| `subaccountcode` / `subaccountname` | `ji.*` |
| `description` | `ji.description (+ '(' || additionaldescription || ')')` |
| `debit_ekuiv` | `ji.amount_debit * ji.nilai_kurs` |
| `credit_ekuiv` | `ji.amount_credit * ji.nilai_kurs` |
| `inputer` | `t.inputer` |

Sumber: `transaction.account ac, transaction.journal j, transaction.journalitem ji
LEFT JOIN transaction.transaction t ON t.journalblockid = ji.id_journalblock`,
dengan `ji.fl_account=ac.account_code AND ji.fl_journal=j.journal_no`.
Order default: `journal_date, journal_no, transactionno, amount_debit desc`.
Migrasi SQL: `infra/db/migrations/dwh/v_journal_daily-zakat.sql` (CREATE OR REPLACE VIEW).

### B. report-api (`apps_zakat/report-api/app/modules/report/`)

Modul `report` jadi fungsional; baca via **pool dwh** (`fetch_all_dwh`/`fetch_one_dwh`).

- `service.py`:
  - `journal_daily_page(branch, all_branches, begin, end, page, page_size)` →
    `{rows, total, capped}` (count + slice; `capped = total > CAP`).
  - `journal_daily_rows(branch, all_branches, begin, end, limit)` → list utk export.
  - `list_branches(scope)` → `[{code, name}]` dari `enterprise.cabang`
    (`scope='all'` → semua aktif; `scope=<kode>` → satu cabang).
  - `CAP = 50_000`.
- `router.py`:
  - `GET /report/journal-daily?branch=<kode|ALL>&begin=&end=&page=&page_size=` → ok(page).
  - `GET /report/journal-daily/export.xlsx?branch=&begin=&end=` → `StreamingResponse`
    xlsx; bila `total > CAP` → `422 REPORT_TOO_LARGE`.
  - `GET /report/branches?scope=all|<kode>` → ok(list).
- `export.py` (baru): builder openpyxl (pola `api-python coa/export.py`): judul,
  Cabang, Periode, header kolom (bold), data; format `#,##0.00` debet/kredit,
  tanggal `dd-mm-yyyy`.

### C. Identity (`apps_zakat/api-python/app/modules/identity/`)

`get_profile` + `schema.ProfileResponse`: tambah field `branch_access` —
`'all'` bila `userapp.tipe_akses_cabang='S'`, else `'single'`. (Ambil kolom
`tipe_akses_cabang` di query userapp yang sudah ada.)

### D. BFF (`apps_zakat/bff-api/`)

- **Login** (`routers/auth.py`): simpan `branch_access` ke session dari profil identity.
- `services/proxy.py`: tambah `stream_report_api(path, params)` — proxy **biner**
  (teruskan `content`, `status`, `Content-Type`, `Content-Disposition`) untuk xlsx.
- `routers/report.py` (semua `require_menu('keuangan.report.journal_daily')`):
  - helper `resolve_branch(session, branch_param)` → enforce: `single` user hanya
    boleh `branch==primary_branch` (tolak lain & `ALL` → `403 BRANCH_FORBIDDEN`);
    `all` user boleh kode mana pun atau `ALL`.
  - `GET /report/journal-daily` → validasi → proxy `get_report_api`.
  - `GET /report/journal-daily/export.xlsx` → validasi → `stream_report_api`.
  - `GET /report/journal-daily/branches` → scope dari session
    (`all`→`scope=all`; `single`→`scope=<primary_branch>`) → proxy.
- Register `report_router` (sudah ada dari scaffold; tambah endpoint).

### E. Frontend (`apps_zakat/web-vue/`)

- `stores/auth.ts`: simpan `branch_access` dari `/me`/login.
- `pages/keuangan/LaporanJurnalHarianPage.vue`:
  - Filter: dropdown cabang (load `/api/report/journal-daily/branches`; default
    `primary_branch`; opsi "Semua cabang" hanya bila `auth.branch_access==='all'`;
    bila `'single'` dropdown terkunci ke primary_branch), `Dari`/`Sampai` (default hari ini).
  - Tombol **Tampilkan** → `useFetch` ke `/journal-daily` (paginated); tabel +
    pager; badge peringatan bila `capped`.
  - Tombol **Export Excel** → buka `/api/report/journal-daily/export.xlsx?...`
    (anchor/`window.location`); tangani 422 (pesan persempit rentang).
- Menu registry (`lib/menu/registry.ts`): tambah `keuangan.report.journal_daily`.
- Sidebar: grup **"Laporan"** di bawah Keuangan → item "Jurnal Harian".
- Router (`router/index.ts`): route `/keuangan/laporan/jurnal-harian`,
  `meta.menu_key='keuangan.report.journal_daily'`.

### F. Seed menu (isf_auth_zakat)

`infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql`: tambah row `menu`
(`keuangan.report.journal_daily`) + `role_menu` untuk role keuangan terkait
(mis. KEU, ACC, SPVKEU, SPVADM). Apply ke `isf_auth_zakat`. Untuk verifikasi
end-to-end, pastikan minimal satu role milik user uji mendapat menu ini.

## Data flow

```
web-vue LaporanJurnalHarianPage
  ├─ branches  → bff /api/report/journal-daily/branches → report-api /report/branches → enterprise.cabang (dwh pool)
  ├─ preview   → bff /api/report/journal-daily          → report-api /report/journal-daily → dwh.v_journal_daily
  └─ export    → bff /api/report/journal-daily/export.xlsx (stream) → report-api export.xlsx → dwh.v_journal_daily → openpyxl
        (BFF: require_menu + resolve_branch validasi vs session.branch_access)
```

## Error handling

- report-api: `503 DB_UNAVAILABLE` (pool down); `422 REPORT_TOO_LARGE` (export > CAP).
- BFF: `401` (no session), `403` (require_menu deny / `BRANCH_FORBIDDEN`), passthrough lainnya.
- Preview cap: kembalikan halaman + `total` + `capped=true` (tanpa error) agar UI bisa
  menampilkan peringatan + menyarankan persempit rentang.

## Testing / verification

1. SQL: apply view; `SELECT … LIMIT 5` + `count` untuk satu cabang/tanggal.
2. report-api (:8010 langsung): `/report/branches`, `/report/journal-daily`
   (paginated), `/export.xlsx` (file valid; cek header + beberapa baris).
3. BFF authenticated: user dengan menu `keuangan.report.journal_daily` →
   preview 200, export 200 (xlsx), branches sesuai `branch_access`; user 'single'
   ditolak `ALL`/cabang lain (403).
4. Browser drive (:5173): buka menu Keuangan ▸ Laporan ▸ Jurnal Harian, set filter,
   Tampilkan (tabel), Export (unduh xlsx).

## Di luar scope (follow-up terdokumentasi)

- **Async export + menu "Hasil Laporan"** (fase 2): job store writable + worker +
  storage + polling; dipicu saat volume/timeout jadi masalah.
- ETL → tabel independen `dwh` (ganti view tanpa ubah kontrak API).
- Portal wakaf (mirror setelah zakat stabil).
