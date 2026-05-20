# Product Requirements Document — Portal ZISWAF (`isf-app`)

| Atribut | Nilai |
| --- | --- |
| Nama Produk | `isf-app` — Portal ZISWAF |
| Versi Dokumen | 0.3 (Split portal per domain — zakat + wakaf) |
| Tanggal | 2026-05-20 |
| Status | Aktif |
| Dokumen Terkait | [`docs/architecture.md`](./architecture.md) |

## 1. Ringkasan Eksekutif

`isf-app` adalah portal internal yang menyatukan data operasional ZISWAF (Zakat, Infaq, Sadaqah, Wakaf) dari empat domain utama — **keuangan, program, penghimpunan, dan back office** — ke dalam satu aplikasi web. Portal ini melayani **dua perusahaan/lembaga ZISWAF** yang dikelola di bawah satu manajemen, sehingga satu akun pengguna dapat mengakses data kedua perusahaan secara terpisah (multi-tenant).

Untuk **MVP**, scope dibatasi pada **dummy login + dashboard skeleton** dengan tenant switcher, sebagai pondasi yang akan dikembangkan bertahap menjadi portal penuh. Portal menggunakan **basis data yang sudah berjalan** (existing DB) — tidak ada perubahan skema pada fase awal.

### 1.1 Strategi rilis (sejak v0.2 — read-first)

Karena **existing database sudah berisi data ZISWAF dari sistem berjalan**, portal ini fokus dulu pada **pengalaman read** (dashboard kaya + laporan baik) sebelum membangun fitur input. Pengguna langsung dapat manfaat dari visualisasi & laporan tanpa migrasi data input.

Fitur input transaksional (penyaluran, posting jurnal, dll) dimulai setelah fondasi read & UX matang, dengan workflow otorisasi maker–checker (§7.8). Reorder roadmap lengkap di §10.

### 1.2 Portal terpisah per domain + multi-cabang

Mulai v0.3, portal dipecah menjadi **dua aplikasi independen** karena domain bisnis berbeda dan akan bercabang luas seiring waktu:

- **isf-app-zakat** — portal untuk lembaga LAZ (zakat, infaq, sadaqah). DB: `mziss_laz`.
- **isf-app-wakaf** — portal untuk lembaga wakaf. DB: `mzis_wakaf`.

Tiap portal **single-tenant** (hanya kenal perusahaannya sendiri) tetapi **multi-cabang** (perusahaan tersebut punya beberapa cabang). Lihat §7.2.

Untuk pengalaman "satu login untuk dua portal": gunakan **Google SSO** sebagai shared identity (sudah didesain di [`docs/plan-auth.md`](./plan-auth.md)). Setiap portal verify token Google mandiri, tapi user merasa seamless. Alternatif: login terpisah di tiap portal (lebih sederhana, kurang seamless).

## 2. Konteks & Latar Belakang

Saat ini data operasional kedua lembaga ZISWAF tersebar di berbagai sistem dan laporan terpisah. Manajemen membutuhkan satu pintu akses untuk:

- Memantau capaian penghimpunan dan penyaluran lintas perusahaan.
- Melihat realisasi program dan posisi keuangan secara konsolidasi maupun per entitas.
- Mengurangi waktu yang habis untuk menyusun laporan manual dari beberapa sumber.
- Menjaga jejak audit perubahan data sensitif (mustahik, muzakki, transaksi).

Portal ini juga menjadi fondasi modernisasi sistem ZISWAF: stack baru (Vue + Vite frontend, FastAPI BFF, Python backend dengan migrasi bertahap ke Go) dipilih agar evolusi sistem ke depan tidak perlu rewrite menyeluruh (lihat [`docs/architecture.md`](./architecture.md)).

## 3. Tujuan Bisnis & Sasaran

### 3.1 Tujuan

1. **Sentralisasi akses data ZISWAF** lintas dua lembaga di satu portal.
2. **Mempercepat pengambilan keputusan** dengan ringkasan KPI real-time atau near-real-time.
3. **Meningkatkan akuntabilitas** melalui audit trail dan kontrol akses berbasis peran.
4. **Mengurangi pekerjaan manual** penyusunan laporan dari beberapa sumber.
5. **Menyiapkan fondasi teknis** yang siap di-evolve menjadi platform yang lebih luas (mobile, partner, gateway publik).

### 3.2 Sasaran kualitatif

- Pimpinan dapat melihat ringkasan kondisi ZISWAF kedua perusahaan dalam < 1 menit sejak login.
- Pengguna lintas peran (finance, program, fundraiser, back office) bekerja di satu portal yang sama tanpa berpindah aplikasi.
- Setiap perubahan data tercatat lengkap (siapa, kapan, perusahaan mana).
- Penambahan modul atau migrasi backend tidak mengubah pengalaman pengguna.

> KPI numerik (mis. jumlah pengguna aktif, frekuensi akses) akan ditetapkan bersama stakeholder pada saat sign-off PRD ini.

## 4. Stakeholder & Pengguna

### 4.1 Stakeholder bisnis

| Peran | Tanggung jawab |
| --- | --- |
| Sponsor / Direksi | Memberi mandat, sign-off scope, prioritas |
| Product Owner | Memutuskan prioritas fitur, memvalidasi requirement |
| Domain Lead (Keuangan, Program, Penghimpunan) | Memberi input requirement modul, melakukan UAT |
| IT Lead | Memvalidasi kelayakan teknis, ownership existing DB |

### 4.2 Persona pengguna

| Persona | Aktivitas utama di portal |
| --- | --- |
| **Pimpinan / Eksekutif** | Melihat dashboard, monitor KPI, mengakses laporan ringkas |
| **Finance** | Mengelola dan melihat laporan keuangan ZISWAF, distribusi per asnaf |
| **Program Manager** | Mengelola daftar program, memantau realisasi, mengakses data penerima manfaat |
| **Fundraiser / Penghimpun** | Memantau capaian penghimpunan, daftar donatur/muzakki, channel |
| **Back Office Admin** | Mengelola user, role, master data, mengakses audit log |

## 5. Scope

### 5.1 In-scope (Portal penuh)

**Tahap awal (Fase 1–3) — Read & visualisasi:**

- Autentikasi & manajemen sesi (Fase 1 dummy → Fase 3 production cookie httpOnly).
- Single-tenant per portal + multi-cabang dengan switcher cabang dalam portal.
- Dashboard per peran dengan beragam view (KPI, trend, distribusi, capaian, transaksi terbaru).
- Modul Keuangan — **read & laporan**: penerimaan, penyaluran, saldo per dana, distribusi asnaf, drill-down per cabang, export.
- Modul Program — **read**: daftar/status/realisasi program, penerima manfaat.
- Modul Penghimpunan — **read**: capaian, channel, donatur, target vs realisasi.
- Manajemen user portal & role-cabang (Fase 3) — write **terbatas pada user portal**, bukan data bisnis.
- Audit log viewer (Fase 3).

**Tahap berikutnya (Fase 4–5) — Write & operasional:**

- Input penyaluran dengan workflow otorisasi maker–checker (§7.8).
- Posting jurnal keuangan ke buku besar.
- Pengajuan/perubahan program.
- Registrasi wakaf produktif.
- Perubahan master data (COA, asnaf, channel, cabang) bila lembaga ingin self-manage.
- Provisioning user & role escalation.

RBAC scoped per (perusahaan × cabang).

### 5.2 Out-of-scope (eksplisit, untuk versi ini)

- Portal donatur publik (donasi online untuk masyarakat umum).
- Aplikasi mobile native iOS/Android.
- Integrasi langsung dengan sistem eksternal (mis. SIMBA BAZNAS, perbankan, e-wallet) — dapat dipertimbangkan di fase lanjutan.
- Self-service registrasi user oleh publik.
- Migrasi atau perombakan skema existing DB.
- Modul akuntansi penuh (jurnal, neraca, GL); portal hanya menampilkan/agregasi.
- Workflow approval lintas modul yang kompleks (beyond satu lapis approval).

## 6. Asumsi, Constraint & Dependency

### 6.1 Asumsi

- Dua lembaga ZISWAF berada di bawah satu manajemen induk; user dikelola terpusat.
- Existing DB memiliki struktur data yang cukup lengkap untuk modul-modul yang direncanakan.
- Pengguna mengakses portal melalui jaringan internal/VPN organisasi (tidak public-facing di fase awal).
- Stakeholder bersedia menyediakan domain lead untuk validasi setiap modul.
- Setiap perusahaan ZISWAF memiliki struktur cabang (mis. cabang regional / kantor cabang). Existing DB sudah merepresentasikan cabang (kolom `branch_id` di tabel transaksi); portal mengikuti struktur existing tanpa schema migration.
- User dapat punya akses ke 1+ cabang dalam 1+ perusahaan; akses & data di-scope per (perusahaan, cabang). Role manajemen perusahaan dapat punya wildcard "semua cabang".

### 6.2 Constraint

- **Wajib menggunakan existing database** — Postgres **per perusahaan** (strategi *database-per-tenant*). Saat ini: `mziss_laz` (Perusahaan 1 — LAZ) dan `mzis_wakaf` (Perusahaan 2 — Wakaf). Detail koneksi & routing di [`docs/architecture.md`](./architecture.md) §15.0.
- **Tidak ada schema migration di MVP**; akses bersifat read-mostly. Penulisan data baru hanya untuk hal yang belum tersedia di existing DB (mis. user_session, audit log portal) dan harus terisolasi dari skema existing.
- Arsitektur teknis mengikuti [`docs/architecture.md`](./architecture.md) — FrontEnd Vue + Vite, BFF FastAPI, backend Python FastAPI (dengan migrasi bertahap ke Go), OpenAPI-first.
- Portal harus mengikuti standar respons dan error format yang sudah ditetapkan di architecture.md §12–§13.

### 6.3 Dependency

- Akses (read minimal) ke existing database — kredensial dan dokumentasi skema tersedia.
- Provisioning user awal (untuk MVP dummy) — daftar user contoh dari stakeholder.
- Infrastructure dasar (server/container host) untuk environment dev dan staging.

## 7. Persyaratan Fungsional

### 7.1 Autentikasi & Sesi

**MVP (Fase 1) — Dummy login:**

- Halaman login dengan form username + password.
- Validasi kredensial bersifat **dummy**: menerima kredensial hard-coded dari konfigurasi (mis. 1–2 user demo) atau menerima input apa pun yang non-kosong, sesuai keputusan tim saat implementasi.
- Setelah berhasil login, pengguna mendapat *session* dummy yang berisi: user id, nama, daftar tenant yang dapat diakses, dan tenant default.
- Tombol logout mengakhiri session.
- **Tidak ada** pengelolaan password nyata, password reset, atau lockout di MVP.

**Production (Fase 4 dan setelahnya):**

- Mengikuti Auth Design di [`docs/architecture.md`](./architecture.md) §14 — rekomendasi: **Opsi B (Cookie httpOnly via BFF)** karena portal internal dengan kebutuhan keamanan sesi server-side.
- Password disimpan ter-hash (mis. bcrypt/argon2).
- Session lifetime, idle timeout, dan logout di seluruh device dapat dikonfigurasi.
- Logout mengakhiri session di sisi server (cookie invalidation).
- (Opsional, evaluasi terpisah) Integrasi SSO/OIDC jika organisasi sudah memiliki Identity Provider.

### 7.2 Portal per Domain + Multi-Cabang

Hierarki entitas (v0.3+): **Portal (domain spesifik)** → **Cabang (branch)** → **Data transaksional**. Setiap portal hanya kenal **satu perusahaan/lembaga** = "single-tenant per portal".

#### Dua portal independen

- **isf-app-zakat**: domain zakat/infaq/sadaqah. Backend & DB: `mziss_laz`. Tenant: Perusahaan 1 (LAZ).
- **isf-app-wakaf**: domain wakaf. Backend & DB: `mzis_wakaf`. Tenant: Perusahaan 2 (Wakaf).

Kedua portal di-deploy **independen** (stack masing-masing: web-vue + bff + api-python). Codebase dapat berbagi komponen UI dan auth pattern (lihat `docs/plan-split-deployment.md` — TBD).

#### Cabang (dalam tiap portal)

- Setiap perusahaan memiliki **satu atau lebih cabang**. Salah satu cabang ditandai sebagai **HQ**.
- Setiap user memiliki **akses ke satu/beberapa cabang** (atau wildcard "semua cabang" untuk role manajemen).
- Setiap user memiliki **satu cabang default** sebagai konteks awal setelah login.

#### Switcher di UI

- Header tiap portal menampilkan konteks cabang aktif: contoh `Cabang Jakarta ▾`.
- Klik switcher → daftar cabang yang user dapat akses.
- Untuk user dengan wildcard, tersedia **"Konsolidasi (semua cabang)"** — dashboard agregat lintas cabang dalam portal tersebut.
- **Tidak ada** switcher antar-portal di UI — pindah portal = navigasi ke URL portal lain.

#### Single Sign-On lintas portal

- **Default**: Google SSO (per `docs/plan-auth.md`). User login via Google, tiap portal verify token mandiri. UX: 1 login = akses dua portal.
- **Fallback**: bila Google SSO belum dikonfigurasi, user login terpisah di tiap portal (password lokal masing-masing).
- Tidak ada session sharing antar portal di Fase awal — masing-masing portal punya cookie session sendiri.

#### Isolasi data

- Backend tiap portal hanya kenal DB-nya sendiri (single DSN config).
- Query di-scope ke `(branch_id)` aktif (atau wildcard untuk konsolidasi cabang).
- Tidak ada akses lintas-portal di tingkat data — bila perlu dashboard "konsolidasi lintas-perusahaan", harus dibuat di lapisan agregasi terpisah (di luar scope fase awal).

#### Audit

- Setiap perpindahan cabang tercatat di audit log per portal (user, dari → ke cabang, waktu).

#### Domain field di tenant config

Tiap portal config menyertakan `domain ∈ {zakat, wakaf}` — frontend bisa sesuaikan branding/icon/menu berdasarkan domain. Sidebar dan widget yang khas-domain hanya tampil di portal yang sesuai.

#### Implementasi awal vs target

- **Fase 1 (MVP)**: 1 portal saja (zakat — yang sudah jalan). Wakaf portal di-stub.
- **Fase 2**: portal zakat connect ke `mziss_laz`, multi-cabang aktif. Portal wakaf mulai dibangun parallel atau setelah zakat stabil.
- **Fase 4+**: kedua portal punya fitur input dengan workflow approval (§7.8).

### 7.3 Dashboard

- Menjadi halaman landing setelah login.
- Konten **mengikuti peran** pengguna; semua dashboard menampilkan setidaknya: indikator tenant aktif, ringkasan KPI, filter periode (hari/bulan/tahun/custom).
- Komponen widget umum (tidak semua wajib, tergantung role):
  - Total penerimaan periode berjalan (per jenis dana: zakat / infaq / sadaqah / wakaf).
  - Total penyaluran periode berjalan.
  - Saldo per jenis dana.
  - Jumlah program aktif & realisasi.
  - Capaian penghimpunan vs target.
  - Tren penerimaan (chart sederhana).
- Klik pada widget mengarahkan ke modul terkait (drill-down).

**MVP (Fase 1):** kerangka dashboard dengan **2–3 widget minimum** yang menampilkan data dari existing DB atau data dummy yang representatif. Tujuan utama MVP: memverifikasi flow login → tenant switch → dashboard end-to-end.

### 7.4 Modul Keuangan (Fase 2)

- **Laporan penerimaan** ZISWAF per jenis dana, per periode, per channel.
- **Laporan penyaluran** per jenis dana, per program, per asnaf (untuk zakat).
- **Saldo dana** per jenis dana (zakat, infaq, sadaqah, wakaf) — dengan saldo awal, mutasi, saldo akhir.
- **Distribusi per asnaf** untuk zakat (8 asnaf).
- Filter periode, jenis dana, dan dimensi terkait.
- Ekspor laporan ke Excel/PDF.
- View tabular dengan opsi summary dan detail.

Modul ini bersifat **read-only di MVP/awal**: hanya menampilkan data dari existing DB, tidak melakukan input transaksi keuangan.

### 7.5 Modul Program (Fase 3)

- **Daftar program** ZISWAF (judul, penanggung jawab, periode, anggaran, status, asnaf/jenis dana sumber).
- **Detail program**: deskripsi, milestone, realisasi anggaran, jumlah penerima manfaat, dokumen pendukung.
- **Tracking progress** program (persentase realisasi, status: rencana / berjalan / selesai / dibatalkan).
- Filter dan pencarian berdasarkan periode, status, jenis dana, penanggung jawab.
- (Opsional, fase lanjutan) Workflow pengajuan dan approval program dengan satu lapis approval.

### 7.6 Modul Penghimpunan (Fase 3)

- **Capaian penghimpunan** per periode dengan progress terhadap target.
- **Daftar donatur / muzakki / wakif** dengan ringkasan kontribusi.
- **Channel penghimpunan**: kategorisasi transaksi penerimaan berdasarkan channel (transfer bank, gerai, payroll, e-wallet, dll).
- **Daftar transaksi penerimaan** dengan filter periode, jenis dana, channel, donatur.
- Target vs realisasi per channel dan total.
- Modul bersifat read & view di MVP/awal; input transaksi tetap dilakukan di sistem source.

### 7.7 Modul Back Office (Fase 4)

- **User Management**: tambah/ubah/nonaktifkan user, atur tenant membership, atur role.
- **Role Management**: definisi role dan permission (CRUD per modul) — minimum mengikuti matriks default di §8.
- **Master Data Viewer** (read di awal, CRUD bertahap): kategori program, daftar asnaf, daftar channel penghimpunan, kategori muzakki/donatur — tergantung kebutuhan dan ketersediaan di existing DB.
- **Audit Log Viewer**: log siapa melakukan apa, kapan, di tenant mana. Filter user, tenant, periode, jenis aksi.
- **Konfigurasi Sistem**: parameter portal (label, timezone, periode fiskal, dll).

### 7.8 Otorisasi & Workflow Approval

#### 7.8.1 Prinsip

Beberapa proses input data di portal melibatkan **otorisasi maker–checker** (2-eyes principle minimum): user pembuat (maker) tidak boleh sekaligus jadi penerima persetujuan. Tujuannya: kontrol risiko, akuntabilitas, audit trail jelas, dan mencegah kesalahan/fraud satu pihak.

#### 7.8.2 Proses yang membutuhkan otorisasi

| Domain | Proses | Fase |
| --- | --- | --- |
| Keuangan | Penyaluran dana (disbursement) | 2 |
| Keuangan | Posting jurnal ke buku besar | 2 |
| Keuangan / Master | Tambah/ubah master data: COA, asnaf, channel penghimpunan | 2 |
| Program | Pengajuan program baru, pengakhiran/pembatalan program | 3 |
| Wakaf | Registrasi wakaf produktif (aset tanah/properti) | 3 |
| Back Office | Provisioning user baru, role escalation, perubahan tenant membership | 4 |

Daftar di atas dapat diperluas seiring evolusi sistem; mekanisme di §7.8.4 didesain agar mudah menambah jenis record baru.

#### 7.8.3 Pattern dasar: Maker–Checker + threshold opsional

- **Default**: setiap proses di atas minimal 2-eyes (maker + 1 approver).
- **Threshold opsional** per proses: dapat dikonfigurasi — di bawah nilai/risk tertentu auto-approve, di atas threshold wajib approval (atau butuh approver tier lebih tinggi).
- **Eskalasi**: untuk nilai sangat besar (mis. penyaluran ≥ Rp 500 juta), approver tier eksekutif (Pimpinan) wajib turut menyetujui.
- **Self-approval prevention**: user yang menjadi maker tidak boleh menjadi approver record yang sama; di-enforce di backend, bukan hanya UI.

Threshold awal disetel konservatif (semua butuh approval); pelonggaran dilakukan via Back Office.

#### 7.8.4 State machine record

Setiap record yang masuk approval flow memiliki status:

```text
draft ──submit──► submitted ──approve──► approved ──post──► posted
                       │                     │
                       ├──reject──► rejected (maker bisa revisi)
                       └──recall──► recalled (maker tarik balik)
```

| Status | Definisi |
| --- | --- |
| `draft` | Maker baru membuat, belum submit |
| `submitted` | Diajukan, menunggu review |
| `approved` | Disetujui approver, siap diposting |
| `rejected` | Ditolak approver dengan alasan; maker dapat revisi atau hangus |
| `recalled` | Maker tarik balik sebelum approver memutuskan |
| `posted` | Final & efektif (jurnal masuk buku besar, dll) |

Beberapa transisi tambahan dapat dimasukkan saat implementasi (mis. `under_review` untuk locking).

#### 7.8.5 Audit & notifikasi

- **Audit trail wajib**: setiap transisi state dicatat di `audit_log` dengan user, timestamp, alasan (untuk `rejected`), dan tenant.
- **Notifikasi**: approver menerima notifikasi (in-app bell + email opsional di fase berikutnya) saat ada record dengan status `submitted` menunggu approval.
- **SLA approval** (opsional): dapat dikonfigurasi (mis. approver harus respon dalam 2 hari kerja; jika tidak, eskalasi ke tier atas).

#### 7.8.6 Dampak ke role matriks

Role di §8 akan diperluas saat Fase 2 dengan permission scoped per modul:

- `<modul>:create` — maker (boleh bikin draft & submit)
- `<modul>:approve` — checker (boleh approve/reject)
- `<modul>:post` — final posting (biasanya sama dengan approve untuk non-keuangan; finance dipisah)

Detail mapping permission per role akan dikunci pada saat Fase 2 dimulai, mengacu pada matriks §8 yang sudah ada.

## 8. Model Akses & Role

Matriks akses default — **starter, dapat disesuaikan saat sign-off**. Notasi: `R` = Read, `W` = Write/CRUD, `–` = tidak ada akses.

| Role | Dashboard | Keuangan | Program | Penghimpunan | Back Office |
| --- | --- | --- | --- | --- | --- |
| **Pimpinan** | R | R | R | R | R (audit log saja) |
| **Finance** | R | W | R | R | – |
| **Program Manager** | R | R | W | R | – |
| **Fundraiser** | R | R | R | W | – |
| **Back Office Admin** | R | R | R | R | W |

Catatan:

- Semua role membaca data **hanya pada tenant yang menjadi keanggotaannya**.
- **System Administrator** (super-user) bersifat di luar matriks; digunakan terbatas untuk operasional sistem (provisioning, troubleshooting). Aksesnya tercatat di audit log dengan penanda khusus.
- Role dapat **digabung** untuk satu user (mis. user yang merangkap Finance + Program Manager). Permission yang berlaku adalah gabungan paling permisif dari role-role tersebut.

## 9. Persyaratan Non-Fungsional

### 9.1 Keamanan

- Komunikasi seluruh portal menggunakan HTTPS (di production).
- Session menggunakan cookie `Secure`, `HttpOnly`, `SameSite` di production.
- Enforcement RBAC di sisi server (BFF/Backend), bukan hanya di UI.
- Tenant scoping wajib di sisi server pada setiap query.
- Audit log immutable untuk perubahan data sensitif.
- Password policy minimum (panjang, kompleksitas) untuk auth production.
- Tidak ada credential, secret, atau data sensitif yang disimpan di environment variable yang ter-expose ke browser (lihat architecture.md §11).

### 9.2 Audit Trail

Hal yang wajib tercatat di audit log:

- Login, logout, login gagal.
- Pergantian tenant.
- Operasi tulis pada data (create/update/delete) — siapa, kapan, tenant, entitas, ringkasan perubahan.
- Akses ke laporan dengan data sensitif (opsional, configurable).

### 9.3 Performance (target)

- Halaman dashboard tampil < **3 detik** pada koneksi internal normal.
- Endpoint API p95 < **500 ms** untuk query dengan dataset wajar.
- Beban concurrent ≥ **50 user aktif** di MVP, dapat di-scale di fase berikutnya.

### 9.4 Availability

- Target uptime **99%** untuk portal internal (jam kerja).
- Maintenance window: di luar jam kerja dengan notifikasi minimal H-1.

### 9.5 Browser Support

- Browser evergreen versi mutakhir (Chrome, Edge, Firefox, Safari).
- Resolusi desktop minimum 1280×800; tidak ada komitmen mobile-first di fase awal namun UI sebaiknya tidak rusak di layar kecil.

### 9.6 Accessibility

- Target dasar WCAG 2.1 level AA untuk kontras warna, navigasi keyboard, dan label form.

### 9.7 Bahasa & Lokalisasi

- Bahasa antarmuka: **Bahasa Indonesia** di fase awal.
- Format tanggal, angka, dan mata uang mengikuti locale `id-ID`.
- Mata uang utama: **IDR (Rupiah)**.
- Struktur kode disiapkan i18n-ready (string di file terpisah) walau hanya 1 bahasa di awal.

## 10. Fase / Roadmap

Strategi: **read-first**. Existing DB sudah berisi data — portal memberi value dengan pengalaman read yang baik sebelum membangun input.

| Fase | Lingkup | Sifat | Output utama |
| --- | --- | --- | --- |
| **Fase 1 — MVP** | Login dummy + dashboard skeleton + tenant switcher (cabang menyusul di Fase 2) | Read (dummy) | Validasi flow & UX end-to-end |
| **Fase 2 — Dashboard & Laporan ZISWAF** | Koneksi ke existing DB. Dashboard kaya per modul (Keuangan/Program/Penghimpunan). Multi-cabang switcher aktif + mode konsolidasi. Laporan + export. | Read | User langsung dapat manfaat dari data existing; drill-down per cabang; konsolidasi |
| **Fase 3 — Manajemen User Portal + Production Auth** | Cookie httpOnly session, manajemen user portal & role-cabang, audit log viewer | Read + Write **terbatas** (user portal saja, bukan data bisnis) | Self-service akses control + foundation security |
| **Fase 4 — Input Operasional Pertama: Penyaluran** | Form penyaluran + workflow maker–checker (§7.8) + posting ke buku besar via approval | Write transaksional pertama | Fitur write efektif pertama; pattern reusable untuk modul write lain |
| **Fase 5 — Input Lanjutan** | Pengajuan program, registrasi wakaf produktif, posting jurnal manual, perubahan master data | Write | Bertahap menggantikan input dari sistem lama |
| **Fase 6+ — Scale** | API gateway (Kong), migrasi Go per modul, evaluasi mobile/partner API | Infra | Skala consumer & performa |

Roadmap teknis (deploy, contract test, migrasi Go) berjalan paralel sesuai [`docs/architecture.md`](./architecture.md) §28; PRD ini berfokus pada urutan fitur dari sudut produk.

## 11. Kriteria Penerimaan MVP (Fase 1)

MVP dianggap selesai jika seluruh kriteria berikut terpenuhi:

- [ ] Halaman login dapat diakses di environment dev/staging.
- [ ] Pengguna dapat melakukan "login" dengan kredensial dummy (sesuai konfigurasi tim) dan mendapatkan session.
- [ ] Setelah login, pengguna diarahkan ke dashboard pada **tenant default**-nya.
- [ ] **Tenant switcher** muncul di header dan menampilkan kedua perusahaan yang menjadi keanggotaan user.
- [ ] Pengguna dapat **berpindah tenant** tanpa logout; konten dashboard ter-refresh sesuai tenant baru.
- [ ] Dashboard menampilkan **minimum 2 widget** yang menarik data — boleh dari existing DB (preferred) atau data dummy yang representatif.
- [ ] Indikator tenant aktif tampil jelas di UI sepanjang sesi.
- [ ] Tombol logout berfungsi dan mengakhiri sesi.
- [ ] Setiap perpindahan tenant menghasilkan log (konsol/server log) yang berisi user, tenant lama, tenant baru, waktu.
- [ ] UI dapat dibuka di browser evergreen pada resolusi desktop ≥ 1280×800 tanpa rusak.
- [ ] Endpoint API mengikuti format respons standar di architecture.md §12.

## 12. Risiko & Mitigasi

| # | Risiko | Dampak | Likelihood | Mitigasi |
| --- | --- | --- | --- | --- |
| R1 | Struktur existing DB tidak sesuai kebutuhan modul (tabel tidak ada, semantik berbeda) | Tinggi | Sedang | Schema assessment di awal Fase 2; siapkan adapter/view layer di backend |
| R2 | Multi-tenant data leak (user A melihat data tenant B) | Tinggi | Rendah | Tenant scoping di BFF & backend; contract test khusus tenant isolation; review wajib pada setiap PR yang menyentuh query |
| R3 | Single point of failure ke existing DB (downtime existing DB → portal down) | Tinggi | Rendah | Cache hot data via Redis; circuit breaker di BFF; halaman degraded mode |
| R4 | Auth dummy ter-bawa ke production | Sangat tinggi (security) | Rendah | Env flag eksplisit (`AUTH_MODE=dummy`); gating release; checklist pre-prod |
| R5 | Scope creep modul (mis. permintaan akuntansi penuh) | Sedang | Tinggi | PRD ini sebagai baseline; perubahan via change request resmi |
| R6 | Ketergantungan pada satu domain lead per modul (bottleneck UAT) | Sedang | Sedang | Penunjukan backup reviewer untuk setiap modul |
| R7 | Performa lambat pada agregasi keuangan dataset besar | Sedang | Sedang | Indexing review pada existing DB; materialized view jika perlu; pre-aggregation di backend |

## 13. Glosarium

| Istilah | Definisi |
| --- | --- |
| **ZISWAF** | Akronim Zakat, Infaq, Sadaqah, Wakaf |
| **Zakat** | Kewajiban harta tertentu yang dikeluarkan menurut syariat Islam |
| **Infaq** | Pemberian dana sukarela yang dialokasikan untuk kebaikan |
| **Sadaqah** | Pemberian sukarela dalam bentuk apa pun (lebih luas dari infaq) |
| **Wakaf** | Penyerahan hak atas aset untuk dimanfaatkan jangka panjang sesuai syariat |
| **Muzakki** | Pemberi zakat |
| **Mustahik** | Penerima zakat |
| **Wakif** | Pemberi/pendiri wakaf |
| **Nazhir** | Pengelola wakaf |
| **Asnaf** | Kategori penerima zakat (8 kelompok yang ditentukan syariat) |
| **Tenant** | Konteks perusahaan/lembaga; menentukan isolasi data yang dilihat user |
| **Multi-tenant** | Arsitektur di mana satu aplikasi melayani lebih dari satu organisasi/konteks dengan isolasi data |
| **RBAC** | Role-Based Access Control — model otorisasi berbasis peran |
| **BFF** | Backend-for-Frontend; lapisan API yang melayani kebutuhan spesifik frontend |
| **MVP** | Minimum Viable Product — versi paling sederhana yang sudah berguna |
| **UAT** | User Acceptance Testing — pengujian penerimaan oleh pengguna bisnis |
| **Cabang (Branch)** | Unit operasional di bawah perusahaan ZISWAF (mis. cabang regional / kantor cabang) |
| **HQ** | Head Quarter — kantor pusat suatu perusahaan; satu cabang ditandai sebagai HQ |
| **Konsolidasi** | Tampilan agregat lintas cabang dalam satu perusahaan (bukan lintas perusahaan) |
| **Domain** | Lini bisnis ZISWAF yang dilayani satu portal — `zakat` (LAZ) atau `wakaf` |
| **Portal** | Aplikasi end-to-end (frontend + backend + DB) untuk satu domain. Saat ini: `isf-app-zakat`, `isf-app-wakaf` |

## 14. Referensi

- [`docs/architecture.md`](./architecture.md) — desain teknikal lengkap (stack, arsitektur per fase, OpenAPI contract, format respons/error, opsi auth, strategi migrasi Python→Go, anti-pattern).

## 15. Revision History

| Versi | Tanggal | Penulis | Catatan |
| --- | --- | --- | --- |
| 0.1 | 2026-05-20 | Draft awal | Versi draft (BRD) untuk review stakeholder |
| 0.2 | 2026-05-20 | Pivot ke PRD | Read-first roadmap (Fase 2 dashboard & laporan dari existing DB; fitur input transaksional digeser ke Fase 4+); tambah konsep multi-cabang (Perusahaan × Cabang); tambah §1.1 strategi, §1.2 multi-cabang, §7.8 otorisasi maker–checker; rename `docs/brd.md` → `docs/prd.md` |
| 0.3 | 2026-05-20 | Split portal per domain | Multi-tenant 1 portal → **dua portal independen** (`isf-app-zakat` + `isf-app-wakaf`), masing-masing single-tenant + multi-cabang; tenant config tambah field `domain ∈ {zakat, wakaf}`; SSO lintas portal via Google SSO; restructure folder direncanakan (`docs/plan-split-deployment.md`); update §1.2, §5.1, §7.2, §13 |
