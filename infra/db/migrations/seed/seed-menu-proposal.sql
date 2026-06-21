-- Seed: Proposal Bantuan Dana
-- Portal: Zakat (isf_auth_zakat)
-- Domain: Distribution / Penyaluran
-- Fitur: Manajemen proposal permohonan dana dari mustahiq
-- Tanggal: 2026-06-22
--
-- Legacy: dialogs/Kegiatan/QProposal.* AllowedGroups='DIST;SPVDIST'
--
-- 3-Way Consistency Check:
-- menu-keys.ts: distribution.proposal.list → [x] DITAMBAHKAN
-- routes.ts:    /distribution/proposal     → [x] DITAMBAHKAN
-- seed SQL:     [x] FILE INI
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat -f <file>

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  (
    'distribution.proposal.list',
    'Proposal Bantuan Dana',
    'Program / Penyaluran',
    '/distribution/proposal',
    310,
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
-- Roles dari legacy: AllowedGroups='DIST;SPVDIST' (Penyaluran.mnu Kegiatan/QProposal)

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('DIST',    'distribution.proposal.list', 'system'),
  ('SPVDIST', 'distribution.proposal.list', 'system')
ON CONFLICT DO NOTHING;
