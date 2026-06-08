ALTER TABLE transaction.transactiontype
  ADD COLUMN IF NOT EXISTS jenis_limit VARCHAR(1) DEFAULT NULL;

-- Map transaksi input yang mendukung limit
UPDATE transaction.transactiontype
  SET jenis_limit = 'O'
  WHERE transactioncode IN ('SD001', 'SDMULTI', 'SDULBA', 'DD001');
