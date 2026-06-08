-- Seed for "Monitoring dan Kontrol" menu group and "Otorisasi" child menu
-- Parent: keuangan.monitoring (group label)
-- Child: keuangan.monitoring.otorisasi (route: /keuangan/monitoring/otorisasi)
-- Access: SPVDIST, SPVADM, SPVACC, SPVKEU, SPVPHP, SPVGA (all supervisory roles)

-- Parent menu: Monitoring dan Kontrol
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.monitoring',
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
  'keuangan.monitoring.otorisasi',
  'Otorisasi',
  'Keuangan',
  '/keuangan/monitoring/otorisasi',
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
  ('SPVDIST', 'keuangan.monitoring.otorisasi', 'system'),
  ('SPVADM',  'keuangan.monitoring.otorisasi', 'system'),
  ('SPVACC',  'keuangan.monitoring.otorisasi', 'system'),
  ('SPVKEU',  'keuangan.monitoring.otorisasi', 'system'),
  ('SPVPHP',  'keuangan.monitoring.otorisasi', 'system'),
  ('SPVGA',   'keuangan.monitoring.otorisasi', 'system'),
  ('ADM',     'keuangan.monitoring.otorisasi', 'system')
ON CONFLICT DO NOTHING;
