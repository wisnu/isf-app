import { FolderOpen } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const generalaffairMenu: DomainConfig = {
  id: 'generalaffair',
  label: 'Administrasi & Umum',
  sub: 'Kepegawaian, surat, aset & perlengkapan',
  icon: FolderOpen,
  locked: false,
  defaultRoute: '/generalaffair/dokumen-masuk',
  groups: [
    {
      label: 'Parameter',
      children: [
        { label: 'Jenis Dokumen', menu_key: 'generalaffair.parameter.document-type', route: 'generalaffair-jenis-dokumen' },
      ],
    },
    {
      label: 'Manajemen Dokumen',
      children: [
        { label: 'Dokumen Masuk', menu_key: 'generalaffair.document.incoming', route: 'generalaffair-dokumen-masuk-list' },
        { label: 'Dokumen Keluar', menu_key: 'generalaffair.document.outgoing', route: 'generalaffair-dokumen-keluar-list' },
      ],
    },
    {
      label: 'Laporan',
      children: [
        { label: 'Laporan Dokumen Masuk', menu_key: 'generalaffair.report.incoming-document', route: 'generalaffair-laporan-dokumen-masuk' },
        { label: 'Laporan Dokumen Keluar', menu_key: 'generalaffair.report.outgoing-document', route: 'generalaffair-laporan-dokumen-keluar' },
      ],
    },
  ],
}
