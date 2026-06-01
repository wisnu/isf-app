-- [REPORT-PROG] View Grup C: List Uang Muka, Realisasi Project (Memo), Piutang Realisasi
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

-- List Transaksi Uang Muka Kegiatan (fListEmployeeCA): accounttitype 'C' cattype 'D'
CREATE OR REPLACE VIEW dwh.v_cashadvance_trx AS
SELECT
    c.actualdate                              AS actualdate,
    g.branchcode                              AS branch_code,
    g.accountno                               AS accountno,
    g.accountname                             AS accountname,
    c.transactionno                           AS transactionno,
    c.referenceno                             AS referenceno,
    c.description                             AS description,
    c.inputer                                 AS inputer,
    c.authstatus                              AS authstatus,
    b.amount::float8                          AS amount,
    b.ekuivalenamount::float8                 AS ekuiv,
    b.currencycode                            AS currencycode,
    d.full_name                               AS currency_name,
    f.employeeidnumber                        AS employeeidnumber,
    EXISTS (SELECT 1 FROM transaction.cashadvancereturninfo cr
            WHERE cr.sourcetransactionid = c.transactionid) AS has_lpj,
    rtt.transactionno                         AS return_transactionno,
    a.transactionitemid                       AS transactionitemid
FROM transaction.accounttransactionitem a
JOIN transaction.transactionitem b   ON a.transactionitemid = b.transactionitemid
JOIN transaction.transaction c        ON b.transactionid = c.transactionid
LEFT JOIN transaction.currency d      ON c.currencycode = d.currency_code
JOIN transaction.accountreceivable f  ON a.accountno = f.accountno
JOIN transaction.financialaccount g   ON f.accountno = g.accountno
LEFT JOIN transaction.transactionitem rt ON rt.transactionitemid = a.returntransactionitemid
LEFT JOIN transaction.transaction rtt    ON rtt.transactionid = rt.transactionid
WHERE a.accounttitype = 'C' AND a.cattype = 'D';


-- Piutang Realisasi Penyaluran (fSummaryProgramCA): realisasi belum/penuh dilaporkan
CREATE OR REPLACE VIEW dwh.v_program_realization AS
SELECT
    r.realizationid                           AS realizationid,
    r.realizationdate                         AS realizationdate,
    r.realizationamount::float8               AS amount,
    r.realizationinputuser                    AS input_user,
    r.realizationtype                         AS realization_type,
    r.realizationdescription                  AS description,
    r.branchcode                              AS branch_code,
    m.realmemonumber                          AS memo_number,
    e.employeename                            AS employee_name,
    q.reportamount                            AS report_amount,
    q.receivablereportuserinput               AS report_user,
    q.receivablereportdate                    AS report_date
FROM program.realizationmemo m
JOIN program.realization r  ON m.realmemoid = r.realmemoid
JOIN program.vemployee e    ON r.employeeid = e.employeeid
LEFT JOIN (
    SELECT t.realizationid, t.receivablereportuserinput, t.receivablereportdate,
           SUM(d.realizationamount)::float8 AS reportamount
    FROM program.statusreceivablereport t
    JOIN program.statusrecrepdetail d ON t.statusreceivableid = d.statusreceivableid
    WHERE d.reportdetailstatus IN ('1', '2')
    GROUP BY t.realizationid, t.receivablereportuserinput, t.receivablereportdate
) q ON q.realizationid = r.realizationid
WHERE r.statusreceivables = 'Y';


-- Laporan Realisasi Project (Memo) (fDistProjectByMemo_List): ringkasan per memo
CREATE OR REPLACE VIEW dwh.v_realization_memo AS
SELECT
    m.realmemoid                              AS realmemoid,
    m.realmemonumber                          AS memo_number,
    m.realmemodate                            AS memo_date,
    m.realmemosubject                         AS memo_subject,
    m.realmemoamount::float8                  AS memo_amount,
    m.branchcode                              AS branch_code,
    COALESCE(rz.total_realisasi, 0)::float8   AS total_realisasi,
    COALESCE(rz.cnt, 0)                       AS realisasi_count,
    COALESCE(rt.total_return, 0)::float8      AS total_return
FROM program.realizationmemo m
LEFT JOIN (
    SELECT realmemoid, SUM(realizationamount) AS total_realisasi, COUNT(*) AS cnt
    FROM program.realization GROUP BY realmemoid
) rz ON rz.realmemoid = m.realmemoid
LEFT JOIN (
    SELECT r.realmemoid, SUM(rr.returnamount) AS total_return
    FROM program.realization r
    JOIN program.realizationreturn rr ON rr.realizationid = r.realizationid
    GROUP BY r.realmemoid
) rt ON rt.realmemoid = m.realmemoid;
