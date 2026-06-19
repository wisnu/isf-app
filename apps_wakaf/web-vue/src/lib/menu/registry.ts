export const MENU_KEYS = [
  'dashboard.overview',
  'dashboard.finance',
  'dashboard.distribution',
  'dashboard.collection',
  'finance.coa',
  'finance.cash',
  'finance.bank',
  'finance.reports.daily_journal',
  'finance.reports.general_transaction',
  'finance.reports.daily_cash',
  'finance.reports.cash_summary',
  'finance.reports.monthly_balance',
  'admin.role_menu',
  'admin.users',
  'finance.parameter.budget_owner',
  'finance.parameter.budget_owner.create',
  'finance.parameter.budget_owner.edit',
  'finance.parameter.budget_owner.delete',
] as const

export type MenuKey = typeof MENU_KEYS[number]

export function isKnownMenuKey(value: string): value is MenuKey {
  return (MENU_KEYS as readonly string[]).includes(value)
}
