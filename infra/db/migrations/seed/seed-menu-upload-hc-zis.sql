-- Seed: Upload Data Penerimaan ZIS Rutin
-- Portal: Zakat
-- Fitur: Upload HC ZIS (Penerimaan ZIS Rutin)
-- Tanggal: 2026-06-15

-- 1. Menu entry: Upload ZIS Rutin form
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.upload.zis_routine',
  'Upload ZIS Rutin',
  'Keuangan',
  '/finance/upload/zis-routine',
  192,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- 2. Menu entry: List/Monitoring Upload ZIS Rutin
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.upload.zis_routine_list',
  'Daftar Upload ZIS Rutin',
  'Keuangan',
  '/finance/upload/zis-routine/list',
  193,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- 3. Assign role_menu: ACC (upload + list)
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.upload.zis_routine', 'system'),
  ('ACC', 'finance.upload.zis_routine_list', 'system')
ON CONFLICT DO NOTHING;

-- 4. Assign role_menu: SPVKEU (list only — monitoring)
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('SPVKEU', 'finance.upload.zis_routine_list', 'system')
ON CONFLICT DO NOTHING;
