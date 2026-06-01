-- [REPORT-JOURNAL] View laporan jurnal harian (business DB: mziss_laz + mziss_wakaf)
--
-- Fase view-based: membungkus query legacy fListJournalDaily atas tabel live
-- transaction.{account, journal, journalitem, transaction}. Dibaca read-only oleh
-- report-api (pool dwh). Fase berikut bisa diganti tabel ETL independen tanpa ubah
-- nama view / kontrak.
--
-- Filter kolom: branch_code (cabang jurnal), journal_date.
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_journal_daily AS
SELECT
    j.branch_code                                   AS branch_code,
    j.journal_date                                  AS journal_date,
    j.journal_no                                    AS journal_no,
    t.transactionno                                 AS transactionno,
    ji.branch_code                                  AS account_branch_code,
    ac.account_code                                 AS account_code,
    ac.account_type                                 AS account_type,
    ac.account_name                                 AS account_name,
    ji.subaccountcode                               AS subaccountcode,
    ji.subaccountname                               AS subaccountname,
    CASE WHEN ji.additionaldescription IS NOT NULL
         THEN ji.description || ' ( ' || ji.additionaldescription || ' )'
         ELSE ji.description END                    AS description,
    (ji.amount_debit  * ji.nilai_kurs)              AS debit_ekuiv,
    (ji.amount_credit * ji.nilai_kurs)              AS credit_ekuiv,
    t.inputer                                       AS inputer
FROM transaction.account ac
   , transaction.journal j
   , transaction.journalitem ji
     LEFT JOIN transaction.transaction t ON t.journalblockid = ji.id_journalblock
WHERE ji.fl_account = ac.account_code
  AND ji.fl_journal = j.journal_no;
