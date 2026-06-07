-- Seed for "Input Penyaluran Dana" menu and role_menu entries

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.transaksi.penyaluran',
  'Input Penyaluran Dana',
  'Keuangan',
  '/keuangan/transaksi/penyaluran',
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
  ('KEU',     'keuangan.transaksi.penyaluran', 'system'),
  ('SPVKEU',  'keuangan.transaksi.penyaluran', 'system'),
  ('SPVDIST', 'keuangan.transaksi.penyaluran', 'system'),
  ('DIST',    'keuangan.transaksi.penyaluran', 'system'),
  ('ADM',     'keuangan.transaksi.penyaluran', 'system')
ON CONFLICT DO NOTHING;
