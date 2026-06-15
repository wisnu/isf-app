-- Seed for otorisasi.entity_config — HC ZIS Upload entities
-- Mendaftarkan 3 operasi HC ZIS (upload, delete, update tanggal)
-- Portal: zakat
-- Dibuat: 2026-06-15

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('hc_zis_upload',      'keuangan', 1, 'Upload Data Penerimaan ZIS Rutin', 'keuangan.monitoring.otorisasi'),
  ('hc_zis_delete',      'keuangan', 1, 'Hapus Batch Upload ZIS Rutin',     'keuangan.monitoring.otorisasi'),
  ('hc_zis_update_date', 'keuangan', 1, 'Update Tanggal Batch Upload ZIS',  'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
