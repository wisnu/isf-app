-- [REPORT-GT] View laporan List Transaksi Umum (business DB: mziss_laz + mziss_wakaf)
--
-- Fase view-based: membungkus query legacy fGeneralTransaction atas tabel live
-- transaction.*. Grain = transactionitem (master-detail di-group saat disajikan).
-- Hanya transaksi umum: transactioncode = 'GT'.
--
-- Catatan: LEFT JOIN accounttransactionitem di legacy tidak dipakai di output &
-- berisiko menggandakan baris, jadi di-drop. LEFT JOIN budget dipertahankan
-- (meniru legacy; bila item punya >1 budget bisa terduplikasi).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_general_transaction AS
SELECT
    t.branchcode                                   AS branch_code,
    t.actualdate                                   AS actualdate,
    t.transactionid                                AS transactionid,
    t.transactionno                                AS transactionno,
    t.transactiondate                              AS transactiondate,
    t.description                                  AS header_description,
    t.inputer                                      AS inputer,
    ti.refaccountno                                AS refaccountno,
    ti.refaccountname                              AS refaccountname,
    ti.mutationtype                                AS mutationtype,
    ti.amount                                      AS amount,
    ti.description                                 AS item_description,
    qb.budgetcode                                  AS budget_code,
    qb.budgetitemdescription                       AS budget_item_description
FROM transaction.transaction t
   , transaction.transactionitem ti
     LEFT JOIN (
        SELECT bdt.transactionitemid, bdg.budgetcode, bdip.budgetitemdescription
        FROM transaction.budget bdg
           , transaction.budgettransaction bdt
           , transaction.budgetitem bdi
           , transaction.budgetitem bdip
        WHERE bdg.budgetid = bdt.budgetid
          AND bdg.itemid = bdi.itemid
          AND bdi.parentitemid = bdip.itemid
     ) qb ON (qb.transactionitemid = ti.transactionitemid)
WHERE t.transactionid = ti.transactionid
  AND t.transactioncode = 'GT';
