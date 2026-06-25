import type { RouteRecordRaw } from 'vue-router'

export const fundraisingRoutes: RouteRecordRaw[] = [
  // ── Donor Korporat ──────────────────────────────────────────────────────────
  {
    path: '/fundraising/donors/corporate',
    name: 'fundraising-donor-corporate-list',
    component: () => import('@/modules/fundraising/views/donor/CorporateDonorView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.corporate' },
  },
  {
    path: '/fundraising/donors/corporate/create',
    name: 'fundraising-donor-corporate-create',
    component: () => import('@/modules/fundraising/views/donor/CorporateDonorFormView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.corporate' },
  },
  {
    path: '/fundraising/donors/corporate/:id/edit',
    name: 'fundraising-donor-corporate-edit',
    component: () => import('@/modules/fundraising/views/donor/CorporateDonorFormView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.corporate' },
  },
  // ── Donor Individu ──────────────────────────────────────────────────────────
  {
    path: '/fundraising/donors/individual',
    name: 'fundraising-donor-individual-list',
    component: () => import('@/modules/fundraising/views/donor/IndividualDonorView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.individual' },
  },
  {
    path: '/fundraising/donors/individual/create',
    name: 'fundraising-donor-individual-create',
    component: () => import('@/modules/fundraising/views/donor/IndividualDonorFormView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.individual' },
  },
  {
    path: '/fundraising/donors/individual/:id/edit',
    name: 'fundraising-donor-individual-edit',
    component: () => import('@/modules/fundraising/views/donor/IndividualDonorFormView.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donor.individual' },
  },
]
