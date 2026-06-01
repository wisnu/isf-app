-- [REPORT-TRX] View Penghimpunan Dana (fCollectionReport) — business DB
--
-- accounttransactionitem.accounttitype='D' (sisi penerimaan). Amount signed:
-- mutationtype 'C' → +ekuiv, else -ekuiv (kebalikan penyaluran). Dipakai untuk
-- detail list & rekap per dana (saldo awal/mutasi/akhir). Filter di report-api.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_collection AS
SELECT
    t.actualdate                              AS actualdate,
    i.branchcode                              AS branch_code,
    b.branchname                              AS branch_name,
    f.accountname                             AS account_name,
    t.description                             AS description,
    a.fundentity                              AS fund_entity,
    a.donorid                                 AS donorid,
    t.channelcode                             AS channel_code,
    CASE t.channelcode WHEN 'R' THEN 'Kas Cabang' WHEN 'P' THEN 'Kas Kecil'
         WHEN 'A' THEN 'Bank' ELSE 'Aktiva' END AS channel,
    (CASE WHEN i.mutationtype = 'C' THEN i.ekuivalenamount ELSE -i.ekuivalenamount END)::float8 AS amount,
    t.donorname                               AS donorname,
    t.marketerid                              AS marketerid,
    t.referenceno                             AS referenceno,
    t.inputer                                 AS inputer,
    t.transactionno                           AS transactionno,
    t.authstatus                              AS authstatus,
    i.currencycode                            AS currencycode,
    t.channelaccountno                        AS bank_account_no,
    fc.accountname                            AS bank_account_name,
    i.transactionitemid                       AS transactionitemid
FROM transaction.accounttransactionitem a
JOIN transaction.transactionitem i  ON a.transactionitemid = i.transactionitemid
JOIN transaction.transaction t      ON i.transactionid = t.transactionid
JOIN transaction.financialaccount f ON a.accountno = f.accountno
JOIN transaction.branch b           ON b.branchcode = i.branchcode
LEFT JOIN transaction.financialaccount fc ON fc.accountno = t.channelaccountno
WHERE a.accounttitype = 'D';
