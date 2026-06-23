import type { RouteRecordRaw } from 'vue-router'
import type { MenuKey } from '@/shared/constants/menu-keys'

export const appadminRoutes: RouteRecordRaw[] = [
  {
    path: '/appadmin/role-menu',
    name: 'appadmin-role-menu',
    component: () => import('./views/role-menu/RoleMenuView.vue'),
    meta: { title: 'Mapping Role-Menu', menu_key: 'appadmin.role_menu' as MenuKey, domain: 'appadmin' },
  },
  {
    path: '/appadmin/users',
    name: 'appadmin-users',
    component: () => import('./views/users/UsersView.vue'),
    meta: { title: 'List User', menu_key: 'appadmin.users' as MenuKey, domain: 'appadmin' },
  },
  {
    path: '/appadmin/branches',
    name: 'appadmin-branches',
    component: () => import('./views/branches/BranchesView.vue'),
    meta: { title: 'List Cabang', menu_key: 'appadmin.branch.list' as MenuKey, domain: 'appadmin' },
  },
  {
    path: '/appadmin/roles',
    name: 'appadmin-roles',
    component: () => import('./views/roles/RolesView.vue'),
    meta: { title: 'List Role', menu_key: 'appadmin.roles' as MenuKey, domain: 'appadmin' },
  },
]
