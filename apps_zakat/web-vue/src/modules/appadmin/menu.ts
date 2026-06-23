import { Building2, Settings, Users } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const appadminMenu: DomainConfig = {
  id: 'appadmin',
  label: 'Pengaturan Akses',
  sub: 'Manajemen user & hak akses',
  icon: Settings,
  locked: false,
  defaultRoute: '/appadmin/users',
  groups: [
    {
      id: 'user-mgmt',
      label: 'Manajemen User',
      icon: Users,
      items: [
        { label: 'List User',   to: '/appadmin/users',    menu_key: 'appadmin.users' },
        { label: 'List Role',   to: '/appadmin/roles',    menu_key: 'appadmin.roles' },
        { label: 'Role & Menu', to: '/appadmin/role-menu', menu_key: 'appadmin.role_menu' },
      ],
    },
    {
      id: 'branch-mgmt',
      label: 'Manajemen Cabang',
      icon: Building2,
      items: [
        { label: 'List Cabang', to: '/appadmin/branches', menu_key: 'appadmin.branch.list' },
      ],
    },
  ],
}
