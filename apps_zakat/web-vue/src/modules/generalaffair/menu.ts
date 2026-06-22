import { FolderOpen } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const generalaffairMenu: DomainConfig = {
  id: 'generalaffair',
  label: 'Administrasi & Umum',
  sub: 'Kepegawaian, surat, aset & perlengkapan',
  icon: FolderOpen,
  locked: true,
  lockedBadge: 'Belum tersedia',
  defaultRoute: '/',
  groups: [],
}
