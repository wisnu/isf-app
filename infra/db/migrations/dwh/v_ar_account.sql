-- [REPORT-AR] View akun piutang / uang muka (business DB)
--
-- financialaccount + accountreceivable (+ externaldebtor utk tipe 'D'). Tipe:
--   'E' = piutang karyawan, 'D' = piutang non-karyawan (eksternal), 'C' = uang muka.
-- Saldo awal / debet / kredit dihitung di report-api (agregasi mutasi per accountno).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_ar_account AS
SELECT
    a.accountno                 AS accountno,
    a.accountname               AS accountname,
    a.branchcode                AS branch_code,
    b.accountreceivabletype     AS ar_type,
    c.description               AS debtor_description
FROM transaction.financialaccount a
JOIN transaction.accountreceivable b ON a.accountno = b.accountno
LEFT JOIN transaction.externaldebtor c ON b.debtorid = c.debtorid;
