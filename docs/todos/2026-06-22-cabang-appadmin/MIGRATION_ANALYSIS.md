# MIGRATION_ANALYSIS: Manajemen Cabang

**MODUL:** docs/legacy-apps/enterprise/
**PORTAL:** zakat
**SCOPE:** Manajemen Cabang — Inquiry + Input Data
**TANGGAL:** 2026-06-22

---

## FITUR LIST

### 1. Inquiry Cabang
- **ROLES:** ADMIN
- **DIALOG:** dialogs/corporateParameter/cabangQuery.*
- **MENU_KEY_KANDIDAT:** appadmin.branch.list

### 2. Input Data Cabang Baru
- **ROLES:** ADMIN
- **DIALOG:** dialogs/corporateParameter/cabangNew.*
- **MENU_KEY_KANDIDAT:** appadmin.branch.create

### 3. Koreksi Data Cabang (dari popup di list, bukan menu utama)
- **ROLES:** ADMIN
- **DIALOG:** dialogs/corporateParameter/cabangEdit.*
- **MENU_KEY_KANDIDAT:** appadmin.branch.edit
- **CATATAN:** Diakses via context menu pCabang di cabangQuery

### 4. Lihat Data Cabang (dari popup di list)
- **ROLES:** semua (tidak dibatasi AllowedGroups)
- **DIALOG:** dialogs/corporateParameter/cabangView.*
- **MENU_KEY_KANDIDAT:** appadmin.branch.detail

### 5. Non Aktifkan / Aktifkan Cabang (dari popup di list)
- **ROLES:** ADMIN
- **MENU_KEY_KANDIDAT:** appadmin.branch.toggle-status
- **ENDPOINT:** ExecuteScript → scripts/corporateParameter/S_NonAktifkanCabang.py
                            → scripts/corporateParameter/S_AktifkanCabang.py

---

## FORM FIELDS (per dialog)

### DIALOG: corporateParameter/cabangQuery
**FUNGSI:** List + filter cabang

**FILTER FIELDS:**
- `status_aktif` (String, Optional) — Status Aktif
  - Nilai: ALL=-- ALL --, F=Cabang Tidak Aktif, T=Cabang Aktif
  - Default saat Show(): 'T'
- `KeyWord` (String, Optional) — Keyword (pencarian kode/nama cabang)

**COLUMNS DITAMPILKAN:**
- `kode_cabang` (String) — Kode Cabang
- `nama_cabang` (String) — Nama Cabang
- `cabang_induk` (String, dari join LCabangInduk.Nama_Cabang) — Cabang Induk
- `status_aktif` (String) — Status Aktif

OQL QUERY dengan filter status_aktif + keyword LIKE kode/nama

---

### DIALOG: corporateParameter/cabangNew + cabangEdit
**FUNGSI:** Registrasi dan koreksi data cabang

**FIELDS — Section "Data Cabang":**
- `kode_cabang` (String(20), Required, readonly di edit) — Kode Cabang
- `nama_cabang` (String(30), Required) — Nama Cabang
- `tipe_cabang` (String(2), Hidden di dfr, Required logika) — Tipe Cabang
  - Nilai: CP=Cabang Pembantu, CU=Cabang Umum, GM=Gerai, KS=Kantor Kas, NO=Pusat Non Operasional, PO=Pusat Operasional
- `status_cabang` (String(1), Auto dari tipe_cabang) — Status Cabang
  - Nilai: B=Cabang Utama (CU/PO), S=Cabang Pembantu (CP/GM/KS)
- `sandi_bi` (String(7), Hidden di dfr) — Sandi BI
- `zona_waktu` (String(2), Hidden di dfr) — Zona Waktu
  - Nilai: B=WIB, TA=WITA, T=WIT
- `kode_cabang_induk` (FK→Cabang, enabled hanya jika status_cabang='S') — Cabang Induk
- `kode_wilayah` (FK→AreaCabang, Hidden di dfr) — Kode Wilayah

**FIELDS — Section "Kantor":**
- `kantor_nama` (String(100), Optional) — Nama Kantor
- `kantor_npwp` (String(30), Optional) — NPWP Kantor
- `kantor_alamat` (String(200), Optional) — Alamat Kantor
- `kantor_kode_pos` (String(5), Optional) — Kode Pos Kantor
- `kantor_telepon1` (String(15), Optional) — Telepon 1
- `kantor_telepon2` (String(15), Optional) — Telepon 2
- `kantor_telepon3` (String(15), Optional) — Telepon 3

**HIDDEN (tersimpan tapi tidak ditampilkan di legacy):**
- Tab Limit Operasi dan GL Interface (TabVisible=false — warisan core banking)
- Field: status_cabang, sandi_bi, zona_waktu, kode_wilayah, kantor_tipe, level_cabang

---

## UI FLOW

### ON OPEN (list)
- Default filter status_aktif = 'T'
- Data langsung muncul saat form terbuka

### ON OPEN (form new)
- Tidak ada pre-fill dari session
- status_aktif = 'T' di-set saat OnCreate()

### ON OPEN (form edit)
- Load data existing cabang dari key

### ON SAVE (create)
**Validasi:**
1. kode_cabang kosong → error
2. nama_cabang kosong → error
3. kode_cabang sudah terdaftar → error (cek ke server via ExistCheck)

**Save:**
- Auto-set: status_aktif='T', status_otorisasi='1', status_akses='O'
- Auto-set: user_input dari session, tanggal_input = today, terminal_input dari session
- Auto-set: status_cabang berdasarkan tipe_cabang
- Cross-service call ke transaction/GenerateInstanceByBranch (perlu investigasi)

### ON SAVE (edit)
**Validasi:** nama_cabang tidak kosong
**Save:** kode_cabang tidak bisa diubah

### ON ACTION (toggle status)
- Non-Aktifkan: cek status_aktif != 'F' → set status_aktif='F'
- Aktifkan: cek status_aktif != 'T' → set status_aktif='T'

---

## SAVE LOGIC

### CREATE
- **Entry:** OnCreate() di ParameterKorporat.Cabang
- **DB:** INSERT enterprise.CABANG dengan auto fields
- **Cross-service:** rexecscript('transaction', 'AppInterface/GenerateInstanceByBranch', params)
- **KRITIS:** GenerateInstanceByBranch belum diinvestigasi — perlu analisis terpisah

### UPDATE
- **Entry:** CommitBuffer → save Cabang
- **DB:** UPDATE enterprise.CABANG (kode_cabang tetap)
- **Note:** OnUpdate() di-comment out di legacy

### DEACTIVATE
- **DB:** UPDATE enterprise.CABANG SET status_aktif='F' WHERE kode_cabang=:kode

### ACTIVATE
- **DB:** UPDATE enterprise.CABANG SET status_aktif='T' WHERE kode_cabang=:kode

---

## SCHEMA DB

### ENTITIES
- **Cabang** → tabel: enterprise.cabang
  - Kolom: kode_cabang (PK), nama_cabang, tipe_cabang, status_cabang, sandi_bi, zona_waktu, user_input, tanggal_input, terminal_input, user_otorisasi, tanggal_otorisasi, terminal_otorisasi, kode_cabang_induk (FK self), status_aktif, status_otorisasi, kode_lokasi, status_akses, id_sandibi, id_sandilokasi, level_cabang, kode_wilayah_kliring, kantor_alamat, kantor_kode_pos, kantor_nama, kantor_npwp, kantor_telepon1-3, kantor_tipe

### RELASI
- enterprise.cabang.kode_cabang_induk → enterprise.cabang.kode_cabang (self-ref)
- enterprise.cabang → enterprise.areacabang (via kode_wilayah FK, optional)
- enterprise.limitoperasi.kode_cabang → enterprise.cabang.kode_cabang
- enterprise.glinterface.kode_cabang → enterprise.cabang.kode_cabang

---

## DISCRIMINATORS

- **tipe_cabang:** CP/GM/KS → status_cabang='S' (Pembantu), kode_cabang_induk wajib
- **tipe_cabang:** CU/PO → status_cabang='B' (Utama), kode_cabang_induk disabled
- **status_aktif = 'T'** → Cabang Aktif (default filter)
- **status_aktif = 'F'** → Cabang Tidak Aktif
- **status_akses = 'O'** → Branch Open (di-set saat create)
- **status_akses = 'C'** → Branch Closed (session management — bukan fitur form ini)

**KRITIS:** status_aktif (T/F = aktif record) ≠ status_cabang (B/S = tipe hierarki)
**KRITIS:** status_akses (O/C) diset saat OnCreate, dikelola oleh branch management session

---

## KOMPLEKSITAS

- **LEVEL:** SEDANG
- **ALASAN:** 3 entitas, self-referencing FK, cross-service call ke modul transaction, conditional field (cabang_induk visible hanya untuk Pembantu)
- **WORKFLOW:** CRUD (list + create + edit + toggle status + detail)

---

## HANDOFF

### → nuwis-seed-gen
| MENU_KEY | LABEL | ROLES |
|---|---|---|
| appadmin.branch.list | Inquiry Cabang | ADMIN |
| appadmin.branch.create | Input Data Cabang Baru | ADMIN |
| appadmin.branch.edit | Koreksi Data Cabang | ADMIN |
| appadmin.branch.detail | Lihat Data Cabang | ADMIN |

### → nuwis-db-migrator
- **MIGRATIONS:** Tabel enterprise.cabang sudah ada (legacy data)
- Perlu verifikasi kolom aktual di DB: SELECT column_name FROM information_schema.columns WHERE table_schema='enterprise' AND table_name='cabang'

### → nuwis-python-builder
**ENDPOINTS:**
- GET /api/appadmin/branches — list filter status_aktif + keyword
- POST /api/appadmin/branches — create + auto audit fields
- GET /api/appadmin/branches/{branch_code} — detail
- PUT /api/appadmin/branches/{branch_code} — update (kode readonly)
- PATCH /api/appadmin/branches/{branch_code}/deactivate — set status_aktif='F'
- PATCH /api/appadmin/branches/{branch_code}/activate — set status_aktif='T'
- GET /api/appadmin/branches/check-code/{branch_code} — cek duplikasi kode

### → nuwis-ui-builder
- **PAGE_TYPE:** list + form modal
- **FIELDS:** lihat FORM FIELDS di atas
- **FILTERS:** status_aktif (dropdown, default T), keyword (text)
