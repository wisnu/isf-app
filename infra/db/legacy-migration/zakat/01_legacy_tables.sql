-- 01_legacy_tables.sql — Perubahan aditif pada tabel legacy yang dibutuhkan isf-app
-- Hasil diff katalog mziss_laz_origin (legacy) vs mziss_laz (isf-app), 2026-11-18.
-- Semua perubahan ADITIF: tidak ada kolom legacy yang di-drop/rename/ubah tipe,
-- sehingga aplikasi legacy (DAF) tetap bisa berjalan pada DB yang sama.
-- Idempotent (IF NOT EXISTS). Kompatibel PostgreSQL 12+.

-- ── fund.individualdonor ── (asal: infra/db/migrations/fund/V001)
-- Kolom work* lain dari V001 sudah ada di legacy; hanya donorgroup yang belum.
ALTER TABLE fund.individualdonor ADD COLUMN IF NOT EXISTS donorgroup VARCHAR(1);

-- ── transaction.batchupload / batchuploaditem ── (asal: transaction/009_upload_penghimpunan.sql)
-- authstatus: P=pending, Q=processing, A=authorized, F=failed (dipakai modul Upload Penghimpunan).
ALTER TABLE transaction.batchupload ADD COLUMN IF NOT EXISTS authstatus VARCHAR(1) DEFAULT 'P';
ALTER TABLE transaction.batchuploaditem ALTER COLUMN amountzakatperusahaan SET DEFAULT 0;

-- ⚠️ PENTING: batch historis legacy sudah diotorisasi & diposting oleh aplikasi lama
-- (authorizeduser terisi, item sudah ter-link ke transaksi). Tanpa UPDATE ini semuanya
-- akan tampil 'P' (pending) dan bisa di-approve ulang di isf-app → POSTING GANDA.
UPDATE transaction.batchupload
   SET authstatus = CASE WHEN authorizeduser IS NOT NULL AND authorizeduser <> '' THEN 'A' ELSE 'P' END
 WHERE authstatus IS NULL OR authstatus = 'P';

-- ── transaction.budgetowner ── (asal: transaction/011_budgetowner_audit_cols.sql)
ALTER TABLE transaction.budgetowner
  ADD COLUMN IF NOT EXISTS tglubah      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS userpengubah VARCHAR(30),
  ADD COLUMN IF NOT EXISTS terminalubah VARCHAR(30);

-- ── transaction.humancapital* ── (asal: transaction/012_create_humancapital_tables.sql)
-- Tabel sudah ada di legacy; isf-app menambah kolom namafile + index.
ALTER TABLE transaction.humancapitalbatch ADD COLUMN IF NOT EXISTS namafile VARCHAR(200);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_batchperioddesc      ON transaction.humancapitalbatch (batchperioddesc);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_transactiondate      ON transaction.humancapitalbatch (transactiondate);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_uploaduserid         ON transaction.humancapitalbatch (uploaduserid);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_batchid          ON transaction.humancapitalbatchitem (batchid);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_donorid          ON transaction.humancapitalbatchitem (donorid);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_employeenumber   ON transaction.humancapitalbatchitem (employeenumber);
CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_transactionid    ON transaction.humancapitalbatchitem (transactionid);
CREATE INDEX IF NOT EXISTS idx_humancapitalpassedreport_batchid       ON transaction.humancapitalpassedreport (batchid);
CREATE INDEX IF NOT EXISTS idx_humancapitalpassedreport_donorid       ON transaction.humancapitalpassedreport (donorid);

-- ── transaction.transactiontype ── (asal: transaction/add_jenis_limit_to_transactiontype.sql)
-- Grup limit otorisasi; saat ini semua kode memakai 'O' (satu grup).
ALTER TABLE transaction.transactiontype ADD COLUMN IF NOT EXISTS jenis_limit VARCHAR(1) DEFAULT NULL;
UPDATE transaction.transactiontype SET jenis_limit = 'O' WHERE jenis_limit IS NULL;
