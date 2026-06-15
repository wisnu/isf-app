-- Seed: Transaksi Penyerahan Uang Muka
-- Portal: Zakat
-- Fitur: Transaksi Penyerahan Uang Muka (Cash Advance Disbursement)
-- Tanggal: 2026-06-15

-- 3-Way Consistency Check:
-- registry.ts: keuangan.transaksi.uang-muka-penyerahan → [ ] BELUM ADA (perlu tambah)
-- router.ts:   /keuangan/transaksi/uang-muka-penyerahan → [ ] BELUM ADA (perlu tambah)
-- seed SQL:    [x] GENERATE di file ini

-- 1. Menu entry: Penyerahan Uang Muka (transaksi input)
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.transaksi.uang-muka-penyerahan',
  'Penyerahan Uang Muka',
  'Keuangan',
  '/keuangan/transaksi/uang-muka-penyerahan',
  147,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path = EXCLUDED.route_path,
  status = EXCLUDED.status;

-- 2. Role assignment: ACC (Accounting)
-- Transaksi penyerahan uang muka (cash advance disbursement) adalah transaksi akuntansi
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'keuangan.transaksi.uang-muka-penyerahan', 'system')
ON CONFLICT DO NOTHING;
