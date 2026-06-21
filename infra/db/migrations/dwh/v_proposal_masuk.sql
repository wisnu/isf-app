-- [PROPOSAL-BANTUAN-DANA] View untuk Laporan Proposal Masuk
-- Query dari QLapProposal_data.py — JOIN proposal + productgroup + mustahiq + customer
-- + LEFT JOIN realisasi (rank per mustahiqproduct, ambil realisasi terbesar)
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_proposal_masuk AS
SELECT
    p.proposalid                                                AS proposal_id,
    p.proposalno                                               AS proposal_no,
    CAST(p.proposaldate AS DATE)                               AS proposal_date,
    CAST(p.proposalreceiveddate AS DATE)                       AS received_date,
    p.proposaldescription                                      AS description,
    CAST(p.proposalnominal AS FLOAT8)                          AS nominal,
    p.proposalreceivedby                                       AS received_by,
    p.proposalreferenceby                                      AS reference_by,
    p.proposalreferenceposition                                AS reference_position,
    p.proposalstatus                                           AS status,
    p.branchcode                                               AS branch_code,
    p.mustahiqid                                               AS mustahiq_id,
    c.customername                                             AS mustahiq_name,
    c.addressstreet                                            AS address_street,
    c.addresskelurahan                                         AS address_kelurahan,
    c.addresskecamatan                                         AS address_kecamatan,
    p.productgroupid                                           AS product_group_id,
    pg.productgroupcode                                        AS product_group_code,
    pg.productgroupname                                        AS product_group_name,
    q.realizationdate                                          AS realization_date,
    CAST(q.realizationamount AS FLOAT8)                        AS realization_amount,
    CAST(q.memoamount AS FLOAT8)                               AS memo_amount,
    q.realmemonumber                                           AS memo_number,
    q.fundsourceno                                             AS fund_source_no,
    q.fundsourcename                                           AS fund_source_name
FROM program.proposal p
JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
JOIN program.mustahiq m      ON m.mustahiqid = p.mustahiqid
JOIN program.customer c      ON c.customerid = m.customerid
LEFT JOIN (
    SELECT
        rd.mustahiqproductid,
        mp.proposalid,
        r.realizationdate,
        CAST(rd.realizationamount AS FLOAT8)                   AS realizationamount,
        CAST(rd.memoamount AS FLOAT8)                          AS memoamount,
        rm.realmemonumber,
        mp.accountno                                           AS fundsourceno,
        f.accountname                                          AS fundsourcename,
        RANK() OVER (
            PARTITION BY rd.mustahiqproductid
            ORDER BY rd.realizationamount DESC
        )                                                      AS data_rank
    FROM program.realizationdetail rd
    JOIN program.realization r            ON r.realizationid = rd.realizationid
    JOIN program.realizationmemo rm       ON rm.realmemoid = r.realmemoid
    JOIN program.mustahiqproduct mp       ON mp.mustahiqproductid = rd.mustahiqproductid
    JOIN transaction.financialaccount f   ON f.accountno = mp.accountno
) q ON q.data_rank = 1 AND q.proposalid = p.proposalid;
