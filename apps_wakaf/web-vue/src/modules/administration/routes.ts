import type { RouteRecordRaw } from 'vue-router'
import type { MenuKey } from '@/shared/constants/menu-keys'

export const administrationRoutes: RouteRecordRaw[] = [
  {
    path: '/administration/role-menu',
    name: 'administration-role-menu',
    component: () => import('./views/role-menu/RoleMenuView.vue'),
    meta: { title: 'Mapping Role-Menu', menu_key: 'admin.role_menu' as MenuKey, domain: 'administration' },
  },
  {
    path: '/administration/users',
    name: 'administration-users',
    component: () => import('./views/users/UsersView.vue'),
    meta: { title: 'List User', menu_key: 'admin.users' as MenuKey, domain: 'administration' },
  },
]
