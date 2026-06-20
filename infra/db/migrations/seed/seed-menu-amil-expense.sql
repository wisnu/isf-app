-- Seed: Menu Pengeluaran Amil (CO - Cash Out Amil)
-- Portal: Zakat (apply to isf_auth_zakat)
-- Tanggal: 2026-06-20

-- 3-Way Consistency Check:
-- registry.ts: finance.transactions.amil_expense → [DONE] added to registry.ts (MENU_KEYS)
-- router.ts:   /finance/transactions/amil-expense → [DONE] route meta.menu_key added in router/index.ts
-- seed SQL:    [DONE] THIS FILE

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.transactions.amil_expense',
  'Pengeluaran Amil',
  'Keuangan',
  '/finance/transactions/amil-expense',
  151,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- Role: ACC (Accounting) — inputer pengeluaran amil
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'finance.transactions.amil_expense', 'system')
ON CONFLICT DO NOTHING;

-- NOTE: otorisasi.entity_config (entity_type='amil_expense') lives in a SEPARATE
-- seed targeting mziss_laz (business DB), not isf_auth_zakat:
--   infra/db/migrations/seed/seed-entity-config-amil-expense.sql
-- Do not add it here — this file applies to isf_auth_zakat only.
