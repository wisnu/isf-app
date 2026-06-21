import { FolderOpen, Users } from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const administrationMenu: DomainConfig = {
  id: 'administration',
  label: 'Administrasi',
  sub: 'Manajemen user & hak akses',
  icon: FolderOpen,
  locked: false,
  defaultRoute: '/administration/users',
  groups: [
    {
      id: 'user-mgmt',
      label: 'Manajemen User',
      icon: Users,
      items: [
        { label: 'List User',  to: '/administration/users',    menu_key: 'admin.users' },
        { label: 'Role & Menu', to: '/administration/role-menu', menu_key: 'admin.role_menu' },
      ],
    },
  ],
}
