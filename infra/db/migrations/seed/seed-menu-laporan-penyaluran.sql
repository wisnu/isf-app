-- Seed: Laporan Penyaluran — 7 laporan distribution reports
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Laporan
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.report.proposal-incoming         → [ ] PENDING
--               distribution.report.mustahiq-list             → [ ] PENDING
--               distribution.report.realization-regular       → [ ] PENDING
--               distribution.report.realization-non-regular   → [ ] PENDING
--               distribution.report.realization-receivable    → [ ] PENDING
--               distribution.report.realization-return        → [ ] PENDING
--               distribution.report.realization-by-mustahiq  → [ ] PENDING
-- routes.ts:    /distribution/report/proposal-incoming        → [ ] PENDING
--               /distribution/report/mustahiq-list            → [ ] PENDING
--               /distribution/report/realization-regular      → [ ] PENDING
--               /distribution/report/realization-non-regular  → [ ] PENDING
--               /distribution/report/realization-receivable   → [ ] PENDING
--               /distribution/report/realization-return       → [ ] PENDING
--               /distribution/report/realization-by-mustahiq → [ ] PENDING
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.report.proposal-incoming',
    'Laporan Proposal Masuk',
    'Program / Penyaluran',
    '/distribution/report/proposal-incoming',
    340,
    'A'
  ),
  (
    'distribution.report.mustahiq-list',
    'Laporan Daftar Mustahiq',
    'Program / Penyaluran',
    '/distribution/report/mustahiq-list',
    341,
    'A'
  ),
  (
    'distribution.report.realization-regular',
    'Laporan Program Penyaluran Rutin',
    'Program / Penyaluran',
    '/distribution/report/realization-regular',
    342,
    'A'
  ),
  (
    'distribution.report.realization-non-regular',
    'Laporan Program Penyaluran Non Rutin',
    'Program / Penyaluran',
    '/distribution/report/realization-non-regular',
    343,
    'A'
  ),
  (
    'distribution.report.realization-receivable',
    'Laporan Piutang Realisasi Penyaluran',
    'Program / Penyaluran',
    '/distribution/report/realization-receivable',
    344,
    'A'
  ),
  (
    'distribution.report.realization-return',
    'Laporan Pengembalian Realisasi',
    'Program / Penyaluran',
    '/distribution/report/realization-return',
    345,
    'A'
  ),
  (
    'distribution.report.realization-by-mustahiq',
    'Laporan Penyaluran Per Mustahiq',
    'Program / Penyaluran',
    '/distribution/report/realization-by-mustahiq',
    346,
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
-- ============================================================================
-- Roles dari legacy Penyaluran.mnu: AllowedGroups='DIST;SPVDIST' untuk semua laporan
-- QAC dari legacy tidak ada di isf-app → diabaikan

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.report.proposal-incoming',        'system'),
  ('SPVDIST', 'distribution.report.proposal-incoming',        'system'),
  ('DIST',    'distribution.report.mustahiq-list',            'system'),
  ('SPVDIST', 'distribution.report.mustahiq-list',            'system'),
  ('DIST',    'distribution.report.realization-regular',      'system'),
  ('SPVDIST', 'distribution.report.realization-regular',      'system'),
  ('DIST',    'distribution.report.realization-non-regular',  'system'),
  ('SPVDIST', 'distribution.report.realization-non-regular',  'system'),
  ('DIST',    'distribution.report.realization-receivable',   'system'),
  ('SPVDIST', 'distribution.report.realization-receivable',   'system'),
  ('DIST',    'distribution.report.realization-return',       'system'),
  ('SPVDIST', 'distribution.report.realization-return',       'system'),
  ('DIST',    'distribution.report.realization-by-mustahiq',  'system'),
  ('SPVDIST', 'distribution.report.realization-by-mustahiq',  'system')
ON CONFLICT DO NOTHING;
