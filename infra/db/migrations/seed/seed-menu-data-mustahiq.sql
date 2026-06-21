-- Seed: Data Mustahiq — Mustahiq Lembaga & Mustahiq Individu
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Penyaluran
-- Fitur: Master data penerima manfaat — lembaga (MC) dan individu (MP)
-- Tanggal: 2026-06-22

-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.mustahiq.corporate → [x] TAMBAHKAN di menu-keys.ts
-- menu-keys.ts: distribution.mustahiq.personal  → [x] TAMBAHKAN di menu-keys.ts
-- routes.ts:    /distribution/mustahiq/corporate → [x] TAMBAHKAN di routes.ts
-- routes.ts:    /distribution/mustahiq/personal  → [x] TAMBAHKAN di routes.ts
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.mustahiq.corporate',
    'Mustahiq Lembaga',
    'Program / Penyaluran',
    '/distribution/mustahiq/corporate',
    301,
    'A'
  ),
  (
    'distribution.mustahiq.personal',
    'Mustahiq Individu',
    'Program / Penyaluran',
    '/distribution/mustahiq/personal',
    302,
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
  ('DIST',    'distribution.mustahiq.corporate', 'system'),
  ('SPVDIST', 'distribution.mustahiq.corporate', 'system'),
  ('DIST',    'distribution.mustahiq.personal',  'system'),
  ('SPVDIST', 'distribution.mustahiq.personal',  'system')
ON CONFLICT DO NOTHING;
