import type { RouteRecordRaw } from 'vue-router'

export const generalaffairRoutes: RouteRecordRaw[] = [
  // Parameter
  {
    path: '/generalaffair/parameter/jenis-dokumen',
    name: 'generalaffair-jenis-dokumen',
    component: () => import('./views/document/JenisDokumenView.vue'),
    meta: { menu_key: 'generalaffair.parameter.document-type' },
  },
  // Dokumen Masuk
  {
    path: '/generalaffair/dokumen-masuk',
    name: 'generalaffair-dokumen-masuk-list',
    component: () => import('./views/document/DokumenMasukListView.vue'),
    meta: { menu_key: 'generalaffair.document.incoming' },
  },
  {
    path: '/generalaffair/dokumen-masuk/baru',
    name: 'generalaffair-dokumen-masuk-create',
    component: () => import('./views/document/DokumenMasukFormView.vue'),
    meta: { menu_key: 'generalaffair.document.incoming' },
  },
  {
    path: '/generalaffair/dokumen-masuk/:id/edit',
    name: 'generalaffair-dokumen-masuk-edit',
    component: () => import('./views/document/DokumenMasukFormView.vue'),
    meta: { menu_key: 'generalaffair.document.incoming' },
  },
  // Dokumen Keluar
  {
    path: '/generalaffair/dokumen-keluar',
    name: 'generalaffair-dokumen-keluar-list',
    component: () => import('./views/document/DokumenKeluarListView.vue'),
    meta: { menu_key: 'generalaffair.document.outgoing' },
  },
  {
    path: '/generalaffair/dokumen-keluar/baru',
    name: 'generalaffair-dokumen-keluar-create',
    component: () => import('./views/document/DokumenKeluarFormView.vue'),
    meta: { menu_key: 'generalaffair.document.outgoing' },
  },
  {
    path: '/generalaffair/dokumen-keluar/:id/edit',
    name: 'generalaffair-dokumen-keluar-edit',
    component: () => import('./views/document/DokumenKeluarFormView.vue'),
    meta: { menu_key: 'generalaffair.document.outgoing' },
  },
  // Laporan
  {
    path: '/generalaffair/laporan/dokumen-masuk',
    name: 'generalaffair-laporan-dokumen-masuk',
    component: () => import('./views/document/LaporanDokumenMasukView.vue'),
    meta: { menu_key: 'generalaffair.report.incoming-document' },
  },
  {
    path: '/generalaffair/laporan/dokumen-keluar',
    name: 'generalaffair-laporan-dokumen-keluar',
    component: () => import('./views/document/LaporanDokumenKeluarView.vue'),
    meta: { menu_key: 'generalaffair.report.outgoing-document' },
  },
]
