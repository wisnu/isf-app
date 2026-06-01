-- [REPORT-ACCT] View pemetaan item Arus Kas → account_code (business DB)
--
-- Membungkus config legacy: BalanceSumItem (item bernama per GroupCode) +
-- BalanceSumItemMember (parent account per item) di-roll up via accounthierarchy
-- ke seluruh akun detail. Dipakai Laporan Arus Kas (group AK_MUT) & saldo kas
-- (group AK_BAL). Mutasi/saldo dihitung di report-api dengan join ke journalitem
-- / dailybalance + filter tanggal & cabang.
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz -f <file>
--        PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

CREATE SCHEMA IF NOT EXISTS dwh;

CREATE OR REPLACE VIEW dwh.v_aruskas_item_account AS
SELECT
    t.groupcode                 AS group_code,
    lower(t.itemcode)           AS item_code,
    ac.account_code             AS account_code,
    ac.account_type             AS account_type
FROM transaction.balancesumitem t
JOIN transaction.balancesumitemmember m ON m.itemid = t.itemid
JOIN transaction.accounthierarchy ah    ON m.account_code = ah.fl_parentaccountcode
JOIN transaction.account ac              ON ah.fl_childaccountcode = ac.account_code;
