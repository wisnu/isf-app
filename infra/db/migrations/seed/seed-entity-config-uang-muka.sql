-- Seed for otorisasi.entity_config — uang muka penyerahan entity
-- Portal: zakat (mziss_laz / isf_auth_zakat)
-- Maps 'uang_muka' entity type to otorisasi menu key

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('uang_muka', 'keuangan', 1, 'Penyerahan Uang Muka', 'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
