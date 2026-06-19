-- Seed for "Input Penghimpunan Dana" menu and role_menu entries
-- AllowedGroups legacy: ACC (core/menus/Transaksi.mnu TR0020)

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.fund_collection',
  'Input Penghimpunan Dana',
  'Keuangan',
  '/finance/transactions/fund-collection',
  145,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- Role: ACC (dari AllowedGroups legacy)
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.transactions.fund_collection', 'system')
ON CONFLICT DO NOTHING;
