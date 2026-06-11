-- V011: Tambah kolom audit ke transaction.budgetowner
-- Apply to: mziss_laz, mziss_wakaf

ALTER TABLE transaction.budgetowner
  ADD COLUMN IF NOT EXISTS tglubah      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS userpengubah VARCHAR(30),
  ADD COLUMN IF NOT EXISTS terminalubah VARCHAR(30);

COMMENT ON COLUMN transaction.budgetowner.tglubah      IS 'Waktu terakhir diubah';
COMMENT ON COLUMN transaction.budgetowner.userpengubah IS 'User yang terakhir mengubah';
COMMENT ON COLUMN transaction.budgetowner.terminalubah IS 'Terminal/IP yang terakhir mengubah';
