-- [REPORT-CASH] View mutasi kas/bank harian (zakat / mziss_laz)
--
-- Fase view-based: membungkus query legacy fDailyCash (per rekening kas/bank).
-- Grain = transactionitem per rekening. Saldo awal & running balance dihitung di
-- report-api (dailybalancecash kosong). Drop join transactionbatch legacy (BatchNo
-- tak ditampilkan).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_cash_mutation AS
SELECT
    a.accountno          AS account_no,
    t.actualdate         AS actualdate,
    t.transactionid      AS transactionid,
    t.transactionno      AS transactionno,
    i.mutationtype       AS mutationtype,
    i.amount             AS amount,
    t.referenceno        AS reference_no,
    t.description        AS description,
    t.authstatus         AS auth_status,
    t.inputer            AS inputer,
    i.transactionitemid  AS transactionitemid
FROM transaction.accounttransactionitem a
JOIN transaction.transactionitem i ON a.transactionitemid = i.transactionitemid
JOIN transaction.transaction t     ON i.transactionid = t.transactionid;
