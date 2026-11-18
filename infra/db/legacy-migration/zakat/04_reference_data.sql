-- 04_reference_data.sql — Data konfigurasi/referensi untuk schema baru isf-app
-- Data TRANSAKSIONAL dari DB dev (otorisasi.submission, approval_log, dwh.dm_*/fact_*,
-- etl_log) SENGAJA TIDAK dibawa — itu data uji. Hanya config yang wajib ada.
-- Idempotent (ON CONFLICT). Kompatibel PostgreSQL 12+.

-- ── otorisasi.entity_config ──────────────────────────────────────────────────
-- Snapshot dari mziss_laz 2026-11-18 (gabungan semua seed-entity-config-*.sql).
-- menu_key dinormalisasi ke key English kanonik 'finance.monitoring.authorization'
-- (di DB dev sebagian masih 'keuangan.monitoring.otorisasi' — pra-refactor naming).
-- entity_type FROZEN (jangan diterjemahkan) — kunci dispatcher registry + literal FE.
INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('amil_expense', 'keuangan', 1, 'Pengeluaran Amil', 'finance.monitoring.authorization'),
  ('amil_income', 'keuangan', 1, 'Penerimaan Amil', 'finance.monitoring.authorization'),
  ('bank', 'keuangan', 1, 'Master Bank', 'finance.monitoring.authorization'),
  ('budget_owner', 'keuangan', 1, 'Pemilik Anggaran', 'finance.monitoring.authorization'),
  ('coa', 'keuangan', 1, 'Master COA', 'finance.monitoring.authorization'),
  ('hc_zis_delete', 'keuangan', 1, 'Hapus Batch Upload ZIS Rutin', 'finance.monitoring.authorization'),
  ('hc_zis_update_date', 'keuangan', 1, 'Update Tanggal Batch Upload ZIS', 'finance.monitoring.authorization'),
  ('hc_zis_upload', 'keuangan', 1, 'Upload Data Penerimaan ZIS Rutin', 'finance.monitoring.authorization'),
  ('kas', 'keuangan', 1, 'Master Kas', 'finance.monitoring.authorization'),
  ('penghimpunan', 'keuangan', 1, 'Penghimpunan Dana', 'finance.monitoring.authorization'),
  ('penyaluran', 'keuangan', 1, 'Penyaluran Dana', 'finance.monitoring.authorization'),
  ('piutang', 'keuangan', 1, 'Piutang Pinjam/Bayar', 'finance.monitoring.authorization'),
  ('transaksi_umum', 'keuangan', 1, 'Transaksi Umum', 'finance.monitoring.authorization'),
  ('uang_muka', 'keuangan', 1, 'Penyerahan Uang Muka', 'finance.monitoring.authorization'),
  ('uang_muka_pengembalian', 'keuangan', 1, 'Pengembalian Uang Muka (LPJ)', 'finance.monitoring.authorization'),
  ('upload_penghimpunan', 'keuangan', 1, 'Upload Penghimpunan', 'finance.monitoring.authorization')
ON CONFLICT (entity_type) DO NOTHING;

-- ── dwh.dim_fund_type ── (statis, PSAK 109: fund_entity 1–5 FROZEN)
INSERT INTO dwh.dim_fund_type (fund_entity_code, fund_name_id, fund_name_en, fund_category, amil_max_pct, is_active) VALUES
  (1, 'Zakat',             'Zakat',           'ZAKAT',         12.50, true),
  (2, 'Infaq & Sedekah',   'Infaq & Sadaqah', 'INFAQ_SADAQAH', NULL,  true),
  (3, 'Wakaf',             'Waqf',            'WAQF',          NULL,  true),
  (4, 'Amil',              'Amil',            'AMIL',          NULL,  true),
  (5, 'Non-halal/Lainnya', 'Non-halal/Other', 'OTHER',         NULL,  true)
ON CONFLICT (fund_entity_code) DO NOTHING;

-- ── dwh.dim_branch ── diturunkan dari enterprise.cabang produksi (bukan disalin dari dev)
-- branch_key 0 = baris 'UNKNOWN' untuk fakta tanpa cabang (konvensi ETL).
INSERT INTO dwh.dim_branch (branch_key, branch_code, branch_name, branch_status)
VALUES (0, 'UNKNOWN', 'Unknown / Aggregated', 'X')
ON CONFLICT (branch_code) DO NOTHING;

INSERT INTO dwh.dim_branch (branch_code, branch_name, branch_type, branch_status,
                            parent_branch_code, region_code, branch_level, is_active, input_date)
SELECT c.kode_cabang,
       LEFT(c.nama_cabang, 60),
       LEFT(c.tipe_cabang, 2),
       LEFT(c.status_cabang, 1),
       c.kode_cabang_induk,
       LEFT(c.kode_wilayah, 3),
       CAST(c.level_cabang AS smallint),
       LEFT(c.status_aktif, 1),
       c.tanggal_input
FROM enterprise.cabang c
ORDER BY c.kode_cabang
ON CONFLICT (branch_code) DO NOTHING;

SELECT setval('dwh.dim_cabang_cabang_key_seq',
              GREATEST((SELECT MAX(branch_key) FROM dwh.dim_branch), 1));
