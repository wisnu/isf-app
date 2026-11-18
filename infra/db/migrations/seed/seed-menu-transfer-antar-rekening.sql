-- Seed: Transfer Antar Rekening
-- Portal: Zakat
-- Fitur: Transfer antar rekening kas/bank (transactioncode TI)
-- Tanggal: 2026-06-15

-- 3-Way Consistency Check:
-- registry.ts: finance.transactions.fund_transfer → [x] DITAMBAH di registry.ts
-- router.ts:   /finance/transactions/fund-transfer → [x] DITAMBAH di router/index.ts
-- seed SQL:    [x] FILE INI

-- 1. Menu entry
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.fund_transfer',
  'Transfer Antar Rekening',
  'Keuangan',
  '/finance/transactions/fund-transfer',
  148,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- 2. Role assignments — KEU, ACC, SPVKEU, ADM dapat akses
--    (2026-11-18: dulu menulis ke isf_auth.role_menu yang sudah di-drop oleh
--     add-role-menu-permission.sql → seed ini gagal & menu tidak pernah muncul)
INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action, updated_by) VALUES
  ('KEU',    'finance.transactions.fund_transfer', 'view', 'system'),
  ('ACC',    'finance.transactions.fund_transfer', 'view', 'system'),
  ('SPVKEU', 'finance.transactions.fund_transfer', 'view', 'system'),
  ('ADM',    'finance.transactions.fund_transfer', 'view', 'system')
ON CONFLICT (role_id, menu_key, action) DO NOTHING;
