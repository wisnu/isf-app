import type { FunctionalComponent } from 'vue'
import type { MenuKey } from './menu-keys'

export type DomainId = 'finance' | 'administration' | 'fundraising' | 'distribution' | 'enterprise'

export interface NavItem {
  label: string
  to: string
  menu_key?: MenuKey | string
}

export interface NavSection {
  section: string
}

export interface NavGroup {
  id: string
  label: string
  icon: FunctionalComponent
  items: (NavItem | NavSection)[]
}

export interface DomainConfig {
  id: DomainId
  label: string
  sub: string
  icon: FunctionalComponent
  locked: boolean
  lockedBadge?: string
  defaultRoute: string
  groups: NavGroup[]
}

import {
  Coins,
  Users,
  Inbox,
  FolderOpen,
  Building2,
} from 'lucide-vue-next'

import { financeMenu }        from '@/modules/finance/menu'
import { administrationMenu } from '@/modules/administration/menu'
import { distributionMenu }   from '@/modules/distribution/menu'

export const DOMAIN_MAP: Record<DomainId, DomainConfig> = {
  finance:        financeMenu,
  administration: administrationMenu,
  distribution:   distributionMenu,
  fundraising: {
    id: 'fundraising', label: 'Penghimpunan', sub: 'Data muzakki & donasi',
    icon: Inbox, locked: true, lockedBadge: 'Fase 3',
    defaultRoute: '/', groups: [],
  },
  enterprise: {
    id: 'enterprise', label: 'Enterprise', sub: 'Konfigurasi & parameter sistem',
    icon: Building2, locked: true, lockedBadge: 'Fase 4',
    defaultRoute: '/', groups: [],
  },
}

export const DOMAIN_ORDER: DomainId[] = [
  'finance', 'distribution', 'fundraising', 'administration', 'enterprise',
]
