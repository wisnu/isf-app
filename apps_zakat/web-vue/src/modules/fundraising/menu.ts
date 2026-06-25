import { Inbox, BookOpen, FileDown } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const fundraisingMenu: DomainConfig = {
  id: 'fundraising',
  label: 'Penghimpunan',
  sub: 'Data muzakki, donatur & penghimpunan dana',
  icon: Inbox,
  locked: false,
  defaultRoute: '/fundraising/donors/corporate',
  groups: [
    {
      id: 'kegiatan',
      label: 'Kegiatan',
      icon: BookOpen,
      items: [
        { label: 'Data Donatur Korporat', to: '/fundraising/donors/corporate', menu_key: 'fundraising.donor.corporate' },
        { label: 'Data Donatur Individu', to: '/fundraising/donors/individual', menu_key: 'fundraising.donor.individual' },
        { label: 'Konfirmasi Donasi', to: '/fundraising/donation-confirm', menu_key: 'fundraising.donation.confirm' },
        { label: 'Cetak Bukti Setor Zakat', to: '/fundraising/bsz', menu_key: 'fundraising.donation.bsz' },
      ],
    },
    {
      id: 'laporan',
      label: 'Laporan',
      icon: FileDown,
      items: [
        { label: 'Export Donasi HC Batch', to: '/fundraising/reports/export-hc-batch', menu_key: 'fundraising.report.export-penghimpunan-website-hc-batch' },
        { label: 'Export Donasi Website (Baru)', to: '/fundraising/reports/export-website-new', menu_key: 'fundraising.report.export-penghimpunan-website-new' },
      ],
    },
  ],
}
