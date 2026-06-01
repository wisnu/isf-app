-- [REPORT-UPZ] View List Transaksi UPZ (fLaporanUPZ) — business DB
--
-- Journalitem dari jurnal yang menyentuh akun UPZ: 210302 (TITIPAN PENYALURAN UPZ)
-- atau 110109 (PENAMPUNGAN ZAKAT UPZ). Flag has_210302/has_110109 per jurnal;
-- report-api memfilter: (has_210302 & kredit≠0 & akun≠210302) atau (has_110109 &
-- debit≠0 & transactioncode='TI'). Filter tanggal/cabang di report-api.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_upz_trx AS
SELECT
    a.account_code                            AS account_code,
    a.account_name                            AS account_name,
    j.journal_no                              AS journal_no,
    j.journal_date                            AS journal_date,
    ji.branch_code                            AS branch_code,
    t.transactionno                           AS transactionno,
    t.transactioncode                         AS transactioncode,
    ty.description                            AS trxtypedesc,
    ji.additionaldescription                  AS additionaldescription,
    ji.description                            AS description,
    ji.subaccountcode                         AS subaccountcode,
    ji.subaccountname                         AS subaccountname,
    ji.amount_debit::float8                   AS amount_debit,
    ji.amount_credit::float8                  AS amount_credit,
    EXISTS (SELECT 1 FROM transaction.journalitem r
            WHERE r.fl_journal = j.journal_no AND r.fl_account = '210302') AS has_210302,
    EXISTS (SELECT 1 FROM transaction.journalitem r
            WHERE r.fl_journal = j.journal_no AND r.fl_account = '110109') AS has_110109
FROM transaction.journalitem ji
JOIN transaction.journal j  ON j.journal_no = ji.fl_journal
JOIN transaction.account a  ON a.account_code = ji.fl_account
LEFT JOIN transaction.transaction t       ON t.journalno = j.journal_no
LEFT JOIN transaction.transactiontype ty  ON ty.transactioncode = t.transactioncode;
