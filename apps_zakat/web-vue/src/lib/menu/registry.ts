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
  'keuangan.report.trial_balance',
  'keuangan.report.neraca',
  'keuangan.report.cash_flow',
  'keuangan.report.general_ledger',
  'keuangan.report.fund_changes',
  'keuangan.report.fund_changes_detail',
  'keuangan.report.amil_in',
  'keuangan.report.amil_out',
  'keuangan.report.distribution',
  'keuangan.report.collection',
  'keuangan.report.ar_employee',
  'keuangan.report.ar_external',
  'keuangan.report.ca_employee',
  'keuangan.report.ca_list',
  'keuangan.report.project_memo',
  'keuangan.report.program_ar',
  'keuangan.report.upz',
  'keuangan.transaksi.histori',
  'keuangan.transaksi.penyaluran',
  'keuangan.upload.penghimpunan',
  'keuangan.upload.penghimpunan.approve',
  'admin.role_menu',
  'admin.users',
] as const

export type MenuKey = typeof MENU_KEYS[number]

export function isKnownMenuKey(value: string): value is MenuKey {
  return (MENU_KEYS as readonly string[]).includes(value)
}
