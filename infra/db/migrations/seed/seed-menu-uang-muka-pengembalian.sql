-- Seed: Transaksi Pengembalian / LPJ Uang Muka
-- Portal: Zakat
-- Fitur: Pengembalian Uang Muka (Cash Advance Return, transactioncode=CAR)
-- Tanggal: 2026-06-15

-- 3-Way Consistency Check:
-- registry.ts: keuangan.transaksi.uang-muka-pengembalian → [x] ditambah
-- router.ts:   /keuangan/transaksi/uang-muka-pengembalian → [x] ditambah
-- seed SQL:    [x] file ini

-- 1. Menu entry
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.transaksi.uang-muka-pengembalian',
  'Pengembalian Uang Muka',
  'Keuangan',
  '/keuangan/transaksi/uang-muka-pengembalian',
  148,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- 2. Role assignment: ACC (Accounting) — sama seperti Penyerahan Uang Muka
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'keuangan.transaksi.uang-muka-pengembalian', 'system')
ON CONFLICT DO NOTHING;
