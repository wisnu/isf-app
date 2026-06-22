-- Seed: Program Non Rutin — non-regular distribution programs per mustahiq
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Program / Penyaluran
-- Fitur: CRUD Program Non Rutin (program.mustahiqproduct dengan mustahiqproducttype='N')
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.program.non-regular → [x] DONE
-- routes.ts:    /distribution/program/non-regular → [x] DONE
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.program.non-regular',
    'Program Non Rutin',
    'Program / Penyaluran',
    '/distribution/program/non-regular',
    325,
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
-- Roles dari legacy menu Penyaluran.mnu: AllowedGroups='DIST;SPVDIST'

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.program.non-regular', 'system'),
  ('SPVDIST', 'distribution.program.non-regular', 'system')
ON CONFLICT DO NOTHING;
