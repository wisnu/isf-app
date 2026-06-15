-- Seed for otorisasi.entity_config — uang muka pengembalian / LPJ entity
-- Portal: zakat (mziss_laz)

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('uang_muka_pengembalian', 'keuangan', 1, 'Pengembalian Uang Muka (LPJ)', 'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
