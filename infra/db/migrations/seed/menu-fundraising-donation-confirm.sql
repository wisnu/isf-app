-- Seed: Konfirmasi Transaksi Donasi
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Fundraising / Penghimpunan
-- Legacy: Penghimpunan.mnu > Kegiatan > DonationTransactionClick
-- AllowedGroups legacy: ADM;PHP;SPVPHP
-- Tanggal: 2026-06-26

-- 3-Way Consistency Check:
-- menu-keys.ts: fundraising.donation.confirm → ADDED
-- routes.ts:    /fundraising/donation-confirm → TAMBAHKAN saat buat halaman
-- seed SQL:     [x] FILE INI

-- Actions (mapped ke usePermission standard):
--   view    → akses halaman + lihat list
--   hapus   → hapus transaksi (PHP: own-branch + authstatus='F'; SPVPHP: all)
--   tambah  → post jurnal (SPVPHP saja)
--   edit    → edit donatur pada baris
--   detail  → cetak kwitansi

BEGIN;

-- ============================================================================
-- PART 1: Menu entry (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'fundraising.donation.confirm',
    'Konfirmasi Transaksi Donasi',
    'Penghimpunan / Kegiatan',
    '/fundraising/donation-confirm',
    403,
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
--   ADM    → view only (admin monitoring, tidak hapus/posting)
--   PHP    → view, hapus (own-branch, authstatus=F), edit (donatur), detail (cetak kwitansi)
--   SPVPHP → view, hapus (semua branch), tambah (posting jurnal), edit, detail
-- ============================================================================

INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
VALUES
  -- ADM
  ('ADM', 'fundraising.donation.confirm', 'view'),

  -- PHP (Penghimpunan)
  ('PHP', 'fundraising.donation.confirm', 'view'),
  ('PHP', 'fundraising.donation.confirm', 'hapus'),
  ('PHP', 'fundraising.donation.confirm', 'edit'),
  ('PHP', 'fundraising.donation.confirm', 'detail'),

  -- SPVPHP (Supervisor Penghimpunan)
  ('SPVPHP', 'fundraising.donation.confirm', 'view'),
  ('SPVPHP', 'fundraising.donation.confirm', 'hapus'),
  ('SPVPHP', 'fundraising.donation.confirm', 'tambah'),
  ('SPVPHP', 'fundraising.donation.confirm', 'edit'),
  ('SPVPHP', 'fundraising.donation.confirm', 'detail')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

COMMIT;
