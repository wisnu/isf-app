-- Seed: Monitoring Program Penyaluran
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Kegiatan
-- Fitur: Monitoring status program penyaluran (distribution.monitoring)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.monitoring.list     → [ ] PENDING
-- routes.ts:    /distribution/monitoring         → [ ] PENDING
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.monitoring.list',
    'Monitoring Program Penyaluran',
    'Program / Penyaluran',
    '/distribution/monitoring',
    340,
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
-- Roles: DIST dan SPVDIST untuk monitoring program penyaluran

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.monitoring.list', 'system'),
  ('SPVDIST', 'distribution.monitoring.list', 'system')
ON CONFLICT DO NOTHING;
