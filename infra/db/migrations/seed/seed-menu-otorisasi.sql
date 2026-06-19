-- Seed for "Monitoring dan Kontrol" menu group and "Otorisasi" child menu
-- Parent: finance.monitoring (group label)
-- Child: finance.monitoring.authorization (route: /finance/monitoring/authorization)
-- Access: SPVDIST, SPVADM, SPVACC, SPVKEU, SPVPHP, SPVGA (all supervisory roles)

-- Parent menu: Monitoring dan Kontrol
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.monitoring',
  'Monitoring dan Kontrol',
  'Keuangan',
  NULL,
  155,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  status = EXCLUDED.status;

-- Child menu: Otorisasi
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.monitoring.authorization',
  'Otorisasi',
  'Keuangan',
  '/finance/monitoring/authorization',
  156,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- Role assignments for otorisasi menu (supervisory roles)
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('SPVDIST', 'finance.monitoring.authorization', 'system'),
  ('SPVADM',  'finance.monitoring.authorization', 'system'),
  ('SPVACC',  'finance.monitoring.authorization', 'system'),
  ('SPVKEU',  'finance.monitoring.authorization', 'system'),
  ('SPVPHP',  'finance.monitoring.authorization', 'system'),
  ('SPVGA',   'finance.monitoring.authorization', 'system'),
  ('ADM',     'finance.monitoring.authorization', 'system')
ON CONFLICT DO NOTHING;
