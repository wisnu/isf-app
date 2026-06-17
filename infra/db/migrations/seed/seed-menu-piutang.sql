-- Seed: Piutang (Pinjam & Bayar)
-- Portal: Zakat (isf_auth_zakat)
-- Fitur: Piutang Pinjam/Bayar (transactioncode EAR/PEAR) + entity otorisasi
-- Tanggal: 2026-06-17

-- 3-Way Consistency Check:
-- registry.ts: keuangan.piutang.pinjam-bayar → [x] DITAMBAH di registry.ts
-- router.ts:   /keuangan/transaksi/piutang → [x] DITAMBAH di router/index.ts
-- seed SQL:    [x] FILE INI

-- ============================================================================
-- PART 1: Menu entries (isf_auth.menu)
-- ============================================================================

-- Parent: Piutang (baru — belum ada)
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.piutang',
  'Piutang',
  'Keuangan',
  NULL,
  160,
  'A'
)
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  status      = EXCLUDED.status;

-- Child: Piutang - Pinjam/Bayar
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES (
  'keuangan.piutang.pinjam-bayar',
  'Pinjam/Bayar',
  'Keuangan',
  '/keuangan/transaksi/piutang',
  161,
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

-- ACC (Accounting) — full akses ke Piutang Pinjam/Bayar
INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by)
VALUES
  ('ACC', 'keuangan.piutang.pinjam-bayar', 'system')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- PART 3: Otorisasi entity config (otorisasi.entity_config)
-- ============================================================================
-- Piutang menggunakan submission workflow dengan CheckLimitOtorisasi
-- - Amount <= limit → AUTO-AUTHORIZED
-- - Amount > limit → PENDING (manual approval di otorisasi page)

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key)
VALUES (
  'piutang',
  'keuangan',
  1,
  'Piutang Pinjam/Bayar',
  'keuangan.monitoring.otorisasi'
)
ON CONFLICT (entity_type) DO NOTHING;
