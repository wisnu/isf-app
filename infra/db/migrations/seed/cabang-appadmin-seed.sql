-- Seed: cabang-appadmin-seed.sql
-- Portal: Zakat
-- Fitur: Branch Management (Manajemen Cabang)
-- Tanggal: 2026-06-22
-- Deskripsi: Menambahkan menu branch management dan role_menu assignment untuk ADMIN

-- ============================================================================
-- 1. Tambah menu entries untuk branch management di isf_auth.menu
-- ============================================================================
-- Menu key pattern: appadmin.branch.{action}
-- Group label: Manajemen Cabang (baru, ditempatkan setelah Manajemen User)
-- Sort order dimulai dari 930 (setelah appadmin.users = 920)

INSERT INTO isf_auth.menu (menu_key, label, group_label, sort_order, status)
VALUES
  -- Group: Manajemen Cabang
  ('appadmin.branch.list', 'List Cabang', 'Manajemen Cabang', 930, 'A'),
  ('appadmin.branch.create', 'Input Data Cabang Baru', 'Manajemen Cabang', 931, 'A'),
  ('appadmin.branch.edit', 'Koreksi Data Cabang', 'Manajemen Cabang', 932, 'A'),
  ('appadmin.branch.detail', 'Lihat Data Cabang', 'Manajemen Cabang', 933, 'A')

ON CONFLICT (menu_key) DO UPDATE SET
  label      = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  sort_order = EXCLUDED.sort_order,
  status     = EXCLUDED.status;

-- ============================================================================
-- 2. Assign role_menu untuk role ADMIN (id_peran = 'ADM')
-- ============================================================================
-- ADMIN memiliki akses penuh ke seluruh menu branch management

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADM', 'appadmin.branch.list', 'seed'),
  ('ADM', 'appadmin.branch.create', 'seed'),
  ('ADM', 'appadmin.branch.edit', 'seed'),
  ('ADM', 'appadmin.branch.detail', 'seed')

ON CONFLICT (id_peran, menu_key) DO NOTHING;

-- ============================================================================
-- CHECKLIST SEBELUM APPLY
-- ============================================================================
-- [ ] Menu key di seed cocok dengan lib/menu/registry.ts (MENU_KEYS.appadmin.branch.*)
-- [ ] Menu key di seed cocok dengan route.meta.menu_key di router
-- [ ] ON CONFLICT DO NOTHING/UPDATE — idempotent (bisa dijalankan ulang)
-- [ ] ADMIN (ADM) adalah role yang tepat untuk semua 4 menu
-- [ ] Parent group "Manajemen Cabang" tidak memerlukan parent menu (ini leaf items)
-- [ ] Sort order 930-933 tidak bentrok dengan menu lain (max existing = 920)
-- [ ] Database: isf_auth_zakat (portal zakat)
--
-- CARA APPLY:
-- psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/cabang-appadmin-seed.sql
--
-- CATATAN:
-- - Setelah apply, user perlu logout + login ulang agar menus[] di session ter-update
-- - Verify: SELECT * FROM isf_auth.menu WHERE menu_key LIKE 'appadmin.branch%';
-- - Verify: SELECT * FROM isf_auth.role_menu WHERE menu_key LIKE 'appadmin.branch%';
