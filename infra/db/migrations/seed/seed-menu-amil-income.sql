-- Seed: Menu Penerimaan Amil (CI - Cash In Amil)
-- Portal: Zakat (apply to isf_auth_zakat)
-- Tanggal: 2026-06-20

-- 3-Way Consistency Check:
-- registry.ts: finance.transactions.amil_income → [x] DITAMBAH di registry.ts
-- router.ts:   /finance/transactions/amil-income → [x] DITAMBAH di router/index.ts
-- seed SQL:    [x] FILE INI

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.amil_income',
  'Penerimaan Amil',
  'Keuangan',
  '/finance/transactions/amil-income',
  150,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- Role: ACC (Accounting) — inputer penerimaan amil
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.transactions.amil_income', 'system')
ON CONFLICT DO NOTHING;
