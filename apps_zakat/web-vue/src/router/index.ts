import { createRouter, createWebHistory } from 'vue-router'

import type { MenuKey } from '@/lib/menu/registry'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { public: true, title: 'Masuk' },
    },
    {
      path: '/no-tenant',
      name: 'no-tenant',
      component: () => import('@/pages/NoTenantPage.vue'),
      meta: { requiresNoTenant: true, title: 'Akun' },
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/pages/DashboardPage.vue'),
      meta: { title: 'Dashboard', menu_key: 'dashboard.overview' as MenuKey },
    },
    {
      path: '/keuangan/coa',
      name: 'keuangan-coa',
      component: () => import('@/pages/keuangan/CoaPage.vue'),
      meta: { title: 'Chart of Accounts', menu_key: 'keuangan.coa' as MenuKey },
    },
    {
      path: '/keuangan/kas',
      name: 'keuangan-kas',
      component: () => import('@/pages/keuangan/KasPage.vue'),
      meta: { title: 'Manajemen Kas', menu_key: 'keuangan.kas' as MenuKey },
    },
    {
      path: '/keuangan/bank',
      name: 'keuangan-bank',
      component: () => import('@/pages/keuangan/BankPage.vue'),
      meta: { title: 'Manajemen Bank', menu_key: 'keuangan.bank' as MenuKey },
    },
    {
      path: '/keuangan/kas-kecil',
      name: 'keuangan-kas-kecil',
      component: () => import('@/pages/keuangan/KasKecilPage.vue'),
      meta: { title: 'Manajemen Kas Kecil', menu_key: 'keuangan.kas_kecil' as MenuKey },
    },
    {
      path: '/keuangan/anggaran/import',
      name: 'keuangan-anggaran-import',
      component: () => import('@/pages/keuangan/BudgetImportPage.vue'),
      meta: { title: 'Buat Anggaran Baru', menu_key: 'keuangan.anggaran.import' as MenuKey },
    },
    {
      path: '/keuangan/anggaran/revisi',
      name: 'keuangan-anggaran-revisi',
      component: () => import('@/pages/keuangan/BudgetRevisePage.vue'),
      meta: { title: 'Revisi Anggaran', menu_key: 'keuangan.anggaran.revisi' as MenuKey },
    },
    {
      path: '/keuangan/anggaran/inquiry',
      name: 'keuangan-anggaran-inquiry',
      component: () => import('@/pages/keuangan/BudgetInquiryPage.vue'),
      meta: { title: 'Inquiry Anggaran', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/keuangan/anggaran/inquiry/owner/:owner_id',
      name: 'keuangan-anggaran-inquiry-owner',
      component: () => import('@/pages/keuangan/BudgetInquiryOwnerPage.vue'),
      meta: { title: 'Detail Anggaran Pemilik', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/keuangan/anggaran/inquiry/budget/:budget_id/transaksi',
      name: 'keuangan-anggaran-inquiry-transaksi',
      component: () => import('@/pages/keuangan/BudgetInquiryTransaksiPage.vue'),
      meta: { title: 'Riwayat Transaksi Anggaran', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/keuangan/laporan/jurnal-harian',
      name: 'keuangan-laporan-jurnal-harian',
      component: () => import('@/pages/keuangan/laporan/LaporanJurnalHarianPage.vue'),
      meta: {
        title: 'Laporan Jurnal Harian',
        menu_key: 'keuangan.report.journal_daily' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/transaksi-umum',
      name: 'keuangan-laporan-transaksi-umum',
      component: () => import('@/pages/keuangan/laporan/LaporanGeneralTransactionPage.vue'),
      meta: {
        title: 'List Transaksi Umum',
        menu_key: 'keuangan.report.general_transaction' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/kas-harian',
      name: 'keuangan-laporan-kas-harian',
      component: () => import('@/pages/keuangan/laporan/LaporanCashDailyPage.vue'),
      meta: {
        title: 'Transaksi Kas/Bank Harian',
        menu_key: 'keuangan.report.cash_daily' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/rekap-kas',
      name: 'keuangan-laporan-rekap-kas',
      component: () => import('@/pages/keuangan/laporan/LaporanCashSummaryPage.vue'),
      meta: {
        title: 'Rekapitulasi Transaksi Kas/Bank',
        menu_key: 'keuangan.report.cash_summary' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/saldo-bulanan',
      name: 'keuangan-laporan-saldo-bulanan',
      component: () => import('@/pages/keuangan/laporan/LaporanCashMonthlyPage.vue'),
      meta: {
        title: 'Monitoring Saldo Kas/Bank Bulanan',
        menu_key: 'keuangan.report.cash_monthly' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/trial-balance',
      name: 'keuangan-laporan-trial-balance',
      component: () => import('@/pages/keuangan/laporan/LaporanTrialBalancePage.vue'),
      meta: {
        title: 'Trial Balance',
        menu_key: 'keuangan.report.trial_balance' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/neraca',
      name: 'keuangan-laporan-neraca',
      component: () => import('@/pages/keuangan/laporan/LaporanNeracaPage.vue'),
      meta: {
        title: 'Neraca',
        menu_key: 'keuangan.report.neraca' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/arus-kas',
      name: 'keuangan-laporan-arus-kas',
      component: () => import('@/pages/keuangan/laporan/LaporanArusKasPage.vue'),
      meta: {
        title: 'Arus Kas',
        menu_key: 'keuangan.report.cash_flow' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/buku-besar',
      name: 'keuangan-laporan-buku-besar',
      component: () => import('@/pages/keuangan/laporan/LaporanBukuBesarPage.vue'),
      meta: {
        title: 'Buku Besar',
        menu_key: 'keuangan.report.general_ledger' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/perubahan-dana',
      name: 'keuangan-laporan-perubahan-dana',
      component: () => import('@/pages/keuangan/laporan/LaporanPerubahanDanaPage.vue'),
      meta: {
        title: 'Perubahan Dana',
        menu_key: 'keuangan.report.fund_changes' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/perubahan-dana-detail',
      name: 'keuangan-laporan-perubahan-dana-detail',
      component: () => import('@/pages/keuangan/laporan/LaporanPerubahanDanaDetailPage.vue'),
      meta: {
        title: 'Perubahan Dana Detail',
        menu_key: 'keuangan.report.fund_changes_detail' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/penerimaan-amil',
      name: 'keuangan-laporan-penerimaan-amil',
      component: () => import('@/pages/keuangan/laporan/LaporanAmilPage.vue'),
      meta: {
        title: 'Penerimaan Amil',
        menu_key: 'keuangan.report.amil_in' as MenuKey,
        amilKind: 'in',
      },
    },
    {
      path: '/keuangan/laporan/pengeluaran-amil',
      name: 'keuangan-laporan-pengeluaran-amil',
      component: () => import('@/pages/keuangan/laporan/LaporanAmilPage.vue'),
      meta: {
        title: 'Pengeluaran Amil',
        menu_key: 'keuangan.report.amil_out' as MenuKey,
        amilKind: 'out',
      },
    },
    {
      path: '/keuangan/laporan/penyaluran-dana',
      name: 'keuangan-laporan-penyaluran-dana',
      component: () => import('@/pages/keuangan/laporan/LaporanPenyaluranDanaPage.vue'),
      meta: {
        title: 'Penyaluran Dana',
        menu_key: 'keuangan.report.distribution' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/penghimpunan-dana',
      name: 'keuangan-laporan-penghimpunan-dana',
      component: () => import('@/pages/keuangan/laporan/LaporanPenghimpunanDanaPage.vue'),
      meta: {
        title: 'Penghimpunan Dana',
        menu_key: 'keuangan.report.collection' as MenuKey,
      },
    },
    {
      path: '/keuangan/laporan/piutang-karyawan',
      name: 'keuangan-laporan-piutang-karyawan',
      component: () => import('@/pages/keuangan/laporan/LaporanARSummaryPage.vue'),
      meta: { title: 'Piutang pada Karyawan', menu_key: 'keuangan.report.ar_employee' as MenuKey, arEndpoint: 'employee-ar', arFile: 'piutangkaryawan' },
    },
    {
      path: '/keuangan/laporan/piutang-non-karyawan',
      name: 'keuangan-laporan-piutang-non-karyawan',
      component: () => import('@/pages/keuangan/laporan/LaporanARSummaryPage.vue'),
      meta: { title: 'Piutang pada Non-Karyawan', menu_key: 'keuangan.report.ar_external' as MenuKey, arEndpoint: 'external-ar', arFile: 'piutangnonkaryawan' },
    },
    {
      path: '/keuangan/laporan/uang-muka-kegiatan',
      name: 'keuangan-laporan-uang-muka-kegiatan',
      component: () => import('@/pages/keuangan/laporan/LaporanARSummaryPage.vue'),
      meta: { title: 'Rekapitulasi Uang Muka Kegiatan', menu_key: 'keuangan.report.ca_employee' as MenuKey, arEndpoint: 'cash-advance', arFile: 'rekapuangmuka' },
    },
    {
      path: '/keuangan/laporan/list-uang-muka',
      name: 'keuangan-laporan-list-uang-muka',
      component: () => import('@/pages/keuangan/laporan/LaporanListUangMukaPage.vue'),
      meta: { title: 'List Transaksi Uang Muka Kegiatan', menu_key: 'keuangan.report.ca_list' as MenuKey },
    },
    {
      path: '/keuangan/laporan/realisasi-memo',
      name: 'keuangan-laporan-realisasi-memo',
      component: () => import('@/pages/keuangan/laporan/LaporanRealisasiMemoPage.vue'),
      meta: { title: 'Laporan Realisasi Project (Memo)', menu_key: 'keuangan.report.project_memo' as MenuKey },
    },
    {
      path: '/keuangan/laporan/piutang-realisasi',
      name: 'keuangan-laporan-piutang-realisasi',
      component: () => import('@/pages/keuangan/laporan/LaporanPiutangRealisasiPage.vue'),
      meta: { title: 'Piutang Realisasi Penyaluran', menu_key: 'keuangan.report.program_ar' as MenuKey },
    },
    {
      path: '/keuangan/laporan/upz',
      name: 'keuangan-laporan-upz',
      component: () => import('@/pages/keuangan/laporan/LaporanUpzPage.vue'),
      meta: { title: 'List Transaksi UPZ', menu_key: 'keuangan.report.upz' as MenuKey },
    },
    {
      path: '/dashboard/keuangan',
      name: 'dashboard-keuangan',
      component: () => import('@/pages/DashboardKeuanganPage.vue'),
      meta: { title: 'Dashboard Keuangan', menu_key: 'dashboard.keuangan' as MenuKey },
    },
    {
      path: '/dashboard/penyaluran',
      name: 'dashboard-penyaluran',
      component: () => import('@/pages/DashboardPenyaluranPage.vue'),
      meta: { title: 'Dashboard Penyaluran', menu_key: 'dashboard.penyaluran' as MenuKey },
    },
    {
      path: '/dashboard/penghimpunan',
      name: 'dashboard-penghimpunan',
      component: () => import('@/pages/DashboardPenghimpunanPage.vue'),
      meta: { title: 'Dashboard Penghimpunan', menu_key: 'dashboard.penghimpunan' as MenuKey },
    },
    {
      path: '/admin/role-menu',
      name: 'admin-role-menu',
      component: () => import('@/pages/admin/RoleMenuPage.vue'),
      meta: { title: 'Mapping Role-Menu', menu_key: 'admin.role_menu' as MenuKey },
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('@/pages/admin/UsersPage.vue'),
      meta: { title: 'List User', menu_key: 'admin.users' as MenuKey },
    },
    {
      path: '/profile/password',
      name: 'profile-password',
      component: () => import('@/pages/profile/PasswordPage.vue'),
      meta: { title: 'Ganti Password' },
    },
    {
      path: '/keuangan/upload/penghimpunan',
      name: 'keuangan-upload-penghimpunan',
      component: () => import('@/pages/keuangan/UploadPenghimpunanPage.vue'),
      meta: { title: 'Upload Penghimpunan', menu_key: 'keuangan.upload.penghimpunan' as MenuKey },
    },
    {
      path: '/keuangan/upload/penghimpunan/list',
      name: 'keuangan-upload-penghimpunan-list',
      component: () => import('@/pages/keuangan/UploadPenghimpunanListPage.vue'),
      meta: { title: 'Daftar Batch Upload', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
    },
    {
      path: '/keuangan/upload/penghimpunan/:id',
      name: 'keuangan-upload-penghimpunan-detail',
      component: () => import('@/pages/keuangan/UploadPenghimpunanDetailPage.vue'),
      meta: { title: 'Detail Batch', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
    },
    {
      path: '/keuangan/upload/zis-rutin',
      name: 'keuangan-upload-zis-rutin',
      component: () => import('@/pages/keuangan/UploadHCZisPage.vue'),
      meta: { title: 'Upload ZIS Rutin', menu_key: 'keuangan.upload.zis-rutin' as MenuKey },
    },
    {
      path: '/keuangan/upload/zis-rutin-list',
      name: 'keuangan-upload-zis-rutin-list',
      component: () => import('@/pages/keuangan/UploadHCZisListPage.vue'),
      meta: { title: 'Daftar Upload ZIS Rutin', menu_key: 'keuangan.upload.zis-rutin-list' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/histori',
      name: 'keuangan-transaksi-histori',
      component: () => import('@/pages/keuangan/HistoriTransaksiPage.vue'),
      meta: { title: 'Histori Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/histori/:id',
      name: 'keuangan-transaksi-histori-detail',
      component: () => import('@/pages/keuangan/HistoriTransaksiDetailPage.vue'),
      meta: { title: 'Detail Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penyaluran',
      name: 'keuangan-transaksi-penyaluran',
      component: () => import('@/pages/keuangan/PenyaluranDanaPage.vue'),
      meta: { title: 'Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penyaluran/baru',
      name: 'keuangan-transaksi-penyaluran-baru',
      component: () => import('@/pages/keuangan/PenyaluranDanaFormPage.vue'),
      meta: { title: 'Input Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penyaluran/edit/:id',
      name: 'keuangan-transaksi-penyaluran-edit',
      component: () => import('@/pages/keuangan/PenyaluranDanaFormPage.vue'),
      meta: { title: 'Edit Draft Penyaluran', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penghimpunan',
      name: 'keuangan-transaksi-penghimpunan',
      component: () => import('@/pages/keuangan/PenghimpunanDanaPage.vue'),
      meta: { title: 'Penghimpunan Dana', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penghimpunan/baru',
      name: 'keuangan-transaksi-penghimpunan-baru',
      component: () => import('@/pages/keuangan/PenghimpunanDanaFormPage.vue'),
      meta: { title: 'Input Penghimpunan Dana', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penghimpunan/edit/:id',
      name: 'keuangan-transaksi-penghimpunan-edit',
      component: () => import('@/pages/keuangan/PenghimpunanDanaFormPage.vue'),
      meta: { title: 'Edit Draft Penghimpunan', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/uang-muka-penyerahan',
      name: 'keuangan-transaksi-uang-muka-penyerahan',
      component: () => import('@/pages/keuangan/UangMukaPenyerahanPage.vue'),
      meta: { title: 'Penyerahan Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-penyerahan' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/uang-muka-pengembalian',
      name: 'keuangan-transaksi-uang-muka-pengembalian',
      component: () => import('@/pages/keuangan/UangMukaPengembalianPage.vue'),
      meta: { title: 'Pengembalian Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-pengembalian' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/transfer-antar-rekening',
      name: 'keuangan-transaksi-transfer-antar-rekening',
      component: () => import('@/pages/keuangan/TransferAntarRekeningPage.vue'),
      meta: { title: 'Transfer Antar Rekening', menu_key: 'keuangan.transaksi.transfer-antar-rekening' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/umum',
      name: 'keuangan-transaksi-umum',
      component: () => import('@/pages/keuangan/transaksi-umum/TransaksiUmumListPage.vue'),
      meta: { title: 'Transaksi Umum', menu_key: 'keuangan.transaksi.umum' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/umum/input',
      name: 'keuangan-transaksi-umum-create',
      component: () => import('@/pages/keuangan/transaksi-umum/TransaksiUmumCreatePage.vue'),
      meta: { title: 'Input Transaksi Umum', menu_key: 'keuangan.transaksi.umum' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/piutang',
      name: 'keuangan-transaksi-piutang',
      component: () => import('@/pages/keuangan/PiutangPage.vue'),
      meta: { title: 'Piutang (Pinjam/Bayar)', menu_key: 'keuangan.piutang.pinjam-bayar' as MenuKey },
    },
    {
      path: '/keuangan/monitoring/otorisasi',
      name: 'keuangan-monitoring-otorisasi',
      component: () => import('@/pages/keuangan/OtorisasiPage.vue'),
      meta: { title: 'Otorisasi', menu_key: 'keuangan.monitoring.otorisasi' as MenuKey },
    },
    {
      path: '/keuangan/monitoring/riwayat',
      name: 'keuangan-monitoring-riwayat',
      component: () => import('@/pages/keuangan/RiwayatSubmissionPage.vue'),
      meta: { title: 'Riwayat Submission', menu_key: 'keuangan.monitoring.riwayat' as MenuKey },
    },
    {
      path: '/parameter/pemilik-anggaran',
      name: 'parameter-pemilik-anggaran',
      component: () => import('@/pages/parameter/PemilikAnggaranPage.vue'),
      meta: { title: 'Pemilik Anggaran', menu_key: 'keuangan.parameter.pemilik-anggaran' as MenuKey },
    },
    {
      path: '/parameter/anggaran/item',
      name: 'parameter-anggaran-item',
      component: () => import('@/pages/parameter/BudgetItemPage.vue'),
      meta: { title: 'Item Anggaran', menu_key: 'keuangan.parameter.anggaran.item' as MenuKey },
    },
    {
      path: '/parameter/anggaran/periode',
      name: 'parameter-anggaran-periode',
      component: () => import('@/pages/parameter/BudgetPeriodPage.vue'),
      meta: { title: 'Periode Anggaran', menu_key: 'keuangan.parameter.anggaran.periode' as MenuKey },
    },
    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.initialized) await auth.bootstrap()

  if (!to.meta.public && !auth.user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && auth.user) {
    return auth.activeTenantId ? { name: 'dashboard' } : { name: 'no-tenant' }
  }

  if (auth.user && !auth.activeTenantId && to.name !== 'no-tenant' && to.name !== 'login') {
    return { name: 'no-tenant' }
  }

  if (auth.user && auth.activeTenantId && to.name === 'no-tenant') {
    return { name: 'dashboard' }
  }

  // Menu authorization check
  const requiredMenu = to.meta.menu_key as MenuKey | undefined
  if (requiredMenu && auth.user && !auth.hasMenu(requiredMenu)) {
    return { name: 'dashboard', query: { denied: requiredMenu } }
  }
})

export default router
