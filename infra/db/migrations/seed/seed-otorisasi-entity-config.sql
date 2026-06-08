-- Seed for otorisasi.entity_config — authorization staging entities
-- Maps transaction types to menu access control

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('penghimpunan',        'keuangan', 1, 'Penghimpunan Dana',   'keuangan.monitoring.otorisasi'),
  ('penyaluran',          'keuangan', 1, 'Penyaluran Dana',     'keuangan.monitoring.otorisasi'),
  ('upload_penghimpunan', 'keuangan', 1, 'Upload Penghimpunan', 'keuangan.monitoring.otorisasi'),
  ('coa',                 'keuangan', 1, 'Master COA',          'keuangan.monitoring.otorisasi'),
  ('kas',                 'keuangan', 1, 'Master Kas',          'keuangan.monitoring.otorisasi'),
  ('bank',                'keuangan', 1, 'Master Bank',         'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
