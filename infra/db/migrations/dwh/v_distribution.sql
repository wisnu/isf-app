-- [REPORT-TRX] View Penyaluran Dana (fDistributionReport) — business DB
--
-- accounttransactionitem.accounttitype='Z' (sisi penyaluran). Amount signed:
-- mutationtype 'D' → +ekuiv, else -ekuiv. Join produk (grandparent), cabang,
-- channel-account & anggaran. Filter tanggal/cabang/fund di report-api.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_distribution AS
SELECT
    t.actualdate                              AS actualdate,
    i.branchcode                              AS branch_code,
    b.branchname                              AS branch_name,
    gpr.productname                           AS product_name,
    f.accountname                             AS account_name,
    t.description                             AS description,
    a.ashnaf                                  AS ashnaf,
    a.distributioncategory                    AS distribution_category,
    a.fundentity                              AS fund_entity,
    t.channelcode                             AS channel_code,
    CASE t.channelcode WHEN 'R' THEN 'Kas Cabang' WHEN 'P' THEN 'Kas Kecil'
         WHEN 'A' THEN 'Bank' ELSE 'Aktiva' END AS channel,
    (CASE WHEN i.mutationtype = 'D' THEN i.ekuivalenamount ELSE -i.ekuivalenamount END)::float8 AS amount,
    t.donorname                               AS donorname,
    t.referenceno                             AS referenceno,
    t.inputer                                 AS inputer,
    t.transactionno                           AS transactionno,
    t.authstatus                              AS authstatus,
    t.channelaccountno                        AS bank_account_no,
    fc.accountname                            AS bank_account_name,
    qb.budgetcode                             AS budgetcode,
    qb.budgetitemdescription                  AS budgetitemdescription,
    i.transactionitemid                       AS transactionitemid
FROM transaction.accounttransactionitem a
JOIN transaction.transactionitem i  ON a.transactionitemid = i.transactionitemid
JOIN transaction.transaction t      ON i.transactionid = t.transactionid
JOIN transaction.financialaccount f ON a.accountno = f.accountno
JOIN transaction.branch b           ON b.branchcode = i.branchcode
LEFT JOIN transaction.productaccount p ON p.accountno = f.accountno
LEFT JOIN transaction.product pr       ON p.productid = pr.productid
LEFT JOIN transaction.product gpr      ON pr.parentproductid = gpr.productid
LEFT JOIN transaction.financialaccount fc ON fc.accountno = t.channelaccountno
LEFT JOIN (
    SELECT bdt.transactionitemid, bdg.budgetcode, bdip.budgetitemdescription
    FROM transaction.budget bdg
    JOIN transaction.budgettransaction bdt ON bdg.budgetid = bdt.budgetid
    JOIN transaction.budgetitem bdi  ON bdg.itemid = bdi.itemid
    JOIN transaction.budgetitem bdip ON bdi.parentitemid = bdip.itemid
) qb ON qb.transactionitemid = i.transactionitemid
WHERE a.accounttitype = 'Z';
