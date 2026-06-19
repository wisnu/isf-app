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
  ('finance.budget.import',    'Buat Anggaran Baru',   'Keuangan',  '/finance/budget/import',    159, 'A'),
  ('finance.budget.revise',    'Revisi Anggaran',      'Keuangan',  '/finance/budget/revise',    160, 'A'),
  ('finance.budget.inquiry',   'Inquiry Anggaran',     'Keuangan',  '/finance/budget/inquiry',   161, 'A'),
  -- Master Data Anggaran di Parameter
  ('finance.parameter.budget.owner', 'Pemilik Anggaran',  'Parameter', '/parameter/budget-owner',  210, 'A'),
  ('finance.parameter.budget.item',    'Item Anggaran',     'Parameter', '/parameter/anggaran/item',     211, 'A'),
  ('finance.parameter.budget.period', 'Periode Anggaran',  'Parameter', '/parameter/anggaran/periode',  212, 'A')
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
  ('ADMIN', 'finance.budget.import', 'system'),
  ('KEU',   'finance.budget.import', 'system'),
  ('SPVKEU','finance.budget.import', 'system')
ON CONFLICT DO NOTHING;

-- Revisi Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'finance.budget.revise', 'system'),
  ('KEU',   'finance.budget.revise', 'system'),
  ('SPVKEU','finance.budget.revise', 'system')
ON CONFLICT DO NOTHING;

-- Inquiry Anggaran: ADMIN, KEU, SPVKEU, ACC, SPVACC
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'finance.budget.inquiry', 'system'),
  ('KEU',   'finance.budget.inquiry', 'system'),
  ('SPVKEU','finance.budget.inquiry', 'system'),
  ('ACC',   'finance.budget.inquiry', 'system'),
  ('SPVACC','finance.budget.inquiry', 'system')
ON CONFLICT DO NOTHING;

-- ── 3. Role → Menu mapping untuk master data Anggaran ────────────────────────────
-- Pemilik Anggaran: ADMIN, KEU, SPVKEU, ACC, SPVACC
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'finance.parameter.budget.owner', 'system'),
  ('KEU',   'finance.parameter.budget.owner', 'system'),
  ('SPVKEU','finance.parameter.budget.owner', 'system'),
  ('ACC',   'finance.parameter.budget.owner', 'system'),
  ('SPVACC','finance.parameter.budget.owner', 'system')
ON CONFLICT DO NOTHING;

-- Item Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'finance.parameter.budget.item', 'system'),
  ('KEU',   'finance.parameter.budget.item', 'system'),
  ('SPVKEU','finance.parameter.budget.item', 'system')
ON CONFLICT DO NOTHING;

-- Periode Anggaran: ADMIN, KEU, SPVKEU
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADMIN', 'finance.parameter.budget.period', 'system'),
  ('KEU',   'finance.parameter.budget.period', 'system'),
  ('SPVKEU','finance.parameter.budget.period', 'system')
ON CONFLICT DO NOTHING;

-- ── Verifikasi 3-Way Consistency ──────────────────────────────────────────────────
-- 1. Menu keys di seed SQL harus ada di lib/menu/registry.ts (MENU_KEYS):
--    - finance.budget.import
--    - finance.budget.revise
--    - finance.budget.inquiry
--    - finance.parameter.budget.owner
--    - finance.parameter.budget.item
--    - finance.parameter.budget.period
--
-- 2. Route meta.menu_key harus sesuai dengan menu_key di seed:
--    - /finance/budget/import → meta.menu_key: 'finance.budget.import'
--    - /finance/budget/revise → meta.menu_key: 'finance.budget.revise'
--    - /finance/budget/inquiry → meta.menu_key: 'finance.budget.inquiry'
--    - /parameter/budget-owner → meta.menu_key: 'finance.parameter.budget.owner'
--    - /parameter/anggaran/item → meta.menu_key: 'finance.parameter.budget.item'
--    - /parameter/anggaran/periode → meta.menu_key: 'finance.parameter.budget.period'
--
-- 3. Sidebar AppSidebar.vue harus include menu_key di children
