-- [REPORT-UM] View Penyerahan Uang Muka (Cash Advance) — business DB (mziss_laz + mziss_wakaf)
--
-- Transaksi penyerahan uang muka kepada karyawan. Discriminators:
--   - transaction.transactioncode = 'CA'
--   - accounttransactionitem.accounttitype = 'C' (Cash Advance account type)
--   - accounttransactionitem.cattype = 'D' (Debit = penyerahan)
--   - accountreceivable.accountreceivabletype = 'C' (Cash Advance account receivable type)
--
-- View ini menampilkan: transaksi UM, karyawan penerima, jumlah, kas/bank sumber,
-- status otorisasi, dan status ada/tidaknya pengembalian (cattype='C').
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_uang_muka_penyerahan AS
SELECT
    t.transactionid                                      AS transactionid,
    t.transactionno                                      AS transactionno,
    t.actualdate                                         AS actualdate,
    t.transactiondate                                    AS transactiondate,
    t.referenceno                                        AS referenceno,
    t.description                                        AS description,
    t.inputer                                            AS inputer,
    t.branchcode                                         AS branch_code,
    b.branchname                                         AS branch_name,
    t.authstatus                                         AS authstatus,
    ati.amount                                           AS amount,
    t.receivedfrom                                       AS receivedfrom,
    fa.accountno                                         AS employee_account_no,
    fa.accountname                                       AS employee_account_name,
    ar.employeeid                                        AS employee_id,
    COALESCE(emp.employeename, fa.accountname)           AS employee_name,
    ca.cashaccountno                                     AS cash_account_no,
    cafa.accountname                                     AS cash_account_name,
    EXISTS (
        SELECT 1
        FROM transaction.accounttransactionitem ati_return
        WHERE ati_return.accountno = ati.accountno
          AND ati_return.accounttitype = 'C'
          AND ati_return.cattype = 'C'
          AND CAST(ati_return.transactionid AS INTEGER) IN (
              SELECT CAST(ti_sub.transactionid AS INTEGER)
              FROM transaction.transactionitem ti_sub
              WHERE ti_sub.transactionitemid = ati_return.returntransactionitemid
            )
    ) AS has_return_trans
FROM transaction.accounttransactionitem ati
JOIN transaction.transactionitem ti  ON ati.transactionitemid = ti.transactionitemid
JOIN transaction.transaction t       ON ti.transactionid = t.transactionid
JOIN transaction.financialaccount fa ON ati.accountno = fa.accountno
JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
LEFT JOIN transaction.employee emp  ON ar.employeeid = emp.employeeid
LEFT JOIN transaction.cashadvancememoinfo cami ON t.transactionid = cami.transactionid
LEFT JOIN (
    SELECT DISTINCT accountno
    FROM transaction.accounttransactionitem ati_ca
    WHERE ati_ca.accounttitype = 'C'
      AND ati_ca.cattype = 'C'
) ca ON ca.accountno = ati.accountno
LEFT JOIN transaction.financialaccount cafa ON ca.accountno = cafa.accountno
WHERE t.transactioncode = 'CA'
  AND ati.accounttitype = 'C'
  AND ati.cattype = 'D'
  AND ar.accountreceivabletype = 'C';

-- Documentation
COMMENT ON VIEW dwh.v_uang_muka_penyerahan IS
  'Cash advance (uang muka karyawan) transactions with employee details, '
  'cash account info, authorization status, and return transaction flag. '
  'Filters: transactioncode=CA, accounttitype=C, cattype=D, accountreceivabletype=C';
