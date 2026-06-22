import type { RouteRecordRaw } from 'vue-router'

export const distributionRoutes: RouteRecordRaw[] = [
  {
    path: '/distribution/mustahiq/corporate',
    name: 'distribution-mustahiq-corporate',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporateView.vue'),
    meta: { title: 'Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal',
    name: 'distribution-mustahiq-personal',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalView.vue'),
    meta: { title: 'Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
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
]
