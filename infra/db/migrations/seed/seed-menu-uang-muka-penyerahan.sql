-- Seed: Transaksi Penyerahan Uang Muka
-- Portal: Zakat
-- Fitur: Transaksi Penyerahan Uang Muka (Cash Advance Disbursement)
-- Tanggal: 2026-06-15

-- 3-Way Consistency Check:
-- registry.ts: finance.transactions.cash_advance → [ ] BELUM ADA (perlu tambah)
-- router.ts:   /finance/transactions/cash-advance → [ ] BELUM ADA (perlu tambah)
-- seed SQL:    [x] GENERATE di file ini

-- 1. Menu entry: Penyerahan Uang Muka (transaksi input)
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.cash_advance',
  'Penyerahan Uang Muka',
  'Keuangan',
  '/finance/transactions/cash-advance',
  147,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- 2. Role assignment: ACC (Accounting)
-- Transaksi penyerahan uang muka (cash advance disbursement) adalah transaksi akuntansi
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.transactions.cash_advance', 'system')
ON CONFLICT DO NOTHING;
