-- DWH View: dwh.v_piutang_non_karyawan
-- Portal: zakat
-- Modul: Piutang (Pinjam/Bayar) — Non Karyawan
-- Dipakai oleh: laporan-piutang-non-karyawan, api-piutang
--
-- Menampilkan transaksi piutang non-karyawan.
-- Notes: Modul piutang legacy menggunakan tabel transaction tanpa proper relasi ke
-- accountreceivable. Debitur disimpan di field receivedfrom (nama penerima).
-- View ini menyajikan data 'as-is' dari transaction dengan filter transactioncode EAR/PEAR.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_piutang_non_karyawan AS
SELECT
    t.transactionid,
    t.transactionno,
    t.transactioncode,
    CAST(t.actualdate AS DATE) AS actualdate,
    t.branchcode,
    t.inputer,
    CAST(t.amount AS NUMERIC(20, 4)) AS amount,
    t.currencycode,
    t.referenceno,
    t.description,
    t.receivedfrom AS debtor_name,
    t.authstatus,
    CAST(t.transactiondate AS TIMESTAMPTZ) AS transaction_timestamp,
    t.paidto
FROM transaction.transaction t
WHERE t.transactioncode IN ('EAR', 'PEAR');

COMMENT ON VIEW dwh.v_piutang_non_karyawan IS 'Transaksi piutang (EAR/PEAR) — legacy modul tanpa relasi structured ke accountreceivable';
