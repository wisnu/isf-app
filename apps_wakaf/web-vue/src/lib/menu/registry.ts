export const MENU_KEYS = [
  'dashboard.overview',
  'dashboard.keuangan',
  'dashboard.penyaluran',
  'dashboard.penghimpunan',
  'keuangan.coa',
  'keuangan.kas',
  'keuangan.bank',
  'keuangan.report.journal_daily',
  'keuangan.report.general_transaction',
  'keuangan.report.cash_daily',
  'keuangan.report.cash_summary',
  'keuangan.report.cash_monthly',
  'admin.role_menu',
  'admin.users',
] as const

export type MenuKey = typeof MENU_KEYS[number]

export function isKnownMenuKey(value: string): value is MenuKey {
  return (MENU_KEYS as readonly string[]).includes(value)
}
