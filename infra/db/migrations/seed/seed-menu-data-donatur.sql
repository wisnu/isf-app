-- Seed: Data Donatur Korporat & Data Donatur Individu
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Fundraising / Penghimpunan
-- Legacy: Penghimpunan.mnu > Kegiatan > CorporateDonorClick / IndividualDonorClick
-- AllowedGroups legacy: ADM;PHP;SPVPHP
-- Tanggal: 2026-06-25

-- 3-Way Consistency Check:
-- menu-keys.ts: fundraising.donor.corporate → TAMBAHKAN di menu-keys.ts
-- menu-keys.ts: fundraising.donor.individual → TAMBAHKAN di menu-keys.ts
-- routes.ts: /fundraising/donors/corporate → TAMBAHKAN di routes.ts
-- routes.ts: /fundraising/donors/individual → TAMBAHKAN di routes.ts

BEGIN;

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'fundraising.donor.corporate',
    'Data Donatur Korporat',
    'Penghimpunan / Kegiatan',
    '/fundraising/donors/corporate',
    401,
    'A'
  ),
  (
    'fundraising.donor.individual',
    'Data Donatur Individu',
    'Penghimpunan / Kegiatan',
    '/fundraising/donors/individual',
    402,
    'A'
  )
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status;

-- ============================================================================
-- PART 2: Role permissions (isf_auth.role_menu_permission)
-- Roles: PHP (Penghimpunan), SPVPHP (Supervisor), ADM (Admin)
-- Actions: view, tambah, edit (hapus tidak tersedia — hanya nonaktif/aktif)
-- ============================================================================

INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
VALUES
  ('ADM',    'fundraising.donor.corporate',  'view'),
  ('ADM',    'fundraising.donor.corporate',  'tambah'),
  ('ADM',    'fundraising.donor.corporate',  'edit'),
  ('PHP',    'fundraising.donor.corporate',  'view'),
  ('PHP',    'fundraising.donor.corporate',  'tambah'),
  ('PHP',    'fundraising.donor.corporate',  'edit'),
  ('SPVPHP', 'fundraising.donor.corporate',  'view'),
  ('SPVPHP', 'fundraising.donor.corporate',  'tambah'),
  ('SPVPHP', 'fundraising.donor.corporate',  'edit'),
  ('ADM',    'fundraising.donor.individual', 'view'),
  ('ADM',    'fundraising.donor.individual', 'tambah'),
  ('ADM',    'fundraising.donor.individual', 'edit'),
  ('PHP',    'fundraising.donor.individual', 'view'),
  ('PHP',    'fundraising.donor.individual', 'tambah'),
  ('PHP',    'fundraising.donor.individual', 'edit'),
  ('SPVPHP', 'fundraising.donor.individual', 'view'),
  ('SPVPHP', 'fundraising.donor.individual', 'tambah'),
  ('SPVPHP', 'fundraising.donor.individual', 'edit')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

COMMIT;
