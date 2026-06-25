# MIGRATION_ANALYSIS: Donatur Korporat & Individu

## Modul: fundraising.donor
## Portal: zakat
## Tanggal: 2026-06-25

---

## 1. DB Tables (schema fund)

### 1.1 Tabel Induk — fund.donor (Superclass)

Tabel dasar untuk semua donatur (diwariskan CorporateDonor dan IndividualDonor melalui pola table-per-class inheritance DAF).

| Kolom | Tipe | Keterangan |
|---|---|---|
| `donorid` | integer NOT NULL PK | ID donatur (auto-generated via custom_idgen) |
| `donorno` | varchar(20) | Nomor donatur — korporat: `C0000001`, individu: `P0000001` |
| `donorname` | varchar(200) | Nama donatur/perusahaan |
| `donortype` | varchar(1) | Discriminator: belum diperjelas di kode (ada di tabel, tidak di form) |
| `status` | varchar(1) | `'A'` = Aktif, `'N'` = Non-Aktif |
| `branchcode` | varchar(5) | Kode cabang (dari session saat create, via `OnCreate`) |
| `joindate` | timestamp | Tanggal bergabung |
| `npwp` | varchar(50) | Nomor NPWP (15 digit tanpa separator) |
| `npwz` | varchar(30) | Nomor NPWZ (auto-generate dari `GenerateNPWZ()`) |
| `addressstreet` | varchar(200) | Alamat jalan |
| `addresskelurahan` | varchar(100) | Kelurahan |
| `addresskecamatan` | varchar(50) | Kecamatan |
| `addresscity` | varchar(50) | Kota |
| `addresspostalcode` | varchar(10) | Kode pos |
| `addressstate` | varchar(50) | Provinsi (teks, berbeda dari `idpropinsi`) |
| `idpropinsi` | integer | FK ke fund.propinsi.idpropinsi |
| `idnegara` | integer | FK ke fund.negara.idnegara |
| `marketerid` | integer | FK ke fund.marketer.marketerid |
| `economicsector` | varchar(1) | Kode sektor ekonomi (enum) |
| `phonenumber` | varchar(20) | Nomor telepon |
| `fax` | varchar(20) | Nomor fax |
| `referenceby` | varchar(30) | Referensi (tidak ada di form edit) |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/DDL.sql` baris 124–160

### 1.2 Tabel Korporat — fund.corporatedonor

Ekstensi dari fund.donor — joined via PK yang sama (`donorid`).

| Kolom | Tipe | Keterangan |
|---|---|---|
| `donorid` | integer NOT NULL PK/FK | FK ke fund.donor.donorid |
| `corporation` | varchar(1) | Tipe korporat (enum): `'C'`/`'F'` = badan usaha → kode NPWZ `B2`; selainnya → `B1` |
| `siupp` | varchar(20) | Nomor SIUPP perusahaan |
| `tdp` | varchar(20) | Nomor TDP (tidak ada di form edit) |
| `locationtype` | varchar(30) | (tidak ada di form edit) |
| `ownertype` | varchar(30) | (tidak ada di form edit) |
| `establisheddate` | timestamp | Tanggal berdiri (tidak ada di form edit) |
| `establishedplace` | varchar(50) | Tempat berdiri (tidak ada di form edit) |
| `contactperson` | varchar(50) | (deprecated, digantikan cpname) |
| `patronagecompany` | varchar(1) | (tidak ada di form edit) |
| `cpname` | varchar(150) | Nama contact person |
| `cpemail` | varchar(200) | Email contact person |
| `cpphonenumber` | varchar(30) | Telepon contact person |
| `cpmobilenumber` | varchar(30) | HP contact person |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/DDL.sql` baris 78–105

Catatan: kolom `tdp`, `locationtype`, `ownertype`, `establisheddate`, `establishedplace`, `contactperson`, `patronagecompany` tidak dimunculkan di form edit — kemungkinan kolom legacy yang tidak lagi digunakan.

### 1.3 Tabel Individu — fund.individualdonor

Ekstensi dari fund.donor — joined via PK yang sama (`donorid`).

| Kolom | Tipe | Keterangan |
|---|---|---|
| `donorid` | integer NOT NULL PK/FK | FK ke fund.donor.donorid |
| `gender` | varchar(1) | Jenis kelamin (enum) |
| `birthplace` | varchar(30) | Tempat lahir |
| `birthdate` | timestamp | Tanggal lahir |
| `identitytype` | varchar(1) | Tipe identitas — selalu `'K'` (KTP) saat create |
| `identitynumber` | varchar(20) | Nomor KTP |
| `religion` | integer | Agama (enum integer) |
| `language` | varchar(1) | Bahasa (tidak di form edit) |
| `lastformaleducation` | integer | Pendidikan terakhir (tidak di form edit) |
| `incomepermonth` | double precision | Penghasilan/bulan (tidak di form edit) |
| `expensepermonth` | double precision | Pengeluaran/bulan (tidak di form edit) |
| `maritalstate` | varchar(1) | Status pernikahan (enum) |
| `email` | varchar(200) | Email individu |
| `mobilephone` | varchar(20) | Nomor HP |
| `statusrumah` | varchar(1) | Status kepemilikan rumah |
| `officeaddress` | varchar(200) | Alamat kantor |
| `officekelurahan` | varchar(50) | Kelurahan kantor |
| `officekecamatan` | varchar(50) | Kecamatan kantor |
| `officecity` | varchar(50) | Kota kantor |
| `officestate` | varchar(50) | Provinsi kantor (teks) |
| `officepostalcode` | varchar(50) | Kode pos kantor |
| `officephonenumber` | varchar(50) | Telepon kantor |
| `idpropinsioffice` | integer | FK ke fund.propinsi.idpropinsi (kantor) |
| `corporatename` | varchar(50) | Nama perusahaan tempat bekerja |
| `jobposition` | varchar(50) | Jabatan di perusahaan |
| `couplename` | varchar(50) | Nama pasangan |
| `child` | integer | Jumlah anak |
| `fworkid` | integer | FK ke fund.fieldofwork.fworkid — bidang pekerjaan |
| `isinternalemployee` | varchar(1) | `'T'` = karyawan internal, `'F'` = non-karyawan |
| `workidentitynumber` | varchar(30) | NIP karyawan (wajib jika isinternalemployee='T') |
| `workareaid` | integer | FK ke fund.workarea.workareaid (wilayah kantor) |
| `workunitid` | integer | FK ke fund.workunit.workunitid (tidak ada di SVR/form edit) |

**Kolom ada di kode tapi TIDAK di DDL (ditambahkan setelah DDL export):**

| Field (kode) | Keterangan |
|---|---|
| `DonorGroup` | `'R'` = karyawan internal, `'N'` = non-karyawan (dari `create_internal_individualdonor.py` dan `create_nonemployee_individualdonor.py`) |
| `WorkBusinessArea` | Bidang bisnis/divisi (varchar, di SVR sebagai `WorkBusinessArea`) |
| `WorkPosition` | Posisi/jabatan kerja (varchar, di SVR sebagai `WorkPosition`) |
| `WorkAreaIdInitial` | Wilayah asal (FK ke workarea, berbeda dari WorkAreaId) |
| `WorkUnit` | Unit kerja (varchar, berbeda dari `WorkUnitId`) |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/DDL.sql` baris 278–318, dikombinasikan dengan `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fEIndividualDonor2_data.py` fungsi `authorize`

### 1.4 Tabel Pendukung

| Tabel | PK | Keterangan |
|---|---|---|
| `fund.donorbankaccount` | `bankaccountid` | Rekening bank donatur (FK `donorid`) — extends `fund.bankaccountlist` via PK |
| `fund.bankaccountlist` | `bankaccountid` | Daftar rekening bank — kolom: `bankaccountno`, `bankaccountname`, `bankaccountlisttype`, `bankcode`, `isdefault` |
| `fund.donorcommitment` | `commitmentid` | Komitmen donasi rutin — kolom: `commitmentamount` numeric(30,2), `accountno` varchar(30), `donorid` |
| `fund.fieldofwork` | `fworkid` | Bidang pekerjaan — kolom: `fworkcode`, `fworkname`, `fnpwzcode` (dipakai untuk generate NPWZ) |
| `fund.marketer` | `marketerid` | ZIS Account Manager — kolom: `marketercode`, `marketername`, `marketertype`, dsb. |
| `fund.workarea` | `workareaid` | Kantor wilayah — kolom: `workareacode`, `workareaname` |
| `fund.workunit` | `workunitid` | Unit kerja — kolom: `workunitcode`, `workunitname` |
| `fund.propinsi` | `idpropinsi` | Data provinsi |
| `fund.negara` | `idnegara` | Data negara |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/DDL.sql`

---

## 2. Form Fields

### 2.1 Korporat — Create/Edit Fields

Form: `dialogs/Donatur/fTCorporateDonor` (Create) dan `dialogs/Donatur/fECorporateDonor` (Edit)

**Panel: Profil Perusahaan**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `DonorNo` | ID Donatur | Input (ReadOnly) | Auto-generated |
| `DonorName` | Nama Perusahaan | Input (uppercase) | WAJIB |
| `Corporation` | Tipe Korporat | ComboBox (enum) | Optional |
| `EconomicSector` | Jenis Bidang Usaha | ComboBox (enum) | Optional |
| `SIUPP` | SIUPP | Input (uppercase) | Optional |
| `JoinDate` | Tanggal Bergabung | DateEdit | Optional |
| `NPWP` | NPWP | Input (uppercase) | Optional — validasi 15 digit jika diisi |
| `NPWZ` | NPWZ | Input (uppercase) | Optional — validasi 15 digit jika diisi; bisa di-generate |
| `Status` | Status | ComboBox (enum) | Optional — default `'N'` saat create |
| `LMarketer` | Marketer | Lookup (MarketerCode;MarketerName) | Optional |

**Panel: Detail Alamat Perusahaan**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `LNegara` | Negara | Lookup | Optional |
| `LPropinsi` | Propinsi | Lookup | Optional |
| `AddressCity` | Kota | Input (uppercase) | Optional |
| `AddressPostalCode` | Kode Pos | Input (uppercase) | Optional |
| `AddressKecamatan` | Kecamatan | Input (uppercase) | Optional |
| `AddressKelurahan` | Kelurahan | Input (uppercase) | Optional |
| `AddressStreet` | Alamat | Input (uppercase) | Optional |

**Panel: Detail Kontak**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `PhoneNumber` | No Telepon | Input (uppercase) | Optional |
| `Fax` | Fax | Input (uppercase) | Optional |

**Panel: Detail Contact Person**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `CPName` | Nama CP | Input (uppercase) | Optional |
| `CPPhoneNumber` | No Telepon CP | Input (uppercase) | Optional |
| `CPMobileNumber` | No HP CP | Input (uppercase) | Optional |
| `CPEmail` | Email CP | Input (uppercase) | Optional |

**Tab: Rekening (grid — DonorBankAccount)**

| Field | Caption | Widget |
|---|---|---|
| `BankAccountNo` | No Rekening | Input |
| `BankAccountName` | Atas Nama | Input |
| `LBank.BankName` | Nama Bank | Lookup |
| `BankAccountId` | (hidden) | Hidden |

**Tab: Komitmen Donasi (grid — DonorCommitment)**

| Field | Caption | Widget |
|---|---|---|
| `AccountNo` | No Rekening Bank/Kas | Input |
| `CommitmentAmount` | Nominal Komitmen | Input (Currency) |
| `CommitmentId` | (hidden) | Hidden |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fECorporateDonor.dfr`, `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fECorporateDonor.svr`

### 2.2 Individu — Create/Edit Fields

Form: `dialogs/Donatur/fTIndividualDonor` (Create) dan `dialogs/Donatur/fEIndividualDonor2` (Edit)

**Panel: Detail Alamat Tinggal Dan Kontak**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `LNegara` | Negara | Lookup | Optional |
| `LPropinsi` | Propinsi | Lookup | Optional |
| `AddressCity` | Kota | Input | Optional |
| `AddressPostalCode` | Kode Pos | Input | Optional |
| `AddressKecamatan` | Kecamatan | Input | Optional |
| `AddressKelurahan` | Kelurahan | Input | Optional |
| `AddressStreet` | Jalan | Input | Optional |
| `PhoneNumber` | Nomor Telepon | Input | Optional |
| `MobilePhone` | Nomor HP | Input | Optional |
| `Email` | Email | Input | Optional |
| `Fax` | Fax | Input | Optional |
| `StatusRumah` | Kepemilikan Rumah | ComboBox (enum) | Optional |

**Panel: Personal Detail**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `DonorName` | Nama | Input | WAJIB |
| `IdentityNumber` | Nomor KTP | Input | Optional |
| `IdentityType` | Tipe Identitas | (hidden — selalu `'K'`) | Auto-set |
| `Gender` | Jenis Kelamin | ComboBox (enum) | Optional |
| `JoinDate` | Tanggal Bergabung | DateEdit | Optional |
| `BirthPlace` | Tempat Lahir | Input | Optional |
| `BirthDate` | Tanggal Lahir | DateEdit | Optional |
| `Religion` | Agama | ComboBox (enum) | Optional |
| `NPWP` | NPWP | Input | Optional — validasi 15 digit |
| `NPWZ` | NPWZ | Input | Optional — validasi 15 digit |
| `IsInternalEmployee` | Jenis Donatur | ComboBox | Optional — `'T'`=karyawan, `'F'`=non-karyawan |
| `WorkIdentityNumber` | NIP Karyawan | Input | WAJIB jika `IsInternalEmployee='T'` |
| `LWorkArea` | Kantor Wilayah | Lookup | Optional — disabled jika non-karyawan |
| `LWorkAreaInitial` | Kantor Wilayah Asal | Lookup | Optional |
| `WorkUnit` (Unit) | Unit Kerja | Input | Optional — disabled jika non-karyawan |
| `WorkPosition` (Posisi) | Posisi | Input | Optional — disabled jika non-karyawan |
| `WorkBusinessArea` (BisnisArea) | Bidang Bisnis | Input | Optional — disabled jika non-karyawan |
| `EconomicSector` | Bidang Usaha | Input | Optional |
| `LFieldOfWork` | Bidang Pekerjaan | Lookup | Optional |

**Panel: Family Detail**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `MaritalState` | Status Pernikahan | ComboBox (enum) | Optional |
| `CoupleName` | Nama Pasangan | Input | Optional — disabled jika belum menikah |
| `Child` | Jumlah Anak | Input (number) | Optional — disabled jika belum menikah |

**Panel: Office/Work Detail**

| Field | Caption | Widget | Required |
|---|---|---|---|
| `OfficeAddress` | Alamat Kantor | Input | Optional |
| `OfficeKelurahan` | Kelurahan Kantor | Input | Optional |
| `OfficeKecamatan` | Kecamatan Kantor | Input | Optional |
| `OfficeCity` | Kota Kantor | Input | Optional |
| `LPropinsiOffice` | Propinsi Kantor | Lookup | Optional |
| `OfficePhoneNumber` | Telepon Kantor | Input | Optional |
| `CorporateName` | Nama Perusahaan | Input | Optional |
| `JobPosition` | Jabatan | Input | Optional |
| `DonorGroup` | Grup Donatur | (tidak di form edit, di-set saat create) | Auto-set |
| `LMarketer` | Marketer | Lookup | Optional |

**Tab: Rekening (grid — DonorBankAccount)**

Sama dengan korporat: `BankAccountNo`, `BankAccountName`, `LBank.BankName`.

**Tab: Komitmen Donasi (grid — uipKosong)**

| Field | Caption | Widget |
|---|---|---|
| `AccountNo` | No Account | Lookup ke transaction.BankCash |
| `CommitmentAmount` | Nominal Komitmen | Input (Currency) |
| `BankAccountNo` | No Rekening Bank | Auto-fill dari lookup |
| `BankName` | Nama Bank | Auto-fill dari lookup |
| `AccountName` | Nama Akun | Auto-fill dari lookup |
| `CommitmentId` | (hidden) | Hidden — 0/None = baru |

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fEIndividualDonor2.svr`, `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fTIndividualDonor_data.py`

---

## 3. List/Grid Columns

### 3.1 Korporat — Grid Columns (fCorporateDonor)

Query OQL dari `fCorporateDonor_intr.py` fungsi `Cari`:

| Field | Caption |
|---|---|
| `DonorId` | ID |
| `DonorNo` | ID Donatur |
| `DonorType` (enum) | Tipe |
| `DonorName` | Nama |
| `JoinDate` | Tanggal Bergabung |
| `SIUPP` | SIUPP |
| `Corporation` (enum) | Tipe Korporat |
| `EconomicSector` (enum) | Jenis Bidang Usaha |
| `PhoneNumber` | Nomor Telepon |
| `Fax` | Fax |
| `AddressStreet` | Alamat Tinggal |
| `Lpropinsi.Propinsi` | Propinsi |
| `CPName` | Nama CP |
| `CPEmail` | Email CP |
| `CPMobileNumber` | No HP CP |
| `NPWP` | NPWP |
| `NPWZ` | NPWZ |
| `Status` (enum) | Status |

Order: `DESC DonorId` (terbaru di atas).

Filter/Pencarian via kriteria: `N`=Nama, `I`=ID Donatur, `A`=Alamat, `C`=Nama CP, `T`=Telepon, `E`=Email, `S`=Status, `P`=Tipe Korporat, `J`=Bidang Usaha, `U`=SIUPP, `F`=Fax.

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fCorporateDonor_intr.py` fungsi `Cari`

### 3.2 Individu — Grid Columns (fIndividualDonor)

Query OQL dari `fIndividualDonor_intr.py` fungsi `Cari`:

| Field | Caption |
|---|---|
| `DonorId` | ID |
| `DonorNo` | ID Donatur |
| `DonorType` (enum) | Tipe |
| `DonorName` | Nama |
| `JoinDate` | Tanggal Bergabung |
| `IdentityNumber` | Nomor KTP |
| `Gender` (enum) | Jenis Kelamin |
| `BirthPlace` | Tempat Lahir |
| `BirthDate` | Tanggal Lahir |
| `Religion` (enum) | Agama |
| `MaritalState` (enum) | Status Pernikahan |
| `MobilePhone` | No HP |
| `PhoneNumber` | Nomor Telepon |
| `Fax` | Fax |
| `AddressStreet` | Alamat |
| `Lpropinsi.Propinsi` | Propinsi |
| `OfficeAddress` | Alamat Kantor |
| `NPWP` | NPWP |
| `NPWZ` | NPWZ |
| `Status` (enum) | Status |

Order: `ASC DonorId`.

Filter/Pencarian via kriteria: `N`=Nama, `I`=ID Donatur, `A`=Alamat, `C`=Nama CP, `T`=Telepon, `E`=Email, `S`=Status, `P`=Korporat, `J`=Bidang Usaha, `U`=SIUPP, `F`=Fax, `D`=Nomor KTP.

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fIndividualDonor_intr.py` fungsi `Cari`

---

## 4. Business Rules

### 4.1 Save Logic — Donatur Korporat Create

Entry point: `fTCorporateDonor_data.py` fungsi `save` (kode entri: `FUND005`)

1. Validasi client-side:
   - `DonorName` wajib diisi (raise jika None)
   - `NPWP` jika diisi: hapus `.` dan `-`, cek panjang = 15 digit
   - `NPWZ` jika diisi: hapus `.` dan `-`, cek panjang = 15 digit
2. Tidak langsung INSERT ke DB — data dikirim ke otorisasi via `app.rexecscript("enterprise", "api/otorisasi.storeDataPacket", ph)` dengan `kode_entri='FUND005'`, `id_peran='SPVPHP'`
3. Setelah supervisor approve (authorize), fungsi `authorize` di `fTCorporateDonor_data.py` dijalankan:
   - `helper.CreatePObject('CorporateDonor')` → trigger `OnCreate`:
     - Ambil `BranchCode` dari session
     - Set `Status='A'`
     - Generate `DonorNo = 'C' + zfill(7)` via `custom_idgen('DONOR','C')`
   - Set semua field dari form
   - Default `Status='N'` jika kosong
   - Loop create `DonorBankAccount` (untuk setiap rekening di grid)
   - Loop create `DonorCommitment` (untuk setiap komitmen di grid)
   - Jika ada `DonorProspectiveId` → update `DonorProspective.DonorNo`

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fTCorporateDonor_data.py`

### 4.2 Save Logic — Donatur Korporat Edit

Entry point: `fECorporateDonor_data.py` fungsi `save` (kode entri: `FUND006`)

1. Validasi client-side: sama dengan create
2. Kirim ke otorisasi: `kode_entri='FUND006'`, `nama_tabel='Donor'`, `key_string=str(DonorId)`, `id_peran='SPVPHP'`
3. Setelah approve, fungsi `authorize` di `fECorporateDonor_data.py`:
   - `helper.GetObject('CorporateDonor', donorid)` → UPDATE record
   - Update semua field
   - Loop upsert `DonorBankAccount`: jika `BankAccountId==0` → create, else → update

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fECorporateDonor_data.py`

### 4.3 Save Logic — Donatur Individu Create

Entry point: `fTIndividualDonor_data.py` fungsi `save` (kode entri: `FUND007`)

1. Validasi client-side:
   - `DonorName` wajib
   - `NPWP` validasi 15 digit jika diisi
   - `NPWZ` validasi 15 digit jika diisi
   - Jika `IsInternalEmployee='T'`: `WorkIdentityNumber` wajib
   - Cek uniqueness NIP: `GetObjectByNames('IndividualDonor', {IsInternalEmployee:'T', WorkIdentityNumber: NIP})` — raise jika sudah ada
2. Kirim ke otorisasi: `kode_entri='FUND007'`, `id_peran='SPVPHP'`
3. Setelah approve, fungsi `authorize` di `fTIndividualDonor_data.py`:
   - `helper.CreatePObject('IndividualDonor')` → trigger `OnCreate`:
     - Generate `DonorNo = 'P' + zfill(7)` via `custom_idgen('DONOR','P')`
     - Set `BranchCode` dari session, `Status='A'`
   - Set `IdentityType='K'` (hardcoded)
   - Set semua field dari form
   - Default `Status='N'` jika kosong
   - Loop create `DonorBankAccount`
   - Loop create `DonorCommitment`
   - Jika ada `DonorProspectiveId` → update `DonorProspective.DonorNo`

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fTIndividualDonor_data.py`

### 4.4 Save Logic — Donatur Individu Edit

Entry point: `fEIndividualDonor2_data.py` fungsi `save` (kode entri: `FUND008`)

1. Validasi: sama dengan create; tambahan uniqueness NIP hanya jika NIP berubah
2. Kirim ke otorisasi: `kode_entri='FUND008'`, `nama_tabel='Donor'`, `key_string=str(DonorId)`, `id_peran='SPVPHP'`
3. Setelah approve, fungsi `authorize` di `fEIndividualDonor2_data.py`:
   - `helper.GetObject('IndividualDonor', donorid)` → UPDATE
   - Update semua field
   - Loop upsert `DonorCommitment` via `uipKosong`
   - (Rekening bank dikomentari — tidak diupdate saat edit individu)

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/dialogs/Donatur/fEIndividualDonor2_data.py`

### 4.5 Nonaktif / Aktifkan (tidak lewat otorisasi)

Fungsi `NonAktif` dan `Aktif` di `fCorporateDonor_data.py` dan `fIndividualDonor_data.py`:
- Langsung UPDATE `Status='N'` atau `Status='A'` via `CreatePObjImplProxy`
- Tidak melalui otorisasi (maker-checker bypass)
- Akses: popup menu, AllowedGroups `'ADM;PHP'`

### 4.6 Generate NPWZ

Fungsi `GenerateNPWZ()` di `DonaturModule.py` (kelas `IndividualDonor` dan `CorporateDonor`):
- Syarat individu: `FWorkId != 0` AND `NPWP != ''` AND `EconomicSector != ''`
- Syarat korporat: `Corporation != 0` AND `NPWP != ''` AND `EconomicSector != ''`
- Format korporat: `{CorporationCode}.{seq6}.{EconomicSector}.{KPP}.{PKPP}`
  - `CorporationCode`: `'B2'` jika `Corporation in ('C','F')`, else `'B1'`
- Format individu: `{FNPWZCode}.{seq6}.{EconomicSector}.{KPP}.{PKPP}`
  - `FNPWZCode` berasal dari `FieldOfWork.FNPWZCode.replace('0','B')`
- Sequence dari `custom_idgen('DONOR.EconomicSector', EconomicSector)`

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/script_modules/DonaturModule.py` baris 101–175

---

## 5. CRUD Operations

| Operasi | Korporat | Individu | Keterangan |
|---|---|---|---|
| **Create** | Ya | Ya | Via otorisasi (FUND005/FUND007), approve oleh SPVPHP |
| **Read/View** | Ya (fVCorporateDonor) | Ya (fViewIndividualDonor2) | Read-only view form |
| **Update** | Ya | Ya | Via otorisasi (FUND006/FUND008), approve oleh SPVPHP |
| **Delete** | Tidak ada | Tidak ada | Tidak ditemukan delete function di popup menu |
| **Nonaktifkan** | Ya | Ya | Langsung ubah status='N', TIDAK via otorisasi |
| **Aktifkan** | Ya | Ya | Langsung ubah status='A', TIDAK via otorisasi |
| **Generate NPWZ** | Ya | Ya | Aksi khusus, TIDAK via otorisasi |
| **History** | Ya (fHCorporateDonor) | Ya (fHIndividualDonor) | Laporan history berdasarkan JoinDate range |

**Approval Workflow:**
- Create dan Edit keduanya melalui otorisasi enterprise (`kode_entri=FUND005/006/007/008`)
- Approver role: `SPVPHP` (Supervisor Penghimpunan)
- Mekanisme: `app.rexecscript("enterprise", "api/otorisasi.storeDataPacket")` — ini adalah sistem otorisasi legacy yang berbeda dari sistem `otorisasi` isf-app yang sudah ada

**Delete:** Tidak tersedia — donatur tidak dihapus, hanya dinonaktifkan (soft status change).

**Pre-fill dari DonorProspective:** Jika donatur berasal dari prospek, field-field tertentu di-pre-fill dari `fund.donorprospective` saat form dibuka.

Sumber: `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/menus/popupmenus/transaksi/Donor/MenuDonorCorp.mnu`, `/home/wishnew/workshop/isf-app/docs/legacy-apps/fund/menus/popupmenus/donatur/MenuDonorIndividu.mnu`

---

## 6. Discriminators / Special Fields

| Field | Nilai | Artinya | Lokasi | Catatan |
|---|---|---|---|---|
| `donorno` | prefix `'C'` | Donatur Korporat | `fund.donor` | Generate via `custom_idgen('DONOR','C')` |
| `donorno` | prefix `'P'` | Donatur Individu | `fund.donor` | Generate via `custom_idgen('DONOR','P')` |
| `status` | `'A'` | Aktif | `fund.donor` | Operasi nonaktif/aktif langsung (bypass otorisasi) |
| `status` | `'N'` | Non-Aktif | `fund.donor` | Default saat create jika tidak diisi |
| `isinternalemployee` | `'T'` | Karyawan Internal Mandiri | `fund.individualdonor` | Wajib input NIP; field kerja diaktifkan |
| `isinternalemployee` | `'F'` | Non-Karyawan | `fund.individualdonor` | Field kerja di-disable |
| `donorgroup` | `'R'` | Registrasi karyawan internal | `fund.individualdonor` (?) | Di-set di `create_internal_individualdonor.py` |
| `donorgroup` | `'N'` | Non-karyawan | `fund.individualdonor` (?) | Di-set di `create_nonemployee_individualdonor.py` |
| `identitytype` | `'K'` | KTP | `fund.individualdonor` | Hardcoded saat create (`tambah.IdentityType='K'`) |
| `corporation` | `'C'`, `'F'` | Perusahaan/yayasan → NPWZ code `B2` | `fund.corporatedonor` | Menentukan prefix NPWZ |
| `corporation` | selainnya | Bukan perusahaan → NPWZ code `B1` | `fund.corporatedonor` | |
| `branchcode` | dari session | Cabang saat registrasi | `fund.donor` | Di-set via `config.SecurityContext.GetUserInfo()[4]` |

**KRITIS — jangan hilangkan saat implementasi:**
- `donorno` dengan prefix `C`/`P` — format ini digunakan di laporan dan tampilan
- `identitytype='K'` — selalu hardcoded
- `isinternalemployee` — menentukan field yang wajib/tersedia
- `donorgroup` — membedakan jalur registrasi (manual vs otomatis dari sistem karyawan)

---

## 7. API Endpoints yang Dibutuhkan (rancangan)

### Donatur Korporat

```
GET    /api/fundraising/donors/corporate
       params: page, limit, search, search_by (name/donor_no/address/cp_name/phone/email/npwp/status/corporation/sector/siupp/fax), status
       response: { data: [...], pagination: {...} }

POST   /api/fundraising/donors/corporate
       body: { donor_name, corporation, economic_sector, siupp, join_date, npwp, npwz, status, marketer_id, address_*, id_propinsi, id_negara, cp_name, cp_phone, cp_mobile, cp_email, phone_number, fax, bank_accounts: [...], commitments: [...] }

GET    /api/fundraising/donors/corporate/{donor_id}
       response: { data: { ...semua field + bank_accounts + commitments } }

PUT    /api/fundraising/donors/corporate/{donor_id}
       body: sama dengan POST

PATCH  /api/fundraising/donors/corporate/{donor_id}/status
       body: { status: 'A'|'N' }

POST   /api/fundraising/donors/corporate/{donor_id}/generate-npwz
       (tidak ada body — generate dari data yang sudah ada)
```

### Donatur Individu

```
GET    /api/fundraising/donors/individual
       params: page, limit, search, search_by, status

POST   /api/fundraising/donors/individual
       body: { donor_name, identity_number, gender, join_date, birth_place, birth_date, religion, marital_state, mobile_phone, phone_number, fax, email, address_*, id_propinsi, id_negara, marketer_id, npwp, npwz, status, is_internal_employee, work_identity_number, work_area_id, work_area_id_initial, work_unit, work_position, work_business_area, economic_sector, fwork_id, status_rumah, corporate_name, job_position, couple_name, child, donor_group, office_*, id_propinsi_office, bank_accounts: [...], commitments: [...] }

GET    /api/fundraising/donors/individual/{donor_id}
       response: { data: { ...semua field + bank_accounts + commitments } }

PUT    /api/fundraising/donors/individual/{donor_id}

PATCH  /api/fundraising/donors/individual/{donor_id}/status
       body: { status: 'A'|'N' }

POST   /api/fundraising/donors/individual/{donor_id}/generate-npwz
```

### Lookup Endpoints

```
GET    /api/fundraising/lookup/field-of-work
       response: [{ fwork_id, fwork_code, fwork_name, fnpwz_code }]

GET    /api/fundraising/lookup/work-areas
       response: [{ work_area_id, work_area_code, work_area_name }]

GET    /api/fundraising/lookup/marketers
       response: [{ marketer_id, marketer_code, marketer_name }]

GET    /api/fundraising/lookup/provinces
       response: [{ id_propinsi, propinsi }]

GET    /api/fundraising/lookup/countries
       response: [{ id_negara, nama_negara }]
```

---

## 8. Lookup / Reference Data

| Data | Tabel | Field Tampil | Dipakai di |
|---|---|---|---|
| Tipe Korporat | Enum dalam kode | (Corporation: C/F/dll) | Form korporat |
| Bidang Usaha | Enum dalam kode | (EconomicSector: kode 1 huruf) | Form korporat & individu |
| Status Aktif | Enum dalam kode | A/N | List + form |
| Gender | Enum dalam kode | L/P/dll | Form individu |
| Agama | Enum integer dalam kode | integer enum | Form individu |
| Status Pernikahan | Enum dalam kode | M/S/dll | Form individu |
| Kepemilikan Rumah | Enum dalam kode | varchar(1) | Form individu |
| Jenis Donatur | Enum boolean T/F | IsInternalEmployee | Form individu |
| Bidang Pekerjaan | `fund.fieldofwork` | fwork_code, fwork_name | Form individu |
| Kantor Wilayah | `fund.workarea` | work_area_code, work_area_name | Form individu |
| Marketer | `fund.marketer` | marketer_code, marketer_name | Form korporat & individu |
| Provinsi | `fund.propinsi` | propinsi | Form korporat & individu |
| Negara | `fund.negara` | nama_negara | Form korporat & individu |
| Bank | `transaction.bank` | bank_code, bank_name | Tab Rekening |
| Rekening Kas/Bank | `transaction.BankCash` | account_no, account_name, bank_account_no, bank_name | Tab Komitmen individu |

**Catatan penting:** Enum values (Corporation, EconomicSector, Gender, Religion, MaritalState, dll) disimpan dalam sistem enum DAF (`fund.enum_varchar`, `fund.enum_int`) — nilai aktualnya perlu diverifikasi langsung dari database produksi atau tabel enum legacy.

---

## 9. Migration Risks

### 9.1 Otorisasi Legacy vs Otorisasi isf-app

**RESIKO TINGGI.** Semua operasi Create dan Edit donatur melewati otorisasi enterprise legacy (`app.rexecscript("enterprise", "api/otorisasi.storeDataPacket")`), bukan tabel `otorisasi.submission` yang dipakai isf-app. Ini artinya:

- Belum ada `entity_type` untuk donatur di `otorisasi.entity_config` isf-app
- Dispatcher untuk donatur belum didaftarkan di `otorisasi/service.py`
- Perlu menambah `entity_type='donor_corporate'` dan `'donor_individual'` ke otorisasi isf-app
- Approver role `SPVPHP` perlu dipetakan ke role isf-app

### 9.2 Kolom Tidak ada di DDL

Beberapa field yang dipakai di kode (`DonorGroup`, `WorkBusinessArea`, `WorkPosition`, `WorkAreaIdInitial`, `WorkUnit` sebagai varchar) tidak muncul di DDL.sql yang tersedia. DDL.sql kemungkinan versi lama. Perlu:
- Verifikasi schema aktual di database produksi (`SELECT column_name FROM information_schema.columns WHERE table_schema='fund' AND table_name IN ('donor','individualdonor')`)
- Kemungkinan migration baru diperlukan untuk kolom-kolom ini jika belum ada

### 9.3 Inheritance Tabel (Table-per-Class)

DAF menggunakan pola JOIN antara `fund.donor` (superclass) + `fund.corporatedonor` atau `fund.individualdonor`. Di isf-app, perlu memutuskan:
- Opsi A: Tetap dua tabel, query pakai JOIN
- Opsi B: Merge ke satu tabel dengan nullable columns
- Rekomendasi: Opsi A (tetap JOIN) untuk backward compatibility dan integritas data

### 9.4 Custom ID Generation

Penomoran `DonorNo` menggunakan `fund.custom_idgen` (tabel sequence per prefix). Di isf-app perlu mereplikasi logika ini atau menggunakan mekanisme sequence PostgreSQL baru dengan format yang kompatibel (`C0000001`, `P0000001`).

### 9.5 Nonaktif/Aktifkan Bypass Otorisasi

Operasi nonaktif/aktifkan dilakukan langsung tanpa otorisasi maker-checker. Di isf-app perlu keputusan apakah tetap langsung atau lewat otorisasi.

### 9.6 Enum Values Tidak Terdokumentasi

Nilai aktual untuk `Corporation`, `EconomicSector`, `Gender`, `Religion`, `MaritalState`, `StatusRumah`, `DonorType` tidak tercantum di DDL. Nilai-nilai ini perlu diambil dari `fund.enum_varchar` / `fund.enum_int` di database produksi.

### 9.7 DonorProspective Pre-fill

Form create bisa menerima parameter `DonorProspectiveId` untuk pre-fill dari data prospek. Jika migrasi modul prospek juga dilakukan, flow ini perlu dijaga.

### 9.8 NPWZ Generation

Algoritma generate NPWZ cukup spesifik (bergantung pada `FieldOfWork.FNPWZCode`, `EconomicSector`, sequence, dan 6 digit terakhir NPWP). Perlu diimplementasi ulang di Python service dengan presisi penuh.

---

## Handoff ke Builders

### nuwis-seed-gen

```
MENU_KEY: fundraising.donor.corporate.list  / LABEL: Data Donatur Korporat     / ROLES: ADM, FUND, PHP
MENU_KEY: fundraising.donor.corporate.create / LABEL: Tambah Donatur Korporat   / ROLES: ADM, PHP
MENU_KEY: fundraising.donor.corporate.edit   / LABEL: Ubah Donatur Korporat     / ROLES: ADM, PHP
MENU_KEY: fundraising.donor.individual.list  / LABEL: Data Donatur Individu     / ROLES: ADM, FUND, PHP
MENU_KEY: fundraising.donor.individual.create / LABEL: Tambah Donatur Individu  / ROLES: ADM, PHP
MENU_KEY: fundraising.donor.individual.edit   / LABEL: Ubah Donatur Individu    / ROLES: ADM, PHP
```

**AMBIGU:** Role `PHP` (Penghimpunan) dan `SPVPHP` tidak ada dalam tabel mapping role isf-app yang diketahui. Perlu dikonfirmasi ke nuwis-architect. Kemungkinan mapping:
- `PHP` → `FUND` (fundraising staff)
- `SPVPHP` → `SPVFUND` atau role supervisor baru

### nuwis-db-migrator

```
MIGRATIONS YANG DIPERLUKAN:
- Verifikasi kolom DonorGroup, WorkBusinessArea, WorkPosition, WorkAreaIdInitial, WorkUnit di fund.individualdonor
  → Jika belum ada: tambahkan via migration Vxxx__add_individualdonor_work_fields.sql

TIDAK ADA DWH VIEWS BARU (ini master data, bukan laporan)
```

### nuwis-python-builder

```
ENDPOINTS (api-python):
  POST   /api/fundraising/donors/corporate             → service create_corporate_donor()
  GET    /api/fundraising/donors/corporate             → service list_corporate_donors() + pagination
  GET    /api/fundraising/donors/corporate/{id}        → service get_corporate_donor()
  PUT    /api/fundraising/donors/corporate/{id}        → service update_corporate_donor()
  PATCH  /api/fundraising/donors/corporate/{id}/status → service toggle_corporate_donor_status()
  POST   /api/fundraising/donors/corporate/{id}/generate-npwz → service generate_corporate_npwz()
  POST   /api/fundraising/donors/individual            → service create_individual_donor()
  GET    /api/fundraising/donors/individual            → service list_individual_donors() + pagination
  GET    /api/fundraising/donors/individual/{id}       → service get_individual_donor()
  PUT    /api/fundraising/donors/individual/{id}       → service update_individual_donor()
  PATCH  /api/fundraising/donors/individual/{id}/status → service toggle_individual_donor_status()
  POST   /api/fundraising/donors/individual/{id}/generate-npwz → service generate_individual_npwz()
  GET    /api/fundraising/lookup/field-of-work         → lookup fieldofwork
  GET    /api/fundraising/lookup/work-areas            → lookup workarea
  GET    /api/fundraising/lookup/marketers             → lookup marketer
  GET    /api/fundraising/lookup/provinces             → lookup propinsi
  GET    /api/fundraising/lookup/countries             → lookup negara

DISCRIMINATORS (jangan rename):
  fund.donor.status: 'A'=Aktif, 'N'=Non-Aktif
  fund.donor.donorno: prefix 'C'=korporat, 'P'=individu
  fund.individualdonor.isinternalemployee: 'T'=karyawan, 'F'=non-karyawan
  fund.individualdonor.identitytype: 'K'=KTP (selalu hardcoded)
  fund.individualdonor.donorgroup: 'R'=registrasi karyawan, 'N'=non-karyawan
  fund.corporatedonor.corporation: 'C'/'F' → npwz_prefix='B2', lainnya → 'B1'

BUSINESS RULES KRITIS:
  - DonorNo generate: format 'C'+7digit atau 'P'+7digit via sequence fund.custom_idgen
  - BranchCode dari session user (bukan input form)
  - NIP uniqueness check untuk karyawan internal (WorkIdentityNumber)
  - NPWP validasi: 15 digit setelah strip '.' dan '-'
  - NPWZ validasi: 15 digit setelah strip '.' dan '-'
  - Otorisasi: semua CREATE dan UPDATE via otorisasi.submission (entity_type='donor_corporate'/'donor_individual')
  - Nonaktif/Aktifkan: langsung PATCH tanpa otorisasi
```

### nuwis-ui-builder

```
PAGE_TYPE: list + form (terpisah per tipe donatur)

PAGES YANG DIBUTUHKAN:
  1. CorporateDonorListPage (list)
  2. CorporateDonorFormPage (create/edit — sama form, mode ditentukan param)
  3. IndividualDonorListPage (list)
  4. IndividualDonorFormPage (create/edit — sama form, mode ditentukan param)

FIELDS KORPORAT FORM:
  - Profil: donor_no (readonly), donor_name*, corporation (select), economic_sector (select), siupp, join_date (DateField), npwp, npwz, status (select), marketer_id (SearchSelect)
  - Alamat: negara (SearchSelect), propinsi (SearchSelect), address_city, address_postal_code, address_kecamatan, address_kelurahan, address_street
  - Kontak: phone_number, fax
  - CP: cp_name, cp_phone, cp_mobile, cp_email
  - Tab Rekening: grid bank_accounts (bank_account_no, bank_account_name, bank_name)
  - Tab Komitmen: grid commitments (account_no, commitment_amount, bank_name)

FIELDS INDIVIDU FORM (tabbed/paneled):
  - Personal: donor_name*, identity_number, gender (select), join_date (DateField), birth_place, birth_date (DateField), religion (select), npwp, npwz, is_internal_employee (select — toggle NIP/work fields)
  - Alamat: negara, propinsi, address_*, phone_number, mobile_phone, email, fax, status_rumah (select)
  - Pekerjaan: is_internal_employee (toggle), work_identity_number (enabled jika karyawan), work_area_id (SearchSelect), work_area_id_initial (SearchSelect), work_unit, work_position, work_business_area, economic_sector, fwork_id (SearchSelect), corporate_name, job_position, marketer_id (SearchSelect)
  - Keluarga: marital_state (select), couple_name (disabled jika lajang), child (disabled jika lajang)
  - Alamat Kantor: office_address, office_kelurahan, office_kecamatan, office_city, propinsi_office (SearchSelect), office_phone_number
  - Tab Rekening: grid bank_accounts
  - Tab Komitmen: grid commitments

FILTERS LIST:
  Korporat: search (text), search_by (select: nama/id/alamat/cp/telepon/email/npwp/status/korporat/sektor/siupp/fax), status (select: semua/aktif/nonaktif)
  Individu: search (text), search_by (select: nama/id/alamat/ktp/telepon/email/status), status (select: semua/aktif/nonaktif)
```

---

==== END MIGRATION_ANALYSIS ====
