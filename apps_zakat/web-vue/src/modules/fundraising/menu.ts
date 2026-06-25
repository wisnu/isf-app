import { Inbox, BookOpen } from 'lucide-vue-next'
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
      ],
    },
  ],
}
