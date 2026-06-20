-- Seed for otorisasi.entity_config — amil income (penerimaan amil) entity
-- Portal: zakat (mziss_laz / isf_auth_zakat)
-- Maps 'amil_income' entity type to otorisasi menu key
-- Dispatcher: app.modules.transaction.amil_income_service.create_from_payload
-- menu_key matches the working transaksi_umum row (finance.monitoring.authorization)

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('amil_income', 'keuangan', 1, 'Penerimaan Amil', 'finance.monitoring.authorization')
ON CONFLICT (entity_type) DO NOTHING;
