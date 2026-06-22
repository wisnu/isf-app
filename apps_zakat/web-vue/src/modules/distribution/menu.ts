import { Users, BookOpen, FileText } from 'lucide-vue-next'
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
    {
      id: 'kegiatan',
      label: 'Kegiatan',
      icon: FileText,
      items: [
        { label: 'Proposal Bantuan Dana', to: '/distribution/proposal', menu_key: 'distribution.proposal.list' },
        { label: 'Mitra', to: '/distribution/partner', menu_key: 'distribution.partner.list' },
        { label: 'Program Rutin',             to: '/distribution/program/regular',          menu_key: 'distribution.program.regular' },
        { label: 'Program Non Rutin',         to: '/distribution/program/non-regular',      menu_key: 'distribution.program.non-regular' },
        { label: 'Memo Penyaluran Rutin',     to: '/distribution/program/memo-regular',     menu_key: 'distribution.program.memo-regular' },
        { label: 'Memo Penyaluran Non Rutin', to: '/distribution/program/memo-non-regular', menu_key: 'distribution.program.memo-non-regular' },
      ],
    },
  ],
}
