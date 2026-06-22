-- [LAPORAN-PENYALURAN] DWH Views untuk Laporan Penyaluran Domain Distribution
-- Portal: zakat (mziss_laz)
-- Tanggal: 2026-06-22
--
-- Views:
--   1. dwh.v_report_mustahiq_list — daftar mustahiq dengan detail produk + ashnaf
--   2. dwh.v_report_realization_regular — realisasi program RUTIN (programtype='R')
--   3. dwh.v_report_realization_non_regular — realisasi program NON RUTIN (programtype='N')
--   4. dwh.v_report_realization_return — pengembalian realisasi + biaya detail
--   5. dwh.v_report_realization_by_mustahiq — realisasi cross-type per mustahiq
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f infra/db/migrations/dwh/v_distribution_reports.sql

CREATE SCHEMA IF NOT EXISTS dwh;

-- ============================================================================
-- View 1: Laporan Daftar Mustahiq
-- JOIN: mustahiq + customer + customercorporate + mustahiqproduct + product +
--       mustahiqadditionalinfo + enum_varchar(ashnaf) + supervisor
-- NOTE: sd/smp/sma/universitas tahunawal/tahunakhir stored as timestamp (year encoded)
-- ============================================================================
CREATE OR REPLACE VIEW dwh.v_report_mustahiq_list AS
SELECT
    m.mustahiqid                                                                AS mustahiq_id,
    m.mustahiqtype                                                              AS mustahiq_type,
    c.customername                                                              AS customer_name,
    c.addressstreet                                                             AS address_street,
    c.addresskelurahan                                                          AS address_kelurahan,
    c.addresskecamatan                                                          AS address_kecamatan,
    c.addresscity                                                               AS address_city,
    c.phonenumber                                                               AS phone_number,
    COALESCE(cc.cpname, '')                                                    AS cp_name,
    COALESCE(cc.cpphonenumber, '')                                             AS cp_phone_number,
    COALESCE(cc.cpmobilenumber, '')                                            AS cp_mobile_number,
    COALESCE(ev.enum_description, '')                                          AS ashnaf_label,
    COALESCE(mp.productid, 0)                                                  AS product_id,
    COALESCE(pr.productname, '')                                               AS product_name,
    CAST(mp.datestart AS DATE)                                                 AS date_start,
    CAST(COALESCE(mp.distributionamount, 0) AS FLOAT8)                        AS distribution_amount,
    COALESCE(mai.schoolname, '')                                               AS school_name,
    COALESCE(mai.sd_kelas, '')                                                 AS sd_kelas,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.sd_tahunawal) AS INTEGER), 0)         AS sd_tahun_awal,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.sd_tahunakhir) AS INTEGER), 0)        AS sd_tahun_akhir,
    COALESCE(mai.smp_kelas, '')                                                AS smp_kelas,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.smp_tahunawal) AS INTEGER), 0)        AS smp_tahun_awal,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.smp_tahunakhir) AS INTEGER), 0)       AS smp_tahun_akhir,
    COALESCE(mai.sma_kelas, '')                                                AS sma_kelas,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.sma_tahunawal) AS INTEGER), 0)        AS sma_tahun_awal,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.sma_tahunakhir) AS INTEGER), 0)       AS sma_tahun_akhir,
    COALESCE(mai.universitas_kelas, '')                                        AS universitas_kelas,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.universitas_tahunawal) AS INTEGER), 0) AS universitas_tahun_awal,
    COALESCE(CAST(EXTRACT(YEAR FROM mai.universitas_tahunakhir) AS INTEGER), 0) AS universitas_tahun_akhir,
    COALESCE(mai.achievement, '')                                              AS achievement,
    COALESCE(sc.customername, '')                                              AS supervisor_name
FROM program.mustahiq m
JOIN program.customer c              ON c.customerid = m.customerid
LEFT JOIN program.customercorporate cc   ON cc.customerid = m.customerid
LEFT JOIN program.mustahiqproduct mp     ON mp.mustahiqid = m.mustahiqid
LEFT JOIN program.product pr             ON pr.productid = mp.productid
LEFT JOIN program.mustahiqadditionalinfo mai ON mai.mustahiqproductid = mp.mustahiqproductid
LEFT JOIN enum_varchar ev            ON ev.enum_name = 'eAshnaf'
                                     AND CAST(ev.enum_value AS VARCHAR) = CAST(m.ashnaf AS VARCHAR)
LEFT JOIN program.mustahiq sv        ON sv.mustahiqid = mai.mustahiqidsupervisor
LEFT JOIN program.customer sc        ON sc.customerid = sv.customerid
;

COMMENT ON VIEW dwh.v_report_mustahiq_list IS 'Laporan Daftar Mustahiq — detail program + ashnaf per mustahiq (Individu MP / Lembaga MC)';

-- ============================================================================
-- View 2: Laporan Program Penyaluran RUTIN
-- DISCRIMINATOR KRITIS: program.programtype = 'R'
-- Budget: subquery pulls budgetitemname (NOT itemname) from transaction.budgetitem
-- ============================================================================
CREATE OR REPLACE VIEW dwh.v_report_realization_regular AS
SELECT
    pr.productid                                                               AS product_id,
    pr.productname                                                             AS product_name,
    pgr.productgroupname                                                       AS product_group_name,
    mp.mustahiqproductname                                                     AS mustahiq_product_name,
    c.customername                                                             AS customer_name,
    c.addressstreet                                                            AS address_street,
    r.realizationid                                                            AS realization_id,
    CAST(r.realizationdate AS DATE)                                           AS realization_date,
    r.statusreceivables                                                       AS status_receivables,
    CAST(rd.realizationamount AS FLOAT8)                                      AS realization_amount,
    CAST(COALESCE(s.reportamount, 0) AS FLOAT8)                              AS report_amount,
    COALESCE(s.reportdetailstatus, '0')                                       AS report_detail_status,
    COALESCE(bq.budget_code, '')                                              AS budget_code,
    CASE
        WHEN bq.parent_item_name IS NOT NULL
        THEN CONCAT(bq.item_name, ' - ', bq.parent_item_name)
        ELSE COALESCE(bq.item_name, '')
    END                                                                        AS budget_item_description
FROM program.product pr
JOIN program.program g               ON g.productid = pr.productid
                                     AND CAST(g.programtype AS VARCHAR) = 'R'
JOIN program.productgroup pgr        ON pgr.productgroupid = pr.productgroupid
JOIN program.mustahiqproduct mp      ON mp.productid = pr.productid
JOIN program.realization r           ON r.realizationid IN (
    SELECT rd2.realizationid FROM program.realizationdetail rd2
    WHERE rd2.mustahiqproductid = mp.mustahiqproductid
)
JOIN program.realizationdetail rd    ON rd.realizationid = r.realizationid
                                     AND rd.mustahiqproductid = mp.mustahiqproductid
JOIN program.mustahiq m              ON m.mustahiqid = mp.mustahiqid
JOIN program.customer c              ON c.customerid = m.customerid
LEFT JOIN program.statusrecrepdetail s ON s.realizationdetailid = rd.realizationdetailid
LEFT JOIN (
    SELECT
        rb.realizationid,
        bdg.budgetcode                       AS budget_code,
        bdi.budgetitemname                   AS item_name,
        bdip.budgetitemname                  AS parent_item_name
    FROM program.realizationbudget rb
    JOIN transaction.budget bdg              ON bdg.budgetid = rb.budgetid
    JOIN transaction.budgetitem bdi          ON bdi.itemid = bdg.itemid
    LEFT JOIN transaction.budgetitem bdip    ON bdip.itemid = bdi.parentitemid
) bq ON bq.realizationid = r.realizationid
;

COMMENT ON VIEW dwh.v_report_realization_regular IS 'Laporan Program Penyaluran Rutin (programtype=R) dengan LPJ status dan anggaran';

-- ============================================================================
-- View 3: Laporan Program Penyaluran NON RUTIN
-- DISCRIMINATOR KRITIS: program.programtype = 'N'
-- Includes: proposal, sumber dana, branch_code (untuk filter cabang)
-- ============================================================================
CREATE OR REPLACE VIEW dwh.v_report_realization_non_regular AS
SELECT
    pr.productid                                                               AS product_id,
    pr.productname                                                             AS product_name,
    pgr.productgroupname                                                       AS product_group_name,
    mp.mustahiqproductname                                                     AS mustahiq_product_name,
    c.customername                                                             AS customer_name,
    c.addressstreet                                                            AS address_street,
    r.realizationid                                                            AS realization_id,
    CAST(r.realizationdate AS DATE)                                           AS realization_date,
    CAST(rd.realizationamount AS FLOAT8)                                      AS realization_amount,
    rd.detaildescription                                                       AS detail_description,
    COALESCE(po.proposalno, '')                                               AS proposal_no,
    COALESCE(po.proposaldescription, '')                                      AS proposal_description,
    CAST(COALESCE(po.proposalnominal, 0) AS FLOAT8)                          AS proposal_nominal,
    COALESCE(po.proposalreferenceby, '')                                      AS proposal_reference_by,
    COALESCE(fa.accountname, '')                                              AS account_name,
    COALESCE(bq.budget_code, '')                                              AS budget_code,
    CASE
        WHEN bq.parent_item_name IS NOT NULL
        THEN CONCAT(bq.item_name, ' - ', bq.parent_item_name)
        ELSE COALESCE(bq.item_name, '')
    END                                                                        AS budget_item_description,
    COALESCE(mp.branchcode, '')                                               AS branch_code
FROM program.product pr
JOIN program.program g               ON g.productid = pr.productid
                                     AND CAST(g.programtype AS VARCHAR) = 'N'
JOIN program.productgroup pgr        ON pgr.productgroupid = pr.productgroupid
JOIN program.mustahiqproduct mp      ON mp.productid = pr.productid
JOIN program.realization r           ON r.realizationid IN (
    SELECT rd2.realizationid FROM program.realizationdetail rd2
    WHERE rd2.mustahiqproductid = mp.mustahiqproductid
)
JOIN program.realizationdetail rd    ON rd.realizationid = r.realizationid
                                     AND rd.mustahiqproductid = mp.mustahiqproductid
JOIN program.mustahiq m              ON m.mustahiqid = mp.mustahiqid
JOIN program.customer c              ON c.customerid = m.customerid
LEFT JOIN program.proposal po        ON po.proposalid = mp.proposalid
LEFT JOIN transaction.financialaccount fa ON fa.accountno = mp.accountno
LEFT JOIN (
    SELECT
        rb.realizationid,
        bdg.budgetcode                       AS budget_code,
        bdi.budgetitemname                   AS item_name,
        bdip.budgetitemname                  AS parent_item_name
    FROM program.realizationbudget rb
    JOIN transaction.budget bdg              ON bdg.budgetid = rb.budgetid
    JOIN transaction.budgetitem bdi          ON bdi.itemid = bdg.itemid
    LEFT JOIN transaction.budgetitem bdip    ON bdip.itemid = bdi.parentitemid
) bq ON bq.realizationid = r.realizationid
;

COMMENT ON VIEW dwh.v_report_realization_non_regular IS 'Laporan Program Penyaluran Non Rutin (programtype=N) dengan proposal + sumber dana + cabang';

-- ============================================================================
-- View 4: Laporan Pengembalian Realisasi (Report variant — multiple cost rows per return)
-- FILTER KRITIS: returndate (bukan realizationdate)
-- Multiple rows per return_id jika ada >1 cost item; single row with NULL cost jika tidak ada
-- ============================================================================
CREATE OR REPLACE VIEW dwh.v_report_realization_return AS
SELECT
    rr.returnid                                                                AS return_id,
    CAST(rr.returndate AS DATE)                                               AS return_date,
    CAST(r.realizationamount AS FLOAT8)                                       AS realization_amount,
    CAST(rr.returnamount AS FLOAT8)                                           AS return_amount,
    rm.realmemonumber                                                          AS memo_number,
    rr.returndescription                                                       AS return_description,
    rr.inputuser                                                               AS input_user,
    r.realizationid                                                            AS realization_id,
    COALESCE(ci.costitemdescription, '')                                      AS cost_item_description,
    CAST(COALESCE(rc.costamount, 0) AS FLOAT8)                               AS cost_amount
FROM program.realizationreturn rr
JOIN program.realization r           ON r.realizationid = rr.realizationid
JOIN program.realizationmemo rm      ON rm.realmemoid = r.realmemoid
LEFT JOIN program.realizationcost rc ON rc.returnid = rr.returnid
LEFT JOIN program.costitem ci        ON ci.costitemid = rc.costitemid
;

COMMENT ON VIEW dwh.v_report_realization_return IS 'Laporan Pengembalian Realisasi dengan detail biaya (multiple rows per return jika ada biaya); filter pada returndate';

-- ============================================================================
-- View 5: Laporan Penyaluran Per Mustahiq
-- TIDAK ADA filter programtype (R dan N sekaligus)
-- Includes: branch_code untuk filter cabang
-- ORDER BY embedded untuk konsistensi grouped display
-- ============================================================================
CREATE OR REPLACE VIEW dwh.v_report_realization_by_mustahiq AS
SELECT
    c.customerid                                                               AS customer_id,
    c.customername                                                             AS customer_name,
    c.addressstreet                                                            AS address_street,
    pr.productid                                                               AS product_id,
    pr.productname                                                             AS product_name,
    pgr.productgroupname                                                       AS product_group_name,
    CAST(r.realizationdate AS DATE)                                           AS realization_date,
    CAST(rd.realizationamount AS FLOAT8)                                      AS realization_amount,
    rd.detaildescription                                                       AS detail_description,
    COALESCE(fa.accountname, '')                                              AS account_name,
    COALESCE(po.proposalno, '')                                               AS proposal_no,
    CAST(COALESCE(po.proposalnominal, 0) AS FLOAT8)                          AS proposal_nominal,
    COALESCE(po.proposaldescription, '')                                      AS proposal_description,
    COALESCE(po.proposalreferenceby, '')                                      AS proposal_reference_by,
    COALESCE(bq.budget_code, '')                                              AS budget_code,
    CASE
        WHEN bq.parent_item_name IS NOT NULL
        THEN CONCAT(bq.item_name, ' - ', bq.parent_item_name)
        ELSE COALESCE(bq.item_name, '')
    END                                                                        AS budget_item_description,
    COALESCE(mp.branchcode, '')                                               AS branch_code,
    r.realizationid                                                            AS realization_id
FROM program.product pr
JOIN program.productgroup pgr        ON pgr.productgroupid = pr.productgroupid
JOIN program.mustahiqproduct mp      ON mp.productid = pr.productid
JOIN program.realization r           ON r.realizationid IN (
    SELECT rd2.realizationid FROM program.realizationdetail rd2
    WHERE rd2.mustahiqproductid = mp.mustahiqproductid
)
JOIN program.realizationdetail rd    ON rd.realizationid = r.realizationid
                                     AND rd.mustahiqproductid = mp.mustahiqproductid
JOIN program.mustahiq m              ON m.mustahiqid = mp.mustahiqid
JOIN program.customer c              ON c.customerid = m.customerid
LEFT JOIN program.proposal po        ON po.proposalid = mp.proposalid
LEFT JOIN transaction.financialaccount fa ON fa.accountno = mp.accountno
LEFT JOIN (
    SELECT
        rb.realizationid,
        bdg.budgetcode                       AS budget_code,
        bdi.budgetitemname                   AS item_name,
        bdip.budgetitemname                  AS parent_item_name
    FROM program.realizationbudget rb
    JOIN transaction.budget bdg              ON bdg.budgetid = rb.budgetid
    JOIN transaction.budgetitem bdi          ON bdi.itemid = bdg.itemid
    LEFT JOIN transaction.budgetitem bdip    ON bdip.itemid = bdi.parentitemid
) bq ON bq.realizationid = r.realizationid
;

COMMENT ON VIEW dwh.v_report_realization_by_mustahiq IS 'Laporan Penyaluran Per Mustahiq (semua jenis R+N), grouped by customer, filter cabang';
