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
  // ── Konfirmasi Transaksi Donasi ─────────────────────────────────────
  {
    path: '/fundraising/donation-confirm',
    name: 'fundraising-donation-confirm',
    component: () => import('@/modules/fundraising/views/DonationConfirmPage.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donation.confirm' },
  },
  // ── Cetak Bukti Setor Zakat (BSZ) ────────────────────────────────────
  {
    path: '/fundraising/bsz',
    name: 'fundraising-bsz-list',
    component: () => import('@/modules/fundraising/views/bsz/BszListPage.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donation.bsz' },
  },
  {
    path: '/fundraising/bsz/create',
    name: 'fundraising-bsz-create',
    component: () => import('@/modules/fundraising/views/bsz/BszFormPage.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donation.bsz' },
  },
  {
    path: '/fundraising/bsz/:id/print',
    name: 'fundraising-bsz-print',
    component: () => import('@/modules/fundraising/views/bsz/BszPrintPage.vue'),
    meta: { domain: 'fundraising', menu_key: 'fundraising.donation.bsz' },
  },
]
