-- Seed: Pengembalian Realisasi Program
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Kegiatan
-- Fitur: CRUD Pengembalian Realisasi Program (realization return list)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.realization-return.list     → [ ] PENDING
-- routes.ts:    /distribution/realization-return         → [ ] PENDING
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.realization-return.list',
    'Pengembalian Realisasi Program',
    'Program / Penyaluran',
    '/distribution/realization-return',
    335,
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
-- Roles: DIST dan SPVDIST untuk pengembalian realisasi program

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.realization-return.list', 'system'),
  ('SPVDIST', 'distribution.realization-return.list', 'system')
ON CONFLICT DO NOTHING;
