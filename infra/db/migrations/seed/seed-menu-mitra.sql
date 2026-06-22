-- Seed: Mitra — Data Mitra Program Penyaluran
-- Portal: Zakat (isf_auth_zakat)
-- Fitur: CRUD Mitra (distribution partner)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.partner.list           → [x] DONE
-- routes.ts:    /distribution/partner               → [x] DONE
-- menu.ts:      Kegiatan group                      → [x] DONE
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entry (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'distribution.partner.list',
  'Mitra',
  'Program / Penyaluran',
  '/distribution/partner',
  310,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- ============================================================================
-- PART 2: Role assignments (isf_auth.role_menu)
-- ============================================================================
-- Roles dari legacy AllowedGroups: DIST;SPVDIST

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.partner.list', 'system'),
  ('SPVDIST', 'distribution.partner.list', 'system'),
  ('ADM',     'distribution.partner.list', 'system')
ON CONFLICT DO NOTHING;
