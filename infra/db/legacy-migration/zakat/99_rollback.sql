-- 99_rollback.sql — Membatalkan migrasi legacy → isf-app (portal ZAKAT)
--
-- ⚠️ Menghapus schema otorisasi & dwh BESERTA ISINYA (submission otorisasi yang
--    sudah dibuat di isf-app ikut hilang). Hanya untuk membatalkan migrasi
--    sebelum go-live / setelah uji coba. Backup dulu.
--
-- Kolom tambahan di tabel legacy TIDAK di-drop secara default: kolom aditif
-- tidak mengganggu aplikasi legacy, dan drop kolom pada tabel besar mahal.
-- Bila memang perlu, buka komentar blok "OPSIONAL" di bawah.

BEGIN;

DROP SCHEMA IF EXISTS dwh CASCADE;
DROP SCHEMA IF EXISTS otorisasi CASCADE;

-- Index tambahan humancapital (murah, aman di-drop)
DROP INDEX IF EXISTS transaction.idx_humancapitalbatch_batchperioddesc;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatch_transactiondate;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatch_uploaduserid;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatchitem_batchid;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatchitem_donorid;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatchitem_employeenumber;
DROP INDEX IF EXISTS transaction.idx_humancapitalbatchitem_transactionid;
DROP INDEX IF EXISTS transaction.idx_humancapitalpassedreport_batchid;
DROP INDEX IF EXISTS transaction.idx_humancapitalpassedreport_donorid;

-- OPSIONAL — kembalikan tabel legacy ke struktur asli:
-- ALTER TABLE fund.individualdonor        DROP COLUMN IF EXISTS donorgroup;
-- ALTER TABLE transaction.batchupload     DROP COLUMN IF EXISTS authstatus;
-- ALTER TABLE transaction.batchuploaditem ALTER COLUMN amountzakatperusahaan DROP DEFAULT;
-- ALTER TABLE transaction.budgetowner     DROP COLUMN IF EXISTS tglubah,
--                                         DROP COLUMN IF EXISTS userpengubah,
--                                         DROP COLUMN IF EXISTS terminalubah;
-- ALTER TABLE transaction.humancapitalbatch DROP COLUMN IF EXISTS namafile;
-- ALTER TABLE transaction.transactiontype DROP COLUMN IF EXISTS jenis_limit;

COMMIT;
