-- DWH View: dwh.v_budget_transaction
-- Portal: zakat
-- Purpose: Transaction-level detail view linking budget items with actual transactions
-- Source: budgettransaction, budget, budgetowner, transactionitem, transaction
-- Used by: report-api endpoints for realization detail reports and variance analysis

CREATE OR REPLACE VIEW dwh.v_budget_transaction AS
SELECT
  bt.transactionitemid AS transaction_item_id,
  bt.budgetid AS budget_id,
  b.budgetcode AS budget_code,
  b.budgetid AS header_budget_id,
  bo.ownerid AS owner_id,
  bo.ownername AS owner_name,
  bo.ownercode AS owner_code,
  bp.periodid AS period_id,
  bp.periodvalue AS period_year,
  b.branchcode AS branch_code,
  -- Transaction detail
  ti.transactionitemid,
  ti.transactionid,
  t.transactioncode,
  t.transactionno AS no_transaksi,
  CAST(t.transactiondate AS DATE) AS transaction_date,
  CAST(t.actualdate AS DATE) AS actual_date,
  -- Amount categorization: realisasi vs pengembalian
  CASE
    WHEN bt.budgettranstype = 'A' THEN CAST(ti.amount AS NUMERIC(20, 4))
    ELSE CAST(0 AS NUMERIC(20, 4))
  END AS realization_amount,
  CASE
    WHEN bt.budgettranstype != 'A' THEN CAST(ti.amount AS NUMERIC(20, 4))
    ELSE CAST(0 AS NUMERIC(20, 4))
  END AS return_amount,
  bt.budgettranstype AS transaction_type,
  ti.amount AS full_amount,
  CAST(ti.amount AS NUMERIC(20, 4)) AS amount_numeric,
  -- Metadata
  ti.accountcode,
  ti.description,
  t.inputer,
  t.referenceno AS reference_no,
  t.authstatus,
  t.isposted,
  ti.currencycode
FROM transaction.budgettransaction bt
JOIN transaction.budget b ON bt.budgetid = b.budgetid
JOIN transaction.budgetowner bo ON b.ownerid = bo.ownerid
JOIN transaction.budgetperiod bp ON b.periodid = bp.periodid
JOIN transaction.transactionitem ti ON bt.transactionitemid = ti.transactionitemid
JOIN transaction.transaction t ON ti.transactionid = t.transactionid
WHERE b.budgettype = 'Y'
;

COMMENT ON VIEW dwh.v_budget_transaction IS
'Budget transaction detail view mapping realization transactions to budget items. Categorizes transactions as realisasi (type=A) or pengembalian (type!=A). Includes transaction metadata for audit trail.';
