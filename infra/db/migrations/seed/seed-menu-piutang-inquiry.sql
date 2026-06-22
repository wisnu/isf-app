-- Seed: Piutang — Inquiry per rekening (Karyawan / Non Karyawan)
-- Portal: Zakat (isf_auth_zakat)
-- Fitur: Inquiry histori mutasi rekening piutang (accountreceivabletype='E'/'D')
-- Tanggal: 2026-06-21

-- 3-Way Consistency Check:
-- menu-keys.ts: finance.inquiry.receivable          → [x] TAMBAHKAN di menu-keys.ts
-- routes.ts:    /finance/inquiry/receivable          → [x] TAMBAHKAN di routes.ts
-- menu.ts:      Inquiry group                        → [x] TAMBAHKAN di menu.ts
-- seed SQL:     [x] FILE INI

-- ============================================================================
-- PART 1: Menu entry (isf_auth.menu)
-- ============================================================================

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'finance.inquiry.receivable',
  'Piutang Karyawan/Non Karyawan',
  'Keuangan',
  '/finance/inquiry/receivable',
  176,
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
-- Roles dari legacy: SPVKEU, KEU, ACC, QAC, SPVACC

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('SPVKEU', 'finance.inquiry.receivable', 'system'),
  ('KEU',    'finance.inquiry.receivable', 'system'),
  ('ACC',    'finance.inquiry.receivable', 'system'),
  ('SPVACC', 'finance.inquiry.receivable', 'system'),
  ('ADM',    'finance.inquiry.receivable', 'system')
ON CONFLICT DO NOTHING;
