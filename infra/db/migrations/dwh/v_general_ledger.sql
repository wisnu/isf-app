-- [REPORT-ACCT] View Buku Besar (General Ledger) — business DB
--
-- Baris journalitem (posting langsung) per akun detail + lawan (cpa account).
-- Saldo awal & running balance dihitung di report-api (per-akun, param tanggal/cabang).
-- Filter journal_date & branch dilakukan di service (kolom journal_date/branch_code
-- diekspos di view).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz  -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_general_ledger AS
SELECT
    ac.account_code                          AS account_code,
    ac.account_type                          AS account_type,
    ac.account_name                          AS account_name,
    ji.branch_code                           AS branch_code,
    j.journal_no                             AS journal_no,
    j.journal_date                           AS journal_date,
    t.transactionno                          AS transactionno,
    ji.additionaldescription                 AS additionaldescription,
    ji.description                           AS description,
    ji.subaccountcode                        AS subaccountcode,
    ji.subaccountname                        AS subaccountname,
    (ji.amount_debit  * ji.nilai_kurs)::float8 AS debit_ekuiv,
    (ji.amount_credit * ji.nilai_kurs)::float8 AS credit_ekuiv,
    ac.fl_cpa_accountcode                    AS lawan_code,
    acpa.account_name                        AS lawan_name
FROM transaction.journalitem ji
JOIN transaction.journal j   ON ji.fl_journal = j.journal_no
JOIN transaction.account ac  ON ji.fl_account = ac.account_code
LEFT JOIN transaction.transaction t ON t.journalblockid = ji.id_journalblock
LEFT JOIN transaction.account acpa  ON acpa.account_code = ac.fl_cpa_accountcode
WHERE ac.is_detail = 'T';
