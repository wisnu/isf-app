-- Seed: Uang Muka Kegiatan — Inquiry per rekening
-- Portal: Zakat (isf_auth_zakat)
-- Fitur: Inquiry histori mutasi rekening uang muka kegiatan (accountreceivabletype='C')
-- Tanggal: 2026-06-21

-- 3-Way Consistency Check:
-- menu-keys.ts: finance.inquiry.cash_advance  → [x] TAMBAHKAN di menu-keys.ts
-- routes.ts:    /finance/inquiry/cash-advance  → [x] TAMBAHKAN di routes.ts
-- menu.ts:      Inquiry group                  → [x] TAMBAHKAN di menu.ts
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entry (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.inquiry.cash_advance',
  'Uang Muka Kegiatan',
  'Keuangan',
  '/finance/inquiry/cash-advance',
  175,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  status      = EXCLUDED.status;

-- ============================================================================
-- PART 2: Role assignments (isf_auth.role_menu)
-- ============================================================================
-- Roles dari legacy: ADM, SPVKEU, KEU, ACC (QAC/SPVACC tidak ada di isf-app)

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ADM',    'finance.inquiry.cash_advance', 'system'),
  ('SPVKEU', 'finance.inquiry.cash_advance', 'system'),
  ('KEU',    'finance.inquiry.cash_advance', 'system'),
  ('ACC',    'finance.inquiry.cash_advance', 'system')
ON CONFLICT DO NOTHING;
