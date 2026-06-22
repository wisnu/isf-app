-- Menu: Manajemen Dokumen (Document Management) for generalaffair domain
-- Portal: zakat (isf_auth_zakat)
-- Domain: generalaffair
-- Date: 2026-06-23

-- ============================================================================
-- 3-Way Consistency Check:
-- menu-keys.ts:        generalaffair.parameter.document-type      → [ ] PENDING
--                      generalaffair.document.incoming             → [ ] PENDING
--                      generalaffair.document.outgoing             → [ ] PENDING
--                      generalaffair.report.incoming-document      → [ ] PENDING
--                      generalaffair.report.outgoing-document      → [ ] PENDING
-- routes.ts:           /generalaffair/parameter/document-type      → [ ] PENDING
--                      /generalaffair/document/incoming            → [ ] PENDING
--                      /generalaffair/document/outgoing            → [ ] PENDING
--                      /generalaffair/report/incoming-document     → [ ] PENDING
--                      /generalaffair/report/outgoing-document     → [ ] PENDING
-- seed SQL:            [x] FILE INI
-- ============================================================================

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'generalaffair.parameter.document-type',
    'Jenis Dokumen',
    'Parameter',
    '/generalaffair/parameter/document-type',
    1001,
    'A'
  ),
  (
    'generalaffair.document.incoming',
    'Dokumen Masuk',
    'Manajemen Dokumen',
    '/generalaffair/document/incoming',
    1002,
    'A'
  ),
  (
    'generalaffair.document.outgoing',
    'Dokumen Keluar',
    'Manajemen Dokumen',
    '/generalaffair/document/outgoing',
    1003,
    'A'
  ),
  (
    'generalaffair.report.incoming-document',
    'Laporan Dokumen Masuk',
    'Laporan',
    '/generalaffair/report/incoming-document',
    1004,
    'A'
  ),
  (
    'generalaffair.report.outgoing-document',
    'Laporan Dokumen Keluar',
    'Laporan',
    '/generalaffair/report/outgoing-document',
    1005,
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

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  -- Jenis Dokumen parameter
  ('ADM',    'generalaffair.parameter.document-type', 'seed'),
  ('GA',     'generalaffair.parameter.document-type', 'seed'),
  ('SPVGA',  'generalaffair.parameter.document-type', 'seed'),
  -- Dokumen Masuk
  ('ADM',    'generalaffair.document.incoming', 'seed'),
  ('GA',     'generalaffair.document.incoming', 'seed'),
  ('SPVGA',  'generalaffair.document.incoming', 'seed'),
  -- Dokumen Keluar
  ('ADM',    'generalaffair.document.outgoing', 'seed'),
  ('GA',     'generalaffair.document.outgoing', 'seed'),
  ('SPVGA',  'generalaffair.document.outgoing', 'seed'),
  -- Laporan Dokumen Masuk
  ('ADM',    'generalaffair.report.incoming-document', 'seed'),
  ('GA',     'generalaffair.report.incoming-document', 'seed'),
  ('SPVGA',  'generalaffair.report.incoming-document', 'seed'),
  ('QAC',    'generalaffair.report.incoming-document', 'seed'),
  -- Laporan Dokumen Keluar
  ('ADM',    'generalaffair.report.outgoing-document', 'seed'),
  ('GA',     'generalaffair.report.outgoing-document', 'seed'),
  ('SPVGA',  'generalaffair.report.outgoing-document', 'seed'),
  ('QAC',    'generalaffair.report.outgoing-document', 'seed')
ON CONFLICT DO NOTHING;
