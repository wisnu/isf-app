==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/core/dialogs/Mustahiq/
         docs/legacy-apps/program/menus/Penyaluran.mnu
PORTAL:  zakat
SCOPE:   Master Data Mustahiq (penerima manfaat/beneficiary) — dua sub-modul:
         1. Mustahiq Lembaga (Corporate) — organisasi/institusi
         2. Mustahiq Individu (Personal) — perorangan
TANGGAL: 2026-06-22

── FITUR LIST ──────────────────────────────────────────────────
  1. Mustahiq Lembaga
     ROLES:             DIST, SPVDIST
     DIALOG:            dialogs/Mustahiq/QryMustahiqCorporate.*
                        dialogs/Mustahiq/fMustahiqCorpNew.*
                        dialogs/Mustahiq/fMustahiqCorpEdit.*
                        dialogs/Mustahiq/fMustahiqCorpDetail.*
     MENU_KEY_KANDIDAT: distribution.mustahiq.corporate

  2. Mustahiq Individu
     ROLES:             DIST, SPVDIST
     DIALOG:            dialogs/Mustahiq/QryMustahiqPersonal.*
                        dialogs/Mustahiq/fMustahiqPersNew.*
                        dialogs/Mustahiq/fMustahiqPersEdit.*
                        dialogs/Mustahiq/fMustahiqPersDetail.*
     MENU_KEY_KANDIDAT: distribution.mustahiq.personal

  Sumber: Penyaluran.mnu baris 39–51
  Parent menu: "Kegiatan > Data Mustahiq"

── DISCRIMINATORS ──────────────────────────────────────────────
KRITIS — jangan hilangkan saat implementasi:

  - mustahiqtype = 'MC' → Mustahiq Corporate (Lembaga)
  - mustahiqtype = 'MP' → Mustahiq Personal (Individu)
  - mustahiqstatus = 'A' → Aktif
  - mustahiqstatus = 'N' → NonAktif
  - bankaccountlisttype = 'M' → MustahiqBankAccount (discriminator inheritance dari BankAccountList)
  - isdefault = 'T' / 'F' → rekening bank default/non-default (FTBoolean)

  Kolom `mustahiqtype` di tabel MUSTAHIQ adalah IsClassifierField=true —
  dipakai oleh DAF PClass inheritance untuk menentukan subclass mana yang
  di-load (MC→MustahiqCorporate, MP→MustahiqPersonal).
  Sumber: app.mdt baris 5382–5386, 5492, 5531

── FORM FIELDS (per dialog) ────────────────────────────────────

=== DIALOG: QryMustahiqCorporate (List/Query Mustahiq Lembaga) ===
FILTER COLUMNS:
  - Incolumn   : integer  [Optional] — dropdown pilihan kolom pencarian
                 (0=Seluruh Data, 1=Nomor, 2=Nama, 3=Alamat, 4=Telepon, 5=Status)
  - keywords   : varchar  [Optional] — keyword pencarian

LIST COLUMNS DISPLAYED:
  - MustahiqNo           → no_mustahiq (nomor mustahiq)
  - MustahiqName         → name
  - MustahiqAddress      → address
  - MustahiqPhoneNumber  → phone_number
  - MustahiqStatus       → status (A=Active, N=NonActive)
  - MustahiqType         → mustahiq_type (selalu 'MC' di view ini)

FILTER AKTIF di query: WHERE mustahiqtype = 'MC'
Sumber: QryMustahiqCorporate_intr.py baris 24–26, QryMustahiqCorporate.dfr baris 37

ACTIONS (dari popup menu popupmenus/Kegiatan/MnuMustahiq2.mnu):
  - Tambah Data Mustahiq Korporat → DIST
  - Ubah Data Mustahiq Korporat   → DIST
  - Tampilkan Detail               → DIST, SPVDIST
  - Hapus Data Mustahiq Korporat   → DIST, SPVDIST


=== DIALOG: QryMustahiqPersonal (List/Query Mustahiq Individu) ===
FILTER COLUMNS (sama dengan Corporate, kecuali tidak ada filter Tipe):
  - Incolumn : integer  [Optional] — (0=Seluruh Data, 1=Nomor, 2=Nama, 3=Alamat, 4=Telepon, 5=Status)
  - keywords : varchar  [Optional]

LIST COLUMNS DISPLAYED:
  - MustahiqNo          → no_mustahiq
  - MustahahiqName      → name
  - MustahiqAddress     → address
  - MustahiqPhoneNumber → phone_number
  - MustahiqStatus      → status
  - MustahiqType        → mustahiq_type (selalu 'MP' di view ini)

FILTER AKTIF di query: WHERE mustahiqtype = 'MP'
Sumber: QryMustahiqPersonal_intr.py baris 24–26

ACTIONS (dari popup menu popupmenus/Kegiatan/MnuMustahiq.mnu):
  - Tambah Data Mustahiq → DIST
  - Ubah Data Mustahiq   → DIST
  - Tampilkan Detail     → DIST, SPVDIST
  - Hapus Data Mustahiq  → DIST, SPVDIST


=== DIALOG: fMustahiqCorpNew (Form Tambah Mustahiq Lembaga) ===
PClass: MustahiqCorporate (param tipe='MC' dikirim ke helper.CreatePObject)
Sub-form: uipBankAccount (list rekening bank — bisa 0 atau lebih)

FIELDS uipmc (MustahiqCorporate):
  - MustahiqName               : varchar(50)   [REQUIRED*]  — Nama lembaga
  - MustahiqAddress            : varchar(100)  [Optional]   — Alamat
  - MustahiqAddressKelurahan   : varchar(30)   [Optional]   — Kelurahan
  - MustahiqAddressKecamatan   : varchar(30)   [Optional]   — Kecamatan
  - LPropinsi (IdPropinsi)     : integer FK    [Optional]   — Provinsi (lookup ke Propinsi)
  - MustahiqPostalCode         : varchar(10)   [Optional]   — Kode Pos
  - MustahiqReferenceBy        : varchar(150)  [Optional]   — Referensi
  - MustahiqPhoneNumber        : varchar(30)   [Optional]   — Nomor Telepon
  - CPName                     : varchar(150)  [Optional]   — Nama Kontak (Contact Person)
  - CPPhoneNumber              : varchar(30)   [Optional]   — Nomor Telepon Kontak
  - CPMobileNumber             : varchar(30)   [Optional]   — Nomor HP Kontak

FIELDS uipBankAccount (sub-list, MustahiqBankAccount):
  - BankAccountNo    : varchar(20)  [Optional] — Nomor Rekening
  - BankAccountName  : varchar(200) [Optional] — Nama Rekening
  - LBank (BankCode) : varchar FK   [Optional] — Kode Bank (lookup ke Bank)
  - IsDefault        : varchar(1)   [Optional] — Default (F=false, T=true)

SECTIONS: Panel utama (data lembaga) + Grid bawah (Rekening Bank Mustahiq)
READ_ONLY: tidak ada field read-only di form New
HIDDEN:    MustahiqType='MC' di-set otomatis via param di _data.py, tidak terlihat di UI
Sumber: fMustahiqCorpNew.dfr, fMustahiqCorpNew.svr


=== DIALOG: fMustahiqCorpEdit (Form Ubah Mustahiq Lembaga) ===
PClass: MustahiqCorporate (load by key dari parent form)
Fields sama persis dengan fMustahiqCorpNew.
Perbedaan: formSetDataEx load data existing dari key, Save = UPDATE.
Untuk bank account: BankAccountId=0 → CREATE baru; BankAccountId!=0 → UPDATE existing.
Sumber: fMustahiqCorpEdit_data.py baris 7–47, fMustahiqCorpEdit.svr


=== DIALOG: fMustahiqCorpDetail (View Detail Mustahiq Lembaga) ===
Fields: semua field Edit + MustahiqNo (ID) + MustahiqStatus (combo, disabled)
READ_ONLY: semua field (caView action), termasuk LPropinsi (Enabled=false),
           MustahiqStatus (Enabled=false), semua bank account columns (ReadOnly=true)
SECTIONS: Panel data lembaga (atas) + Grid rekening bank (bawah, read-only)
Sumber: fMustahiqCorpDetail.dfr, fMustahiqCorpDetail.svr


=== DIALOG: fMustahiqPersNew (Form Tambah Mustahiq Individu) ===
PClass: MustahiqPersonal (param tipe='MP', idpropinsi dikirim ke helper.CreatePObject)
Sub-form: uipBankAccount (list rekening bank)
Layout: TWO-COLUMN — kolom kiri (data identitas dasar) + kolom kanan (data sosial/demografi)

FIELDS uipmp — KOLOM KIRI (field2 panel):
  - MustahiqName               : varchar(50)   [REQUIRED*]  — Nama
  - MustahiqAddress            : varchar(100)  [Optional]   — Alamat
  - MustahiqAddressKelurahan   : varchar(30)   [Optional]   — Kelurahan
  - MustahiqAddressKecamatan   : varchar(30)   [Optional]   — Kecamatan
  - LPropinsi (IdPropinsi)     : integer FK    [Optional]   — Provinsi (lookup)
  - MustahiqPostalCode         : varchar(10)   [Optional]   — Kode Pos
  - MustahiqReferenceBy        : varchar(150)  [Optional]   — Referensi
  - MustahiqPhoneNumber        : varchar(30)   [Optional]   — Nomor Telepon
  - MustahiqGender             : varchar(1)    [Optional]   — Jenis Kelamin (L=Laki-Laki, P=Perempuan)
  - MustahiqAshnaf             : varchar(1)    [Optional]   — Ashnaf (lihat enum eAshnaf)

FIELDS uipmp — KOLOM KANAN (fields panel, tambahan untuk Personal):
  - MustahiqBirthPlace         : varchar(150)  [Optional]   — Tempat Lahir
  - MustahiqBirthDate          : timestamp/date [Optional]  — Tanggal Lahir (DateEdit)
  - MustahiqIdentityNumber     : varchar(30)   [Optional]   — Nomor Identitas
  - MustahiqIdentityType       : varchar(1)    [Optional]   — Jenis Identitas (K=KTP, S=SIM, F=KK, P=Passport)
  - MustahiqReligion           : integer       [Optional]   — Agama (1=Islam, 2=Katolik, 3=Protestan, 4=Hindu, 5=Budha, 6=Aliran Kepercayaan)
  - MustahiqTotalFamily        : integer       [Optional]   — Jumlah Keluarga
  - MustahiqFormalEducation    : integer       [Optional]   — Pendidikan (0=Tdk Formal, 1=SD, 2=SMP, 3=SMU, 4=S1, 5=S2, 6=S3)
  - MustahiqIncome             : double        [Optional]   — Pendapatan per Bulan
  - MustahiqMarital            : varchar(1)    [Optional]   — Status Pernikahan (K=Menikah, B=Belum, S=Duda/Janda)
  - MustahiqWorkSector         : varchar(1)    [Optional]   — Bidang Pekerjaan (1–9, lihat enum eEconomicSector)

FIELDS uipBankAccount (sub-list, sama dengan Corp):
  - BankAccountNo, BankAccountName, LBank, IsDefault

SECTIONS: Split horizontal — panel kiri/kanan (data mustahiq) + Grid bawah (Rekening Bank)
READ_ONLY: tidak ada yang read-only di form New
HIDDEN:    MustahiqType='MP' di-set otomatis via param di _data.py
Catatan UI: Propinsi di-set via param idpropinsi saat CreatePObject; berbeda dari Corp yang set manual
Sumber: fMustahiqPersNew.dfr, fMustahiqPersNew.svr, fMustahiqPersNew_data.py baris 7


=== DIALOG: fMustahiqPersEdit (Form Ubah Mustahiq Individu) ===
PClass: MustahiqPersonal (load by key)
Fields: identik dengan fMustahiqPersNew, semua editable.
Tidak ada validasi nama di bSaveClick — berbeda dari Corp yang validasi MustahiqName.
Untuk bank account: BankAccountId=0 → CREATE; BankAccountId!=0 → UPDATE.
Sumber: fMustahiqPersEdit_data.py, fMustahiqPersEdit_intr.py


=== DIALOG: fMustahiqPersDetail (View Detail Mustahiq Individu) ===
Fields: semua field Edit + MustahiqNo + MustahiqStatus
Layout: TWO-COLUMN (sama dengan Edit/New)
READ_ONLY: MustahiqNo (read-only), MustahiqGender (disabled), MustahiqAshnaf (disabled),
           LPropinsi (disabled), MustahiqIdentityType (disabled), MustahiqReligion (disabled),
           MustahiqFormalEducation (disabled), MustahiqMarital (disabled),
           MustahiqWorkSector (disabled), MustahiqStatus (disabled)
SECTIONS: Panel kiri (data utama) + Panel kanan (data sosial) + Grid bank account + Panel tutup
Catatan: bank account grid di Detail Personal menggunakan caEdit action (berbeda dari Corp yang caView)
         namun secara UX hanya tampilan karena tidak ada Save button.
Sumber: fMustahiqPersDetail.dfr, fMustahiqPersDetail.svr

── UI FLOW ─────────────────────────────────────────────────────

=== LIST VIEW (QryMustahiqCorporate / QryMustahiqPersonal) ===
ON OPEN:
  - Auto-load data sesuai mustahiqtype filter ('MC' atau 'MP')
  - QryMustahiqCorporate.dfr: DirectDisplay=true → data langsung tampil tanpa klik Perform
  - QryMustahiqPersonal.dfr: DirectDisplay=true → sama
  - QryMustahiq (all-types): DirectDisplay=false → perlu klik Perform dulu

ON FILTER/SEARCH:
  - User pilih kolom dari dropdown Incolumn
  - Input keyword di field Search
  - Klik "Perform" → FilterClick() → ShowMustahiq() → OQL query baru

ON CONTEXT MENU (klik kanan pada baris):
  - Tambah: buka fMustahiqCorpNew/fMustahiqPersNew (tidak perlu pilih baris)
  - Ubah:   buka fMustahiqCorpEdit/fMustahiqPersEdit dengan key baris terpilih
  - Detail: buka fMustahiqCorpDetail/fMustahiqPersDetail dengan key baris terpilih
  - Hapus:  konfirmasi → ExecuteScript('Mustahiq/HapusData') → refresh
  - NonAktif: ExecuteScript('Mustahiq/NonAktifkanData') → refresh
  - Aktif:    ExecuteScript('Mustahiq/AktifkanData') → refresh

Role notes:
  - Tambah/Ubah: DIST only
  - Detail/Hapus/NonAktif/Aktif: DIST dan SPVDIST
Sumber: pMenuCorporate.py, pMenuPersonal.py, MnuMustahiq.mnu, MnuMustahiq2.mnu


=== FORM NEW (fMustahiqCorpNew / fMustahiqPersNew) ===
ON OPEN:
  - Form kosong — tidak ada pre-fill dari session
  - Bank account grid kosong — user bisa menambah baris baru inline

ON SAVE (bSaveClick):
  Validasi client (Corp):
    - MustahiqName tidak boleh kosong → focus ke field + raise Exception
  Validasi client (Personal):
    - MustahiqName tidak boleh kosong → focus ke field + raise Exception
    (tidak ada validasi lain di bSaveClick Personal)
  - FormObject.CommitBuffer() → kumpulkan data dari form buffer
  - FormObject.GetDataPacket() → serialize ke packet
  - CallServerMethod('SimpanData', ph) → kirim ke server

ON CANCEL:
  - ExitAction=2 → tutup form tanpa save

Sumber: fMustahiqCorpNew_intr.py baris 17–36, fMustahiqPersNew_intr.py baris 17–37


=== FORM EDIT ===
ON OPEN:
  - formSetDataEx → UIDefList.SetData('uipmc'/'uipmp', key) → load data existing dari DB
  - Bank account sub-list di-load otomatis bersamaan (LsBankAccount)

ON SAVE: sama dengan New, tapi menggunakan GetObject (UPDATE) bukan CreatePObject (INSERT)

Sumber: fMustahiqCorpEdit_data.py baris 4–5, fMustahiqPersEdit_data.py baris 4–5


=== FORM DETAIL ===
ON OPEN:
  - formSetDataEx → load data sama seperti Edit
  - Semua field read-only (caView action, Enabled=false)
  - Tidak ada tombol Save

ON CLOSE:
  - bCancelClick → ExitAction=2 → tutup

── SAVE LOGIC ──────────────────────────────────────────────────

=== INSERT (fMustahiqCorpNew_data.py: SimpanData) ===
ENTRY: dialogs/Mustahiq/fMustahiqCorpNew_data.py → SimpanData()

ALUR:
  1. Ambil record dari parameter.FirstRecord
  2. config.BeginTransaction()
  3. helper.CreatePObject('MustahiqCorporate', {'tipe': 'MC'})
     → INSERT ke tabel MUSTAHIQ dengan mustahiqtype='MC'
     → INSERT ke tabel MUSTAHIQCORPORATE (inherit, mustahiqid FK)
     → Sistem auto-generate MustahiqNo dan MustahiqId
  4. Set semua field: MustahiqName, Address, Kelurahan, Kecamatan,
     PostalCode, ReferenceBy, PhoneNumber, CPName, CPPhoneNumber, CPMobileNumber
  5. Set IdPropinsi = LPropinsi.IdPropinsi (dari linked field)
  6. Loop uipBankAccount records:
     - helper.CreatePObject('MustahiqBankAccount', acc.key)
     - Set: MustahiqId, BankAccountName, BankAccountNo, BankCode (LBank.BankCode)
     → INSERT ke tabel MUSTAHIQBANKACCOUNT (inherit dari BANKACCOUNTLIST, type='M')
  7. config.Commit()
  8. On error: config.Rollback() + raise

Sumber: fMustahiqCorpNew_data.py baris 6–37


=== INSERT (fMustahiqPersNew_data.py: SimpanData) ===
ENTRY: dialogs/Mustahiq/fMustahiqPersNew_data.py → SimpanData()

ALUR:
  1. Ambil record dari parameter.FirstRecord
  2. config.BeginTransaction()
  3. helper.CreatePObject('MustahiqPersonal', {'tipe': 'MP', 'idpropinsi': IdPropinsi})
     → INSERT ke tabel MUSTAHIQ dengan mustahiqtype='MP'
     → INSERT ke tabel MUSTAHIQPERSONAL (inherit, mustahiqid FK)
  4. Set semua field dasar (sama dengan Corp: Name, Address, Kelurahan, Kecamatan,
     PostalCode, ReferenceBy, PhoneNumber)
  5. Set field khusus Personal: Ashnaf, BirthDate, BirthPlace,
     FormalEducation, Gender, IdentityNumber, IdentityType,
     Income, Marital, Religion, TotalFamily, WorkSector
  6. Set IdPropinsi = LPropinsi.IdPropinsi
  7. Loop uipBankAccount records → CreatePObject('MustahiqBankAccount', ...)
     (tanpa IsDefault di New Personal — berbeda dari Corp Edit)
  8. config.Commit()
  9. On error: config.Rollback() + raise

Catatan: Personal New tidak set IsDefault di bank account; Corp New juga tidak set IsDefault.
         Hanya di Edit (Corp & Personal) yang set IsDefault saat update bank account.
Sumber: fMustahiqPersNew_data.py baris 4–42


=== UPDATE (fMustahiqCorpEdit_data.py: SimpanData) ===
ENTRY: dialogs/Mustahiq/fMustahiqCorpEdit_data.py → SimpanData()

ALUR:
  1. rec = parameter.uipmc.GetRecord(0); key = rec.key.split('=')
  2. config.BeginTransaction()
  3. iAppt = helper.GetObject('MustahiqCorporate', app_id[-1])
     → bukan CreatePObject, ini GetObject → UPDATE record existing
  4. Set semua field (sama dengan New, tanpa type discriminator karena sudah ada)
  5. Loop uipBankAccount:
     - BankKey = acc.BankAccountId
     - Jika BankKey==0 (baru): helper.CreatePObject('MustahiqBankAccount', ...) → INSERT
     - Jika BankKey!=0 (existing): helper.GetObject('MustahiqBankAccount', BankKey) → UPDATE
     - Selalu set IsDefault saat Edit (berbeda dari New)
  6. config.Commit()
  7. On error: config.Rollback() + raise

Sumber: fMustahiqCorpEdit_data.py baris 7–47


=== UPDATE (fMustahiqPersEdit_data.py: SimpanData) ===
Logic identik dengan Corp Edit, menggunakan MustahiqPersonal dan field tambahan Personal.
Sumber: fMustahiqPersEdit_data.py baris 7–56


=== DELETE (scripts/Mustahiq/HapusData.py: DAFScriptMain) ===
ENTRY: scripts/Mustahiq/HapusData.py → DAFScriptMain()
Dipanggil via: ExecuteScript('Mustahiq/HapusData', ph) dari popup menu

ALUR:
  1. key = parameter.FirstRecord.key; MustahiqId = key.split('=')[-1]
  2. config.BeginTransaction()
  3. OQL: delete from MustahiqBankAccount WHERE MustahiqId = :MustahiqId
     → DELETE semua rekening bank mustahiq ini
  4. config.AccessPObject(key).Delete()
     → DELETE dari tabel MUSTAHIQ (cascade ke MUSTAHIQPERSONAL/MUSTAHIQCORPORATE)
  5. config.Commit()
  6. On error: config.Rollback(), return IsErr=1 + ErrMsg

Sumber: scripts/Mustahiq/HapusData.py baris 1–31


=== NONAKTIF (scripts/Mustahiq/NonAktifkanData.py) ===
ENTRY: scripts/Mustahiq/NonAktifkanData.py → NonAktifkanData()
Dipanggil via: ExecuteScript('Mustahiq/NonAktifkanData', ph)

ALUR:
  1. Obj = config.AccessPObject(key)
  2. Guard: Obj.IsNull → raise "Data tidak ditemukan"
  3. Guard: Obj.MustahiqStatus == 'N' → raise "Data sudah nonaktif"
  4. config.BeginTransaction()
  5. Obj.MustahiqStatus = 'N'
  6. modman.getModule('scripts#GeneralModule.S_ObjectEditor').NonActivateData(config, Obj)
     → UPDATE MUSTAHIQ SET mustahiqstatus='N'
  7. config.Commit()

Sumber: scripts/Mustahiq/NonAktifkanData.py baris 4–19


=== AKTIFKAN (scripts/Mustahiq/AktifkanData.py) ===
Kebalikan NonAktif: set MustahiqStatus='A', sama guards.
Sumber: scripts/Mustahiq/AktifkanData.py baris 4–19

── SCHEMA DB ───────────────────────────────────────────────────

ENTITIES (dari app.mdt baris 5338–5611):

Tabel: MUSTAHIQ (base/parent untuk kedua sub-tipe)
  - mustahiqid         : INTEGER  PK AUTO
  - mustahiqno         : VARCHAR(20)  — nomor urut mustahiq, di-generate otomatis
  - mustahiqname       : VARCHAR(50)  NOT NULL (required di UI)
  - mustahiqaddress    : VARCHAR(100)
  - mustahiqstatus     : VARCHAR(1)   — 'A'=Active, 'N'=NonActive
  - mustahiqreferenceby: VARCHAR(150)
  - mustahiqphonenumber: VARCHAR(30)
  - mustahiqtype       : VARCHAR(2)   DISCRIMINATOR — 'MC'=Corporate, 'MP'=Personal
  - branchcode         : VARCHAR(5)   — kode cabang
  - mustahiqaddresskelurahan  : VARCHAR(30)
  - mustahiqaddresskecamatan  : VARCHAR(30)
  - idpropinsi         : INTEGER FK → PROPINSI (nullable)
  - mustahiqpostalcode : VARCHAR(10)

Tabel: MUSTAHIQCORPORATE (extends MUSTAHIQ, mustahiqtype='MC')
  - mustahiqid   : INTEGER PK FK → MUSTAHIQ.mustahiqid
  - cpname       : VARCHAR(150)  — Contact Person Name
  - cpphonenumber: VARCHAR(30)   — Contact Person Phone
  - cpmobilenumber: VARCHAR(30)  — Contact Person Mobile

Tabel: MUSTAHIQPERSONAL (extends MUSTAHIQ, mustahiqtype='MP')
  - mustahiqid             : INTEGER PK FK → MUSTAHIQ.mustahiqid
  - mustahiqgender         : VARCHAR(1)  — L=Laki-Laki, P=Perempuan
  - mustahiqbirthplace     : VARCHAR(150)
  - mustahiqbirthdate      : TIMESTAMP   — tanggal lahir
  - mustahiqidentitynumber : VARCHAR(30) — nomor KTP/SIM/dll
  - mustahiqreligion       : INTEGER     — 1=Islam, 2=Katolik, 3=Protestan, 4=Hindu, 5=Budha, 6=Aliran
  - mustahiqtotalfamily    : INTEGER
  - mustahiqformaleducation: INTEGER     — 0=Tdk Formal, 1=SD, 2=SMP, 3=SMU, 4=S1, 5=S2, 6=S3
  - mustahiqincome         : DOUBLE      — pendapatan per bulan (numerik, bukan Currency)
  - mustahiqmarital        : VARCHAR(1)  — K=Menikah, B=Belum Menikah, S=Duda/Janda
  - mustahiqworksector     : VARCHAR(1)  — sektor ekonomi (1–9)
  - mustahiqashnaf         : VARCHAR(1)  — F=Fakir, M=Miskin, U=Mualaf, H=Hamba Sahaya, G=Gharimin, S=Fisabilillah, I=Ibnu Sabil, A=Amil
  - mustahiqidentitytype   : VARCHAR(1)  — K=KTP, S=SIM, F=Kartu Keluarga, P=Passport

Tabel: BANKACCOUNTLIST (base untuk semua rekening bank)
  - bankaccountid       : INTEGER  PK AUTO
  - bankaccountno       : VARCHAR(20)
  - bankaccountname     : VARCHAR(200)
  - bankcode            : VARCHAR FK → BANK.bankcode (via LBank AutoForeignKey)
  - isdefault           : VARCHAR(1)  — T=true, F=false
  - bankaccountlisttype : VARCHAR(1)  DISCRIMINATOR — 'M'=MustahiqBankAccount, dll

Tabel: MUSTAHIQBANKACCOUNT (extends BANKACCOUNTLIST, bankaccountlisttype='M')
  - bankaccountid : INTEGER PK FK → BANKACCOUNTLIST.bankaccountid
  - mustahiqid    : INTEGER FK → MUSTAHIQ.mustahiqid (via LMustahiq AutoForeignKey)

RELASI:
  - MUSTAHIQ.idpropinsi → PROPINSI.idpropinsi (FK nullable, optional)
  - MUSTAHIQCORPORATE.mustahiqid → MUSTAHIQ.mustahiqid (inheritance, 1:1)
  - MUSTAHIQPERSONAL.mustahiqid → MUSTAHIQ.mustahiqid (inheritance, 1:1)
  - MUSTAHIQBANKACCOUNT.mustahiqid → MUSTAHIQ.mustahiqid (1:N, list LsBankAccount)
  - MUSTAHIQBANKACCOUNT.bankaccountid → BANKACCOUNTLIST.bankaccountid (inheritance, 1:1)
  - BANKACCOUNTLIST.bankcode → BANK.bankcode (via AutoForeignKey)

── ENUM VALUES (untuk frontend dropdown dan backend validation) ─
eStatus:         A=Active, N=NonActive
eGender:         L=Laki-Laki, P=Perempuan
eReligion:       1=Islam, 2=Katolik, 3=Protestan, 4=Hindu, 5=Budha, 6=Aliran Kepercayaan
eIdentityType:   K=KTP, S=SIM, F=Kartu Keluarga, P=Passport
eMaritalState:   K=Menikah, B=Belum Menikah, S=Duda/Janda
eEducation:      0=Tdk Sekolah Formal, 1=SD, 2=SMP, 3=SMU/Sederajat, 4=S1, 5=S2, 6=S3
eEconomicSector: 1=Pertanian/Perkebunan/Perikanan, 2=Pertambangan,
                 3=Industri/Pabrik/Konsumer Goods, 4=Listrik/Gas/Air, 5=Konstruksi,
                 6=Perdagangan, 7=Pengangkutan/Pergudangan/Komunikasi,
                 8=Jasa-jasa Bisnis/Keuangan, 9=Jasa-jasa Sosial
eAshnaf:         F=Fakir, M=Miskin, U=Mualaf, H=Hamba Sahaya,
                 G=Gharimin, S=Fisabilillah, I=Ibnu Sabil, A=Amil
FTBoolean:       T=true, F=false (IsDefault di bank account)
Sumber: app.mdt baris 44–56, 523–531, 804–913, 1647–1675, 5719–5750

── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    SEDANG
ALASAN:   2 dialog linked (Corp dan Personal), masing-masing dengan sub-form bank account;
          inheritance table pattern (MUSTAHIQ → MUSTAHIQPERSONAL/MUSTAHIQCORPORATE);
          5 operasi berbeda (new, edit, detail, delete, aktif/nonaktif);
          tidak ada jurnal akuntansi, tidak ada JOIN kompleks
WORKFLOW: CRUD

── HANDOFF ─────────────────────────────────────────────────────

→ nuwis-seed-gen:
  MENU_KEY_1: distribution.mustahiq.corporate  / LABEL: Mustahiq Lembaga  / ROLES: DIST, SPVDIST
  MENU_KEY_2: distribution.mustahiq.personal   / LABEL: Mustahiq Individu / ROLES: DIST, SPVDIST
  Parent menu group: "Kegiatan" di modul Penyaluran/Distribution


→ nuwis-db-migrator:
  MIGRATIONS:
    Tabel baru tidak diperlukan jika mziss_laz sudah punya tabel legacy.
    Perlu cek apakah tabel MUSTAHIQ, MUSTAHIQPERSONAL, MUSTAHIQCORPORATE,
    MUSTAHIQBANKACCOUNT, BANKACCOUNTLIST sudah ada di schema transaction.
    Jika belum: buat migration CREATE TABLE dengan CAST(... AS type) convention.
    Kandidat DWH_VIEW: dwh.v_mustahiq — join MUSTAHIQ + MUSTAHIQPERSONAL/MUSTAHIQCORPORATE
    untuk laporan Daftar Mustahiq.
  SQL NOTE: Gunakan CAST(mustahiqid AS INTEGER) bukan mustahiqid::INTEGER.


→ nuwis-python-builder:
  ENDPOINTS:

  -- Mustahiq Corporate --
  GET    /api/distribution/mustahiq/corporate
         Query: search, page, limit
         Filter: WHERE mustahiqtype='MC' (selalu, jangan hapus)
         Response: { rows: [{ mustahiq_id, no_mustahiq, name, address, phone_number, status }],
                     pagination: {...} }

  POST   /api/distribution/mustahiq/corporate
         Body: { name*, address, address_kelurahan, address_kecamatan, province_id,
                 postal_code, reference_by, phone_number,
                 cp_name, cp_phone_number, cp_mobile_number,
                 bank_accounts: [{ account_no, account_name, bank_code, is_default }] }
         Logic: INSERT MUSTAHIQ (mustahiqtype='MC'), INSERT MUSTAHIQCORPORATE,
                INSERT MUSTAHIQBANKACCOUNT untuk tiap bank_accounts

  PUT    /api/distribution/mustahiq/corporate/{mustahiq_id}
         Body: sama dengan POST
         Logic: UPDATE MUSTAHIQ + MUSTAHIQCORPORATE; bank_accounts:
                jika bank_account_id=null/0 → INSERT; jika bank_account_id exists → UPDATE

  GET    /api/distribution/mustahiq/corporate/{mustahiq_id}
         Response: data lengkap + bank_accounts[]

  DELETE /api/distribution/mustahiq/corporate/{mustahiq_id}
         Logic: DELETE MUSTAHIQBANKACCOUNT WHERE mustahiqid=..., DELETE MUSTAHIQ

  PATCH  /api/distribution/mustahiq/corporate/{mustahiq_id}/status
         Body: { status: 'A' | 'N' }
         Logic: UPDATE MUSTAHIQ SET mustahiqstatus=:status
         Guard: cek status saat ini, tolak jika sudah sama

  -- Mustahiq Personal --
  GET    /api/distribution/mustahiq/personal
         Filter: WHERE mustahiqtype='MP' (selalu, jangan hapus)

  POST   /api/distribution/mustahiq/personal
         Body: { name*, address, address_kelurahan, address_kecamatan, province_id,
                 postal_code, reference_by, phone_number, gender, ashnaf,
                 birth_place, birth_date, identity_number, identity_type,
                 religion, total_family, formal_education, income, marital,
                 work_sector,
                 bank_accounts: [{ account_no, account_name, bank_code, is_default }] }
         Logic: INSERT MUSTAHIQ (mustahiqtype='MP'), INSERT MUSTAHIQPERSONAL,
                INSERT MUSTAHIQBANKACCOUNT

  PUT    /api/distribution/mustahiq/personal/{mustahiq_id}
  GET    /api/distribution/mustahiq/personal/{mustahiq_id}
  DELETE /api/distribution/mustahiq/personal/{mustahiq_id}
  PATCH  /api/distribution/mustahiq/personal/{mustahiq_id}/status

  DISCRIMINATORS (wajib di semua endpoint):
    - WHERE mustahiqtype='MC'  → hanya untuk Corporate endpoint
    - WHERE mustahiqtype='MP'  → hanya untuk Personal endpoint
    - Jangan gunakan endpoint yang sama tanpa filter tipe
    - status guard: cek MustahiqStatus sebelum aktif/nonaktif


→ nuwis-ui-builder:
  PAGE_TYPE: list + form (CRUD)

  -- Halaman List Corporate: MustahiqCorporatePage.vue --
  Toolbar: [Search input + kolom pilih] [Tambah button — DIST only]
  Pagination: standalone Paginator di atas DataTable (25 per page)
  DataTable columns: No. Mustahiq | Nama | Alamat | Telepon | Status (badge) | Aksi
  Aksi per-row: Detail (DIST+SPVDIST), Edit (DIST), Hapus (DIST+SPVDIST),
                Aktifkan/NonAktifkan (DIST+SPVDIST)
  Status badge: A=Active (hijau), N=NonActive (merah/abu)
  Modal Tambah/Edit: form dengan bank account sub-table (inline editable)
  Modal Detail: read-only, semua field disabled
  Modal Hapus: tampilkan data lengkap (sesuai delete-form-modal convention)

  FIELDS (form):
    - name*               → Input text         (wajib)
    - address             → Input text
    - address_kelurahan   → Input text
    - address_kecamatan   → Input text
    - province_id         → SearchSelect.vue    (lookup Propinsi)
    - postal_code         → Input text
    - reference_by        → Input text
    - phone_number        → Input text
    - cp_name             → Input text
    - cp_phone_number     → Input text
    - cp_mobile_number    → Input text
    - bank_accounts[]     → Sub-tabel dengan kolom:
                            account_no, account_name, bank_code (lookup Bank),
                            is_default (T/F toggle)

  -- Halaman List Personal: MustahiqPersonalPage.vue --
  Layout/kolom sama dengan Corporate.
  FIELDS tambahan di form Personal:
    - gender              → Dropdown (L/P)
    - ashnaf              → Dropdown (F/M/U/H/G/S/I/A)
    - birth_place         → Input text
    - birth_date          → DateField.vue       (v-model = ISO string)
    - identity_number     → Input text
    - identity_type       → Dropdown (K/S/F/P)
    - religion            → Dropdown (1–6, integer)
    - total_family        → Input number
    - formal_education    → Dropdown (0–6, integer)
    - income              → Input number (decimal, Pendapatan per Bulan)
    - marital             → Dropdown (K/B/S)
    - work_sector         → Dropdown ('1'–'9')
    - bank_accounts[]     → Sub-tabel (sama dengan Corp)

  FILTERS di list:
    - Search text + pilih kolom: Nomor, Nama, Alamat, Telepon, Status
    - Status filter: All | Active | NonActive

  TANGGAL: selalu gunakan DateField.vue untuk birth_date, dmy() untuk display.

==== END MIGRATION_ANALYSIS ====
