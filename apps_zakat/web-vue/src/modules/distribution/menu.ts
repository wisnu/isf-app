import { Users, BookOpen, FileText, BarChart2, Settings } from 'lucide-vue-next'
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
      id: 'parameter',
      label: 'Parameter',
      icon: Settings,
      items: [
        { label: 'Jenis Program',           to: '/distribution/parameter/program-type', menu_key: 'distribution.parameter.program-type' },
        { label: 'Program Penyaluran',      to: '/distribution/parameter/program',      menu_key: 'distribution.parameter.program' },
        { label: 'Bidang Pekerjaan',        to: '/distribution/parameter/work-sector',  menu_key: 'distribution.parameter.work-sector' },
        { label: 'Rincian Biaya Realisasi', to: '/distribution/parameter/cost-item',    menu_key: 'distribution.parameter.cost-item' },
      ],
    },
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
        { label: 'Realisasi Program Rutin',     to: '/distribution/realization/regular',     menu_key: 'distribution.realization.regular.list' },
        { label: 'Realisasi Program Non Rutin', to: '/distribution/realization/non-regular', menu_key: 'distribution.realization.non-regular.list' },
        { label: 'Monitoring Program Penyaluran', to: '/distribution/monitoring', menu_key: 'distribution.monitoring.list' },
        { label: 'Pengembalian Realisasi Program', to: '/distribution/realization-return', menu_key: 'distribution.realization-return.list' },
      ],
    },
    {
      id: 'laporan',
      label: 'Laporan',
      icon: BarChart2,
      items: [
        { label: 'Laporan Proposal Masuk',            to: '/distribution/report/proposal-incoming',       menu_key: 'distribution.report.proposal-incoming' },
        { label: 'Laporan Daftar Mustahiq',           to: '/distribution/report/mustahiq-list',           menu_key: 'distribution.report.mustahiq-list' },
        { label: 'Laporan Penyaluran Rutin',          to: '/distribution/report/realization-regular',     menu_key: 'distribution.report.realization-regular' },
        { label: 'Laporan Penyaluran Non Rutin',      to: '/distribution/report/realization-non-regular', menu_key: 'distribution.report.realization-non-regular' },
        { label: 'Laporan Piutang Realisasi',         to: '/distribution/report/realization-receivable',  menu_key: 'distribution.report.realization-receivable' },
        { label: 'Laporan Pengembalian Realisasi',    to: '/distribution/report/realization-return',      menu_key: 'distribution.report.realization-return' },
        { label: 'Laporan Penyaluran Per Mustahiq',   to: '/distribution/report/realization-by-mustahiq', menu_key: 'distribution.report.realization-by-mustahiq' },
      ],
    },
  ],
}
