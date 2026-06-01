-- [REPORT-CASH] View sumber rekap kas/bank (business DB: mziss_laz + mziss_wakaf)
--
-- Fase view-based: mutasi mentah + metadata rekening untuk fSummaryCash.
-- Agregasi (saldo awal/debet/kredit per akun) dihitung di report-api dgn param
-- begin/end. Join cashaccountall membatasi ke rekening kas + memberi nama/valuta.
-- Filter cabang pakai i.branchcode (mengikuti legacy fSummaryCash).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_cash_summary_src AS
SELECT
    ca.accountno        AS account_no,
    ca.accountname      AS account_name,
    ca.currencycode     AS currency_code,
    i.branchcode        AS branch_code,
    t.actualdate        AS actualdate,
    i.mutationtype      AS mutationtype,
    i.amount            AS amount,
    ca.cashaccounttype  AS account_type
FROM transaction.accounttransactionitem a
JOIN transaction.transactionitem i ON a.transactionitemid = i.transactionitemid
JOIN transaction.transaction t     ON i.transactionid = t.transactionid
JOIN transaction.cashaccountall ca ON ca.accountno = a.accountno;
