-- Seed for "Input Penyaluran Dana" menu and role_menu entries

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.fund_distribution',
  'Input Penyaluran Dana',
  'Keuangan',
  '/finance/transactions/fund-distribution',
  146,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- Role assignments: keuangan, distribusi, admin
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('KEU',     'finance.transactions.fund_distribution', 'system'),
  ('SPVKEU',  'finance.transactions.fund_distribution', 'system'),
  ('SPVDIST', 'finance.transactions.fund_distribution', 'system'),
  ('DIST',    'finance.transactions.fund_distribution', 'system'),
  ('ADM',     'finance.transactions.fund_distribution', 'system')
ON CONFLICT DO NOTHING;
