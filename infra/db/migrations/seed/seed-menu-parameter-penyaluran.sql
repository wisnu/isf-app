-- Seed for Parameter Penyaluran menu items and role_menu entries
-- Covers: Jenis Program, Program Penyaluran, Bidang Pekerjaan, Rincian Biaya Realisasi
-- Roles from legacy Penyaluran.mnu: AllowedGroups='DIST;SPVDIST;ADM;SPVADM'

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.parameter.program-type',
    'Jenis Program',
    'Program / Penyaluran',
    '/distribution/parameter/program-type',
    211,
    'A'
  ),
  (
    'distribution.parameter.program',
    'Program Penyaluran',
    'Program / Penyaluran',
    '/distribution/parameter/program',
    212,
    'A'
  ),
  (
    'distribution.parameter.work-sector',
    'Bidang Pekerjaan',
    'Program / Penyaluran',
    '/distribution/parameter/work-sector',
    213,
    'A'
  ),
  (
    'distribution.parameter.cost-item',
    'Rincian Biaya Realisasi',
    'Program / Penyaluran',
    '/distribution/parameter/cost-item',
    214,
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
  ('DIST',    'distribution.parameter.program-type', 'system'),
  ('SPVDIST', 'distribution.parameter.program-type', 'system'),
  ('ADM',     'distribution.parameter.program-type', 'system'),
  ('SPVADM',  'distribution.parameter.program-type', 'system'),
  ('DIST',    'distribution.parameter.program', 'system'),
  ('SPVDIST', 'distribution.parameter.program', 'system'),
  ('ADM',     'distribution.parameter.program', 'system'),
  ('SPVADM',  'distribution.parameter.program', 'system'),
  ('DIST',    'distribution.parameter.work-sector', 'system'),
  ('SPVDIST', 'distribution.parameter.work-sector', 'system'),
  ('ADM',     'distribution.parameter.work-sector', 'system'),
  ('SPVADM',  'distribution.parameter.work-sector', 'system'),
  ('DIST',    'distribution.parameter.cost-item', 'system'),
  ('SPVDIST', 'distribution.parameter.cost-item', 'system'),
  ('ADM',     'distribution.parameter.cost-item', 'system'),
  ('SPVADM',  'distribution.parameter.cost-item', 'system')
ON CONFLICT DO NOTHING;
