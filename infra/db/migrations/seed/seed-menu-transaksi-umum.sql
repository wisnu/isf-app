-- Seed: Menu Transaksi Umum (GT - General Transaction)
-- Portal: Zakat
-- Tanggal: 2026-06-17

-- 3-Way Consistency Check:
-- registry.ts: finance.transactions.general → [x] DITAMBAH di registry.ts
-- router.ts:   /finance/transactions/general → [x] DITAMBAH di router/index.ts
-- seed SQL:    [x] FILE INI

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.general',
  'Transaksi Umum',
  'Keuangan',
  '/finance/transactions/general',
  149,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- Role: ACC (Accounting) — inputer transaksi umum
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.transactions.general', 'system')
ON CONFLICT DO NOTHING;

-- Otorisasi entity_config (apply to mziss_laz ONLY)
-- Maps 'transaksi_umum' entity type to otorisasi workflow
INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key)
VALUES ('transaksi_umum', 'keuangan', 1, 'Transaksi Umum', 'finance.monitoring.authorization')
ON CONFLICT (entity_type) DO NOTHING;
