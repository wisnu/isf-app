-- Seed for "Kas Kecil" menu and role_menu entries
-- Feature: Rekening Kas Kecil (Petty Cash) — migrasi dari fDaftarRekeningKasKecil (DAF)
-- Portal: zakat

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.kas_kecil',
  'Kas Kecil',
  'Keuangan',
  '/keuangan/kas-kecil',
  135,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status;

-- Roles: ADM, KEU, ACC
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADM', 'keuangan.kas_kecil', 'system'),
  ('KEU', 'keuangan.kas_kecil', 'system'),
  ('ACC', 'keuangan.kas_kecil', 'system')
ON CONFLICT DO NOTHING;
