-- DWH View: dwh.v_realization_return
-- Modul: Pengembalian Realisasi Program
-- Portal: zakat (mziss_laz) — juga dapat diapply ke mziss_wakaf jika diperlukan
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f infra/db/migrations/dwh/v_realization_return.sql

CREATE SCHEMA IF NOT EXISTS dwh;

-- View utama: list + detail pengembalian realisasi
CREATE OR REPLACE VIEW dwh.v_realization_return AS
SELECT
    rr.returnid                                          AS return_id,
    CAST(rr.returndate AS date)                          AS return_date,
    rr.returndescription                                 AS return_description,
    CAST(rr.returnamount AS numeric(30,8))               AS return_amount,
    CAST(rr.costamount AS numeric(30,4))                 AS cost_amount,
    rr.realizationid                                     AS realization_id,
    CAST(r.realizationdate AS date)                      AS realization_date,
    r.realizationdescription                             AS realization_description,
    CAST(r.realizationamount AS numeric(30,8))           AS realization_amount,
    r.realizationtype                                    AS realization_type,
    rm.realmemonumber                                    AS memo_number,
    rm.realmemosubject                                   AS memo_subject,
    rr.branchcode                                        AS branch_code,
    rr.inputuser                                         AS input_user,
    CAST(rr.inputdate AS date)                           AS input_date,
    rr.authuser                                          AS auth_user,
    CAST(rr.authdate AS date)                            AS auth_date
FROM program.realizationreturn rr
JOIN program.realization r
     ON r.realizationid = rr.realizationid
JOIN program.realizationmemo rm
     ON rm.realmemoid = r.realmemoid;
