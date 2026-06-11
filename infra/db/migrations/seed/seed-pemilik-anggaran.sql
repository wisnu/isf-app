-- Seed: Pemilik Anggaran — menu, role_menu, dan entity_config
-- Apply isf_auth_zakat  : psql -U transaction -d isf_auth_zakat  -f seed-pemilik-anggaran.sql
-- Apply isf_auth_wakaf  : psql -U transaction -d isf_auth_wakaf  -f seed-pemilik-anggaran.sql
-- Apply entity_config   : psql -U transaction -d mziss_laz       -f seed-pemilik-anggaran.sql
--                         (mziss_wakaf tidak butuh entity_config — tidak ada otorisasi)

-- ── 1. Menu keys (isf_auth.menu) ────────────────────────────────────────────

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  ('keuangan.parameter.pemilik-anggaran',        'Pemilik Anggaran',        'Parameter', '/parameter/pemilik-anggaran', 200, 'A'),
  ('keuangan.parameter.pemilik-anggaran.tambah', 'Tambah Pemilik Anggaran', 'Parameter', '/parameter/pemilik-anggaran', 201, 'A'),
  ('keuangan.parameter.pemilik-anggaran.ubah',   'Ubah Pemilik Anggaran',   'Parameter', '/parameter/pemilik-anggaran', 202, 'A'),
  ('keuangan.parameter.pemilik-anggaran.hapus',  'Hapus Pemilik Anggaran',  'Parameter', '/parameter/pemilik-anggaran', 203, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- ── 2. Role → Menu mapping (isf_auth.role_menu) ──────────────────────────────
-- View: SPVKEU, ADM, KEU, ACC, SPVADM
-- CRUD: SPVKEU, ADM, KEU, ACC

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('SPVKEU', 'keuangan.parameter.pemilik-anggaran',        'system'),
  ('ADM',    'keuangan.parameter.pemilik-anggaran',        'system'),
  ('KEU',    'keuangan.parameter.pemilik-anggaran',        'system'),
  ('ACC',    'keuangan.parameter.pemilik-anggaran',        'system'),
  ('SPVADM', 'keuangan.parameter.pemilik-anggaran',        'system'),

  ('SPVKEU', 'keuangan.parameter.pemilik-anggaran.tambah', 'system'),
  ('ADM',    'keuangan.parameter.pemilik-anggaran.tambah', 'system'),
  ('KEU',    'keuangan.parameter.pemilik-anggaran.tambah', 'system'),
  ('ACC',    'keuangan.parameter.pemilik-anggaran.tambah', 'system'),

  ('SPVKEU', 'keuangan.parameter.pemilik-anggaran.ubah',   'system'),
  ('ADM',    'keuangan.parameter.pemilik-anggaran.ubah',   'system'),
  ('KEU',    'keuangan.parameter.pemilik-anggaran.ubah',   'system'),
  ('ACC',    'keuangan.parameter.pemilik-anggaran.ubah',   'system'),

  ('SPVKEU', 'keuangan.parameter.pemilik-anggaran.hapus',  'system'),
  ('ADM',    'keuangan.parameter.pemilik-anggaran.hapus',  'system'),
  ('KEU',    'keuangan.parameter.pemilik-anggaran.hapus',  'system'),
  ('ACC',    'keuangan.parameter.pemilik-anggaran.hapus',  'system')
ON CONFLICT DO NOTHING;

-- ── 3. Otorisasi entity_config (apply to mziss_laz ONLY) ────────────────────
-- Tidak ada limit checker untuk master data → selalu AUTHORIZED langsung

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key)
VALUES ('budget_owner', 'keuangan', 1, 'Pemilik Anggaran', 'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
