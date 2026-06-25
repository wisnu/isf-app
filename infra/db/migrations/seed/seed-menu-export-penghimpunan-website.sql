-- Seed: Export Penghimpunan Website (dua varian)
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Fundraising / Penghimpunan / Laporan
-- Legacy: Penghimpunan.mnu > Kegiatan > "Export Data Penghimpunan Untuk Website" (HC Batch)
--         Penghimpunan.mnu > Kegiatan > "Export Data Penghimpunan Untuk Website(New)" (Date Range)
-- AllowedGroups legacy: ADM;PHP;SPVPHP
-- Tanggal: 2026-06-26

-- 3-Way Consistency Check:
-- menu-keys.ts: fundraising.report.export-penghimpunan-website-hc-batch → ADDED
--               fundraising.report.export-penghimpunan-website-new      → ADDED
-- routes.ts:    /fundraising/report/export-penghimpunan-website-hc-batch → PENDING
--               /fundraising/report/export-penghimpunan-website-new      → PENDING
-- seed SQL:     [x] FILE INI

-- Aksi:
--   view → akses halaman + download Excel report (HC Batch dan Date Range)
--   Catatan: ini adalah laporan export-only (read permission saja, tidak ada create/edit/delete)

BEGIN;

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================
-- Dua menu items: satu untuk HC Batch, satu untuk Date Range
-- Group label: Penghimpunan / Laporan (mengikuti konvensi distribution reports)

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'fundraising.report.export-penghimpunan-website-hc-batch',
    'Export Donasi HC Batch',
    'Penghimpunan / Laporan',
    '/fundraising/report/export-penghimpunan-website-hc-batch',
    501,
    'A'
  ),
  (
    'fundraising.report.export-penghimpunan-website-new',
    'Export Donasi Website (Range Tanggal)',
    'Penghimpunan / Laporan',
    '/fundraising/report/export-penghimpunan-website-new',
    502,
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
--   ADM    → view both export features (admin monitoring + export data)
--   PHP    → view both export features (penghimpunan staff)
--   SPVPHP → view both export features (supervisor penghimpunan)
-- ============================================================================
-- Aksi: hanya 'view' (download Excel adalah bentuk dari read/view permission)
-- Tidak ada create/edit/delete karena ini report export-only

INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
VALUES
  -- ADM
  ('ADM', 'fundraising.report.export-penghimpunan-website-hc-batch', 'view'),
  ('ADM', 'fundraising.report.export-penghimpunan-website-new', 'view'),

  -- PHP (Penghimpunan)
  ('PHP', 'fundraising.report.export-penghimpunan-website-hc-batch', 'view'),
  ('PHP', 'fundraising.report.export-penghimpunan-website-new', 'view'),

  -- SPVPHP (Supervisor Penghimpunan)
  ('SPVPHP', 'fundraising.report.export-penghimpunan-website-hc-batch', 'view'),
  ('SPVPHP', 'fundraising.report.export-penghimpunan-website-new', 'view')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

COMMIT;
