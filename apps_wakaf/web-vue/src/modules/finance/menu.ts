import {
  LayoutDashboard,
  BookOpen,
  FileText,
  Coins,
} from 'lucide-vue-next'
import type { DomainConfig } from '@/shared/constants/domains'

export const financeMenu: DomainConfig = {
  id: 'finance',
  label: 'Keuangan',
  sub: 'Akuntansi & Transaksi',
  icon: Coins,
  locked: false,
  defaultRoute: '/',
  groups: [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
      items: [
        { label: 'Overview',     to: '/',                       menu_key: 'dashboard.overview' },
        { label: 'Keuangan',     to: '/dashboard/finance',      menu_key: 'dashboard.finance' },
        { label: 'Penyaluran',   to: '/dashboard/distribution', menu_key: 'dashboard.distribution' },
        { label: 'Penghimpunan', to: '/dashboard/collection',   menu_key: 'dashboard.collection' },
      ],
    },
    {
      id: 'master',
      label: 'Master Data',
      icon: BookOpen,
      items: [
        { label: 'Chart of Accounts', to: '/finance/coa',                menu_key: 'finance.coa' },
        { label: 'Kas',               to: '/finance/cash',               menu_key: 'finance.cash' },
        { label: 'Bank',              to: '/finance/bank',               menu_key: 'finance.bank' },
        { label: 'Pemilik Anggaran',  to: '/finance/master/budget-owner', menu_key: 'finance.parameter.budget_owner' },
      ],
    },
    {
      id: 'reports',
      label: 'Laporan',
      icon: FileText,
      items: [
        { section: 'Kas & Transaksi' },
        { label: 'Transaksi Kas/Bank Harian',   to: '/finance/reports/daily-cash',          menu_key: 'finance.reports.daily_cash' },
        { label: 'Rekapitulasi Kas/Bank',        to: '/finance/reports/cash-summary',        menu_key: 'finance.reports.cash_summary' },
        { label: 'Monitoring Saldo Bulanan',     to: '/finance/reports/monthly-balance',     menu_key: 'finance.reports.monthly_balance' },
        { label: 'Jurnal Harian',                to: '/finance/reports/daily-journal',       menu_key: 'finance.reports.daily_journal' },
        { label: 'List Transaksi Umum',          to: '/finance/reports/general-transaction', menu_key: 'finance.reports.general_transaction' },
      ],
    },
  ],
}
