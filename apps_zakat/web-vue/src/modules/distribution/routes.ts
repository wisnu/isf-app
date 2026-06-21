import type { RouteRecordRaw } from 'vue-router'

export const distributionRoutes: RouteRecordRaw[] = [
  {
    path: '/distribution/mustahiq/corporate',
    name: 'distribution-mustahiq-corporate',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqCorporatePage.vue'),
    meta: { title: 'Mustahiq Lembaga', menu_key: 'distribution.mustahiq.corporate', domain: 'distribution' },
  },
  {
    path: '/distribution/mustahiq/personal',
    name: 'distribution-mustahiq-personal',
    component: () => import('@/modules/distribution/views/mustahiq/MustahiqPersonalPage.vue'),
    meta: { title: 'Mustahiq Individu', menu_key: 'distribution.mustahiq.personal', domain: 'distribution' },
  },
]
