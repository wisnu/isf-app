-- Seed: Program Rutin — regular distribution programs per mustahiq
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Program / Penyaluran
-- Fitur: CRUD Program Rutin (program.mustahiqproduct dengan mustahiqproducttype='R')
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.program.regular → [x] TAMBAHKAN di menu-keys.ts
-- routes.ts:    /distribution/program/regular → [x] TAMBAHKAN di routes.ts
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.program.regular',
    'Program Rutin',
    'Program / Penyaluran',
    '/distribution/program/regular',
    320,
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
  ('DIST',    'distribution.program.regular', 'system'),
  ('SPVDIST', 'distribution.program.regular', 'system')
ON CONFLICT DO NOTHING;
