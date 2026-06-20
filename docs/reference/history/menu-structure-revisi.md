# Menu Structure — Portal Zakat

> Generated from `apps_zakat/web-vue/src/components/AppSidebar.vue`
> Last updated: 2026-06-18

---

## Dashboard

| Label | Route | menu_key |
|---|---|---|
| Overview | `/` | `dashboard.overview` |
| Keuangan | `/dashboard/keuangan` | `dashboard.keuangan` |
| Penyaluran | `/dashboard/penyaluran` | `dashboard.penyaluran` |
| Penghimpunan | `/dashboard/penghimpunan` | `dashboard.penghimpunan` |

---

## Master Data

| Label | Route | menu_key |
|---|---|---|
| Chart of Accounts | `/keuangan/coa` | `keuangan.coa` |
| Kas | `/keuangan/kas` | `keuangan.kas` |
| Bank | `/keuangan/bank` | `keuangan.bank` |
| Kas Kecil | `/keuangan/kas-kecil` | `keuangan.kas_kecil` |
| Pemilik Anggaran | `/parameter/pemilik-anggaran` | `keuangan.parameter.pemilik-anggaran` |

---
## Anggaran

| Label | Route | menu_key |
|---|---|---|
| Buat Anggaran Baru | `/keuangan/anggaran/import` | `keuangan.anggaran.import` |
| Revisi Anggaran | `/keuangan/anggaran/revisi` | `keuangan.anggaran.revisi` |
| Inquiry Anggaran | `/keuangan/anggaran/inquiry` | `keuangan.anggaran.inquiry` |

---
## Transaksi

| Label | Route | menu_key |
|---|---|---|
| Histori Transaksi | `/keuangan/transaksi/histori` | `keuangan.transaksi.histori` |
| Input Penghimpunan Dana | `/keuangan/transaksi/penghimpunan` | `keuangan.transaksi.penghimpunan` |
| Input Penyaluran Dana | `/keuangan/transaksi/penyaluran` | `keuangan.transaksi.penyaluran` |
| Penyerahan Uang Muka | `/keuangan/transaksi/uang-muka-penyerahan` | `keuangan.transaksi.uang-muka-penyerahan` |
| Pengembalian Uang Muka | `/keuangan/transaksi/uang-muka-pengembalian` | `keuangan.transaksi.uang-muka-pengembalian` |
| Transfer Antar Rekening | `/keuangan/transaksi/transfer-antar-rekening` | `keuangan.transaksi.transfer-antar-rekening` |
| Transaksi Umum | `/keuangan/transaksi/umum` | `keuangan.transaksi.umum` |
| Piutang (Pinjam/Bayar) | `/keuangan/transaksi/piutang` | `keuangan.piutang.pinjam-bayar` |

---
## Upload

| Label | Route | menu_key |
|---|---|---|
| Upload Penghimpunan | `/keuangan/upload/penghimpunan` | `keuangan.upload.penghimpunan` |
| Otorisasi Upload | `/keuangan/upload/penghimpunan/list` | `keuangan.upload.penghimpunan.approve` |
| Upload ZIS Rutin | `/keuangan/upload/zis-rutin` | `keuangan.upload.zis-rutin` |
| Daftar Upload ZIS | `/keuangan/upload/zis-rutin-list` | `keuangan.upload.zis-rutin-list` |

---
## Laporan

### Kas & Transaksi

| Label | Route | menu_key |
|---|---|---|
| Transaksi Kas/Bank Harian | `/keuangan/laporan/kas-harian` | `keuangan.report.cash_daily` |
| Rekapitulasi Kas/Bank | `/keuangan/laporan/rekap-kas` | `keuangan.report.cash_summary` |
| Monitoring Saldo Kas Bulanan | `/keuangan/laporan/saldo-bulanan` | `keuangan.report.cash_monthly` |
| Jurnal Harian | `/keuangan/laporan/jurnal-harian` | `keuangan.report.journal_daily` |
| List Transaksi Umum | `/keuangan/laporan/transaksi-umum` | `keuangan.report.general_transaction` |

### Akuntansi

| Label | Route | menu_key |
|---|---|---|
| Trial Balance | `/keuangan/laporan/trial-balance` | `keuangan.report.trial_balance` |
| Neraca | `/keuangan/laporan/neraca` | `keuangan.report.neraca` |
| Arus Kas | `/keuangan/laporan/arus-kas` | `keuangan.report.cash_flow` |
| Buku Besar | `/keuangan/laporan/buku-besar` | `keuangan.report.general_ledger` |
| Perubahan Dana | `/keuangan/laporan/perubahan-dana` | `keuangan.report.fund_changes` |
| Perubahan Dana Detail | `/keuangan/laporan/perubahan-dana-detail` | `keuangan.report.fund_changes_detail` |

### Penghimpunan & Penyaluran

| Label | Route | menu_key |
|---|---|---|
| Penghimpunan Dana | `/keuangan/laporan/penghimpunan-dana` | `keuangan.report.collection` |
| Penyaluran Dana | `/keuangan/laporan/penyaluran-dana` | `keuangan.report.distribution` |

### Amil

| Label | Route | menu_key |
|---|---|---|
| Penerimaan Amil | `/keuangan/laporan/penerimaan-amil` | `keuangan.report.amil_in` |
| Pengeluaran Amil | `/keuangan/laporan/pengeluaran-amil` | `keuangan.report.amil_out` |

### Piutang

| Label | Route | menu_key |
|---|---|---|
| Piutang pada Karyawan | `/keuangan/laporan/piutang-karyawan` | `keuangan.report.ar_employee` |
| Piutang pada Non-Karyawan | `/keuangan/laporan/piutang-non-karyawan` | `keuangan.report.ar_external` |

### Uang Muka Kegiatan

| Label | Route | menu_key |
|---|---|---|
| Rekapitulasi Uang Muka Kegiatan | `/keuangan/laporan/uang-muka-kegiatan` | `keuangan.report.ca_employee` |
| List Transaksi Uang Muka Kegiatan | `/keuangan/laporan/list-uang-muka` | `keuangan.report.ca_list` |
| Laporan Realisasi Project (Memo) | `/keuangan/laporan/realisasi-memo` | `keuangan.report.project_memo` |
| Piutang Realisasi Penyaluran | `/keuangan/laporan/piutang-realisasi` | `keuangan.report.program_ar` |

### UPZ

| Label | Route | menu_key |
|---|---|---|
| List Transaksi UPZ | `/keuangan/laporan/upz` | `keuangan.report.upz` |

---
## Monitoring dan Kontrol

| Label | Route | menu_key |
|---|---|---|
| Otorisasi | `/keuangan/monitoring/otorisasi` | `keuangan.monitoring.otorisasi` |
| Riwayat Submission | `/keuangan/monitoring/riwayat` | `keuangan.monitoring.riwayat` |

---

## Disabled (Belum Tersedia)

| Label | Badge |
|---|---|
| Program | Fase 3 |
| Penghimpunan | Fase 3 |
| Manajemen User | Fase 4 |
| Back Office | Fase 4 |
| Audit Log | Fase 4 |
