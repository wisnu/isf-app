-- Seed: Menu Anggaran (Budget) Module
-- Portal: zakat
-- Feature: Anggaran (Budget) — Import, Revisi, Inquiry, dan Master Data
-- Date: 2026-06-15
-- Apply: psql -U transaction -d isf_auth_zakat -f seed-menu-anggaran.sql

-- ── 1. Parent Menu: "Anggaran" di bawah Keuangan ────────────────────────────────
-- Catatan: Akan ditampilkan sebagai group section di sidebar Keuangan

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  -- Transaksi Anggaran
  ('keuangan.anggaran.import',    'Buat Anggaran Baru',   'Keuangan',  '/keuangan/anggaran/import',    159, 'A'),
  ('keuangan.anggaran.revisi',    'Revisi Anggaran',      'Keuangan',  '/keuangan/anggaran/revisi',    160, 'A'),
  ('keuangan.anggaran.inquiry',   'Inquiry Anggaran',     'Keuangan',  '/keuangan/anggaran/inquiry',   161, 'A'),
  -- Master Data Anggaran di Parameter
  ('keuangan.parameter.anggaran.pemilik', 'Pemilik Anggaran',  'Parameter', '/parameter/anggaran/pemilik',  210, 'A'),
  ('keuangan.parameter.anggaran.item',    'Item Anggaran',     'Parameter', '/parameter/anggaran/item',     211, 'A'),
  ('keuangan.parameter.anggaran.periode', 'Periode Anggaran',  'Parameter', '/parameter/anggaran/periode',  212, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status;

-- ── 2. Role → Menu mapping untuk transaksi Anggaran ──────────────────────────────
-- Buat Anggaran Baru: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.anggaran.import', 'system'),
  ('KEU',   'keuangan.anggaran.import', 'system'),
  ('SPVKEU','keuangan.anggaran.import', 'system')
ON CONFLICT DO NOTHING;

-- Revisi Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.anggaran.revisi', 'system'),
  ('KEU',   'keuangan.anggaran.revisi', 'system'),
  ('SPVKEU','keuangan.anggaran.revisi', 'system')
ON CONFLICT DO NOTHING;

-- Inquiry Anggaran: ADMIN, KEU, SPVKEU, ACC, SPVACC
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.anggaran.inquiry', 'system'),
  ('KEU',   'keuangan.anggaran.inquiry', 'system'),
  ('SPVKEU','keuangan.anggaran.inquiry', 'system'),
  ('ACC',   'keuangan.anggaran.inquiry', 'system'),
  ('SPVACC','keuangan.anggaran.inquiry', 'system')
ON CONFLICT DO NOTHING;

-- ── 3. Role → Menu mapping untuk master data Anggaran ────────────────────────────
-- Pemilik Anggaran: ADMIN, KEU, SPVKEU, ACC, SPVACC
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.parameter.anggaran.pemilik', 'system'),
  ('KEU',   'keuangan.parameter.anggaran.pemilik', 'system'),
  ('SPVKEU','keuangan.parameter.anggaran.pemilik', 'system'),
  ('ACC',   'keuangan.parameter.anggaran.pemilik', 'system'),
  ('SPVACC','keuangan.parameter.anggaran.pemilik', 'system')
ON CONFLICT DO NOTHING;

-- Item Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.parameter.anggaran.item', 'system'),
  ('KEU',   'keuangan.parameter.anggaran.item', 'system'),
  ('SPVKEU','keuangan.parameter.anggaran.item', 'system')
ON CONFLICT DO NOTHING;

-- Periode Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'keuangan.parameter.anggaran.periode', 'system'),
  ('KEU',   'keuangan.parameter.anggaran.periode', 'system'),
  ('SPVKEU','keuangan.parameter.anggaran.periode', 'system')
ON CONFLICT DO NOTHING;

-- ── Verifikasi 3-Way Consistency ──────────────────────────────────────────────────
-- 1. Menu keys di seed SQL harus ada di lib/menu/registry.ts (MENU_KEYS):
--    - keuangan.anggaran.import
--    - keuangan.anggaran.revisi
--    - keuangan.anggaran.inquiry
--    - keuangan.parameter.anggaran.pemilik
--    - keuangan.parameter.anggaran.item
--    - keuangan.parameter.anggaran.periode
--
-- 2. Route meta.menu_key harus sesuai dengan menu_key di seed:
--    - /keuangan/anggaran/import → meta.menu_key: 'keuangan.anggaran.import'
--    - /keuangan/anggaran/revisi → meta.menu_key: 'keuangan.anggaran.revisi'
--    - /keuangan/anggaran/inquiry → meta.menu_key: 'keuangan.anggaran.inquiry'
--    - /parameter/anggaran/pemilik → meta.menu_key: 'keuangan.parameter.anggaran.pemilik'
--    - /parameter/anggaran/item → meta.menu_key: 'keuangan.parameter.anggaran.item'
--    - /parameter/anggaran/periode → meta.menu_key: 'keuangan.parameter.anggaran.periode'
--
-- 3. Sidebar AppSidebar.vue harus include menu_key di children
