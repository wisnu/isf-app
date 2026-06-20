-- Seed for otorisasi.entity_config — amil expense (pengeluaran amil) entity
-- Portal: zakat (mziss_laz / isf_auth_zakat)
-- Maps 'amil_expense' entity type to otorisasi menu key
-- Dispatcher: app.modules.transaction.amil_expense_service.create_from_payload
-- menu_key matches the working otorisasi menu key (finance.monitoring.authorization)
--
-- NOTE: transaction.transactiontype row (transactioncode='CO', vouchercode='KK')
-- is assumed to exist in the database (legacy data). If missing, manual verification
-- is required — see verification query below.

INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('amil_expense', 'keuangan', 1, 'Pengeluaran Amil', 'finance.monitoring.authorization')
ON CONFLICT (entity_type) DO NOTHING;

-- VERIFICATION QUERIES (run manually if unsure):
-- 1. Check if CO/KK exists:
--    SELECT vouchercode FROM transaction.transactiontype WHERE transactioncode='CO';
--    Expected: 'KK'
-- 2. If query returns nothing, manually INSERT the row:
--    INSERT INTO transaction.transactiontype (transactioncode, transactionname, vouchercode, jenis_limit)
--    VALUES ('CO', 'Cash Out Amil', 'KK', 'O')
--    ON CONFLICT (transactioncode) DO NOTHING;
