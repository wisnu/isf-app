-- 009_upload_penghimpunan.sql
-- Kolom legacy yang belum ada di schema dump batchuploaditem
ALTER TABLE transaction.batchuploaditem
  ADD COLUMN IF NOT EXISTS amountzakatperusahaan numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amountinfaqterikat     numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amounttitipanqurban    numeric(30,6) DEFAULT 0;

-- Status otorisasi batch: P=pending, A=approved
ALTER TABLE transaction.batchupload
  ADD COLUMN IF NOT EXISTS authstatus character varying(1) DEFAULT 'P';
