import type { RouteRecordRaw } from 'vue-router'

export const distributionRoutes: RouteRecordRaw[] = [
  // ── Mustahiq ─────────────────────────────────────────────────────────────
  {
    path: '/distribution/mustahiq/corporate',
    name: 'distribution-mustahiq-corporate',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporateView.vue'),
    meta: { title: 'Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/corporate/create',
    name: 'distribution-mustahiq-corporate-create',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporateFormView.vue'),
    meta: { title: 'Tambah Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/corporate/:id',
    name: 'distribution-mustahiq-corporate-detail',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporateDetailView.vue'),
    meta: { title: 'Detail Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/corporate/:id/edit',
    name: 'distribution-mustahiq-corporate-edit',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporateFormView.vue'),
    meta: { title: 'Ubah Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal',
    name: 'distribution-mustahiq-personal',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalView.vue'),
    meta: { title: 'Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal/create',
    name: 'distribution-mustahiq-personal-create',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalFormView.vue'),
    meta: { title: 'Tambah Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal/:id',
    name: 'distribution-mustahiq-personal-detail',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalDetailView.vue'),
    meta: { title: 'Detail Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal/:id/edit',
    name: 'distribution-mustahiq-personal-edit',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalFormView.vue'),
    meta: { title: 'Ubah Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
  },
  {
    path: '/distribution/proposal',
    name: 'distribution-proposal-list',
    component: () => import('@/modules/distribution/views/proposal/ProposalListView.vue'),
    meta: { title: 'Proposal Bantuan Dana', menu_key: 'distribution.proposal.list', domain: 'distribution' },
  },
  {
    path: '/distribution/partner',
    name: 'distribution-partner-list',
    component: () => import('@/modules/distribution/views/partner/PartnerView.vue'),
    meta: { title: 'Mitra', menu_key: 'distribution.partner.list', domain: 'distribution' },
  },
  {
    path: '/distribution/program/regular',
    name: 'distribution-program-regular',
    component: () => import('@/modules/distribution/views/regular-program/RegularProgramView.vue'),
    meta: { title: 'Program Rutin', menu_key: 'distribution.program.regular', domain: 'distribution' },
  },
  {
    path: '/distribution/program/non-regular',
    name: 'distribution-program-non-regular',
    component: () => import('@/modules/distribution/views/non-regular-program/NonRegularProgramView.vue'),
    meta: { title: 'Program Non Rutin', menu_key: 'distribution.program.non-regular', domain: 'distribution' },
  },
  {
    path: '/distribution/program/memo-regular',
    name: 'distribution-program-memo-regular',
    component: () => import('@/modules/distribution/views/realization-memo/RegularMemoView.vue'),
    meta: { title: 'Memo Penyaluran Rutin', menu_key: 'distribution.program.memo-regular', domain: 'distribution' },
  },
  {
    path: '/distribution/program/memo-non-regular',
    name: 'distribution-program-memo-non-regular',
    component: () => import('@/modules/distribution/views/realization-memo/NonRegularMemoView.vue'),
    meta: { title: 'Memo Penyaluran Non Rutin', menu_key: 'distribution.program.memo-non-regular', domain: 'distribution' },
  },
  {
    path: '/distribution/realization/regular',
    name: 'distribution-realization-regular',
    component: () => import('@/modules/distribution/views/realization/RegularRealizationView.vue'),
    meta: { title: 'Realisasi Program Rutin', menu_key: 'distribution.realization.regular.list', domain: 'distribution' },
  },
  {
    path: '/distribution/realization/non-regular',
    name: 'distribution-realization-non-regular',
    component: () => import('@/modules/distribution/views/realization/NonRegularRealizationView.vue'),
    meta: { title: 'Realisasi Program Non Rutin', menu_key: 'distribution.realization.non-regular.list', domain: 'distribution' },
  },
  {
    path: '/distribution/monitoring',
    name: 'distribution-monitoring',
    component: () => import('@/modules/distribution/views/monitoring/MonitoringVisitView.vue'),
    meta: { title: 'Monitoring Program Penyaluran', menu_key: 'distribution.monitoring.list', domain: 'distribution' },
  },
  {
    path: '/distribution/realization-return',
    name: 'distribution-realization-return',
    component: () => import('@/modules/distribution/views/realization-return/RealizationReturnView.vue'),
    meta: { title: 'Pengembalian Realisasi Program', menu_key: 'distribution.realization-return.list', domain: 'distribution' },
  },
  // ── Parameter ────────────────────────────────────────────────────────────
  {
    path: '/distribution/parameter/program-type',
    name: 'distribution-parameter-program-type',
    component: () => import('@/modules/distribution/views/parameter/ProgramTypeView.vue'),
    meta: { title: 'Jenis Program', menu_key: 'distribution.parameter.program-type', domain: 'distribution' },
  },
  {
    path: '/distribution/parameter/program',
    name: 'distribution-parameter-program',
    component: () => import('@/modules/distribution/views/parameter/DistributionProgramView.vue'),
    meta: { title: 'Program Penyaluran', menu_key: 'distribution.parameter.program', domain: 'distribution' },
  },
  {
    path: '/distribution/parameter/work-sector',
    name: 'distribution-parameter-work-sector',
    component: () => import('@/modules/distribution/views/parameter/WorkSectorView.vue'),
    meta: { title: 'Bidang Pekerjaan', menu_key: 'distribution.parameter.work-sector', domain: 'distribution' },
  },
  {
    path: '/distribution/parameter/cost-item',
    name: 'distribution-parameter-cost-item',
    component: () => import('@/modules/distribution/views/parameter/CostItemView.vue'),
    meta: { title: 'Rincian Biaya Realisasi', menu_key: 'distribution.parameter.cost-item', domain: 'distribution' },
  },
  // ── Laporan ───────────────────────────────────────────────────────────────
  {
    path: '/distribution/report/proposal-incoming',
    name: 'distribution-report-proposal-incoming',
    component: () => import('@/modules/distribution/views/reports/LaporanProposalIncomingView.vue'),
    meta: { title: 'Laporan Proposal Masuk', menu_key: 'distribution.report.proposal-incoming', domain: 'distribution' },
  },
  {
    path: '/distribution/report/mustahiq-list',
    name: 'distribution-report-mustahiq-list',
    component: () => import('@/modules/distribution/views/reports/LaporanMustahiqListView.vue'),
    meta: { title: 'Laporan Daftar Mustahiq', menu_key: 'distribution.report.mustahiq-list', domain: 'distribution' },
  },
  {
    path: '/distribution/report/realization-regular',
    name: 'distribution-report-realization-regular',
    component: () => import('@/modules/distribution/views/reports/LaporanRealizationRegularView.vue'),
    meta: { title: 'Laporan Program Penyaluran Rutin', menu_key: 'distribution.report.realization-regular', domain: 'distribution' },
  },
  {
    path: '/distribution/report/realization-non-regular',
    name: 'distribution-report-realization-non-regular',
    component: () => import('@/modules/distribution/views/reports/LaporanRealizationNonRegularView.vue'),
    meta: { title: 'Laporan Program Penyaluran Non Rutin', menu_key: 'distribution.report.realization-non-regular', domain: 'distribution' },
  },
  {
    path: '/distribution/report/realization-receivable',
    name: 'distribution-report-realization-receivable',
    component: () => import('@/modules/distribution/views/reports/LaporanRealizationReceivableView.vue'),
    meta: { title: 'Laporan Piutang Realisasi Penyaluran', menu_key: 'distribution.report.realization-receivable', domain: 'distribution' },
  },
  {
    path: '/distribution/report/realization-return',
    name: 'distribution-report-realization-return',
    component: () => import('@/modules/distribution/views/reports/LaporanRealizationReturnView.vue'),
    meta: { title: 'Laporan Pengembalian Realisasi', menu_key: 'distribution.report.realization-return', domain: 'distribution' },
  },
  {
    path: '/distribution/report/realization-by-mustahiq',
    name: 'distribution-report-realization-by-mustahiq',
    component: () => import('@/modules/distribution/views/reports/LaporanRealizationByMustahiqView.vue'),
    meta: { title: 'Laporan Penyaluran Per Mustahiq', menu_key: 'distribution.report.realization-by-mustahiq', domain: 'distribution' },
  },
]
