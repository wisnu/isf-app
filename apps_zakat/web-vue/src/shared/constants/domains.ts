import type { FunctionalComponent } from 'vue'
import type { MenuKey } from './menu-keys'

export type DomainId = 'finance' | 'generalaffair' | 'fundraising' | 'distribution' | 'appadmin'

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


import { financeMenu }       from '@/modules/finance/menu'
import { appadminMenu }      from '@/modules/appadmin/menu'
import { generalaffairMenu } from '@/modules/generalaffair/menu'
import { distributionMenu }  from '@/modules/distribution/menu'
import { fundraisingMenu }   from '@/modules/fundraising/menu'

export const DOMAIN_MAP: Record<DomainId, DomainConfig> = {
  finance:      financeMenu,
  appadmin:     appadminMenu,
  generalaffair: generalaffairMenu,
  distribution: distributionMenu,
  fundraising:  fundraisingMenu,
}

export const DOMAIN_ORDER: DomainId[] = [
  'finance', 'distribution', 'fundraising', 'generalaffair', 'appadmin',
]
