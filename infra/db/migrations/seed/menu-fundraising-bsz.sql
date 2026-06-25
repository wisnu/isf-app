-- Seed: Cetak Bukti Setor Zakat (BSZ)
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Fundraising / Penghimpunan / Kegiatan
-- Legacy: Penghimpunan.mnu > Kegiatan > CetakClick → fBSZList
-- AllowedGroups legacy: ADM;PHP;SPVPHP
-- Tanggal: 2026-06-26

-- 3-Way Consistency Check:
-- menu-keys.ts: fundraising.donation.bsz → ADDED
-- routes.ts:    /fundraising/bsz, /fundraising/bsz/create, /fundraising/bsz/:id → ADDED
-- seed SQL:     [x] FILE INI

-- Actions:
--   view    → akses halaman + lihat list BSZ
--   tambah  → buat BSZ baru (ADM;PHP;SPVPHP)
--   hapus   → hapus BSZ
--   detail  → lihat detail + cetak BSZ

BEGIN;

-- ============================================================================
-- PART 1: Menu entry (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'fundraising.donation.bsz',
    'Cetak Bukti Setor Zakat',
    'Penghimpunan / Kegiatan',
    '/fundraising/bsz',
    404,
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
-- Roles:
--   ADM    → view, tambah, hapus, detail (admin monitoring)
--   PHP    → view, tambah, hapus, detail
--   SPVPHP → view, tambah, hapus, detail
-- ============================================================================

INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
VALUES
  -- ADM
  ('ADM', 'fundraising.donation.bsz', 'view'),
  ('ADM', 'fundraising.donation.bsz', 'tambah'),
  ('ADM', 'fundraising.donation.bsz', 'hapus'),
  ('ADM', 'fundraising.donation.bsz', 'detail'),

  -- PHP (Penghimpunan)
  ('PHP', 'fundraising.donation.bsz', 'view'),
  ('PHP', 'fundraising.donation.bsz', 'tambah'),
  ('PHP', 'fundraising.donation.bsz', 'hapus'),
  ('PHP', 'fundraising.donation.bsz', 'detail'),

  -- SPVPHP (Supervisor Penghimpunan)
  ('SPVPHP', 'fundraising.donation.bsz', 'view'),
  ('SPVPHP', 'fundraising.donation.bsz', 'tambah'),
  ('SPVPHP', 'fundraising.donation.bsz', 'hapus'),
  ('SPVPHP', 'fundraising.donation.bsz', 'detail')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

COMMIT;
