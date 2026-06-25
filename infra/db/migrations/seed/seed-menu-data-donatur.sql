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
-- PART 2: Role assignments (isf_auth.role_menu)
-- Roles: PHP (Penghimpunan), SPVPHP (Supervisor), ADM (Admin)
-- ============================================================================

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADM',    'fundraising.donor.corporate',  'system'),
  ('PHP',    'fundraising.donor.corporate',  'system'),
  ('SPVPHP', 'fundraising.donor.corporate',  'system'),
  ('ADM',    'fundraising.donor.individual', 'system'),
  ('PHP',    'fundraising.donor.individual', 'system'),
  ('SPVPHP', 'fundraising.donor.individual', 'system')
ON CONFLICT DO NOTHING;

COMMIT;
