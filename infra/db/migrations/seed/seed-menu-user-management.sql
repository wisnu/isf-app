-- Menu: Pengelolaan User (User Management) + Role Management
-- Portal: zakat (isf_auth_zakat)
-- Domain: appadmin
-- Date: 2026-06-22

-- ============================================================
-- 1. INSERT menu rows
-- ============================================================
INSERT INTO isf_auth.menu (menu_key, label, group_label, sort_order, status) VALUES
  ('appadmin.users.create', 'Input User Baru',       'Manajemen User',  921, 'A'),
  ('appadmin.users.edit',   'Koreksi Data User',     'Manajemen User',  922, 'A'),
  ('appadmin.roles',        'Inquiry Role',           'Manajemen User',  923, 'A'),
  ('appadmin.roles.create', 'Input Role Baru',        'Manajemen User',  924, 'A'),
  ('appadmin.roles.edit',   'Koreksi Data Role',      'Manajemen User',  925, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status;

-- ============================================================
-- 2. GRANT to ADM role
-- ============================================================
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES
  ('ADM', 'appadmin.users.create', 'seed'),
  ('ADM', 'appadmin.users.edit',   'seed'),
  ('ADM', 'appadmin.roles',        'seed'),
  ('ADM', 'appadmin.roles.create', 'seed'),
  ('ADM', 'appadmin.roles.edit',   'seed')
ON CONFLICT DO NOTHING;
