-- [REPORT-TRX] View Penerimaan & Pengeluaran Amil (business DB)
--
-- fCashInReport  : transaksi kas masuk amil (transactioncode 'CI', mutationtype 'C').
-- fCashOutReport : transaksi beban amil — akun di bawah hierarki 530000
--                  (PENYALURAN DANA AMIL) + lookup budget. Rekonsiliasi ke
--                  Perubahan Dana "Penggunaan Amil" & Arus Kas OpsPenyaluranAmil.
-- Filter tanggal & cabang dilakukan di report-api.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_amil_cashin AS
SELECT
    t.actualdate                              AS actualdate,
    t.branchcode                              AS branch_code,
    a.account_code                            AS account_code,
    a.account_name                            AS account_name,
    t.description                             AS description,
    i.amount::float8                          AS amount,
    t.referenceno                             AS referenceno,
    t.transactionno                           AS transactionno,
    t.inputer                                 AS inputer,
    t.authstatus                              AS authstatus,
    CASE t.channelcode WHEN 'R' THEN 'Kas Cabang' WHEN 'P' THEN 'Kas Kecil'
         WHEN 'A' THEN 'Bank' ELSE 'Aktiva' END AS channel,
    i.transactionitemid                       AS transactionitemid
FROM transaction.transaction t
JOIN transaction.transactionitem i ON t.transactionid = i.transactionid
JOIN transaction.account a         ON a.account_code = i.refaccountno
WHERE t.transactioncode = 'CI' AND i.mutationtype = 'C';


CREATE OR REPLACE VIEW dwh.v_amil_cashout AS
SELECT
    t.actualdate                              AS actualdate,
    t.branchcode                              AS branch_code,
    a.account_code                            AS account_code,
    a.account_name                            AS account_name,
    t.description                             AS description,
    (CASE WHEN i.mutationtype = 'D' THEN i.amount ELSE -i.amount END)::float8 AS amount,
    t.referenceno                             AS referenceno,
    t.transactionno                           AS transactionno,
    t.inputer                                 AS inputer,
    t.authstatus                              AS authstatus,
    CASE t.channelcode WHEN 'R' THEN 'Kas Cabang' WHEN 'P' THEN 'Kas Kecil'
         WHEN 'A' THEN 'Bank' ELSE 'Aktiva' END AS channel,
    qb.budgetcode                             AS budgetcode,
    qb.budgetitemdescription                  AS budgetitemdescription,
    i.transactionitemid                       AS transactionitemid
FROM transaction.transaction t
JOIN transaction.transactionitem i ON t.transactionid = i.transactionid
JOIN transaction.account a         ON a.account_code = i.refaccountno
LEFT JOIN (
    SELECT bdt.transactionitemid, bdg.budgetcode, bdip.budgetitemdescription
    FROM transaction.budget bdg
    JOIN transaction.budgettransaction bdt ON bdg.budgetid = bdt.budgetid
    JOIN transaction.budgetitem bdi  ON bdg.itemid = bdi.itemid
    JOIN transaction.budgetitem bdip ON bdi.parentitemid = bdip.itemid
) qb ON qb.transactionitemid = i.transactionitemid
WHERE EXISTS (
    SELECT 1 FROM transaction.accounthierarchy ah
    WHERE ah.fl_parentaccountcode = '530000' AND ah.fl_childaccountcode = a.account_code
);
