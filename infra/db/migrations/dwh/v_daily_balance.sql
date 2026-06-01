-- [REPORT-ACCT] View saldo harian per akun (business DB: mziss_laz + mziss_wakaf)
--
-- Untuk Trial Balance & Neraca (legacy-faithful): accountinstance + dailybalance
-- + account. Logika max-date (saldo kumulatif terakhir ≤ tanggal) & rollup
-- accounthierarchy dilakukan di report-api. balance_sign untuk normalisasi arah.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_daily_balance AS
SELECT
    d.accountinstance_id                AS accountinstance_id,
    ai.account_code                     AS account_code,
    a.account_name                      AS account_name,
    a.account_type                      AS account_type,
    a.account_level                     AS account_level,
    a.is_detail                         AS is_detail,
    ai.branch_code                      AS branch_code,
    ai.currency_code                    AS currency_code,
    COALESCE(ai.balance_sign, 1)        AS balance_sign,
    d.datevalue                         AS datevalue,
    COALESCE(d.balancecumulative, 0)    AS balancecumulative,
    COALESCE(d.debit, 0)                AS debit,
    COALESCE(d.credit, 0)               AS credit
FROM transaction.dailybalance d
JOIN transaction.accountinstance ai ON ai.accountinstance_id = d.accountinstance_id
JOIN transaction.account a          ON a.account_code = ai.account_code;
