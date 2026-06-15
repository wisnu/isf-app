-- Seed: Transfer Antar Rekening
-- Portal: Zakat
-- Fitur: Transfer antar rekening kas/bank (transactioncode TI)
-- Tanggal: 2026-06-15

-- 3-Way Consistency Check:
-- registry.ts: keuangan.transaksi.transfer-antar-rekening → [x] DITAMBAH di registry.ts
-- router.ts:   /keuangan/transaksi/transfer-antar-rekening → [x] DITAMBAH di router/index.ts
-- seed SQL:    [x] FILE INI

-- 1. Menu entry
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.transaksi.transfer-antar-rekening',
  'Transfer Antar Rekening',
  'Keuangan',
  '/keuangan/transaksi/transfer-antar-rekening',
  148,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- 2. Role assignments — KEU, ACC, SPVKEU, ADM dapat akses
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES
  ('KEU',    'keuangan.transaksi.transfer-antar-rekening', 'system'),
  ('ACC',    'keuangan.transaksi.transfer-antar-rekening', 'system'),
  ('SPVKEU', 'keuangan.transaksi.transfer-antar-rekening', 'system'),
  ('ADM',    'keuangan.transaksi.transfer-antar-rekening', 'system')
ON CONFLICT DO NOTHING;
