ALTER TABLE transaction.transactiontype
  ADD COLUMN IF NOT EXISTS jenis_limit VARCHAR(1) DEFAULT NULL;

-- Semua tx code pakai jenis_limit 'O' (satu limit group untuk sementara)
UPDATE transaction.transactiontype
  SET jenis_limit = 'O';
