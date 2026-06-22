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
]
