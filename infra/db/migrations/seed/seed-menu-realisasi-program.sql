-- Seed: Realisasi Program — realisasi rutin + non rutin
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Kegiatan
-- Fitur: CRUD Realisasi Program (program.realization, discriminator realizationtype R/N)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.realization.regular.list     → [ ] PENDING
--               distribution.realization.non-regular.list → [ ] PENDING
-- routes.ts:    /distribution/realization/regular         → [ ] PENDING
--               /distribution/realization/non-regular     → [ ] PENDING
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.realization.regular.list',
    'Realisasi Program Rutin',
    'Program / Penyaluran',
    '/distribution/realization/regular',
    333,
    'A'
  ),
  (
    'distribution.realization.non-regular.list',
    'Realisasi Program Non Rutin',
    'Program / Penyaluran',
    '/distribution/realization/non-regular',
    334,
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
-- Roles dari legacy Penyaluran.mnu: AllowedGroups='DIST;SPVDIST' untuk Realisasi Program

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.realization.regular.list',     'system'),
  ('SPVDIST', 'distribution.realization.regular.list',     'system'),
  ('DIST',    'distribution.realization.non-regular.list', 'system'),
  ('SPVDIST', 'distribution.realization.non-regular.list', 'system')
ON CONFLICT DO NOTHING;
