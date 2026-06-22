-- Seed: Memo Penyaluran — memo rutin + non rutin
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Kegiatan
-- Fitur: CRUD Memo Penyaluran (program.realizationmemo, discriminator realizationmemotype R/N)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.program.memo-regular     → [x] DONE
--               distribution.program.memo-non-regular → [x] DONE
-- routes.ts:    /distribution/program/memo-regular     → [x] DONE
--               /distribution/program/memo-non-regular → [x] DONE
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.program.memo-regular',
    'Memo Penyaluran Rutin',
    'Program / Penyaluran',
    '/distribution/program/memo-regular',
    331,
    'A'
  ),
  (
    'distribution.program.memo-non-regular',
    'Memo Penyaluran Non Rutin',
    'Program / Penyaluran',
    '/distribution/program/memo-non-regular',
    332,
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
-- Roles dari legacy Penyaluran.mnu: AllowedGroups='DIST;SPVDIST' untuk Memo Penyaluran

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.program.memo-regular',     'system'),
  ('SPVDIST', 'distribution.program.memo-regular',     'system'),
  ('DIST',    'distribution.program.memo-non-regular', 'system'),
  ('SPVDIST', 'distribution.program.memo-non-regular', 'system')
ON CONFLICT DO NOTHING;
