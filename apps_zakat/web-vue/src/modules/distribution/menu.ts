import { Users, BookOpen } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const distributionMenu: DomainConfig = {
  id: 'distribution',
  label: 'Program / Penyaluran',
  sub: 'Manajemen penerima manfaat & distribusi',
  icon: Users,
  locked: false,
  defaultRoute: '/distribution/mustahiq/corporate',
  groups: [
    {
      id: 'mustahiq',
      label: 'Data Mustahiq',
      icon: BookOpen,
      items: [
        { label: 'Mustahiq Lembaga', to: '/distribution/mustahiq/corporate', menu_key: 'distribution.mustahiq.corporate' },
        { label: 'Mustahiq Individu', to: '/distribution/mustahiq/personal',  menu_key: 'distribution.mustahiq.personal' },
      ],
    },
  ],
}
